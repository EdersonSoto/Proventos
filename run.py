import sys
from pathlib import Path

from streamlit.web.cli import main

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent

APP_SCRIPT = BASE_DIR / "app" / "app_sqlite.py"

sys.argv = [
    "streamlit",
    "run",
    str(APP_SCRIPT),
    "--global.developmentMode=false",
]

sys.exit(main())