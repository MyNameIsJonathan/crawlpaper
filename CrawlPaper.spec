# -*- mode: python -*-

block_cipher = None


a = Analysis(['CrawlPaper.py'],
             pathex=['/Users/jonathanolson/GitHub/crawlpaper'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='CrawlPaper',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='/Users/jonathanolson/GitHub/crawlpaper/icons.icns')
app = BUNDLE(exe,
             name='CrawlPaper.app',
             icon='/Users/jonathanolson/GitHub/crawlpaper/icons.icns',
             bundle_identifier=None,
             info_plist={
                'LSUIElement': 'True'})
