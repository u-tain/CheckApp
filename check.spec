# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['check.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)


# these two lines add after use pyinstaller check.py
a.datas += [('bit.ico','path_to_your_icon\\bit.ico', "DATA")]
a.datas += [('res.png','path_to_your_picture\\res.png', "DATA")]


exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='check',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='path_to_your_icon\\bit.ico', # this line add after use pyinstaller check.py
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
