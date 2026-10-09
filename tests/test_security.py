import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import _paths
import docx_lib
import build_review_tracked as tracked
from _security import safe_url


class SecurityTests(unittest.TestCase):
    def test_comment_ids_cannot_inject_html_or_xml(self):
        for cid in ('1"><script>alert(1)</script><li id="x', '1" injected="yes', -1, True):
            comments = {cid: ("Label", "Reason")}
            with self.subTest(cid=cid):
                with self.assertRaises(ValueError):
                    docx_lib.render_html([], comments=comments)
                with patch.object(tracked, "COMMENTS", comments):
                    with self.assertRaises(ValueError):
                        tracked._comments_xml()
                    with self.assertRaises(ValueError):
                        tracked._replace_sentinels("<w:document/>")

    def test_numeric_comment_ids_are_preserved(self):
        for cid in (0, 12, "12"):
            self.assertIn(f'id="c{cid}"', docx_lib.render_html([], {cid: ("Label", "Reason")}))

    def test_data_is_not_executed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "blog").mkdir()
            data = root / "tools/data"
            data.mkdir(parents=True)
            marker = root / "executed"
            (data / "example.py").write_text(
                f"PREP = {{'blocks': []}}\nopen({str(marker)!r}, 'w').write('bad')", encoding="utf-8")
            with patch.object(_paths, "ROOT", root):
                with self.assertRaises(ValueError):
                    _paths.load_data("example")
            self.assertFalse(marker.exists())

    def test_literals_still_load(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "legacy_Name").mkdir()
            (root / "legacy_Name/data.py").write_text(
                '"""Content"""\nPREP = {"blocks": [("body", "Hello " "world")]}\n', encoding="utf-8")
            with patch.object(_paths, "ROOT", root):
                self.assertEqual(_paths.load_data("legacy_Name").PREP["blocks"], [("body", "Hello world")])

    def test_path_traversal_and_windows_devices(self):
        for slug in ("../escape", "..\\escape", "C:\\temp", "/absolute", "x:y", "CON", "LPT1", "x.", "a/b", ""):
            with self.subTest(slug=slug), self.assertRaises(ValueError):
                _paths.resolve(slug)

    def test_outside_output_is_rejected(self):
        with self.assertRaises(ValueError):
            _paths.checked_path(_paths.ROOT.parent / "outside.docx")

    def test_unsafe_links_blocked_in_both_renderers(self):
        for url in ("javascript:alert%281%29", "data:text/html,bad", "file:///C:/private", "\\\\host\\file", "https://user:pass@example.com", "https://example.com\n"):
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    docx_lib.render_html([("body", f"[click]({url})")])
                with self.assertRaises(ValueError):
                    docx_lib.render_docx([("body", f"[click]({url})")])
                with self.assertRaises(ValueError):
                    tracked._html_tokens(None, [("kl", "click", url)])
                with self.assertRaises(ValueError):
                    tracked._add_hyperlink(docx_lib.render_docx([]).add_paragraph(), url, "click")

    def test_safe_links_and_escaping_preserved(self):
        for url in ("https://example.com/a?q=1&b=2", "http://example.com", "mailto:editor@example.com"):
            self.assertEqual(safe_url(url), url)
        result = docx_lib.render_html([("body", '<script>alert(1)</script> [Read](https://example.com)')])
        self.assertNotIn("<script>", result)
        self.assertIn('href="https://example.com"', result)


if __name__ == "__main__":
    unittest.main()
