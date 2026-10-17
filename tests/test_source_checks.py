from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from source_checks import (
    article_sources, at_tokens, bibliography_entries, citation_issues, label_issues, labels,
    source_files, visible_markdown,
)


class MarkdownChecks(unittest.TestCase):
    def setUp(self):
        self.path = Path("section.qmd")

    def test_masks_examples_without_losing_line_numbers(self):
        text = (
            "---\nauthor: example@example.org\n---\n"
            "<!-- @hidden {#eq-hidden} -->\n"
            "````markdown\n```\n@code {#eq-code}\n```\n````\n"
            "`@inline` and `` `@nested` ``\n"
            "See @eq-visible and [@key_2026:paper/part, p. 2].\n"
            "$$ x = y $$ {#eq-visible}\n"
        )
        self.assertEqual(
            [(item.value, item.line) for item in at_tokens(self.path, text)],
            [("eq-visible", 11), ("key_2026:paper/part", 11)],
        )
        self.assertEqual([item.value for item in labels(self.path, text)], ["eq-visible"])
        self.assertEqual(visible_markdown(text).count("\n"), text.count("\n"))

    def test_escapes_emails_html_and_punctuation(self):
        text = (
            r"\@escaped person+tag@example.org <a href='@attribute'>" "\n"
            r"[@smith2026; -@jones2025, sec. 2]. **@author2024**. @eq-result." "\n"
            r"\\@unescaped"
        )
        self.assertEqual(
            [item.value for item in at_tokens(self.path, text)],
            ["smith2026", "jones2025", "author2024", "eq-result", "unescaped"],
        )

    def test_tilde_and_raw_fences_are_examples(self):
        text = "~~~{=latex}\n@raw {#eq-raw}\n~~~\nSee @eq-real.\n"
        self.assertEqual([item.value for item in at_tokens(self.path, text)], ["eq-real"])
        self.assertEqual(labels(self.path, text), [])

    def test_raw_html_and_tex_do_not_create_citations(self):
        text = (
            "<script>const example = '@script';</script>\n"
            "<pre>@html {#eq-html}</pre>\n"
            r"\begin{equation}@raw\end{equation}" "\n"
            r"\verb|@verbatim| and @rendered."
        )
        self.assertEqual([item.value for item in at_tokens(self.path, text)], ["rendered"])
        self.assertEqual(labels(self.path, text), [])

    def test_cross_file_duplicates_unresolved_and_proposition_prefix(self):
        sources = {
            self.path: "# Heading {#sec-topic}\nSee @eq-missing and @prp-example.\n",
            Path("other.qmd"): "# Again {#sec-topic}\n::: {#prp-example}\n::: \n",
        }
        issues, count, references = label_issues(sources)
        self.assertEqual((count, references), (2, 2))
        self.assertEqual(len(issues), 2)
        self.assertTrue(any("duplicate label 'sec-topic'" in issue.message for issue in issues))
        self.assertTrue(any("unresolved cross-reference '@eq-missing'" in issue.message for issue in issues))

    def test_prop_requires_native_prp(self):
        issues, _, _ = label_issues({self.path: "::: {#prop-demo}\nSee @prop-demo.\n:::"})
        self.assertEqual(len(issues), 2)
        self.assertTrue(all("native" in issue.message for issue in issues))

    def test_native_conjecture_prefix_is_reserved_for_assumptions(self):
        issues, _, _ = label_issues({self.path: "::: {#cnj-demo}\nSee @cnj-demo.\n:::"})
        self.assertEqual(len(issues), 2)
        self.assertTrue(all("reserved" in issue.message for issue in issues))

    def test_discovery_ignores_outputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "sections").mkdir()
            (root / "_output").mkdir()
            (root / "index.qmd").touch()
            (root / "sections" / "intro.qmd").touch()
            (root / "_output" / "rendered.qmd").touch()
            self.assertEqual(
                [str(path.relative_to(root)) for path in source_files(root)],
                ["index.qmd", "sections/intro.qmd"],
            )


class IncludeChecks(unittest.TestCase):
    def test_nested_includes_use_main_document_paths_and_ignore_unused_sources(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "sections").mkdir()
            (root / "index.qmd").write_text(
                "{{< include sections/intro.qmd >}}\n\nSee @eq-unused.\n", encoding="utf-8",
            )
            (root / "sections" / "intro.qmd").write_text(
                '{{< include "sections/a result.qmd" >}}\n', encoding="utf-8",
            )
            (root / "sections" / "a result.qmd").write_text(
                "$$ a=b $$ {#eq-result}\n", encoding="utf-8",
            )
            (root / "unused.qmd").write_text("$$ a=b $$ {#eq-unused}\n", encoding="utf-8")
            sources, issues = article_sources(root)
            self.assertEqual(len(sources), 3)
            self.assertEqual(issues, [])
            label_errors, _, _ = label_issues(sources)
            self.assertEqual(len(label_errors), 1)
            self.assertIn("@eq-unused", label_errors[0].message)

    def test_missing_repeated_and_cyclic_includes_report_the_include_location(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "index.qmd").write_text(
                "{{< include section.qmd >}}\n\n"
                "{{< include /section.qmd >}}\n\n"
                "{{< include missing.qmd >}}\n", encoding="utf-8",
            )
            (root / "section.qmd").write_text(
                "{{< include index.qmd >}}\n", encoding="utf-8",
            )
            sources, issues = article_sources(root)
            self.assertEqual(len(sources), 2)
            self.assertEqual(len(issues), 3)
            self.assertEqual([issue.line for issue in issues], [1, 3, 5])
            self.assertTrue(any("cyclic include" in issue.message for issue in issues))
            self.assertTrue(any("duplicate include" in issue.message for issue in issues))
            self.assertTrue(any("does not exist" in issue.message for issue in issues))

    def test_commented_and_example_includes_do_not_affect_graph(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "index.qmd").write_text(
                "<!-- {{< include missing.qmd >}} -->\n"
                "```markdown\n{{< include also-missing.qmd >}}\n```\n"
                "`{{< include inline.qmd >}}`\n", encoding="utf-8",
            )
            sources, issues = article_sources(root)
            self.assertEqual(len(sources), 1)
            self.assertEqual(issues, [])


class BibliographyChecks(unittest.TestCase):
    def setUp(self):
        self.path = Path("references.bib")

    def test_better_bibtex_and_special_entries(self):
        text = '''% @article{notAnEntry, title={ignored}}
@comment{An example @article{alsoIgnored, title={Example}}}
@string{journal = "A journal"}
@preamble{"\\newcommand{\\example}{test}"}
@article{author_2026:part/one,
  title = {Nested {title} with an @ sign},
  abstract = {See @article{notAnotherEntry, title={Example}}},
}
@book(second-key,
  title = "A title with (parentheses) and {braces}",
)
'''
        entries, issues = bibliography_entries(self.path, text)
        self.assertEqual(set(entries), {"author_2026:part/one", "second-key"})
        self.assertEqual(issues, [])

    def test_duplicate_and_unterminated_entries(self):
        text = "@misc{same, title={First}}\n@misc{same, title={Second}}\n@book{broken, title={Unclosed}"
        entries, issues = bibliography_entries(self.path, text)
        self.assertEqual(set(entries), {"same"})
        self.assertEqual([issue.line for issue in issues], [2, 3])

    def test_missing_citations_exclude_crossrefs_and_code(self):
        entries, _ = bibliography_entries(self.path, "@misc{known, title={Example}}")
        issues, used = citation_issues({
            Path("index.qmd"): "@known, [@missing]. See @asm-assumption and `@example`.\n",
        }, entries)
        self.assertEqual(used, 2)
        self.assertEqual(len(issues), 1)
        self.assertIn("@missing", issues[0].message)


if __name__ == "__main__":
    unittest.main()
