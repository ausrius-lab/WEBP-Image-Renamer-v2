# Responsive Image Renamer

Renames `.webp`, `.jpg`, `.jpeg`, and `.png` images inside resolution-named
folders by appending a size suffix, based on which folders exist.

## What it does

It's a pure GUI app — no terminal or console window at any point.

1. Double-click the program (from anywhere — it doesn't need to sit inside
   the project folder).
2. A folder picker window opens. Select the folder that contains your
   resolution subfolders:

   ```
   your-project/
   ├── 1920px/
   ├── 1200px/
   ├── 992px/
   ├── 768px/
   ├── 576px/
   └── 375px/
   ```
3. It renames the files, then shows a small **"Renaming Complete"** window
   listing how many files were renamed in each folder.

Suffixes are fixed by folder name:

| Folder   | Suffix                                   |
|----------|------------------------------------------|
| `1920px` | `-xxl` (or `-xl` if there is no `1200px`) |
| `1200px` | `-xl`                                    |
| `992px`  | `-lg`                                    |
| `768px`  | `-md`                                    |
| `576px`  | `-sm`                                    |
| `375px`  | untouched                                |

Folders that don't exist are skipped.

Subfolders inside each resolution folder are processed too (recursively).
Running the tool more than once is safe — files that already end in a known
suffix are skipped.

Example: `768px/image.webp` → `768px/image-md.webp`

## Running it

- **Windows:** double-click `rename_images.exe`.
- **Mac:** you'll get `RenameImages-mac.zip` from the Releases page. Unzip it
  (double-click the zip if it doesn't auto-extract), then double-click
  `RenameImages.app` from anywhere.
  - The very first time, macOS will likely block it since it's not from an
    identified developer. Go to **System Settings → Privacy & Security**,
    scroll down, and click **"Open Anyway"** next to the RenameImages
    message, then double-click the app again. You only need to do this once.

Either way: pick the folder in the dialog, wait a moment, then read the
results in the popup that appears. No windows are left open afterward —
just click OK to dismiss it.

## Building the executables yourself (via GitHub Actions)

This repo already includes a workflow (`.github/workflows/build.yml`) that
builds both binaries for you — no local setup needed:

1. Push this repo to GitHub.
2. Create and push a version tag, e.g.:
   ```
   git tag v1.0.0
   git push origin v1.0.0
   ```
3. GitHub Actions will build `rename_images.exe` (Windows) and
   `RenameImages-mac.zip` (Mac, containing a double-clickable `.app`),
   then attach both to a new GitHub Release automatically.
4. Share the Release link — anyone can download the right file for their OS.

You can also trigger a build manually anytime from the **Actions** tab
("Run workflow") without pushing a tag; the binaries will appear as
downloadable artifacts on that run.

## Running it without building (for testing)

If you have Python 3 installed (with tkinter, which ships with most
standard installs), you can just run:

```
python3 rename_images.py
```

You can also skip the folder-picker dialog by passing a path directly,
handy for quick testing from a terminal:

```
python3 rename_images.py /path/to/your/project
```
