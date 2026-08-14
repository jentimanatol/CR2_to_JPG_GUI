# CR2 to JPG Converter

A Windows desktop application for converting Canon `.CR2` RAW photographs to high-quality `.JPG` files.

## Features

- Select a folder containing Canon CR2 files
- Convert all `.CR2` files to `.JPG`
- Optional separate output folder
- Adjustable JPEG quality from 50 to 100
- Include subfolders
- Preserve subfolder structure
- Skip or overwrite existing JPG files
- Progress bar and conversion log
- Stop button
- Keeps original CR2 files untouched
- Standalone Windows EXE with PyInstaller
- GitHub Actions workflow for automatic EXE builds

## Run from Python

```powershell
py -m pip install -r requirements.txt
py app.py
```

## Build the EXE locally

Double-click:

```text
build_exe.bat
```

or run:

```powershell
py -m pip install -r requirements-build.txt
py -m PyInstaller --clean --noconfirm CR2_to_JPG.spec
```

The EXE will appear here:

```text
dist\CR2-to-JPG-Converter.exe
```

## GitHub Actions EXE build

The included workflow is:

```text
.github/workflows/build-windows.yml
```

After you push the repository to GitHub, open:

**GitHub -> Actions -> Build Windows EXE -> latest successful run -> Artifacts**

Download:

```text
CR2-to-JPG-Converter-Windows
```

The workflow runs on pushes to `main`, pull requests to `main`, version tags such as `v1.0.0`, and manual workflow runs.

## RAW processing

The application uses `rawpy`, which is based on LibRaw, and Pillow for JPEG encoding. It uses the camera white balance when available and exports 8-bit JPEG files.

Different RAW processors can render color and tone slightly differently from Canon Digital Photo Professional, Lightroom, or Adobe Camera Raw.

## License

MIT
