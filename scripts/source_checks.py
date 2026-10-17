"""Small, source-oriented checks for a Quarto research note."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import re
import shlex


IGNORED_DIRECTORIES = {
    ".git", ".quarto", ".venv", "__pycache__", "_freeze", "_output",
    "_site", "build", "dist", "node_modules", "venv",
}
CROSSREF_PREFIXES = {
    "sec", "eq", "fig", "tbl", "thm", "prp", "prop", "lem", "cor",
    "def", "asm", "cnj", "rem", "exm", "lst",
}
AT_TOKEN = re.compile(
    r"@(?P<key>[\w](?:[\w:.#$%&+?<>~/-]*[\w])?)", re.UNICODE
)
ATTRIBUTES = re.compile(r"(?<!\\)\{(?P<attributes>[^{}]*)\}")
IDENTIFIER = re.compile(r"(?:^|\s)#(?P<label>[\w][\w:.-]*)")
EMAIL = re.compile(r"[\w.!#$%&'*+/=?^`{|}~-]+@[\w-]+(?:\.[\w-]+)+")
INCLUDE = re.compile(r"\{\{<\s*include\b(?P<arguments>[\s\S]*?)>\}\}")


@dataclass(frozen=True)
class Occurrence:
    path: Path
    line: int
    value: str


@dataclass(frozen=True)
class Issue:
    path: Path
    line: int
    message: str


def source_files(root: Path) -> list[Path]:
    paths = []
    for directory, subdirectories, filenames in os.walk(root):
        subdirectories[:] = [name for name in subdirectories if name not in IGNORED_DIRECTORIES]
        paths.extend(Path(directory) / name for name in filenames if name.endswith(".qmd"))
    return sorted(paths)


def _blank(text: str) -> str:
    return "".join("\n" if character == "\n" else " " for character in text)


def _escaped(text: str, position: int) -> bool:
    backslashes = 0
    position -= 1
    while position >= 0 and text[position] == "\\":
        backslashes += 1
        position -= 1
    return backslashes % 2 == 1


def visible_markdown(text: str) -> str:
    """Mask examples and metadata, preserving offsets for useful diagnostics.

    This deliberately does not implement Pandoc. It recognizes the common
    Markdown constructs used in the note and leaves rendered prose and math.
    """
    text = re.sub(r"<!--[\s\S]*?(?:-->|\Z)", lambda match: _blank(match[0]), text)
    lines = text.splitlines(keepends=True)
    in_front_matter = bool(lines and lines[0].strip() == "---")
    fence_character = ""
    fence_length = 0
    for line_number, line in enumerate(lines):
        if in_front_matter:
            lines[line_number] = _blank(line)
            if line_number and line.strip() in {"---", "..."}:
                in_front_matter = False
            continue
        fence = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
        if fence_character:
            lines[line_number] = _blank(line)
            if (
                fence and fence[1][0] == fence_character
                and len(fence[1]) >= fence_length and not fence[2].strip()
            ):
                fence_character = ""
            continue
        if fence:
            fence_character = fence[1][0]
            fence_length = len(fence[1])
            lines[line_number] = _blank(line)
    text = "".join(lines)
    characters = list(text)
    position = 0
    while position < len(text):
        if text[position] != "`" or _escaped(text, position):
            position += 1
            continue
        opening = re.match(r"`+", text[position:])[0]
        end = position + len(opening)
        closing = None
        while end < len(text):
            candidate = text.find(opening, end)
            if candidate < 0:
                break
            after = candidate + len(opening)
            if (candidate == 0 or text[candidate - 1] != "`") and (
                after == len(text) or text[after] != "`"
            ):
                closing = after
                break
            end = after
        if closing is None:
            position += len(opening)
            continue
        characters[position:closing] = _blank(text[position:closing])
        position = closing
    text = "".join(characters)
    text = re.sub(
        r"<(script|style|pre|textarea)\b[^>]*>[\s\S]*?</\1\s*>",
        lambda match: _blank(match[0]), text, flags=re.IGNORECASE,
    )
    text = re.sub(
        r"\\begin\{(?P<environment>[A-Za-z*]+)\}[\s\S]*?\\end\{(?P=environment)\}",
        lambda match: _blank(match[0]), text,
    )
    text = re.sub(
        r"\\verb\*?(?P<delimiter>[^\w\s])[^\n]*?(?P=delimiter)",
        lambda match: _blank(match[0]), text,
    )
    text = re.sub(
        r"<(?:/?[A-Za-z][^<>\n]*|[!?][^<>\n]*|[^<>\s]+@[^<>\s]+)>",
        lambda match: _blank(match[0]), text,
    )
    return EMAIL.sub(lambda match: _blank(match[0]), text)


def at_tokens(path: Path, text: str) -> list[Occurrence]:
    visible = visible_markdown(text)
    occurrences = []
    for match in AT_TOKEN.finditer(visible):
        if _escaped(visible, match.start()):
            continue
        if match.start() and (visible[match.start() - 1].isalnum() or visible[match.start() - 1] == "@"):
            continue
        occurrences.append(Occurrence(path, visible.count("\n", 0, match.start()) + 1, match["key"]))
    return occurrences


def labels(path: Path, text: str) -> list[Occurrence]:
    visible = visible_markdown(text)
    occurrences = []
    for attributes in ATTRIBUTES.finditer(visible):
        for match in IDENTIFIER.finditer(attributes["attributes"]):
            offset = attributes.start("attributes") + match.start("label")
            occurrences.append(Occurrence(path, visible.count("\n", 0, offset) + 1, match["label"]))
    return occurrences


def is_crossref(key: str) -> bool:
    return "-" in key and key.split("-", 1)[0] in CROSSREF_PREFIXES


def display_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def format_issue(issue: Issue, root: Path) -> str:
    return f"{display_path(issue.path, root)}:{issue.line}: {issue.message}"


def article_sources(root: Path) -> tuple[dict[Path, str], list[Issue]]:
    """Follow index.qmd includes using paths relative to the main document."""
    root = root.resolve()
    entry = root / "index.qmd"
    sources = {}
    issues = []
    included = {entry: Occurrence(entry, 1, "index.qmd")}

    def visit(path: Path, ancestors: set[Path]) -> None:
        sources[path] = path.read_text(encoding="utf-8")
        visible = visible_markdown(sources[path])
        for match in INCLUDE.finditer(visible):
            line = visible.count("\n", 0, match.start()) + 1
            try:
                arguments = shlex.split(match["arguments"])
            except ValueError as error:
                issues.append(Issue(path, line, f"invalid include path: {error}"))
                continue
            if len(arguments) != 1:
                issues.append(Issue(path, line, "include shortcode requires one path; quote paths containing spaces"))
                continue
            target = (root / arguments[0].lstrip("/")).resolve()
            name = display_path(target, root)
            if target in ancestors:
                issues.append(Issue(path, line, f"cyclic include '{name}'"))
            elif target in included:
                previous = included[target]
                issues.append(Issue(
                    path, line,
                    f"duplicate include '{name}'; first included at {display_path(previous.path, root)}:{previous.line}",
                ))
            elif not target.is_file():
                issues.append(Issue(path, line, f"included source '{name}' does not exist or is not a file"))
            else:
                included[target] = Occurrence(path, line, name)
                visit(target, ancestors | {target})

    visit(entry, {entry})
    return sources, issues


def label_issues(sources: dict[Path, str]) -> tuple[list[Issue], int, int]:
    definitions: dict[str, Occurrence] = {}
    references = []
    issues = []
    for path, text in sources.items():
        for occurrence in labels(path, text):
            if occurrence.value.startswith("prop-"):
                issues.append(Issue(path, occurrence.line, "use Quarto's native 'prp-' prefix instead of 'prop-'"))
            elif occurrence.value.startswith("cnj-"):
                issues.append(Issue(path, occurrence.line, "'cnj-' is reserved by the Assumption adapter; use 'asm-'"))
            previous = definitions.get(occurrence.value)
            if previous:
                issues.append(Issue(
                    path, occurrence.line,
                    f"duplicate label '{occurrence.value}'; first defined at {previous.path}:{previous.line}",
                ))
            else:
                definitions[occurrence.value] = occurrence
        references.extend(occurrence for occurrence in at_tokens(path, text) if is_crossref(occurrence.value))
    for occurrence in references:
        if occurrence.value.startswith("prop-"):
            issues.append(Issue(occurrence.path, occurrence.line, "use Quarto's native '@prp-' prefix instead of '@prop-'"))
        elif occurrence.value.startswith("cnj-"):
            issues.append(Issue(occurrence.path, occurrence.line, "'@cnj-' is reserved by the Assumption adapter; use '@asm-'"))
        elif occurrence.value not in definitions:
            issues.append(Issue(occurrence.path, occurrence.line, f"unresolved cross-reference '@{occurrence.value}'"))
    return issues, len(definitions), len(references)


def _entry_end(text: str, opening: int) -> int | None:
    delimiter = text[opening]
    brace_depth = int(delimiter == "{")
    quoted = False
    position = opening + 1
    while position < len(text):
        character = text[position]
        if character == "\\":
            position += 2
            continue
        if character == '"' and brace_depth == int(delimiter == "{"):
            quoted = not quoted
        if character == "{":
            brace_depth += 1
        elif character == "}":
            brace_depth -= 1
            if delimiter == "{" and brace_depth == 0:
                return position
        elif character == ")" and delimiter == "(" and brace_depth == 0 and not quoted:
            return position
        position += 1
    return None


def bibliography_entries(path: Path, text: str) -> tuple[dict[str, Occurrence], list[Issue]]:
    entries = {}
    issues = []
    position = 0
    pattern = re.compile(r"@([A-Za-z]+)\s*([({])")
    while match := pattern.search(text, position):
        line_start = text.rfind("\n", 0, match.start()) + 1
        if "%" in text[line_start:match.start()]:
            position = match.end()
            continue
        closing = _entry_end(text, match.end() - 1)
        line = text.count("\n", 0, match.start()) + 1
        if closing is None:
            issues.append(Issue(path, line, f"unterminated @{match[1]} bibliography entry"))
            break
        if match[1].lower() not in {"comment", "preamble", "string"}:
            content = text[match.end():closing]
            key, comma, _ = content.partition(",")
            key = key.strip()
            if not comma or not key or re.search(r"[\s{}()=\"]", key):
                issues.append(Issue(path, line, f"invalid citation key in @{match[1]} entry"))
            elif key in entries:
                issues.append(Issue(path, line, f"duplicate bibliography key '{key}'"))
            else:
                entries[key] = Occurrence(path, line, key)
        position = closing + 1
    return entries, issues


def citation_issues(
    sources: dict[Path, str], entries: dict[str, Occurrence],
) -> tuple[list[Issue], int]:
    issues = []
    used = set()
    for path, text in sources.items():
        for occurrence in at_tokens(path, text):
            if is_crossref(occurrence.value):
                continue
            used.add(occurrence.value)
            if occurrence.value not in entries:
                issues.append(Issue(
                    path, occurrence.line,
                    f"unknown citation key '@{occurrence.value}'; export it to references.bib with Zotero/Better BibTeX",
                ))
    return issues, len(used)
