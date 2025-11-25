#!/usr/bin/env python3
"""
backup.py – copy files from a source directory to a destination directory,
ensuring unique names by appending a timestamp when a conflict occurs.

Usage:
    python backup.py /path/to/source /path/to/destination
"""

import sys
import os
import shutil
import datetime
from pathlib import Path

def _timestamp() -> str:
    """Return current time formatted for a filename."""
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def _unique_dest_path(dest_dir: Path, filename: str) -> Path:
    """
    Return a Path inside *dest_dir* that does not clash with an existing file.
    If ``dest_dir/filename`` exists, insert a timestamp before the extension:
        example.txt → example_20241012_153045.txt
    """
    target = dest_dir / filename
    if not target.exists():
        return target

    stem, suffix = os.path.splitext(filename)
    new_name = f"{stem}_{_timestamp()}{suffix}"
    return dest_dir / new_name

def backup(source: Path, destination: Path) -> None:
    """Copy all regular files from *source* to *destination* with conflict handling."""
    try:
        if not source.is_dir():
            raise NotADirectoryError(f"Source '{source}' is not a directory.")
        if not destination.is_dir():
            raise NotADirectoryError(f"Destination '{destination}' is not a directory.")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    for item in source.iterdir():
        if item.is_file():
            try:
                dest_path = _unique_dest_path(destination, item.name)
                shutil.copy2(item, dest_path)          # copy with metadata
                print(f"Copied: {item.name} → {dest_path.name}")
            except PermissionError:
                print(f"Permission denied while copying '{item}'.", file=sys.stderr)
            except OSError as e:
                print(f"Failed to copy '{item}': {e}", file=sys.stderr)

def main():
    if len(sys.argv) != 3:
        print("Usage: python backup.py <source_dir> <destination_dir>", file=sys.stderr)
        sys.exit(1)

    src_path = Path(sys.argv[1]).resolve()
    dst_path = Path(sys.argv[2]).resolve()
    backup(src_path, dst_path)

if __name__ == "__main__":
    main()