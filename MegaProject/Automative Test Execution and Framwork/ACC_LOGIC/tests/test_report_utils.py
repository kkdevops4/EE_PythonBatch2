import pandas as pd

from modules.report_utils import build_execution_summary, clean_text, get_status_counts, normalize_records


def test_clean_text_and_status_counts():
    df = pd.DataFrame(
        [
            {"Status": "Pass", "TC_ID": "TC01", "Expected_Result": "A", "Actual_Result": "A"},
            {"Status": "Fail", "TC_ID": "TC02", "Expected_Result": "A", "Actual_Result": "B"},
            {"Status": "Missing Value Error", "TC_ID": "TC03", "Expected_Result": None, "Actual_Result": ""},
            {"Status": "Invalid Value Error", "TC_ID": "TC04", "Expected_Result": "A", "Actual_Result": "C"},
        ]
    )

    assert clean_text(None) == ""
    assert clean_text("  demo  ") == "demo"

    counts = get_status_counts(df)
    assert counts["total"] == 4
    assert counts["pass"] == 1
    assert counts["fail"] == 1
    assert counts["missing"] == 1
    assert counts["invalid"] == 1

    summary = build_execution_summary(df)
    assert summary["counts"]["total"] == 4
    assert len(summary["status_rows"]["fail"]) == 1
    assert summary["status_rows"]["missing"].iloc[0]["TC_ID"] == "TC03"

    records = normalize_records(df)
    assert records[0]["TC_ID"] == "TC01"
    assert records[2]["Expected_Result"] == ""
