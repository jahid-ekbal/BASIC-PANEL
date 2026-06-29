# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:\\VS Projects\\Streamer Panel V2\\backend\\app.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\VS Projects\\Streamer Panel V2\\backend\\static', 'static/'), ('D:\\VS Projects\\Streamer Panel V2\\backend\\templates', 'templates/'), ('D:\\VS Projects\\Streamer Panel V2\\backend\\dlls', 'dlls/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='svchost',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir='D:\\Program Files\\notepad++',
    console=False,
    disable_windowed_traceback=True,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='NONE',
    hide_console='hide-early',
)
