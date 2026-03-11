from __future__ import annotations


class ReportTool:
    def get_latest_report(self, patient_id: str) -> str | None:
        return "Impression: Mild degenerative changes in L4-L5. No acute findings."

    def summarize(self, report_text: str) -> str:
        return "The report notes mild age-related changes at L4-L5 and no urgent findings."
