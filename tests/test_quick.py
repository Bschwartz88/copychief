import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import docx_lib
import quick


class QuickTests(unittest.TestCase):
    def test_converter_filename_cannot_be_an_option(self):
        hostile = Path("--lua-filter=payload.md")
        with patch.object(quick.shutil, "which", return_value="pandoc"), patch.object(
                quick.subprocess, "run", return_value=SimpleNamespace(returncode=0, stdout="Text", stderr="")) as run:
            self.assertEqual(quick._to_markdown(hostile), "Text")
        args = run.call_args.args[0]
        self.assertEqual(args[-1], str(hostile.resolve()))
        self.assertNotIn(str(hostile), args)
        self.assertIn("--sandbox", args)
        self.assertEqual(run.call_args.kwargs["timeout"], 60)

    def test_nested_html_conversion_fails_closed(self):
        import subprocess
        with patch.object(quick.subprocess, "run", side_effect=subprocess.CalledProcessError(1, "pandoc")) as run:
            with self.assertRaises(subprocess.CalledProcessError):
                quick._html_to_md("<table><tr><td>text</td></tr></table>")
        self.assertIn("--sandbox", run.call_args.args[0])
        self.assertTrue(run.call_args.kwargs["check"])

    def test_missing_insertion_target_is_rejected(self):
        source = {"paragraphs": [{"n": 1, "style": "p", "text": "Original."}]}
        for target in (-1, 2, 999):
            with self.subTest(target=target), self.assertRaisesRegex(SystemExit, "insertion refers"):
                quick.build_blocks(source, {"edits": [{"after": target, "r": "Must not disappear."}]})

    def test_valid_insertions_survive_accept_and_disappear_on_reject(self):
        source = {"paragraphs": [{"n": 1, "style": "p", "text": "Original."}]}
        blocks, _, reject, accept = quick.build_blocks(source, {"edits": [
            {"after": 0, "r": "Before."}, {"after": 1, "r": "After."},
        ]})
        self.assertEqual(accept, ["Before.", "Original.", "After."])
        self.assertEqual(reject, ["Original."])
        self.assertEqual(quick._simulate(blocks, "accept"), accept)
        self.assertEqual(quick._simulate(blocks, "reject"), reject)

    def test_compaction_preserves_neighbor_and_document(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "review.docx"
            neighbor = output.with_suffix(".slim.tmp")
            neighbor.write_text("Unrelated content", encoding="utf-8")
            docx_lib.render_docx([("body", "Retained article text.")]).save(output)
            quick.slim_docx(output)
            self.assertEqual(neighbor.read_text(encoding="utf-8"), "Unrelated content")
            with zipfile.ZipFile(output) as archive:
                self.assertIsNone(archive.testzip())
                self.assertIn(b"Retained article text.", archive.read("word/document.xml"))
            self.assertEqual(sorted(p.name for p in Path(temp).iterdir()), ["review.docx", "review.slim.tmp"])


if __name__ == "__main__":
    unittest.main()
