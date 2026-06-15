import unittest
from pathlib import Path

from app.manual_review import build_sidecar_multipart_context


class ManualReviewMultipartTests(unittest.TestCase):
    def test_existing_sidecar_chapter_list_is_authoritative(self):
        folder = Path("/library/Multipart Book")
        chapter_two = folder / "Part 02.m4a"
        chapter_one = folder / "Part 01.mp3"
        completed_output = folder / "Multipart Book.m4b"

        context = build_sidecar_multipart_context(
            [chapter_two, chapter_one],
            lambda path: path.name.casefold(),
        )

        self.assertIsNotNone(context)
        files, group_map, processing_items = context
        self.assertEqual(files, [chapter_one, chapter_two])
        self.assertEqual(processing_items, [chapter_one])
        self.assertEqual(group_map[folder], [chapter_one, chapter_two])
        self.assertNotIn(completed_output, files)


if __name__ == "__main__":
    unittest.main()
