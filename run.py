import subprocess
import sys
from pathlib import Path

# Obtém o diretório onde o script (ou o executável) está localizado.
if getattr(sys, 'frozen', False):
    # Se estiver rodando como um executável PyInstaller
    BASE_DIR = Path(sys._MEIPASS)
else:
    # Se estiver rodando como um script normal
    BASE_DIR = Path(__file__).resolve().parent

# Caminho para o script principal do Streamlit
APP_SCRIPT = BASE_DIR / "app" / "app_sqlite.py"

subprocess.run(["streamlit", "run", str(APP_SCRIPT)])