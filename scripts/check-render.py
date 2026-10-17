import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys


class LinkChecker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.identifiers = set()
        self.links = []
        self.duplicates = set()
        self.unresolved = False

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        if "id" in attributes:
            if attributes["id"] in self.identifiers:
                self.duplicates.add(attributes["id"])
            self.identifiers.add(attributes["id"])
        if tag == "a" and attributes.get("href", "").startswith("#"):
            self.links.append(attributes["href"][1:])
        if "unresolved" in attributes.get("class", "").split():
            self.unresolved = True


def main():
    parser = argparse.ArgumentParser(description="Render both formats and check diagnostics and HTML links.")
    parser.add_argument("--quarto", default="quarto")
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    html_path = root / "_output/index.html"
    pdf_path = root / "_output/index.pdf"
    html_path.unlink(missing_ok=True)
    pdf_path.unlink(missing_ok=True)
    result = subprocess.run(
        [arguments.quarto, "render", "--to", "all"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    print(result.stdout, end="")
    if result.returncode:
        return result.returncode
    diagnostics = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", result.stdout)
    if re.search(
        r"unable to resolve crossref|citation .* not found|undefined (?:references|citations)"
        r"|multiply[- ]defined|duplicate (?:label|identifier)|LaTeX Warning:.*undefined",
        diagnostics,
        re.IGNORECASE,
    ):
        print("Render check failed: unresolved or duplicate references in render diagnostics.", file=sys.stderr)
        return 1
    if not html_path.is_file() or not pdf_path.is_file() or pdf_path.stat().st_size < 100:
        print("Render check failed: HTML or PDF output is missing or empty.", file=sys.stderr)
        return 1
    checker = LinkChecker()
    checker.feed(html_path.read_text(encoding="utf-8"))
    missing = sorted(set(checker.links) - checker.identifiers - {""})
    if checker.unresolved or missing or checker.duplicates:
        print(
            f"Render check failed: unresolved HTML targets: {missing}; "
            f"duplicate IDs: {sorted(checker.duplicates)}",
            file=sys.stderr,
        )
        return 1
    print("Render checks passed: HTML/PDF built; local HTML links resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
