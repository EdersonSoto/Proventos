# Historico do Projeto Proventos

## 2026-07-13

### Icone do executavel e do instalador

- Criado `assets/icon.ico` (moeda verde/dourada com grafico de crescimento),
  gerado programaticamente com Pillow via `assets/gerar_icone.py` (sem depender
  de imagem externa). Aplicado no `build.spec` (`EXE(..., icon=...)`) e no
  `proventos_setup.iss` (`SetupIconFile`), valendo tanto para o `.exe` quanto
  para os atalhos e o instalador em si.

### Botao de fechar o programa

- Adicionado botao "Fechar Programa" na barra lateral (`app/app_sqlite.py`). Ao
  clicar, mostra uma mensagem de despedida e encerra o processo (`os._exit(0)`)
  apos um pequeno atraso em thread separada, fechando o servidor Streamlit e o
  console de forma limpa, sem precisar fechar a janela do terminal manualmente.

### Projeto preparado para gerar o instalador (PyInstaller + Inno Setup) em outro computador

- Corrigido bug critico no `build.spec`: os modulos de `app/` (config.py, backup.py,
  importar_csv.py) sao executados dinamicamente pelo Streamlit e nao eram vistos pela
  `Analysis`, entao o `python-dotenv` (import obrigatorio em `config.py`) nao era
  empacotado e o executavel quebrava ao abrir em outro computador. Adicionado
  `collect_all` para `dotenv` e para as bibliotecas do Google Drive.
- Corrigido o `COLLECT` do `build.spec`: as tuplas `("app", "app")` etc. nao sao mais
  aceitas pela versao atual do PyInstaller; substituidas por `Tree(...)`.
- `requirements.txt` completado (faltava `python-dotenv`) e com versoes fixadas,
  incluindo `pyinstaller`, para reproduzir o mesmo ambiente em outro computador.
- Build validado localmente: `pyinstaller build.spec` e depois `ISCC proventos_setup.iss`
  geraram `Output\Controle_de_Proventos_Setup.exe` com sucesso, e o executavel
  (`dist\Proventos\ProventosApp.exe`) sobe o dashboard Streamlit normalmente.
- `build/` e `dist/` (saida gerada do PyInstaller, milhares de arquivos binarios)
  removidos do controle de versao e adicionados ao `.gitignore`, junto com `Output/`.
- Adicionado `build.ps1` para automatizar `pip install` + PyInstaller + Inno Setup em
  um unico comando.
- Adicionados `database/.gitkeep` e `csv/.gitkeep` para que essas pastas (referenciadas
  pelo `build.spec`) existam apos um `git clone` novo, mesmo com o conteudo ignorado.
- Removido `app/app.py` (versao antiga do dashboard, com caminho fixo
  `C:\Investimentos\Proventos\csv`, ja substituida por `app/app_sqlite.py`).
- `config/ID cliente.txt` (Client ID OAuth do Google, nao usado por nenhum codigo)
  removido do controle de versao, por consistencia com as demais credenciais em
  `config/`.

## 2026-07-06

Projeto em Python com Streamlit e SQLite para controle de dividendos de acoes e FIIs.

### Contexto recuperado

O historico antigo do chat foi perdido, mas o projeto nao foi perdido porque existem:

- Pasta local em `C:\Investimentos\Proventos`.
- Repositorio Git local.
- Repositorio privado no GitHub.
- Arquivos principais do sistema no projeto.

O Git/GitHub passa a ser a memoria permanente do projeto. O chat deve ser usado apenas como apoio ao desenvolvimento.

### Estrutura principal conhecida

- `app/app_sqlite.py`: dashboard Streamlit usando SQLite.
- `app/importar_csv.py`: importacao automatica de arquivos `.xlsx` e `.csv`.
- `app/banco.py`: conexao e criacao da tabela SQLite.
- `app/config.py`: caminhos de pastas do projeto.
- `app/teste_banco.py`: leitura simples do banco para conferencia.
- `database/proventos.db`: banco SQLite local.
- `csv/`: arquivos de extrato/importacao.

### Funcionalidades ja existentes

- Banco SQLite.
- Importacao automatica de extratos Clear.
- Dashboard Streamlit.
- Filtros por ano, tipo e ativo.
- Grafico mensal.
- Grafico anual.
- Evolucao acumulada.
- Distribuicao Acoes x FIIs.
- Meta mensal.
- Ranking de ativos.
- Listagem de lancamentos.

### Ajustes feitos nesta retomada

- Removido o debug `DEBUG RESUMO TIPO` da tela.
- Adicionada mensagem quando filtros nao retornam lancamentos.
- Protegida a media mensal contra valor vazio.
- Confirmado que o banco possui tipos de acao e FII gravados corretamente no SQLite e exibidos corretamente no app.
- Adicionado backup automatico do banco ao abrir o app.
- O backup e salvo sempre na pasta local `backup/`.
- Quando o Google Drive e encontrado no computador, uma copia tambem e salva no Drive.
- Adicionado suporte a envio online para Google Drive via API, sem depender da pasta sincronizada no PC.
- Para envio online, configurar `PROVENTOS_GOOGLE_DRIVE_FOLDER_ID` e salvar as credenciais em `config/google_credentials.json`.

### Como rodar

```powershell
cd C:\Investimentos\Proventos
streamlit run app\app_sqlite.py
```

Ou:

```powershell
cd C:\Investimentos\Proventos\app
streamlit run app_sqlite.py
```

### Configuracao do Google Drive online

O backup online usa a API do Google Drive.

Arquivos locais esperados:

- `config/google_credentials.json`: credenciais OAuth baixadas no Google Cloud.
- `config/google_token.json`: token gerado automaticamente no primeiro login.

Variavel obrigatoria:

```powershell
$env:PROVENTOS_GOOGLE_DRIVE_FOLDER_ID="ID_DA_PASTA_DO_GOOGLE_DRIVE"
```

Os arquivos de credenciais e token ficam fora do GitHub por seguranca.

### Proximos passos sugeridos

1. Criar cadastro manual de proventos pela interface.
2. Criar exportacao para Excel.
3. Melhorar visual e organizacao do dashboard.
4. Criar backup automatico do banco SQLite.
5. Separar o app em paginas: Dashboard, Lancamentos, Importacao e Configuracoes.
6. Criar `README.md` com instalacao, execucao e descricao do projeto.

### Comandos uteis de versionamento

```powershell
git status
git add .
git commit -m "Registra historico e ajustes do dashboard"
git push
```

para instalar as ferramentas online API google
pip install -r requirements.txt