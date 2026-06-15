import re


def canonical_m4b_title(*, title: str, subtitle: str, sequence: str) -> str:
    """Add a missing series position to a book title exactly once."""
    title = str(title or "").strip()
    sequence = str(sequence or "").strip()
    if not title or not sequence:
        return title

    number_pattern = re.escape(sequence).replace(r"\.", r"[.]")
    position_pattern = re.compile(
        rf"\b(?:book|vol(?:ume)?[.]?)\s*0*{number_pattern}(?![\d.])",
        re.IGNORECASE,
    )
    if position_pattern.search(title):
        return title

    subtitle_match = position_pattern.search(str(subtitle or ""))
    label = "Book"
    if subtitle_match:
        evidence = subtitle_match.group(0)
        if re.match(r"vol[.]", evidence, re.IGNORECASE):
            label = "Vol."
        elif re.match(r"volume", evidence, re.IGNORECASE):
            label = "Volume"

    return f"{title}, {label} {sequence}"
