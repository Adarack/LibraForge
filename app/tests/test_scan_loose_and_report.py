import tempfile
import unittest
from pathlib import Path

from app.main import _find_book_folders, build_report_items


class FindBookFoldersTests(unittest.TestCase):
    def test_loose_root_files_counted_as_units(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # Loose audiobooks directly in the scanned folder.
            (root / "Loose One.m4b").write_bytes(b"")
            (root / "Loose Two.m4b").write_bytes(b"")
            # A proper book subfolder.
            sub = root / "Author - Book"
            sub.mkdir()
            (sub / "book.m4b").write_bytes(b"")
            # A non-audio file that must be ignored.
            (root / "Thumbs.db").write_bytes(b"")

            units = _find_book_folders(root)
            names = {u.name for u in units}
            self.assertIn("Loose One.m4b", names)
            self.assertIn("Loose Two.m4b", names)
            self.assertIn("Author - Book", names)
            self.assertNotIn("Thumbs.db", names)
            self.assertEqual(len(units), 3)


class BuildReportItemsTitleTests(unittest.TestCase):
    def test_fill_detail_does_not_become_generic_title(self):
        fbc = {
            "fill:filled": [{"path": "/x/book.m4b", "title": "series, sequence, asin"}],
            "fill:asin": [{"path": "/x/book.m4b", "title": ""}],
            "status:matched": [{"path": "/x/book.m4b", "title": ""}],
        }
        items, categories = build_report_items(fbc)
        self.assertEqual(items[0]["title"], "")
        self.assertIn("fill:asin", categories)
        self.assertEqual(categories["fill:asin"], [items[0]["id"]])

    def test_real_title_still_inherited(self):
        fbc = {
            "duration:perfect": [{"path": "/x/book.m4b", "title": "The Real Book"}],
        }
        items, _ = build_report_items(fbc)
        self.assertEqual(items[0]["title"], "The Real Book")


if __name__ == "__main__":
    unittest.main()
