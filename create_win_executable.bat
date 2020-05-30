REM Creates Windows executable using the pyinstaller

call venv\scripts\activate

pyinstaller -n kroger-cli ^
            --onefile ^
            --exclude-module tkinter ^
            --hidden-import=six ^
            --hidden-import=packaging ^
            --hidden-import=packaging.version ^
            --hidden-import=packaging.requirements ^
            --hidden-import=packaging.specifiers ^
            --hidden-import=pkg_resources ^
            --hidden-import=pkg_resources.py2_warn ^
            kroger_cli/__main__.py