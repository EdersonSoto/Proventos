# Proventos

Dashboard desktop para controle de proventos (dividendos, JCP e rendimentos) recebidos em ações e Fundos Imobiliários (FIIs), com importação automática de extratos, gráficos de evolução e backup em nuvem.

## Sobre o projeto

O sistema foi criado para centralizar e visualizar o histórico de proventos recebidos em investimentos, substituindo o controle manual por planilhas. Os lançamentos são importados a partir de extratos exportados da corretora e armazenados em um banco SQLite local, exibidos em um painel interativo construído com Streamlit.

## Funcionalidades

- Importação automática de extratos em `.csv` e `.xlsx`.
- Banco de dados local em SQLite.
- Dashboard interativo com filtros por ano, tipo de provento e ativo.
- Gráficos de evolução mensal, anual e acumulada.
- Distribuição entre Ações e FIIs.
- Acompanhamento de meta mensal e ranking de ativos.
- Listagem detalhada de todos os lançamentos.
- Backup automático do banco a cada abertura do app, salvo localmente e, opcionalmente, na nuvem (Google Drive, via API OAuth).
- Empacotamento como executável Windows (PyInstaller + Inno Setup), para uso sem precisar instalar Python.

## Tecnologias utilizadas

- **Python 3**
- **Streamlit** — dashboard web local
- **SQLite** — banco de dados
- **Pandas** — processamento dos dados
- **Plotly** — gráficos interativos
- **openpyxl** — leitura de planilhas Excel
- **Google Drive API** (`google-api-python-client`, `google-auth-oauthlib`) — backup em nuvem
- **PyInstaller** + **Inno Setup** — geração do executável e instalador Windows

## Como executar

### Pré-requisitos

- Python 3.10+

### Passos

```bash
git clone https://github.com/EdersonSoto/Proventos.git
cd Proventos
pip install -r requirements.txt
streamlit run app/app_sqlite.py
```

O dashboard abre automaticamente no navegador padrão.

### Backup em nuvem (opcional)

Para habilitar o envio automático de backup ao Google Drive:

1. Gere as credenciais OAuth no Google Cloud e salve como `config/google_credentials.json`.
2. Defina a variável de ambiente com o ID da pasta de destino no Drive:

   ```powershell
   $env:PROVENTOS_GOOGLE_DRIVE_FOLDER_ID="ID_DA_PASTA_DO_GOOGLE_DRIVE"
   ```

Os arquivos de credenciais e token ficam fora do controle de versão por segurança.

### Gerando o executável (Windows)

```powershell
./build.ps1
```

O script automatiza a instalação das dependências, a geração do executável com PyInstaller (`build.spec`) e do instalador com Inno Setup (`proventos_setup.iss`).

## Estrutura do projeto

```
Proventos/
├── app/                 # Código da aplicação (dashboard, importação, backup, config)
├── assets/               # Ícones e recursos visuais
├── database/              # Banco de dados SQLite (gerado localmente)
├── csv/                    # Extratos importados
├── build.spec              # Configuração do PyInstaller
├── build.ps1                # Script de build automatizado
├── proventos_setup.iss       # Script do instalador (Inno Setup)
├── ROADMAP.md                 # Próximos passos planejados
├── HISTORICO.md                # Histórico de desenvolvimento do projeto
└── requirements.txt              # Dependências Python
```

## Roadmap

O andamento e os próximos passos planejados para o projeto estão documentados em [ROADMAP.md](ROADMAP.md).

## Autor

Desenvolvido por [Ederson Soto](https://github.com/EdersonSoto).
