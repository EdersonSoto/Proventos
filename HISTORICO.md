# Historico do Projeto Proventos

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
