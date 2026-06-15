import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from app import main


class ManualReviewApplyTests(unittest.TestCase):
    def test_grouped_manual_apply_writes_sidecar_with_existing_group(self):
        chapter_files = [
            "/library/Book/Part 01.m4a",
            "/library/Book/Part 02.mp3",
        ]
        group_search = {
            "applied": True,
            "folder": "/library/Book",
            "file_count": 2,
            "files": chapter_files,
        }
        context = {
            "source_path": chapter_files[0],
            "display_path": "/library/Book",
            "is_grouped": True,
            "group_search": group_search,
            "metadata": {
                "title": "Existing Title",
                "author": "Existing Author",
                "series": "Existing Series",
                "sequence": "2",
            },
        }
        written = {}

        def write_sidecar(source, metadata, clues, score):
            written["source"] = source
            written["metadata"] = metadata
            written["clues"] = clues
            written["score"] = score
            return Path("/library/Book/Book.m4b-tool-metadata.json")

        fixer = SimpleNamespace(
            clean_text=lambda value: value,
            clean_author_value=lambda value: value,
            normalize_book_number=lambda value: value,
            should_write_json_sidecar=lambda source, clues: bool(
                clues.get("group_search", {}).get("applied")
            ),
            write_m4b_tool_metadata_sidecar=write_sidecar,
            write_tags=lambda *args, **kwargs: self.fail("grouped apply wrote tags"),
            write_marker=lambda **kwargs: None,
        )
        selected_result = {
            "score": 1.0,
            "title": "Matched Title",
            "sequence": "2",
            "year": "2024",
            "duration_minutes": 600,
            "allowed_edit_modes": ["full"],
            "chosen_metadata_by_mode": {
                "full": {
                    "asin": "B012345678",
                    "title": "Matched Title",
                    "author": "Matched Author",
                    "series": "Matched Series",
                    "sequence": "2",
                }
            },
        }
        request = main.ManualReviewApplyRequest(
            path="/library/Book",
            selected_result=selected_result,
            edit_mode="full",
        )

        with (
            patch.object(main, "inspect_manual_review_target", return_value=context),
            patch.object(main, "load_fixer_module", return_value=fixer),
        ):
            result = main.apply_manual_review_result(request)

        self.assertEqual(result["output_kind"], "json_sidecar")
        self.assertEqual(written["source"], Path(chapter_files[0]))
        self.assertEqual(written["clues"]["group_search"], group_search)
        self.assertEqual(
            written["clues"]["group_search"]["files"],
            chapter_files,
        )


if __name__ == "__main__":
    unittest.main()
