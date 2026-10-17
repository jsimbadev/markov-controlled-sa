#!/usr/bin/env python3
"""Generate the MathJax vocabulary from the canonical portable TeX macros."""

import argparse
import json
from pathlib import Path
import re
import sys


DEFINITION = re.compile(r"\\newcommand\{\\([A-Za-z]+)\}(?:\[([1-9])\])?\{(.*)\}")


def read_macros(path):
    macros = {}
    for line_number, source_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        source_line = source_line.strip()
        if not source_line or source_line.startswith("%"):
            continue
        match = DEFINITION.fullmatch(source_line)
        if match is None:
            raise ValueError(f"{path.name}:{line_number}: expected a single-line \\newcommand definition")
        name, argument_count, body = match.groups()
        if name in macros:
            raise ValueError(f"{path.name}:{line_number}: duplicate macro \\{name}")
        depth = 0
        escaped = False
        for character in body:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == "{":
                depth += 1
            elif character == "}":
                depth -= 1
                if depth < 0:
                    break
        if depth != 0:
            raise ValueError(f"{path.name}:{line_number}: unbalanced braces in \\{name}")
        count = int(argument_count or 0)
        arguments = {int(number) for number in re.findall(r"(?<!\\)#([1-9])", body)}
        if arguments != set(range(1, count + 1)):
            raise ValueError(f"{path.name}:{line_number}: argument mismatch in \\{name}")
        macros[name] = [body, count] if count else body
    if not macros:
        raise ValueError(f"{path.name}: no macro definitions found")
    return macros


def render_header(macros):
    definitions = json.dumps(macros, ensure_ascii=True, indent=2)
    return (
        '<!-- Generated from macros.tex by scripts/sync-macros.py; edit macros.tex. -->\n'
        '<script>\n'
        'window.MathJax = window.MathJax || {};\n'
        'window.MathJax.tex = window.MathJax.tex || {};\n'
        'window.MathJax.tex.macros = Object.assign(\n'
        '  {},\n'
        '  window.MathJax.tex.macros || {},\n'
        f'{definitions}\n'
        ');\n'
        '</script>\n'
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the generated HTML header is stale")
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    target = root / "mathjax-macros.html"
    try:
        macros = read_macros(root / "macros.tex")
        expected = render_header(macros)
        current = target.read_text(encoding="utf-8") if target.exists() else None
        if arguments.check:
            if current != expected:
                print("MathJax macros are stale; run python3 scripts/sync-macros.py", file=sys.stderr)
                return 1
            print(f"MathJax macros match macros.tex ({len(macros)} commands).")
        else:
            if current != expected:
                with target.open("w", encoding="utf-8", newline="\n") as output:
                    output.write(expected)
            print(f"MathJax macros synchronized ({len(macros)} commands).")
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
