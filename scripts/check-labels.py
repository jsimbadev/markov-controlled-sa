#!/usr/bin/env python3
"""Check index.qmd and its includes for broken includes, labels, and references."""

import argparse
from pathlib import Path
import sys

from source_checks import article_sources, format_issue, label_issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    arguments = parser.parse_args()
    root = arguments.root.resolve()
    try:
        sources, issues = article_sources(root)
    except (OSError, UnicodeError) as error:
        print(f"Label check failed: {error}", file=sys.stderr)
        return 1
    label_errors, definition_count, reference_count = label_issues(sources)
    issues.extend(label_errors)
    for issue in issues:
        print(format_issue(issue, root), file=sys.stderr)
    if issues:
        return 1
    print(f"Label check passed ({definition_count} labels, {reference_count} cross-references).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
