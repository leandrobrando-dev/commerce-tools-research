#!/usr/bin/env python3
"""Regenerate HTML twins for planning artifacts.

Two modes per file:
  1. Lagging update — existing .html exists; refresh embedded markdown + meta date,
     preserve the chrome (title, breadcrumb, phase chip, eyebrow, subtitle).
  2. New twin — no .html exists; instantiate from _doc-reader-header.html and
     _doc-reader-footer.html templates with explicit metadata supplied.

Run from repo root:
    python3 scripts/regenerate_html_twins.py
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PA_ROOT = REPO_ROOT / "_bmad-output" / "planning-artifacts"
HTML_ROOT = PA_ROOT / "html"
TODAY = date.today().isoformat()


# ----------------------------------------------------------------------
# Lagging-twin update — replace embedded markdown + bump "updated" date
# ----------------------------------------------------------------------

LAGGING_TWINS = [
    # (md_relpath_under_PA_ROOT, html_relpath_under_HTML_ROOT)
    ("prd.md", "prd.html"),
    ("epics.md", "epics.html"),
    ("stories.md", "stories.html"),
    ("architecture.md", "architecture.html"),
    ("ux-design-specification.md", "ux-design-specification.html"),
    (
        "briefs/elevator-pitch-commercetools-next-gen-frontend-2026-05-05.md",
        "briefs/elevator-pitch-commercetools-next-gen-frontend-2026-05-05.html",
    ),
    (
        "briefs/interview-narrative-head-of-product-nextgen-frontend-2026-05-04.md",
        "briefs/interview-narrative-head-of-product-nextgen-frontend-2026-05-04.html",
    ),
    (
        "decisions/adr-004-tracking-layer-architecture.md",
        "adr-004-tracking-layer-architecture.html",
    ),
    (
        "reports/implementation-readiness-report-2026-05-12.md",
        "implementation-readiness-report-2026-05-12.html",
    ),
    (
        "research/market-golden-path-architecture-cdp-positioning-research-2026-05-12.md",
        "research/market-golden-path-architecture-cdp-positioning-research-2026-05-12.html",
    ),
    (
        "reports/implementation-readiness-report-2026-05-12-v2.md",
        "implementation-readiness-report-2026-05-12-v2.html",
    ),
]


def update_lagging_twin(md_path: Path, html_path: Path) -> None:
    md_content = md_path.read_text()
    html = html_path.read_text()

    pattern = (
        r'(<script type="text/markdown" id="markdown-source">\n)'
        r"(.*?)"
        r"(\n</script>)"
    )

    def _swap(m: re.Match[str]) -> str:
        return m.group(1) + md_content + m.group(3)

    new_html, n = re.subn(pattern, _swap, html, count=1, flags=re.DOTALL)
    if n != 1:
        raise RuntimeError(f"Could not locate <script type=text/markdown> in {html_path}")

    new_html = re.sub(
        r'<span class="meta">updated \d{4}-\d{2}-\d{2}',
        f'<span class="meta">updated {TODAY}',
        new_html,
        count=1,
    )

    html_path.write_text(new_html)
    print(f"  refreshed {html_path.relative_to(REPO_ROOT)}")


# ----------------------------------------------------------------------
# New-twin instantiation — use header/footer templates with metadata
# ----------------------------------------------------------------------

NEW_TWINS: list[dict] = [
    # md_relpath, html_relpath, title, subtitle, phase_slug, phase_label, breadcrumb, doc_type
    # Empty after each session — entries move to LAGGING_TWINS once instantiated.
]


def create_new_twin(spec: dict) -> None:
    md_path = PA_ROOT / spec["md"]
    html_path = HTML_ROOT / spec["html"]

    md_content = md_path.read_text()
    header_template = (HTML_ROOT / "_doc-reader-header.html").read_text()
    footer_template = (HTML_ROOT / "_doc-reader-footer.html").read_text()

    depth = len(html_path.relative_to(HTML_ROOT).parts) - 1
    css_path = "../" * depth
    backlink_path = "../" * depth

    header = (
        header_template
        .replace("DOC_TITLE", spec["title"])
        .replace("CSS_PATH_", css_path)
        .replace("BACKLINK_PATH", backlink_path)
        .replace("PHASE_SLUG", spec["phase_slug"])
        .replace("PHASE_LABEL", spec["phase_label"])
        .replace("BREADCRUMB_TEXT", spec["breadcrumb"])
        .replace("DOC_META", f"created {TODAY}")
        .replace("DOC_SUBTITLE", spec["subtitle"])
        .replace("DOC_TYPE", spec["doc_type"])
    )

    full_html = header + md_content + footer_template

    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(full_html)
    print(f"  created   {html_path.relative_to(REPO_ROOT)}")


# ----------------------------------------------------------------------
# Driver
# ----------------------------------------------------------------------


def main() -> None:
    print(f"Regenerating HTML twins (date: {TODAY})")
    print()
    print("Lagging-twin updates:")
    for md_rel, html_rel in LAGGING_TWINS:
        md_path = PA_ROOT / md_rel
        html_path = HTML_ROOT / html_rel
        if not md_path.exists():
            print(f"  SKIP (md missing): {md_rel}")
            continue
        if not html_path.exists():
            print(f"  SKIP (html missing — would need new-twin spec): {html_rel}")
            continue
        update_lagging_twin(md_path, html_path)

    print()
    print("New-twin instantiations:")
    for spec in NEW_TWINS:
        md_path = PA_ROOT / spec["md"]
        html_path = HTML_ROOT / spec["html"]
        if not md_path.exists():
            print(f"  SKIP (md missing): {spec['md']}")
            continue
        if html_path.exists():
            print(f"  SKIP (already exists, use lagging-update path): {spec['html']}")
            continue
        create_new_twin(spec)

    print()
    print("Done.")


if __name__ == "__main__":
    main()
