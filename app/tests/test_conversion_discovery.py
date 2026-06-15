import unittest
from pathlib import Path

from app.conversion_discovery import conversion_candidate, summarize_audio_probes


class ConversionDiscoveryTests(unittest.TestCase):
    def test_multipart_returns_one_folder_candidate(self):
        folder = Path("/library/Book")
        files = [folder / "Chapter 1.opus", folder / "Chapter 2.opus"]

        candidate = conversion_candidate(
            source_path=files[0],
            display_path=folder,
            item_files=files,
            mode="multipart",
        )

        self.assertEqual(candidate["path"], str(folder))
        self.assertEqual(candidate["file_count"], 2)
        self.assertEqual(candidate["files"], [str(item) for item in files])
        self.assertEqual(candidate["formats"], ["opus"])
        self.assertTrue(candidate["is_grouped"])

    def test_loose_non_m4b_file_is_a_conversion_candidate(self):
        source = Path("/library/Book.mp3")

        candidate = conversion_candidate(
            source_path=source,
            display_path=source,
            item_files=[source],
            mode="non_m4b",
        )

        self.assertEqual(candidate["formats"], ["mp3"])
        self.assertFalse(candidate["is_grouped"])

    def test_existing_single_m4b_is_not_a_conversion_candidate(self):
        source = Path("/library/Book.m4b")

        candidate = conversion_candidate(
            source_path=source,
            display_path=source,
            item_files=[source],
            mode="non_m4b",
        )

        self.assertIsNone(candidate)

    def test_unsupported_mode_is_rejected(self):
        with self.assertRaises(ValueError):
            conversion_candidate(
                source_path=Path("/library/Book.mp3"),
                display_path=Path("/library/Book.mp3"),
                item_files=[Path("/library/Book.mp3")],
                mode="unknown",
            )

    def test_consistent_aac_recommends_no_conversion(self):
        files = [Path("/library/1.m4a"), Path("/library/2.m4a")]
        probes = [
            {
                "probed": True,
                "codec": "aac",
                "codec_label": "AAC",
                "container": "QuickTime / MOV",
                "bitrate_kbps": bitrate,
                "channels": 2,
                "sample_rate_hz": 44100,
            }
            for bitrate in (96, 128)
        ]

        summary = summarize_audio_probes(files, probes)

        self.assertTrue(summary["no_conversion"]["recommended"])
        self.assertTrue(summary["mixed"]["bitrate"])
        self.assertFalse(summary["mixed"]["sample_rate"])

    def test_non_aac_recommends_conversion(self):
        summary = summarize_audio_probes(
            [Path("/library/book.mp3")],
            [{
                "probed": True,
                "codec": "mp3",
                "codec_label": "MP3",
                "container": "MP3",
                "bitrate_kbps": 128,
                "channels": 2,
                "sample_rate_hz": 44100,
            }],
        )

        self.assertFalse(summary["no_conversion"]["recommended"])
        self.assertEqual(summary["no_conversion"]["status"], "convert")

    def test_mixed_sample_rate_recommends_conversion(self):
        files = [Path("/library/1.m4a"), Path("/library/2.m4a")]
        probes = [
            {
                "probed": True,
                "codec": "aac",
                "codec_label": "AAC",
                "container": "QuickTime / MOV",
                "bitrate_kbps": 128,
                "channels": 2,
                "sample_rate_hz": sample_rate,
            }
            for sample_rate in (44100, 48000)
        ]

        summary = summarize_audio_probes(files, probes)

        self.assertFalse(summary["no_conversion"]["recommended"])
        self.assertTrue(summary["mixed"]["sample_rate"])


if __name__ == "__main__":
    unittest.main()
