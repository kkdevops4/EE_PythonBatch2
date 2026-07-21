import base64
import os
from datetime import datetime

from jinja2 import Template

from modules.report_utils import normalize_records

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ report_title }}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    :root {
        --bg: #0a0e13;
        --panel: #12181f;
        --panel-alt: #161e27;
        --border: #232c37;
        --text: #e6edf3;
        --muted: #7c8a99;
        --cyan: #22d3ee;
        --amber: #f5a623;
        --red: #ef4444;
        --green: #2dd4a7;
        --violet: #a78bfa;
    }
    * { box-sizing: border-box; }
    body {
        margin: 0;
        background: var(--bg);
        color: var(--text);
        font-family: 'Inter', -apple-system, Segoe UI, sans-serif;
        padding: 32px 24px 64px;
    }
    .wrap { max-width: 1150px; margin: 0 auto; }

    .eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        letter-spacing: 0.18em;
        color: var(--cyan);
        text-transform: uppercase;
        margin: 0 0 10px;
    }
    h1 { font-size: 30px; font-weight: 800; margin: 0 0 6px; letter-spacing: -0.01em; }
    .meta {
        font-family: 'JetBrains Mono', monospace;
        font-size: 12.5px;
        color: var(--muted);
        margin: 0 0 28px;
        border-bottom: 1px solid var(--border);
        padding-bottom: 24px;
    }

    .stat-rail {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 14px;
        margin-bottom: 32px;
    }
    @media (max-width: 900px) {
        .stat-rail { grid-template-columns: repeat(2, 1fr); }
    }
    .stat-tile {
        background: var(--panel);
        border: 1px solid var(--border);
        border-left: 3px solid var(--cyan);
        border-radius: 10px;
        padding: 16px 18px;
    }
    .stat-tile.pass { border-left-color: var(--green); }
    .stat-tile.fail { border-left-color: var(--red); }
    .stat-tile.missing { border-left-color: var(--amber); }
    .stat-tile.invalid { border-left-color: var(--violet); }
    .stat-tile .label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--muted);
        margin-bottom: 8px;
    }
    .stat-tile .value { font-family: 'JetBrains Mono', monospace; font-size: 28px; font-weight: 700; line-height: 1; }
    .stat-tile.pass .value { color: var(--green); }
    .stat-tile.fail .value { color: var(--red); }
    .stat-tile.missing .value { color: var(--amber); }
    .stat-tile.invalid .value { color: var(--violet); }

    h2 {
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--cyan);
        margin: 36px 0 14px;
        padding-bottom: 10px;
        border-bottom: 1px solid var(--border);
    }

    .table-wrap { background: var(--panel); border: 1px solid var(--border); border-radius: 10px; overflow: auto; }
    table { border-collapse: collapse; width: 100%; font-size: 12.5px; }
    thead th {
        text-align: left;
        font-family: 'JetBrains Mono', monospace;
        font-size: 10.5px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--muted);
        background: var(--panel-alt);
        padding: 11px 14px;
        border-bottom: 1px solid var(--border);
        white-space: nowrap;
    }
    tbody td { padding: 10px 14px; border-bottom: 1px solid var(--border); color: var(--text); vertical-align: top; }
    tbody tr:last-child td { border-bottom: none; }
    tbody tr:hover { background: var(--panel-alt); }
    tbody tr.row-missing { background: rgba(245, 166, 35, 0.05); }
    tbody tr.row-invalid { background: rgba(167, 139, 250, 0.06); }
    td.mono, th.mono { font-family: 'JetBrains Mono', monospace; }
    td.audit-cell { font-family: 'JetBrains Mono', monospace; font-size: 11.5px; }
    td.audit-cell.missing-text { color: var(--amber); }
    td.audit-cell.invalid-text { color: var(--violet); }
    td.audit-cell.none { color: var(--muted); }
    .field-blank { color: var(--amber); font-style: italic; }

    .pill {
        display: inline-block; font-family: 'JetBrains Mono', monospace; font-size: 10.5px;
        font-weight: 700; letter-spacing: 0.06em; padding: 3px 9px; border-radius: 999px; white-space: nowrap;
    }
    .pill-pass { background: rgba(45, 212, 167, 0.12); color: var(--green); border: 1px solid rgba(45, 212, 167, 0.35); }
    .pill-fail { background: rgba(239, 68, 68, 0.12); color: var(--red); border: 1px solid rgba(239, 68, 68, 0.35); }
    .pill-missing { background: rgba(245, 166, 35, 0.12); color: var(--amber); border: 1px solid rgba(245, 166, 35, 0.35); }
    .pill-invalid { background: rgba(167, 139, 250, 0.12); color: var(--violet); border: 1px solid rgba(167, 139, 250, 0.35); }

    .alert-panel { border-radius: 8px; padding: 14px 18px; margin-bottom: 10px; border: 1px solid; border-left-width: 3px; }
    .alert-panel.fail { background: rgba(239, 68, 68, 0.06); border-color: rgba(239, 68, 68, 0.3); border-left-color: var(--red); }
    .alert-panel.missing { background: rgba(245, 166, 35, 0.06); border-color: rgba(245, 166, 35, 0.3); border-left-color: var(--amber); }
    .alert-panel.invalid { background: rgba(167, 139, 250, 0.06); border-color: rgba(167, 139, 250, 0.3); border-left-color: var(--violet); }
    .alert-panel .tc-id { font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 12.5px; margin-bottom: 4px; }
    .alert-panel.fail .tc-id { color: var(--red); }
    .alert-panel.missing .tc-id { color: var(--amber); }
    .alert-panel.invalid .tc-id { color: var(--violet); }
    .alert-panel .detail { font-size: 13px; color: var(--text); }
    .alert-panel .detail .lbl { color: var(--muted); }
    .clean-panel {
        background: rgba(45, 212, 167, 0.06); border: 1px solid rgba(45, 212, 167, 0.3); border-left: 3px solid var(--green);
        border-radius: 8px; padding: 14px 18px; color: var(--text); font-size: 13.5px;
    }

    .footer {
        margin-top: 44px; padding-top: 18px; border-top: 1px solid var(--border);
        font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--muted);
        display: flex; justify-content: space-between;
    }

    .chart-panel {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 18px 20px;
        display: flex;
        align-items: center;
        gap: 24px;
        flex-wrap: wrap;
        margin-bottom: 8px;
    }
    .chart-panel img { max-width: 300px; width: 100%; height: auto; }
    .chart-legend { display: flex; flex-direction: column; gap: 10px; font-size: 12.5px; }
    .chart-legend .swatch {
        display: inline-block; width: 11px; height: 11px; border-radius: 3px; margin-right: 8px; vertical-align: middle;
    }
    .chart-legend .swatch.positive { background: #2e7d32; }
    .chart-legend .swatch.negative { background: #c62828; }
    .chart-legend .swatch.missing { background: #f9a825; }
    .chart-legend .swatch.invalid { background: #a78bfa; }
</style>
</head>
<body>
<div class="wrap">

    <p class="eyebrow">Test Execution Report</p>
    <h1>{{ report_title }}</h1>
    <p class="meta">GENERATED {{ generated_on }} &nbsp;&middot;&nbsp; {{ total_tc }} TEST CASE(S) EXECUTED</p>

    <div class="stat-rail">
        <div class="stat-tile">
            <div class="label">Total Cases</div>
            <div class="value">{{ total_tc }}</div>
        </div>
        <div class="stat-tile pass">
            <div class="label">Passed</div>
            <div class="value">{{ pass_count }}</div>
        </div>
        <div class="stat-tile fail">
            <div class="label">Failed</div>
            <div class="value">{{ fail_count }}</div>
        </div>
        <div class="stat-tile missing">
            <div class="label">Missing Value Error</div>
            <div class="value">{{ missing_count }}</div>
        </div>
        <div class="stat-tile invalid">
            <div class="label">Invalid Value Error</div>
            <div class="value">{{ invalid_count }}</div>
        </div>
    </div>

    {% if chart_base64 %}
    <h2>Pass / Fail / Missing Distribution</h2>
    <div class="chart-panel">
        <img src="data:image/png;base64,{{ chart_base64 }}" alt="Pass Fail Missing pie chart">
        <div class="chart-legend">
            <span><span class="swatch positive"></span>Passed Cases &mdash; {{ pass_count }}</span>
            <span><span class="swatch negative"></span>Failed Cases &mdash; {{ fail_count }}</span>
            <span><span class="swatch missing"></span>Missing Data &mdash; {{ missing_count }}</span>
            <span><span class="swatch invalid"></span>Invalid Data &mdash; {{ invalid_count }}</span>
        </div>
    </div>
    {% endif %}

    <h2>Detailed Test Results</h2>
    <div class="table-wrap">
    <table>
        <thead>
        <tr>
            <th class="mono">TC ID</th>
            <th class="mono">Row</th>
            <th>Description</th>
            <th class="mono">Action</th>
            <th>Expected</th>
            <th>Actual</th>
            <th>Status</th>
            <th>Remarks</th>
            <th>Missing Fields</th>
            <th>Invalid Fields</th>
        </tr>
        </thead>
        <tbody>
        {% for row in results %}
        <tr class="{% if row.Status == 'Missing Value Error' %}row-missing{% elif row.Status == 'Invalid Value Error' %}row-invalid{% endif %}">
            <td class="mono">{{ row.TC_ID }}</td>
            <td class="mono">{{ row.Excel_Row }}</td>
            <td>{% if row.Test_Description %}{{ row.Test_Description }}{% else %}<span class="field-blank">(blank)</span>{% endif %}</td>
            <td class="mono">{% if row.User_Action %}{{ row.User_Action }}{% else %}<span class="field-blank">(blank)</span>{% endif %}</td>
            <td>{% if row.Expected_Result %}{{ row.Expected_Result }}{% else %}<span class="field-blank">(blank)</span>{% endif %}</td>
            <td>{{ row.Actual_Result }}</td>
            <td>
                {% if row.Status == "Pass" %}<span class="pill pill-pass">PASS</span>
                {% elif row.Status == "Fail" %}<span class="pill pill-fail">FAIL</span>
                {% elif row.Status == "Missing Value Error" %}<span class="pill pill-missing">MISSING VALUE</span>
                {% else %}<span class="pill pill-invalid">INVALID VALUE</span>{% endif %}
            </td>
            <td>{{ row.Remarks }}</td>
            <td class="audit-cell {{ 'missing-text' if row.Missing_Fields else 'none' }}">{{ row.Missing_Fields if row.Missing_Fields else '&mdash;' }}</td>
            <td class="audit-cell {{ 'invalid-text' if row.Invalid_Fields else 'none' }}">{{ row.Invalid_Fields if row.Invalid_Fields else '&mdash;' }}</td>
        </tr>
        {% endfor %}
        </tbody>
    </table>
    </div>

    <h2>Failed Test Cases</h2>
    {% if failed_results %}
        {% for row in failed_results %}
        <div class="alert-panel fail">
            <div class="tc-id">{{ row.TC_ID }} &middot; Row {{ row.Excel_Row }}</div>
            <div class="detail"><span class="lbl">Expected:</span> {{ row.Expected_Result }} &nbsp;&nbsp; <span class="lbl">Actual:</span> {{ row.Actual_Result }}</div>
            <div class="detail" style="margin-top:4px;"><span class="lbl">Remarks:</span> {{ row.Remarks }}</div>
            {% if row.Mismatch_Reason %}
            <div class="detail" style="margin-top:4px;"><span class="lbl">Reason:</span> {{ row.Mismatch_Reason }}</div>
            {% endif %}
        </div>
        {% endfor %}
    {% else %}
        <div class="clean-panel">No failed test cases.</div>
    {% endif %}

    <h2>Missing Value Errors</h2>
    {% if missing_results %}
        {% for row in missing_results %}
        <div class="alert-panel missing">
            <div class="tc-id">{{ row.TC_ID }} &middot; Row {{ row.Excel_Row }}</div>
            <div class="detail"><span class="lbl">Missing:</span> {{ row.Missing_Fields if row.Missing_Fields else "Expected Result" }}</div>
            <div class="detail" style="margin-top:4px;"><span class="lbl">Details:</span> {{ row.Remarks }}</div>
        </div>
        {% endfor %}
    {% else %}
        <div class="clean-panel">No missing value errors - every required cell was filled in.</div>
    {% endif %}

    <h2>Invalid Value Errors</h2>
    {% if invalid_results %}
        {% for row in invalid_results %}
        <div class="alert-panel invalid">
            <div class="tc-id">{{ row.TC_ID }} &middot; Row {{ row.Excel_Row }}</div>
            <div class="detail"><span class="lbl">Invalid:</span> {{ row.Invalid_Fields }}</div>
            <div class="detail" style="margin-top:4px;"><span class="lbl">Details:</span> {{ row.Remarks }}</div>
        </div>
        {% endfor %}
    {% else %}
        <div class="clean-panel">No invalid value errors - every recognized cell matched its expected format.</div>
    {% endif %}

    <div class="footer">
        <span>TEST AUTOMATION FRAMEWORK</span>
        <span>{{ generated_on }}</span>
    </div>
</div>
</body>
</html>
"""


class HTMLReportGenerator:

    @staticmethod
    def create_report(df, pass_count, fail_count, missing_count, invalid_count, output_html,
                       report_title="Test Execution Report", chart_path=None):
        total_tc = len(df)

        results = normalize_records(df)
        failed_results = normalize_records(df[df["Status"] == "Fail"])
        missing_results = normalize_records(df[df["Status"] == "Missing Value Error"])
        invalid_results = normalize_records(df[df["Status"] == "Invalid Value Error"])

        chart_base64 = None
        if chart_path and os.path.exists(chart_path):
            with open(chart_path, "rb") as chart_file:
                chart_base64 = base64.b64encode(chart_file.read()).decode("utf-8")

        template = Template(HTML_TEMPLATE)
        html_content = template.render(
            report_title=report_title,
            generated_on=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_tc=total_tc,
            pass_count=pass_count,
            fail_count=fail_count,
            missing_count=missing_count,
            invalid_count=invalid_count,
            chart_base64=chart_base64,
            results=results,
            failed_results=failed_results,
            missing_results=missing_results,
            invalid_results=invalid_results,
        )

        os.makedirs(os.path.dirname(output_html), exist_ok=True)
        with open(output_html, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"[HTMLReportGenerator] HTML report saved to '{output_html}'")
