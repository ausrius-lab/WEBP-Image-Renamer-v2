# Responsive Image Renamer

Renames `.webp` images inside resolution-named folders by appending a size
suffix, based on which folders exist.

## What it does

Put the program in a folder next to any of these subfolders:

```
your-project/
├── rename_images.exe   (or the Mac binary)
├── 1920px/
├── 1200px/
├── 992px/
├── 768px/
├── 576px/
└── 375px/
```

Suffixes are assigned by rank, smallest folder to largest — not by a fixed
name. The smallest folder that exists is always left untouched; the rest get
`-sm`, `-md`, `-lg`, `-xl`, `-xxl` going up in size:

| Rank (smallest → largest) | Suffix   |
|----------------------------|----------|
| 1st                        | none     |
| 2nd                        | `-sm`    |
| 3rd                        | `-md`    |
| 4th                        | `-lg`    |
| 5th                        | `-xl`    |
| 6th                        | `-xxl`   |

With all six folders present, that works out to:

```
375px  -> untouched
576px  -> -sm
768px  -> -md
992px  -> -lg
1200px -> -xl
1920px -> -xxl
```

If a folder is missing it's skipped entirely, and everything above it shifts
down one rank. For example, if `1200px` doesn't exist, `1920px` becomes the
4th-smallest existing folder, so it gets `-xl` instead of `-xxl`.

Subfolders inside each resolution folder are processed too (recursively).
Running the tool more than once is safe — files that already end in a known
suffix are skipped.

Example: `768px/image.webp` → `768px/image-md.webp`

## Running it

- **Windows:** double-click `rename_images.exe`.
- **Mac:** double-click the `rename_images` binary, or run it from Terminal
  (`./rename_images`). The first time, you may need to right-click → Open
  once to get past Gatekeeper, since the binary isn't code-signed.

A console window will show what was renamed, then wait for you to press
Enter before closing.

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
   `rename_images` (Mac), then attach both to a new GitHub Release
   automatically.
4. Share the Release link — anyone can download the right file for their OS.

You can also trigger a build manually anytime from the **Actions** tab
("Run workflow") without pushing a tag; the binaries will appear as
downloadable artifacts on that run.

## Running it without building (for testing)

If you have Python 3 installed, you can just run:

```
python3 rename_images.py
```

from inside the project folder — no build needed.
