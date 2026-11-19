"""!
@file confined_path.py
@brief Resolve a relative path so that it cannot leave a folder.
"""

from pathlib import Path


def resolve_inside(root: Path, relative_path: str) -> Path | None:
    """!
    @brief Resolve a relative path against a folder and keep it inside the folder.

    An absolute path, a `..` segment and a symbolic link that points out of the
    folder all give None.
    @param root The folder, already resolved.
    @param relative_path The path to resolve.
    @return The resolved path, or None when it is the folder itself or outside it.
    """
    try:
        target = (root / relative_path).resolve()
    except (OSError, ValueError):
        return None
    if target == root or not target.is_relative_to(root):
        return None
    return target
