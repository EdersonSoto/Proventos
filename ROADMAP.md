# Roadmap do Projeto Proventos

## Situacao atual

O projeto ja passou da fase de prototipo e esta entrando na fase de produto.

Existem duas versoes principais:

### Versao inicial

Arquivo: `app/app.py`

Esta versao le diretamente arquivos CSV/XLSX da pasta e gera graficos. Ela e mais simples e nao usa banco de dados.

### Versao principal

Arquivo: `app/app_sqlite.py`

Esta e a versao que deve continuar evoluindo.

Ela possui:

- Importacao automatica dos arquivos.
- Banco SQLite.
- Filtros.
- Meta mensal.
- Graficos.
- Ranking.
- Dashboard.
- Evolucao acumulada.
- Grafico de distribuicao.
- Controle de duplicidade na importacao.

## Banco de dados atual

Tabela principal:

```text
proventos
---------
id
data_pagamento
ativo
tipo
valor
origem
```

Essa estrutura atende bem a primeira etapa do sistema de controle de dividendos.

## Importador atual

O importador em `app/importar_csv.py` ja resolve pontos importantes:

- Le arquivos XLSX.
- Le arquivos CSV.
- Identifica automaticamente o tipo de arquivo.
- Encontra o ticker do ativo.
- Identifica se o ativo e FII ou acao.
- Evita importar registros duplicados.

## Versao 2.0

Objetivo: evoluir o sistema atual sem reescrever o que ja funciona.

Modulos sugeridos:

- Dashboard: existente.
- Carteira: novo.
- Operacoes: novo.
- Dividendos: existente.
- FIIs: existente.
- Acoes: existente.
- Indicadores: novo.
- Imposto: novo.
- Comparador: novo.
- Backup: novo.
- Configuracao: novo.

Prioridade sugerida:

1. Cadastro manual de proventos.
2. Exportacao para Excel.
3. Backup automatico do banco SQLite: implementado com copia local e suporte a Google Drive online.
4. Separacao em paginas Streamlit.
5. Cadastro de carteira.
6. Cadastro de operacoes de compra e venda.

## Versao 3.0

Objetivo: transformar o projeto de controle de dividendos em um software de investimentos mais completo.

Classes de ativos planejadas:

- Acoes.
- FIIs.
- BDRs.
- ETFs.
- Tesouro Direto.
- Renda fixa.
- Cripto.
- Investimentos no exterior.

## Versao 4.0

Objetivo: automatizar dados externos e indicadores.

Possiveis integracoes:

- Yahoo Finance.
- Fundamentus.
- CVM.
- B3.
- Banco Central.

Dados a atualizar automaticamente:

- Cotacao.
- Dividend Yield.
- P/L.
- P/VP.
- ROE.
- ROIC.
- CAGR.
- Payout.
- Patrimonio.
- Valor patrimonial.
- Historico de dividendos.

## Principio do projeto

O Git e o GitHub devem ser a fonte permanente de verdade do projeto.

O chat serve como apoio para desenvolvimento, planejamento e revisao, mas as decisoes importantes devem ser registradas em arquivos do repositorio.
