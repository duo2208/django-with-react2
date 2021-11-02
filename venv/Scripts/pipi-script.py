#!"c:\users\izimi\onedrive\πŸ≈¡ »≠∏È\programing\vscode\django_with_react2\venv\scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'pipi==1.0.1','console_scripts','pipi'
__requires__ = 'pipi==1.0.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('pipi==1.0.1', 'console_scripts', 'pipi')()
    )
