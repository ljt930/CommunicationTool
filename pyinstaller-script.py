#!c:\python27\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'PyInstaller==3.3.1','console_scripts','pyinstaller'
__requires__ = 'PyInstaller==3.3.1'
import re
import sys
from pkg_resources import load_entry_point

import  os
if __name__ == '__main__':
    from PyInstaller.__main__ import run
    # opts=['main.py','-w','-D','-iico/tool.ico']
    opts=['main.spec','-D']
    run(opts)
