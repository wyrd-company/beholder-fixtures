"""Markup report domain glue (thematic integration).

Combines report building, markup rendering, and utility helpers
without adding new checklist obligations beyond the per-module files.
"""

from markup_report_toolkit.docstrings import ReportSection, render_report
from markup_report_toolkit.soft_keywords import classify_report_node
from markup_report_toolkit.fstrings import render_report as f_render

def build_sample_report() -> str:
    sections = [
        ReportSection("Introduction", "This is the opening section."),
        ReportSection("Body", "Main content with markup."),
        ReportSection("Conclusion", "Closing remarks."),
    ]
    return render_report("Quarterly Report", sections)

def classify_sample() -> str:
    return classify_report_node({"kind": "section", "title": "intro"})

def render_f_sample() -> str:
    return f_render("title", 42)

__all__ = ["build_sample_report", "classify_sample", "render_f_sample"]
