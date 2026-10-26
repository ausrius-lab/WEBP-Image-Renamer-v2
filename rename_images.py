"""
Responsive image renamer (GUI version).

Run it from anywhere -- no terminal/console window appears. On launch, a
folder picker window opens; select the folder that contains your
resolution subfolders:

    1920px  1200px  992px  768px  576px  375px

Every .webp/.jpg/.jpeg/.png file inside those folders (including
subfolders) gets a size suffix appended to its filename, based on which
folders are actually present. When done, a small "Renaming Complete"
window reports how many files were renamed in each folder.

Suffixes are fixed by folder name:

    1920px -> -xxl   (or -xl if there is no 1200px folder)
    1200px -> -xl
    992px  -> -lg
    768px  -> -md
    576px  -> -sm
    375px  -> (untouched)

Any folder that doesn't exist is simply skipped.

Example: 768px/image.webp -> 768px/image-md.webp
Running the tool again is safe -- files that already end in a known
suffix are left alone.
"""

import sys
from pathlib import Path

# Processing order (smallest to largest) and fixed suffix per folder name.
SIZE_ORDER = ["375px", "576px", "768px", "992px", "1200px", "1920px"]
FOLDER_SUFFIXES = {
    "375px": "",
    "576px": "-sm",
    "768px": "-md",
    "992px": "-lg",
    "1200px": "-xl",
    "1920px": "-xxl",
}
ALL_SUFFIXES = [x for x in FOLDER_SUFFIXES.values() if x]

IMAGE_EXTENSIONS = {".webp", ".jpg", ".jpeg", ".png"}


def build_mapping(base_dir: Path) -> dict:
    """Map each existing resolution folder name to its suffix (fixed by name)."""
    existing = [name for name in SIZE_ORDER if (base_dir / name).is_dir()]
    mapping = {name: FOLDER_SUFFIXES[name] for name in existing}
    # Special case: with no 1200px folder, the 1920px images get -xl.
    if "1920px" in mapping and "1200px" not in mapping:
        mapping["1920px"] = "-xl"
    return mapping


def already_tagged(stem: str) -> bool:
    return any(stem.endswith(suf) for suf in ALL_SUFFIXES)


def process_folder(folder: Path, suffix: str) -> int:
    """Rename matching image files in folder (recursively). Returns count renamed."""
    if not suffix:
        return 0

    count = 0
    for path in sorted(folder.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        stem = path.stem
        if already_tagged(stem):
            continue

        new_path = path.with_name(f"{stem}{suffix}{path.suffix}")
        if new_path.exists():
            continue

        path.rename(new_path)
        count += 1

    return count


def run(base_dir: Path):
    """Process base_dir. Returns (mapping, results, total) where results is
    a list of (folder_name, suffix_label, count_renamed)."""
    mapping = build_mapping(base_dir)
    results = []
    total = 0
    for name in SIZE_ORDER:
        if name not in mapping:
            continue
        suffix = mapping[name]
        label = suffix if suffix else "untouched"
        count = process_folder(base_dir / name, suffix)
        results.append((name, label, count))
        total += count
    return mapping, results, total


def main():
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox
    except ImportError:
        # No GUI toolkit available -- fall back to console so the program
        # still does something useful rather than silently failing.
        print("tkinter is not available on this system; cannot show the "
              "folder picker or results window.")
        return

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    if len(sys.argv) > 1:
        # Explicit folder passed in (handy for testing from a terminal).
        base_dir = Path(sys.argv[1]).resolve()
    else:
        selected = filedialog.askdirectory(
            title="Select the folder containing your resolution folders "
                  "(1920px, 1200px, 992px, 768px, 576px, 375px)"
        )
        if not selected:
            root.destroy()
            return
        base_dir = Path(selected).resolve()

    mapping, results, total = run(base_dir)

    if not mapping:
        messagebox.showerror(
            "No resolution folders found",
            "Couldn't find any of these folders inside the selected "
            "location:\n\n1920px, 1200px, 992px, 768px, 576px, 375px\n\n"
            "Make sure you selected the folder that directly contains them."
        )
    else:
        lines = []
        for name, label, count in results:
            tag = "untouched" if label == "untouched" else label
            lines.append(f"{name}  [{tag}]  -  {count} renamed")
        summary = "\n".join(lines)
        messagebox.showinfo(
            "Renaming Complete",
            f"Renamed {total} file(s) total.\n\n{summary}"
        )

    root.destroy()


if __name__ == "__main__":
    main()
