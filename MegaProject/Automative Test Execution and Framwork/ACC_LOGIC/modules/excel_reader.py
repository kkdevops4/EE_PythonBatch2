"""
excel_reader.py
----------------
Loads the Adaptive Cruise Control (ACC) test case sheet, normalizes
column names/types, and audits every cell for two distinct kinds of
data problems:

  1. Missing  - the cell is blank / NaN.
  2. Invalid  - the cell has a value, but it isn't one this framework
                understands (e.g. Ignition = "MAYBE" instead of
                ON/OFF, or Vehicle_Speed = "fast" instead of a
                number, or a negative distance).

Both audits are recorded per row as human-readable, comma-separated
strings ("Missing_Fields" / "Invalid_Fields") plus a raw "Excel_Row"
number (the actual row in the spreadsheet, 1-indexed with the header
as row 1) so the report can point a reader straight at the offending
cell: which column, which TC_ID, which sheet row.
"""

import pandas as pd


class ExcelReader:
    """Reads, cleans, and audits the ACC test case Excel file."""

    # Internal column name -> accepted raw Excel header(s). The sheet has
    # been through a couple of revisions (Driver_Action -> Test_Case_Action,
    # and an Actual_Result column was added), so each internal name can
    # match more than one raw header. Actual_Result is intentionally not
    # required - older-style sheets without it still work (see
    # read_excel()), falling back to the ACC logic's own simulation.
    COLUMN_ALIASES = {
        "TC_ID": ["TC_ID"],
        "Test_Description": ["Test_Description"],
        "Ignition_Status": ["Ignition"],
        "Vehicle_Speed": ["Vehicle_Speed (km/h)"],
        "ACC_Status": ["ACC_Status"],
        "Set_Speed": ["Set_Speed (km/h)"],
        "Lead_Vehicle_Detected": ["Lead_Vehicle_Detected"],
        "Lead_Vehicle_Speed": ["Lead_Vehicle_Speed (km/h)"],
        "Following_Distance": ["Following_Distance (m)"],
        "User_Action": ["Test_Case_Action", "Driver_Action"],
        "Expected_Result": ["Expected_Result"],
        "Actual_Result": ["Actual_Result"],
    }

    # Every internal column except these must be present in the sheet.
    OPTIONAL_COLUMNS = {"Actual_Result"}

    # Internal column name -> label used in audit messages / reports
    DISPLAY_LABELS = {
        "Test_Description": "Test Description",
        "Ignition_Status": "Ignition",
        "Vehicle_Speed": "Vehicle Speed",
        "ACC_Status": "ACC Status",
        "Set_Speed": "Set Speed",
        "Lead_Vehicle_Detected": "Lead Vehicle Detected",
        "Lead_Vehicle_Speed": "Lead Vehicle Speed",
        "Following_Distance": "Following Distance",
        "User_Action": "Driver Action",
        "Expected_Result": "Expected Result",
        "Actual_Result": "Actual Result",
    }

    TEXT_COLUMNS = [
        "Test_Description",
        "Ignition_Status",
        "ACC_Status",
        "Lead_Vehicle_Detected",
        "User_Action",
        "Expected_Result",
    ]

    NUMERIC_COLUMNS = [
        "Vehicle_Speed",
        "Set_Speed",
        "Lead_Vehicle_Speed",
        "Following_Distance",
    ]

    # Columns audited for missing/invalid reporting. TC_ID is excluded -
    # a row with no ID is a structurally broken row, not a data note.
    AUDITED_COLUMNS = TEXT_COLUMNS + NUMERIC_COLUMNS

    # ---- Value domains used for the "invalid value" checks ----
    CATEGORICAL_DOMAINS = {
        "Ignition_Status": {"ON", "OFF"},
        "ACC_Status": {"ON", "OFF"},
        "Lead_Vehicle_Detected": {"YES", "NO"},
    }

    KNOWN_ACTIONS = {
        "acc_on", "set_speed", "maintain", "brake_pedal", "acc_cancel",
        "resume", "radar_failure", "camera_failure", "accelerator",
        "increase_setspeed", "decrease_setspeed", "ignition_off",
    }

    # (min, max) sanity bounds for numeric columns - values outside
    # this range are flagged as invalid rather than silently used.
    NUMERIC_BOUNDS = {
        "Vehicle_Speed": (0, 300),
        "Set_Speed": (0, 300),
        "Lead_Vehicle_Speed": (0, 300),
        "Following_Distance": (0, 1000),
    }

    @staticmethod
    def read_excel(file_path):
        """
        Reads the ACC test case Excel file and returns a cleaned
        DataFrame with "Missing_Fields" / "Invalid_Fields" audit
        columns and an "Excel_Row" column, or None if the file can't
        be read or required columns are absent entirely.

        df.attrs["has_actual_result_column"] tells the caller whether a
        real, recorded Actual_Result came from the sheet (True) or the
        sheet is an older-style workbook without one (False), in which
        case the caller falls back to the ACC logic's own simulation.
        """
        header_row = ExcelReader._detect_header_row(file_path)
        try:
            df = pd.read_excel(file_path, header=header_row)
        except Exception as error:
            print(f"[ExcelReader] Failed to open '{file_path}': {error}")
            return None

        # Strip stray whitespace from headers before mapping
        df.columns = [str(col).strip() for col in df.columns]

        rename_map, missing_required = ExcelReader._resolve_columns(df.columns)
        if missing_required:
            print(f"[ExcelReader] Missing expected columns: {missing_required}")
            return None
        has_actual_result_column = "Actual_Result" in rename_map.values()

        # Capture the real spreadsheet row number BEFORE any rows are
        # dropped, so it still points at the right line afterward.
        # +2 accounts for the header row itself plus 1-indexing.
        df["Excel_Row"] = df.index + header_row + 2

        df = df.rename(columns=rename_map)
        if not has_actual_result_column:
            df["Actual_Result"] = ""

        # Drop fully empty trailing rows / rows with no TC_ID at all
        df = df.dropna(subset=None, how="all").reset_index(drop=True)
        df = df[df["TC_ID"].notna()].reset_index(drop=True)

        audited_columns = ExcelReader.AUDITED_COLUMNS + (
            ["Actual_Result"] if has_actual_result_column else []
        )

        # ---- Audit BEFORE any fill/coercion, so raw values are intact ----
        audit = df.apply(lambda r: ExcelReader._audit_row(r, audited_columns), axis=1)
        df["Missing_Fields"] = audit.apply(lambda a: a[0])
        df["Invalid_Fields"] = audit.apply(lambda a: a[1])
        for col in audited_columns:
            df[f"_missing__{col}"] = audit.apply(lambda a, c=col: c in a[2])
            df[f"_invalid__{col}"] = audit.apply(lambda a, c=col: c in a[3])
            df[f"_invalid_reason__{col}"] = audit.apply(lambda a, c=col: a[3].get(c, ""))

        missing_row_count = int((df["Missing_Fields"] != "").sum())
        invalid_row_count = int((df["Invalid_Fields"] != "").sum())
        if missing_row_count:
            print(f"[ExcelReader] {missing_row_count} row(s) have one or more blank cells - see 'Missing_Fields'.")
        if invalid_row_count:
            print(f"[ExcelReader] {invalid_row_count} row(s) have one or more invalid values - see 'Invalid_Fields'.")

        # ---- Normalize types for use by the validator (after auditing) ----
        text_columns = ExcelReader.TEXT_COLUMNS + (["Actual_Result"] if has_actual_result_column else [])
        for col in text_columns:
            df[col] = df[col].apply(lambda v: "" if ExcelReader._is_blank(v) else str(v).strip())

        for col in ExcelReader.NUMERIC_COLUMNS:
            # Keep genuine blanks/garbage as NaN rather than defaulting to
            # 0 - a missing or invalid Following_Distance is not 0 meters.
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df.attrs["has_actual_result_column"] = has_actual_result_column
        print(f"[ExcelReader] Loaded {len(df)} test case(s) from '{file_path}'")
        return df

    @staticmethod
    def _detect_header_row(file_path, max_scan=5):
        """
        Finds the row that holds the real column headers (looks for the
        "TC_ID" cell), so a cosmetic title row above it (e.g. a merged
        "Preconditions (Parameters)" banner) doesn't get mistaken for
        the header.
        """
        try:
            preview = pd.read_excel(file_path, header=None, nrows=max_scan)
        except Exception:
            return 0
        for i in range(len(preview)):
            row_values = {str(v).strip() for v in preview.iloc[i].tolist()}
            if "TC_ID" in row_values:
                return i
        return 0

    @staticmethod
    def _resolve_columns(available_columns):
        """
        Matches each internal column name to whichever of its accepted
        raw headers is present in the sheet. Returns (rename_map,
        missing_required_internal_names).
        """
        available = set(available_columns)
        rename_map = {}
        missing_required = []
        for internal_name, aliases in ExcelReader.COLUMN_ALIASES.items():
            found = next((alias for alias in aliases if alias in available), None)
            if found:
                rename_map[found] = internal_name
            elif internal_name not in ExcelReader.OPTIONAL_COLUMNS:
                missing_required.append(internal_name)
        return rename_map, missing_required

    # -----------------------------------------------------------
    # Auditing
    # -----------------------------------------------------------

    @staticmethod
    def _audit_row(row, audited_columns=None):
        """
        Returns (missing_display, invalid_display, missing_cols_set, invalid_reasons_dict)
        for one raw row, checked BEFORE type coercion.
        """
        if audited_columns is None:
            audited_columns = ExcelReader.AUDITED_COLUMNS

        missing_cols = set()
        invalid_reasons = {}

        for col in audited_columns:
            value = row[col]

            if ExcelReader._is_blank(value):
                missing_cols.add(col)
                continue

            if col in ExcelReader.CATEGORICAL_DOMAINS:
                allowed = ExcelReader.CATEGORICAL_DOMAINS[col]
                if str(value).strip().upper() not in allowed:
                    invalid_reasons[col] = (
                        f"must be one of {'/'.join(sorted(allowed))}, got '{value}'"
                    )

            elif col == "User_Action":
                if str(value).strip().lower() not in ExcelReader.KNOWN_ACTIONS:
                    invalid_reasons[col] = f"unrecognized action '{value}'"

            elif col in ExcelReader.NUMERIC_COLUMNS:
                parsed = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
                if pd.isna(parsed):
                    invalid_reasons[col] = f"not a number, got '{value}'"
                else:
                    lo, hi = ExcelReader.NUMERIC_BOUNDS[col]
                    if parsed < lo or parsed > hi:
                        invalid_reasons[col] = f"out of range ({lo}-{hi}), got {parsed}"

        missing_display = ", ".join(sorted(ExcelReader.DISPLAY_LABELS[c] for c in missing_cols))
        invalid_display = ", ".join(
            f"{ExcelReader.DISPLAY_LABELS[c]} ({reason})" for c, reason in invalid_reasons.items()
        )
        return missing_display, invalid_display, missing_cols, invalid_reasons

    @staticmethod
    def _is_blank(value):
        """True for NaN/None and for strings that are empty after stripping."""
        if pd.isna(value):
            return True
        if isinstance(value, str) and value.strip() == "":
            return True
        return False
