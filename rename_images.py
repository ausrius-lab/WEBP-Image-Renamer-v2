"""
Responsive image renamer.

Run it from anywhere (it no longer needs to sit inside the project
folder). On launch, a folder picker window opens -- select the folder
that contains your resolution subfolders, and it takes it from there.

Every .webp/.jpg/.jpeg/.png file inside those folders (including
subfolders) gets a size suffix appended to its filename, based on which
folders are actually present.

Suffixes are assigned by RANK, smallest folder to largest, not by a fixed
name -> suffix table. The smallest existing folder is always left
untouched, and the rest get -sm, -md, -lg, -xl, -xxl in order:

    1st smallest existing folder -> (untouched)
    2nd smallest existing folder -> -sm
    3rd smallest existing folder -> -md
    4th smallest existing folder -> -lg
    5th smallest existing folder -> -xl
    6th smallest existing folder -> -xxl

With all six folders present that works out to:
    375px  -> (untouched)
    576px  -> -sm
    768px  -> -md
    992px  -> -lg
    1200px -> -xl
    1920px -> -xxl

If, say, 1200px is missing, everything above it shifts down one slot, so
1920px becomes -xl instead of -xxl. Any folder that doesn't exist is simply
skipped.

Example: 768px/image.webp -> 768px/image-md.webp
Running the tool again is safe -- files that already end in a known
suffix are left alone.
"""

import sys
from pathlib import Path

# Ordered smallest to largest.
SIZE_ORDER = ["375px", "576px", "768px", "992px", "1200px", "1920px"]
SUFFIXES = ["", "-sm", "-md", "-lg", "-xl", "-xxl"]

IMAGE_EXTENSIONS = {".webp", ".jpg", ".jpeg", ".png"}


def prompt_for_base_dir() -> Path | None:
    """Show a native folder picker so the user can choose the project folder."""
    try:
        import tkinter as tk
        from tkinter import filedialog
    except ImportError:
        print("Could not open a folder picker (tkinter not available on this system).")
        print("You can instead run this program from a terminal/command prompt")
        print("and pass the folder path as an argument.")
        return None

    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        selected = filedialog.askdirectory(
            title="Select the folder containing your resolution folders "
                  "(1920px, 1200px, 992px, 768px, 576px, 375px)"
        )
        root.destroy()
    except Exception as exc:
        print(f"Could not open a folder picker: {exc}")
        return None

    if not selected:
        return None
    return Path(selected).resolve()


def get_base_dir() -> Path | None:
    """Folder to process: an explicit argument, or ask via a folder picker."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).resolve()
    return prompt_for_base_dir()


def build_mapping(base_dir: Path) -> dict:
    """Map each existing resolution folder name to its suffix, by rank."""
    existing = [name for name in SIZE_ORDER if (base_dir / name).is_dir()]
    return {name: SUFFIXES[i] for i, name in enumerate(existing)}


def already_tagged(stem: str) -> bool:
    return any(suf and stem.endswith(suf) for suf in SUFFIXES)


def process_folder(folder: Path, suffix: str) -> int:
    count = 0
    if not suffix:
        print(f"  (left untouched, no suffix for this rank)")
        return 0

    for path in sorted(folder.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        stem = path.stem
        if already_tagged(stem):
            print(f"  skip (already tagged): {path.relative_to(folder)}")
            continue

        new_path = path.with_name(f"{stem}{suffix}{path.suffix}")
        if new_path.exists():
            print(f"  skip (target already exists): {path.relative_to(folder)}")
            continue

        path.rename(new_path)
        count += 1
        print(f"  {path.relative_to(folder)}  ->  {new_path.name}")

    return count


def main():
    base_dir = get_base_dir()

    if base_dir is None:
        print("No folder selected. Nothing to do.")
        input("\nPress Enter to exit...")
        return

    print(f"Base folder: {base_dir}\n")

    mapping = build_mapping(base_dir)

    if not mapping:
        print("No resolution folders found here "
              "(1920px, 1200px, 992px, 768px, 576px, 375px).")
        print("Make sure you selected the folder that contains those subfolders.")
    else:
        total = 0
        for name in SIZE_ORDER:
            if name not in mapping:
                continue
            suffix = mapping[name]
            label = suffix if suffix else "untouched"
            print(f"Processing {name}  [{label}]")
            total += process_folder(base_dir / name, suffix)
            print()
        print(f"Done. Renamed {total} file(s).")

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
