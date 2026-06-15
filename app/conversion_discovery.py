from __future__ import annotations

from pathlib import Path
from typing import Any


def summarize_audio_probes(
    files: list[Path],
    probes: list[dict[str, Any]],
) -> dict[str, Any]:
    successful = [probe for probe in probes if probe.get("probed")]

    def values(field: str) -> list[Any]:
        return sorted({probe[field] for probe in successful if probe.get(field) not in (None, "")})

    codecs = values("codec")
    codec_labels = values("codec_label")
    containers = values("container")
    bitrates = values("bitrate_kbps")
    channels = values("channels")
    sample_rates = values("sample_rate_hz")
    incomplete = len(successful) != len(files) or any(
        not probe.get("codec") or not probe.get("channels") or not probe.get("sample_rate_hz")
        for probe in successful
    )

    mixed = {
        "codec": len(codecs) > 1,
        "container": len(containers) > 1,
        "bitrate": len(bitrates) > 1,
        "channels": len(channels) > 1,
        "sample_rate": len(sample_rates) > 1,
    }
    mixed_properties = [name for name, is_mixed in mixed.items() if is_mixed]

    if not files or not successful:
        recommendation = {
            "status": "unknown",
            "recommended": False,
            "label": "Convert to AAC",
            "reason": "Audio properties could not be read, so stream-copy compatibility cannot be confirmed.",
        }
    elif incomplete:
        recommendation = {
            "status": "convert",
            "recommended": False,
            "label": "Convert to AAC",
            "reason": "Some source stream properties are missing or unreadable, so no-conversion cannot be recommended safely.",
        }
    elif len(codecs) != 1 or codecs[0] != "aac":
        shown = ", ".join(codec_labels or [codec.upper() for codec in codecs]) or "unknown"
        recommendation = {
            "status": "convert",
            "recommended": False,
            "label": "Convert to AAC",
            "reason": f"The source codec is {shown}; AAC provides the most reliable M4B playback compatibility.",
        }
    elif mixed["sample_rate"] or mixed["channels"]:
        differing = []
        if mixed["sample_rate"]:
            differing.append("sample rates")
        if mixed["channels"]:
            differing.append("channel layouts")
        recommendation = {
            "status": "convert",
            "recommended": False,
            "label": "Convert to AAC",
            "reason": f"The source files have mixed {' and '.join(differing)}, which should be normalized before merging.",
        }
    else:
        bitrate_note = " Bitrates vary, which is acceptable for stream-copy." if mixed["bitrate"] else ""
        recommendation = {
            "status": "copy",
            "recommended": True,
            "label": "No conversion recommended",
            "reason": "All source files use AAC with matching sample rate and channel layout; stream-copy avoids quality loss and is faster." + bitrate_note,
        }

    return {
        "file_count": len(files),
        "probed_file_count": len(successful),
        "codecs": codecs,
        "codec_labels": codec_labels,
        "containers": containers,
        "bitrates_kbps": bitrates,
        "channels": channels,
        "sample_rates_hz": sample_rates,
        "mixed": mixed,
        "mixed_properties": mixed_properties,
        "is_mixed": bool(mixed_properties),
        "no_conversion": recommendation,
    }


def conversion_candidate(
    *,
    source_path: Path,
    display_path: Path,
    item_files: list[Path],
    mode: str,
    audio_summary: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    is_grouped = display_path != source_path
    formats = sorted({item.suffix.lower().lstrip(".") for item in item_files})
    if mode == "multipart":
        include = is_grouped
        reason = "Multiple validated chapter files can be merged into one M4B."
    elif mode == "non_m4b":
        include = any(item.suffix.lower() != ".m4b" for item in item_files)
        reason = "Contains audio that is not already in M4B format."
    else:
        raise ValueError("Discovery mode must be multipart or non_m4b")

    if not include:
        return None
    return {
        "path": str(display_path),
        "representative_path": str(source_path),
        "display_path": str(display_path),
        "is_grouped": is_grouped,
        "file_count": len(item_files),
        "files": [str(item) for item in item_files],
        "formats": formats,
        "reason": reason,
        "audio_summary": audio_summary or {},
    }
