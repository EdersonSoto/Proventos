from datetime import datetime
from pathlib import Path
import os
import shutil

from banco import BANCO
from config import PASTA_BACKUP


SCOPES_GOOGLE_DRIVE = [
    "https://www.googleapis.com/auth/drive.file"
]


def encontrar_pasta_google_drive():

    pasta_configurada = os.getenv("PROVENTOS_GOOGLE_DRIVE_BACKUP")

    if pasta_configurada:

        return Path(pasta_configurada)

    home = Path.home()

    candidatos = [
        home / "Google Drive" / "Proventos",
        home / "Google Drive" / "Meu Drive" / "Proventos",
        home / "Meu Drive" / "Proventos",
    ]

    for letra in "DEFGHIJKLMNOPQRSTUVWXYZ":

        candidatos.extend([
            Path(f"{letra}:/Meu Drive/Proventos"),
            Path(f"{letra}:/My Drive/Proventos"),
            Path(f"{letra}:/Google Drive/Proventos"),
        ])

    for candidato in candidatos:

        if candidato.parent.exists():

            return candidato

    return None


def obter_caminho_config(nome_variavel, nome_arquivo):

    caminho = os.getenv(nome_variavel)

    if caminho:

        return Path(caminho)

    return Path("config") / nome_arquivo


def enviar_google_drive_online(arquivo_backup):

    pasta_id = os.getenv("PROVENTOS_GOOGLE_DRIVE_FOLDER_ID")

    if not pasta_id:

        return {
            "enviado": False,
            "arquivo_id": None,
            "link": None,
            "erro": "ID da pasta do Google Drive nao configurado.",
        }

    try:

        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload

    except ImportError:

        return {
            "enviado": False,
            "arquivo_id": None,
            "link": None,
            "erro": "Bibliotecas do Google Drive nao instaladas.",
        }

    credenciais_path = obter_caminho_config(
        "PROVENTOS_GOOGLE_CREDENTIALS_FILE",
        "google_credentials.json",
    )

    token_path = obter_caminho_config(
        "PROVENTOS_GOOGLE_TOKEN_FILE",
        "google_token.json",
    )

    if not credenciais_path.exists() and not token_path.exists():

        return {
            "enviado": False,
            "arquivo_id": None,
            "link": None,
            "erro": "Arquivo de credenciais do Google nao encontrado.",
        }

    creds = None

    if token_path.exists():

        creds = Credentials.from_authorized_user_file(
            str(token_path),
            SCOPES_GOOGLE_DRIVE,
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            if not credenciais_path.exists():

                return {
                    "enviado": False,
                    "arquivo_id": None,
                    "link": None,
                    "erro": "Token expirado e credenciais do Google nao encontradas.",
                }

            flow = InstalledAppFlow.from_client_secrets_file(
                str(credenciais_path),
                SCOPES_GOOGLE_DRIVE,
            )
            creds = flow.run_local_server(
                port=0
            )

        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(
            creds.to_json(),
            encoding="utf-8",
        )

    servico = build(
        "drive",
        "v3",
        credentials=creds,
    )

    arquivo_backup = Path(arquivo_backup)

    metadados = {
        "name": arquivo_backup.name,
        "parents": [pasta_id],
    }

    media = MediaFileUpload(
        str(arquivo_backup),
        mimetype="application/x-sqlite3",
        resumable=False,
    )

    arquivo = (
        servico.files()
        .create(
            body=metadados,
            media_body=media,
            fields="id, webViewLink",
        )
        .execute()
    )

    return {
        "enviado": True,
        "arquivo_id": arquivo.get("id"),
        "link": arquivo.get("webViewLink"),
        "erro": None,
    }


def criar_backup_automatico():

    banco = Path(BANCO)

    if not banco.exists():

        return {
            "ok": False,
            "local": None,
            "google_drive": None,
            "google_drive_online": None,
            "erro": "Banco de dados ainda nao existe.",
        }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_backup = f"proventos_{timestamp}.db"

    pasta_local = Path(PASTA_BACKUP)
    pasta_local.mkdir(parents=True, exist_ok=True)

    destino_local = pasta_local / nome_backup
    shutil.copy2(banco, destino_local)

    destino_google = None
    pasta_google = encontrar_pasta_google_drive()

    try:

        if pasta_google:

            pasta_google.mkdir(parents=True, exist_ok=True)
            destino_google = pasta_google / nome_backup
            shutil.copy2(banco, destino_google)

    except OSError:

        destino_google = None

    try:

        google_drive_online = enviar_google_drive_online(
            destino_local
        )

    except Exception as erro:

        google_drive_online = {
            "enviado": False,
            "arquivo_id": None,
            "link": None,
            "erro": str(erro),
        }

    return {
        "ok": True,
        "local": str(destino_local),
        "google_drive": str(destino_google) if destino_google else None,
        "google_drive_online": google_drive_online,
        "erro": None,
    }
