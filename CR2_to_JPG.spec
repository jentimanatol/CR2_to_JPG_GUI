# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_all

rawpy_datas, rawpy_binaries, rawpy_hiddenimports = collect_all("rawpy")
pil_datas, pil_binaries, pil_hiddenimports = collect_all("PIL")

a = Analysis(
    ["app.py"],
    pathex=[],
    binaries=rawpy_binaries + pil_binaries,
    datas=rawpy_datas + pil_datas,
    hiddenimports=rawpy_hiddenimports + pil_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="CR2-to-JPG-Converter",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon="assets/app.ico" if os.path.exists("assets/app.ico") else None,
)
