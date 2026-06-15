import unittest

from app.m4b_naming import canonical_m4b_title


class M4BCanonicalTitleTests(unittest.TestCase):
    def test_uses_volume_label_evidenced_by_subtitle(self):
        self.assertEqual(
            canonical_m4b_title(
                title="Reborn as a Space Mercenary",
                subtitle="Light Novel, Vol. 2",
                sequence="2",
            ),
            "Reborn as a Space Mercenary, Vol. 2",
        )

    def test_defaults_to_book_label_without_evidence(self):
        self.assertEqual(
            canonical_m4b_title(
                title="Corporate Warfare",
                subtitle="",
                sequence="3",
            ),
            "Corporate Warfare, Book 3",
        )

    def test_does_not_duplicate_existing_position(self):
        for title in (
            "Corporate Warfare, Book 3",
            "Corporate Warfare, Volume 3",
            "Corporate Warfare, Vol. 03",
        ):
            with self.subTest(title=title):
                self.assertEqual(
                    canonical_m4b_title(
                        title=title,
                        subtitle="Volume 3",
                        sequence="3",
                    ),
                    title,
                )

    def test_title_without_sequence_is_unchanged(self):
        self.assertEqual(
            canonical_m4b_title(
                title="Standalone",
                subtitle="",
                sequence="",
            ),
            "Standalone",
        )


if __name__ == "__main__":
    unittest.main()
