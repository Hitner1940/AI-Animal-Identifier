# -*- mode: python ; coding: utf-8 -*-

# This is a PyInstaller spec file. It tells PyInstaller how to build your
# application into a single executable file. This is necessary for complex
# applications, especially those using libraries like TensorFlow.

block_cipher = None

# Analysis: This section finds all the necessary files.
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    # --- IMPORTANT: Add data files here ---
    # This line ensures that your 'languages.json' file is included in the final .exe
    datas=[('languages.json', '.')],
    # --- IMPORTANT: Handle hidden imports ---
    # TensorFlow and other libraries hide some of their code, so we must tell
    # PyInstaller where to find it explicitly.
    hiddenimports=[
        'tensorflow.keras.applications.mobilenet_v2',
        'h5py',
        'h5py._conv',
        'PIL',
        'PIL._tkinter_finder'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# EXE: This section configures the final executable file.
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AnimalIdentifier',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    # --- IMPORTANT: This creates a windowed app without a console ---
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # --- (Optional) Add your icon file here ---
    # icon='icon.ico',
)
