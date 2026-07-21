#import os
import sys
from pathlib import Path

# ----------------------------------------------------------------
# Paths
# ----------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
ACC_LOGIC_DIR = BASE_DIR / "ACC_LOGIC"

# Allow imports like "from modules..." to resolve when running this
# script from the workspace root.
if str(ACC_LOGIC_DIR) not in sys.path:
    sys.path.insert(0, str(ACC_LOGIC_DIR))

from modules.excel_reader import ExcelReader
from modules.report_utils import build_execution_summary
from modules.acc_validator import ACCValidator
from modules.chart_generator import ChartGenerator
from modules.html_report_generator import HTMLReportGenerator
from modules.word_report_generator import WordReportGenerator
from modules.docx_to_pdf_converter import DocxToPDFConverter

EXCEL_FILE = ACC_LOGIC_DIR / "data" / "ACC_Test_Cases_Simple.xlsx"

CHART_DIR = BASE_DIR / "reports" / "charts"
HTML_DIR = BASE_DIR / "reports" / "html"
WORD_DIR = BASE_DIR / "reports" / "word"
PDF_DIR = BASE_DIR / "reports" / "pdf"

CHART_FILE = CHART_DIR / "pass_fail_missing_pie.png"
HTML_FILE = HTML_DIR / "ACC_Report.html"
WORD_FILE = WORD_DIR / "ACC_Report_v2.docx"
PDF_FILE = PDF_DIR / "ACC_Report.pdf"

REPORT_TITLE = "Adaptive Cruise Control (ACC) - Test Execution Report"


def _resolve_actual_result(row, has_actual_result_column):
    """
    The sheet's own recorded Actual_Result is authoritative when present
    and non-blank; otherwise fall back to what the ACC logic simulates
    for that row's inputs (older-style workbooks without the column).
    """
    if has_actual_result_column:
        recorded = str(row["Actual_Result"]).strip()
        if recorded:
            return recorded
        return ACCValidator.MISSING_RESULT
    return row["Simulated_Result"]


def _determine_status(row):
    """Pass / Fail / Missing Value Error / Invalid Value Error for one row."""
    if row["Simulated_Result"] == ACCValidator.MISSING_RESULT:
        return "Missing Value Error"
    if row["Simulated_Result"] == ACCValidator.INVALID_RESULT:
        return "Invalid Value Error"
    if row.get("_missing__Expected_Result", False):
        return "Missing Value Error"
    if row.get("_missing__Actual_Result", False):
        return "Missing Value Error"
    if str(row["Expected_Result"]).strip().lower() == str(row["Actual_Result"]).strip().lower():
        return "Pass"
    return "Fail"


def _finalize_remarks(row):
    """
    If the row's action evaluated fine but the Expected Result and/or
    Actual Result cell itself was the blank one, append that detail to
    the remarks so the report still names the exact column/TC/row.
    """
    if row["Status"] != "Missing Value Error" or row["Simulated_Result"] in (
        ACCValidator.MISSING_RESULT,
        ACCValidator.INVALID_RESULT,
    ):
        return row["Remarks"]

    notes = []
    if row.get("_missing__Expected_Result", False):
        notes.append(
            f"Missing Value Error: Column 'Expected Result' is empty "
            f"(Test Case {row['TC_ID']}, Row {row['Excel_Row']})."
        )
    if row.get("_missing__Actual_Result", False):
        notes.append(
            f"Missing Value Error: Column 'Actual Result' is empty "
            f"(Test Case {row['TC_ID']}, Row {row['Excel_Row']})."
        )
    return f"{row['Remarks']} | {' | '.join(notes)}" if notes else row["Remarks"]


def _mismatch_reason(row):
    """Reason text for Fail rows only; blank everywhere else."""
    if row["Status"] != "Fail":
        return ""
    return ACCValidator.explain_mismatch(
        row["Actual_Result"], row["Expected_Result"], row["Simulated_Result"], row["Simulated_Remarks"]
    )


def main():
    for folder in (CHART_DIR, HTML_DIR, WORD_DIR, PDF_DIR):
        folder.mkdir(parents=True, exist_ok=True)

    # ---------------- Step 1: Read Excel ----------------
    df = ExcelReader.read_excel(str(EXCEL_FILE))
    if df is None:
        print("Excel loading failed. Aborting.")
        return 1

    # ---------------- Step 2: Run the ACC logic simulation ----------------
    # Always run - it drives the missing/invalid-field audit for every
    # row, and its predicted result/remarks are also the basis for
    # explaining any Expected-vs-Actual mismatch below.
    simulated_results = []
    simulated_remarks_list = []

    for _, row in df.iterrows():
        simulated_result, simulated_remarks = ACCValidator.validate(row)
        simulated_results.append(simulated_result)
        simulated_remarks_list.append(simulated_remarks)

    df["Simulated_Result"] = simulated_results
    df["Simulated_Remarks"] = simulated_remarks_list
    df["Remarks"] = df["Simulated_Remarks"]

    has_actual_result_column = df.attrs.get("has_actual_result_column", False)
    df["Actual_Result"] = df.apply(
        lambda r: _resolve_actual_result(r, has_actual_result_column), axis=1
    )

    # ---------------- Step 3: Status ----------------
    df["Status"] = df.apply(_determine_status, axis=1)
    df["Remarks"] = df.apply(_finalize_remarks, axis=1)
    df["Mismatch_Reason"] = df.apply(_mismatch_reason, axis=1)

    summary = build_execution_summary(df)
    counts = summary["counts"]
    total_tc = counts["total"]
    pass_count = counts["pass"]
    fail_count = counts["fail"]
    missing_count = counts["missing"]
    invalid_count = counts["invalid"]

    print("\n========== ACC EXECUTION SUMMARY ==========")
    print(f"Total Test Cases     : {total_tc}")
    print(f"Passed                : {pass_count}")
    print(f"Failed                : {fail_count}")
    print(f"Missing Value Errors  : {missing_count}")
    print(f"Invalid Value Errors  : {invalid_count}")
    print("============================================\n")

    for label, status in (("Failed test cases", "Fail"), ("Missing Value Errors", "Missing Value Error"), ("Invalid Value Errors", "Invalid Value Error")):
        rows = summary["status_rows"]["fail" if status == "Fail" else "missing" if status == "Missing Value Error" else "invalid"]
        if len(rows):
            print(f"{label}:")
            for _, row in rows.iterrows():
                if status == "Fail":
                    print(f"  {row['TC_ID']}: expected '{row['Expected_Result']}', got '{row['Actual_Result']}'")
                else:
                    print(f"  {row['TC_ID']} (Row {row['Excel_Row']}): {row['Remarks']}")
            print()

    try:
        ChartGenerator.generate(
            pass_count=pass_count,
            fail_count=fail_count,
            missing_count=missing_count,
            invalid_count=invalid_count,
            output_file=str(CHART_FILE),
        )
    except Exception as error:
        print(f"Chart generation failed: {error}")
        return 1

    try:
        HTMLReportGenerator.create_report(
            df=df,
            pass_count=pass_count,
            fail_count=fail_count,
            missing_count=missing_count,
            invalid_count=invalid_count,
            output_html=str(HTML_FILE),
            report_title=REPORT_TITLE,
            chart_path=str(CHART_FILE),
        )
    except Exception as error:
        print(f"HTML report generation failed: {error}")
        return 1

    try:
        WordReportGenerator.create_report(
            df=df,
            pass_count=pass_count,
            fail_count=fail_count,
            missing_count=missing_count,
            invalid_count=invalid_count,
            chart_path=str(CHART_FILE),
            output_docx=str(WORD_FILE),
            report_title="Adaptive Cruise Control (ACC)",
            report_subtitle="Test Execution Report",
        )
    except Exception as error:
        print(f"Word report generation failed: {error}")
        return 1

    try:
        DocxToPDFConverter.convert(str(WORD_FILE), str(PDF_FILE))
    except Exception as error:
        print(f"PDF conversion failed: {error}")
        return 1

    print("Reports generated successfully:")
    print(f"  Chart : {CHART_FILE}")
    print(f"  HTML  : {HTML_FILE}")
    print(f"  Word  : {WORD_FILE}")
    print(f"  PDF   : {PDF_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

