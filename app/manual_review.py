from pathlib import Path
from typing import Callable


def build_sidecar_multipart_context(
    chapter_files: list[Path],
    natural_sort_key: Callable[[Path], object],
) -> tuple[list[Path], dict[Path, list[Path]], list[Path]] | None:
    """Build one manual-review item from a sidecar's explicit chapter list."""
    if len(chapter_files) < 2:
        return None

    ordered_files = sorted(chapter_files, key=natural_sort_key)
    representative = ordered_files[0]
    group_map = {representative.parent: ordered_files}
    return ordered_files, group_map, [representative]
