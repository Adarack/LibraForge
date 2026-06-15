import unittest

from app.main import (
    RunState,
    finalize_organizer_move,
    initial_organizer_stats,
    parse_organizer_line,
)


class OrganizerReviewParserTests(unittest.TestCase):
    def test_review_reasons_and_metadata_source_are_structured(self):
        state = RunState("test")
        state.stats = initial_organizer_stats()
        lines = [
            "BOOK:",
            "  Kind:   folder",
            "  Title:  Second",
            "  Author: Jane Doe",
            "  Files:  1",
            "  Metadata Source: marker:test.json",
            "  Review Reasons: book number differs between metadata and path | author inferred from other books in this run",
            "  Structure: existing",
            "  MOVE:",
            "    /incoming/book",
            "  TO:",
            "    /library/Jane Doe/Example/Book 2 - Second",
        ]

        for line in lines:
            parse_organizer_line(state, line)
        finalize_organizer_move(state)

        item = state.stats["move_items"][0]
        self.assertEqual(item["metadata_source"], "marker:test.json")
        self.assertEqual(
            item["review_reasons"],
            [
                "book number differs between metadata and path",
                "author inferred from other books in this run",
            ],
        )


if __name__ == "__main__":
    unittest.main()
