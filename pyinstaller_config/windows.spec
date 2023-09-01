# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2, glew
from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, get_deps_all, hookspath, runtime_hooks

block_cipher = None


a = Analysis(
    ['../MCQMaker.py'],
    pathex=[],
    datas=[("../mcq_maker_screens","mcq_maker_screens"),("../MCQMaker.kv","."),("../mcq_maker_tools","mcq_maker_tools")],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    hiddenimports=["tkinter"],
    noarchive=False
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

#splash = Splash('../resources/logo.png',
#                binaries=a.binaries,
#                datas=a.datas,
#                text_pos=(10, 50),
#                text_size=12,
#                text_color='black')

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='MCQMaker',
          version="version.txt",
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
          icon='../resources/icon.ico' )

#coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=False,
#     upx_exclude=[],
#     name='MCQMaker'
#)

#app = BUNDLE(
#     coll,
#     name='MCQMaker',
#)

