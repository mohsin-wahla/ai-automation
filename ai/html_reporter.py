from pathlib import Path
from html import escape


class HTMLReporter:

    def __init__(self):
        self.project_root = (
            Path(__file__).resolve().parent.parent
        )

        self.report_dir = (
            self.project_root / "reports"
        )

    def generate(self, report: dict):

        self.report_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        html_file = (
            self.report_dir
            / "test_execution_report.html"
        )

        summary = report.get("summary", {})

        total = summary.get("total", 0)
        passed = summary.get("passed", 0)
        failed = summary.get("failed", 0)
        healed = summary.get("healed", 0)

        execution_time = report.get(
            "execution_time",
            "N/A"
        )

        final_status = report.get(
            "final_status",
            "UNKNOWN"
        )

        status_class = (
            "passed"
            if failed == 0
            else "failed"
        )

        test_rows = []

        for test in report.get("tests", []):

            test_case_id = escape(
                str(test.get("test_case_id", "UNKNOWN"))
            )

            test_name = escape(
                str(test.get("test_name", "UNKNOWN"))
            )

            test_file = escape(
                str(test.get("test_file", "UNKNOWN"))
            )

            status = test.get(
                "status",
                "UNKNOWN"
            )

            if status == "PASSED":

                status_class_test = "passed"
                status_badge = "✓ PASSED"

            elif status == "HEALED":

                status_class_test = "healed"
                status_badge = "✓ HEALED"

            else:

                status_class_test = "failed"
                status_badge = "✗ FAILED"

            ai_analysis = test.get(
                "ai_analysis"
            )

            analysis_html = ""

            if ai_analysis:

                analysis_html = f"""
                <div class="analysis">
                    <div class="analysis-title">
                        AI Failure Analysis
                    </div>

                    <pre>{escape(
                    str(ai_analysis)
                )}</pre>
                </div>
                """

            else:

                if status == "FAILED":
                    analysis_html = """
                    <div class="analysis unavailable">
                        AI failure analysis was not available
                        for this test.
                    </div>
                    """

            # --------------------------------
            # Self-Healing information
            # --------------------------------

            healing = test.get(
                "self_healing"
            )

            healing_html = ""

            if healing:

                healing_attempted = healing.get(
                    "healing_attempted",
                    False
                )

                healing_applied = healing.get(
                    "healing_applied",
                    False
                )

                healing_type = healing.get(
                    "healing_type",
                    "none"
                )

                changed_file = healing.get(
                    "changed_file"
                )

                reason = healing.get(
                    "reason"
                )

                rerun = healing.get(
                    "rerun"
                )

                if healing_applied:

                    if rerun and rerun.get("passed"):

                        healing_status = "✓ HEALED"
                        healing_status_class = "healed"

                    elif rerun:

                        healing_status = "✗ FAILED AFTER HEALING"
                        healing_status_class = "failed"

                    else:

                        healing_status = "⚠ FIX APPLIED"
                        healing_status_class = "healed"

                    changed_file_html = ""

                    if changed_file:
                        changed_file_html = f"""
                        <div class="healing-detail">
                            <strong>Changed File:</strong>
                            {escape(str(changed_file))}
                        </div>
                        """

                    healing_html = f"""
                    <div class="healing">

                        <div class="healing-title">
                            Self-Healing
                        </div>

                        <div class="healing-body">

                            <div class="healing-status {healing_status_class}">
                                {healing_status}
                            </div>

                            <div class="healing-detail">
                                <strong>Type:</strong>
                                {escape(str(healing_type))}
                            </div>

                            {changed_file_html}

                            <div class="healing-detail">
                                <strong>Reason:</strong>
                                {escape(str(reason or "N/A"))}
                            </div>

                        </div>

                    </div>
                    """

                elif healing_attempted:

                    healing_html = f"""
                    <div class="healing not-healed">

                        <div class="healing-title">
                            Self-Healing
                        </div>

                        <div class="healing-body">

                            <div class="healing-status failed">
                                ✗ HEALING NOT APPLIED
                            </div>

                            <div class="healing-detail">
                                <strong>Type:</strong>
                                {escape(str(healing_type))}
                            </div>

                            <div class="healing-detail">
                                <strong>Reason:</strong>
                                {escape(str(reason or "N/A"))}
                            </div>

                        </div>

                    </div>
                    """

                else:

                    healing_html = f"""
                    <div class="healing not-attempted">

                        <div class="healing-title">
                            Self-Healing
                        </div>

                        <div class="healing-body">

                            <div class="healing-status neutral">
                                NOT ATTEMPTED
                            </div>

                            <div class="healing-detail">
                                <strong>Reason:</strong>
                                {escape(str(reason or "N/A"))}
                            </div>

                        </div>

                    </div>
                    """

            test_rows.append(
                f"""
                <tr>
                    <td>
                        <span class="test-id">
                            {test_case_id}
                        </span>
                    </td>

                    <td>
                        <strong>
                            {test_name}
                        </strong>

                        <div class="test-file">
                            {test_file}
                        </div>

                        {analysis_html}
                        {healing_html}
                    </td>

                    <td>
                        <span class="badge {status_class_test}">
                            {status_badge}
                        </span>
                    </td>
                </tr>
                """
            )

        tests_html = "\n".join(test_rows)

        html = f"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>AI Automation Test Report</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    padding: 0;

    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Roboto,
        Arial,
        sans-serif;

    background: #f4f6f9;
    color: #1f2937;
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 32px;
}}

.header {{
    background: linear-gradient(
        135deg,
        #111827,
        #1f2937
    );

    color: white;

    padding: 32px;

    border-radius: 14px;

    margin-bottom: 24px;

    box-shadow:
        0 8px 25px
        rgba(0, 0, 0, 0.08);
}}

.header h1 {{
    margin: 0 0 8px 0;
    font-size: 28px;
}}

.header p {{
    margin: 0;
    color: #d1d5db;
}}

.summary {{
    display: grid;

    grid-template-columns:
        repeat(5, 1fr);

    gap: 16px;

    margin-bottom: 24px;
}}

.card {{
    background: white;

    padding: 22px;

    border-radius: 12px;

    box-shadow:
        0 3px 12px
        rgba(0, 0, 0, 0.06);
}}

.card-label {{
    color: #6b7280;

    font-size: 13px;

    text-transform: uppercase;

    letter-spacing: 0.5px;
}}

.card-value {{
    font-size: 30px;

    font-weight: 700;

    margin-top: 8px;
}}

.card-value.total {{
    color: #374151;
}}

.card-value.passed {{
    color: #16a34a;
}}

.card-value.failed {{
    color: #dc2626;
}}
.card-value.healed {{
    color: #2563eb;
}}
.card-value.status {{
    font-size: 18px;
}}

.status-box {{
    background: white;

    border-radius: 12px;

    padding: 20px;

    margin-bottom: 24px;

    border-left:
        5px solid #16a34a;
}}

.status-box.failed {{
    border-left-color: #dc2626;
}}

.status-box strong {{
    font-size: 16px;
}}

.report-section {{
    background: white;

    border-radius: 12px;

    padding: 24px;

    box-shadow:
        0 3px 12px
        rgba(0, 0, 0, 0.06);
}}

.report-section h2 {{
    margin-top: 0;

    font-size: 20px;
}}

table {{
    width: 100%;

    border-collapse: collapse;
}}

th {{
    text-align: left;

    background: #f9fafb;

    padding: 14px;

    border-bottom:
        1px solid #e5e7eb;

    font-size: 13px;

    color: #6b7280;

    text-transform: uppercase;
}}

td {{
    padding: 18px 14px;

    border-bottom:
        1px solid #e5e7eb;

    vertical-align: top;
}}

tr:last-child td {{
    border-bottom: none;
}}

.test-id {{
    font-family: monospace;

    background: #eef2ff;

    color: #4338ca;

    padding: 6px 9px;

    border-radius: 6px;

    font-size: 13px;
}}

.test-file {{
    color: #9ca3af;

    font-size: 12px;

    margin-top: 6px;

    word-break: break-all;
}}

.badge {{
    display: inline-block;

    padding: 6px 10px;

    border-radius: 20px;

    font-size: 12px;

    font-weight: 700;
}}

.badge.passed {{
    background: #dcfce7;
    color: #15803d;
}}

.badge.failed {{
    background: #fee2e2;
    color: #b91c1c;
}}
.badge.healed {{
    background: #dbeafe;
    color: #1d4ed8;
}}

.analysis {{
    margin-top: 18px;

    border:
        1px solid #fecaca;

    border-radius: 10px;

    background: #fff7f7;

    overflow: hidden;
}}

.analysis-title {{
    background: #fef2f2;

    color: #991b1b;

    font-weight: 700;

    padding: 12px 14px;

    border-bottom:
        1px solid #fecaca;
}}

.analysis pre {{
    margin: 0;

    padding: 16px;

    white-space: pre-wrap;

    word-break: break-word;

    font-family:
        "Segoe UI",
        Arial,
        sans-serif;

    font-size: 13px;

    line-height: 1.6;

    color: #374151;
}}

.analysis.unavailable {{
    padding: 12px 14px;

    background: #f9fafb;

    border-color: #e5e7eb;

    color: #6b7280;

    font-size: 13px;
}}
.healing {{
    margin-top: 18px;

    border:
        1px solid #bfdbfe;

    border-radius: 10px;

    background: #f8fbff;

    overflow: hidden;
}}

.healing-title {{
    background: #eff6ff;

    color: #1d4ed8;

    font-weight: 700;

    padding: 12px 14px;

    border-bottom:
        1px solid #bfdbfe;
}}

.healing-body {{
    padding: 14px;
}}

.healing-status {{
    display: inline-block;

    padding: 6px 10px;

    border-radius: 20px;

    font-size: 12px;

    font-weight: 700;

    margin-bottom: 10px;
}}

.healing-status.healed {{
    background: #dcfce7;

    color: #15803d;
}}

.healing-status.failed {{
    background: #fee2e2;

    color: #b91c1c;
}}

.healing-status.neutral {{
    background: #f3f4f6;

    color: #6b7280;
}}

.healing-detail {{
    font-size: 13px;

    line-height: 1.6;

    color: #374151;

    margin-top: 5px;

    word-break: break-word;
}}

.footer {{
    text-align: center;

    color: #9ca3af;

    font-size: 12px;

    margin-top: 24px;
}}

@media (max-width: 800px) {{

    .container {{
        padding: 16px;
    }}

    .summary {{
        grid-template-columns:
            repeat(2, 1fr);
    }}

    table {{
        display: block;
        overflow-x: auto;
    }}

}}

</style>

</head>

<body>

<div class="container">

    <div class="header">

        <h1>
            AI Automation Test Report
        </h1>

        <p>
            Playwright + Pytest Execution Report
        </p>

    </div>


    <div class="summary">

        <div class="card">

            <div class="card-label">
                Total Tests
            </div>

            <div class="card-value total">
                {total}
            </div>

        </div>


        <div class="card">

            <div class="card-label">
                Passed
            </div>

            <div class="card-value passed">
                {passed}
            </div>

        </div>


        <div class="card">

            <div class="card-label">
                Failed
            </div>

            <div class="card-value failed">
                {failed}
            </div>

        </div>

        <div class="card">

            <div class="card-label">
                Healed
            </div>
        
            <div class="card-value healed">
                {healed}
            </div>
        
        </div>
        <div class="card">

            <div class="card-label">
                Execution Status
            </div>

            <div class="card-value status">
                {escape(final_status)}
            </div>

        </div>

    </div>


    <div class="status-box {status_class}">

        <strong>
            Execution Time:
        </strong>

        {escape(execution_time)}

    </div>


    <div class="report-section">

        <h2>
            Test Results
        </h2>

        <table>

            <thead>

                <tr>

                    <th>
                        Test Case
                    </th>

                    <th>
                        Test Details
                    </th>

                    <th>
                        Status
                    </th>

                </tr>

            </thead>

            <tbody>

                {tests_html}

            </tbody>

        </table>

    </div>


    <div class="footer">

        Generated by AI Automation Framework

    </div>

</div>

</body>

</html>
"""

        html_file.write_text(
            html,
            encoding="utf-8"
        )

        print(
            f"HTML report saved to: {html_file}"
        )

        return html_file
