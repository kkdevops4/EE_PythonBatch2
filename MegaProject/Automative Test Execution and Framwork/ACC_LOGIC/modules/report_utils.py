import math


def clean_text(value):
    if value is None:
        return ""
    if isinstance(value, float) and value != value:
        return ""
    text = str(value).strip()
    return text if text else ""


def get_status_counts(df):
    return {
        "total": len(df),
        "pass": int((df["Status"] == "Pass").sum()),
        "fail": int((df["Status"] == "Fail").sum()),
        "missing": int((df["Status"] == "Missing Value Error").sum()),
        "invalid": int((df["Status"] == "Invalid Value Error").sum()),
    }


def build_execution_summary(df):
    counts = get_status_counts(df)
    return {
        "counts": counts,
        "status_rows": {
            "fail": df[df["Status"] == "Fail"],
            "missing": df[df["Status"] == "Missing Value Error"],
            "invalid": df[df["Status"] == "Invalid Value Error"],
        },
    }


def normalize_records(frame):
    def sanitize_value(value):
        if value is None:
            return ""
        if isinstance(value, float) and math.isnan(value):
            return ""
        return value

    return [
        {key: sanitize_value(value) for key, value in row.items()}
        for row in frame.to_dict(orient="records")
    ]
