#!/usr/bin/env python3
"""Check that citation keys in Quarto prose exist in references.bib."""

import argparse
from pathlib import Path
import sys

from source_checks import bibliography_entries, citation_issues, format_issue, source_files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    arguments = parser.parse_args()
    root = arguments.root.resolve()
    bibliography = root / "references.bib"
    try:
        entries, issues = bibliography_entries(bibliography, bibliography.read_text(encoding="utf-8"))
        sources = {path: path.read_text(encoding="utf-8") for path in source_files(root)}
    except (OSError, UnicodeError) as error:
        print(f"Citation check failed: {error}", file=sys.stderr)
        return 1
    if not sources:
        print("Citation check failed: no .qmd source files found.", file=sys.stderr)
        return 1
    citation_errors, used_count = citation_issues(sources, entries)
    issues.extend(citation_errors)
    for issue in issues:
        print(format_issue(issue, root), file=sys.stderr)
    if issues:
        return 1
    print(f"Citation check passed ({used_count} keys used, {len(entries)} bibliography entries).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
