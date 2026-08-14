# CR2 to JPG Converter

**Version 1.0.0**

A simple Windows desktop application for converting Canon `.CR2` RAW photos to high-quality `.JPG` images.

---

## Download

### Windows EXE

[![Download EXE](https://img.shields.io/badge/Download-Windows%20EXE-blue?style=for-the-badge&logo=windows)](https://github.com/jentimanatol/CR2-to-JPG-Converter/releases/latest/download/CR2-to-JPG-Converter.exe)

**Latest version:** `v1.0.0`

You can also download the latest release from:

[GitHub Releases](https://github.com/jentimanatol/CR2-to-JPG-Converter/releases/latest)

> No Python installation is required when using the compiled `.exe`.

---

## Features

- Convert Canon `.CR2` RAW files to `.JPG`
- High-quality JPEG output
- Adjustable JPEG quality
- Select source folder
- Optional separate output folder
- Convert all CR2 files in a folder
- Include subfolders
- Preserve subfolder structure
- Skip existing JPG files
- Optional overwrite
- Progress bar
- Conversion log
- Stop conversion button
- Open output folder directly from the app
- Original CR2 files are never deleted
- Standalone Windows `.exe`
- Automatic EXE builds with GitHub Actions

---

## Screenshot

Add a screenshot of the application here after uploading one to the repository:

```markdown
![CR2 to JPG Converter](assets/screenshot.png)
```

---

## How to Use

1. Download `CR2-to-JPG-Converter.exe`.
2. Open the application.
3. Select the folder containing your `.CR2` files.
4. Select an output folder, or leave it blank to save JPG files beside the CR2 files.
5. Choose the JPEG quality.
6. Click **Convert CR2 to JPG**.
7. Wait for the progress bar to finish.
8. Click **Open Output Folder** to view the converted photos.

---

## JPEG Quality

The default JPEG quality is:

```text
95
```

This provides very high image quality while keeping the JPG file size smaller than the original RAW file.

---

## RAW Processing

The application uses:

- [rawpy](https://pypi.org/project/rawpy/)
- [LibRaw](https://www.libraw.org/)
- [Pillow](https://python-pillow.org/)

The converter uses the camera white balance when available.

Because Canon Digital Photo Professional, Adobe Camera Raw, Lightroom, Darktable, and LibRaw use different RAW-processing engines, the resulting JPG may look slightly different from Canon's own JPEG rendering.

---

## Run from Source

### Requirements

- Python 3.11 or newer
- Windows 10 or Windows 11

Install dependencies:

```powershell
py -m pip install -r requirements.txt
```

Run the application:

```powershell
py app.py
```

---

## Build the Windows EXE Locally

Double-click:

```text
build_exe.bat
```

Or run:

```powershell
py -m pip install -r requirements-build.txt
pyinstaller CR2_to_JPG.spec
```

The generated executable will be located at:

```text
dist\CR2-to-JPG-Converter.exe
```

---

## Automatic GitHub Build

This project includes a GitHub Actions workflow:

```text
.github/workflows/build-windows.yml
```

Every push to the `main` branch can automatically build the Windows executable.

To manually build it on GitHub:

1. Open the repository.
2. Click **Actions**.
3. Select **Build Windows EXE**.
4. Click **Run workflow**.
5. Wait for the build to finish.
6. Download the generated artifact.

---

## Creating a Release

To make the **Download EXE** button above work, publish the EXE as a GitHub Release asset with exactly this filename:

```text
CR2-to-JPG-Converter.exe
```

For version 1.0.0, create a tag:

```text
v1.0.0
```

Then upload:

```text
CR2-to-JPG-Converter.exe
```

to that GitHub Release.

The README download button always points to the newest release:

```text
https://github.com/jentimanatol/CR2-to-JPG-Converter/releases/latest/download/CR2-to-JPG-Converter.exe
```

---

## Version

### v1.0.0

Initial release.

- CR2 to JPG conversion
- Windows GUI
- Batch folder conversion
- Progress tracking
- Adjustable JPEG quality
- Recursive folder support
- GitHub Actions EXE build
- Standalone Windows executable

---

## License

MIT License

Copyright © 2026 Anatolie Jentimir
