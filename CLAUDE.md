# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Sales dashboard for SG Soluções that pulls live data from the Omie ERP API and displays it via a Streamlit web app. Deployed on Streamlit Community Cloud at https://dashboard-vendas-sg-x8vdpxld7umktnnzcktczn.streamlit.app/

## Running locally

```powershell
# Install dependencies
& "C:\Users\orlan\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m pip install -r requirements.txt

# Start the dashboard
cd "C:\Users\orlan\Dropbox\Claude assist\Codigo"
& "C:\Users\orlan\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m streamlit run dashboard.py --server.port 8501
```

Credentials are loaded from `.streamlit/secrets.toml` locally (gitignored). See `.streamlit/secrets.toml` format:
```toml
OMIE_APP_KEY = "..."
OMIE_APP_SECRET = "..."
```

## Deploying changes

After editing, commit and push via GitHub Desktop or:
```bash
git add dashboard.py omie_api.py
git commit -m "description"
git push origin master
```
Streamlit Cloud auto-redeploys within ~2 minutes of a push to `master`.

## Architecture

Two files do all the work:

**`omie_api.py`** — data layer. All Omie API calls live here. Key functions:
- `carregar_dados()` — single entry point called by the dashboard; returns an 8-tuple: `(df_pedidos, df_linhas, df_clientes, df_ind, df_prod, df_boletos, saldo_cash, df_pagar)`
- `_paginar()` — generic paginator for all Omie list endpoints (50 records/page)
- `calcular_indicadores()` — left-joins all clients against order history; clients with no orders get `dias_sem_comprar=9999`
- `calcular_produtos()` — aggregates order line items and merges CMC costs from the spreadsheet by normalised description (uppercase strip)
- `carregar_cmc_planilha()` — reads `Custos.xlsx` on every call (never cached) so spreadsheet updates are picked up immediately
- `buscar_contas_pagar()` — fetches accounts payable from `financas/contapagar/` → `ListarContasPagar`; returns only ABERTO and ATRASADO (skips PAGO and CANCELADO)

**`dashboard.py`** — presentation layer. Pure Streamlit. Calls `get_dados()` (cached 5 min via `@st.cache_data(ttl=300)`).

### Page layouts

**Visão Geral**
- KPI row 1: Total faturado, Total pedidos, Ticket médio, Omie.CASH
- KPI row 2: Clientes ativos (verde), Atenção, Inativos, Boletos em atraso
- Card: Contas a Pagar desta semana — KPI "Esta semana" + mini tabela (3 linhas, seg–dom)
- Charts: Faturamento Mensal (colunas verticais) + Retenção de Clientes (donut)
- Rankings: Top 10 Clientes + Top 10 Produtos (barras horizontais)

**Clientes** — tabela completa com busca, filtro de status e ordenação

**Produtos** — Top 10 por qtd vendida e receita (barras horizontais) + tabela completa com margem

**Boletos em Atraso** — KPIs + gráfico por cliente + tabela colorida por dias de atraso

**Financeiro**
- KPIs: Faturamento total, Omie.CASH, Boletos em atraso
- Gráfico faturamento mensal (colunas + linha de pedidos, eixo duplo)
- Card Contas a Pagar com filtro **Esta semana / Este mês / Este ano** — KPIs (total, atrasado, aberto) + tabela colorida
- Tabela de pedidos recentes (últimos 50)

## Key data sources

| Source | How accessed |
|---|---|
| Omie API | REST POST to `https://app.omie.com.br/api/v1/` with APP_KEY/APP_SECRET |
| CMC costs | `Custos.xlsx` in repo root — exported manually from Omie "Posição de Estoque" report |
| Omie.CASH balance | `financas/extrato/` → `ListarExtrato` → field `nSaldoDisponivel` (account code `3311955703`) |
| Overdue boletos | `financas/contareceber/` → `ListarContasReceber`, filtered by `status_titulo == "ATRASADO"` |
| Accounts payable | `financas/contapagar/` → `ListarContasPagar`, filtered to ABERTO + ATRASADO |

## Important constraints

- **CMC matching**: product descriptions from the API are matched against the spreadsheet by normalised uppercase description. Format in spreadsheet is `"CODE - DESCRIPTION (UNIT)"` — the regex `^\S+\s*-\s*(.+?)\s*\(\w+\)$` extracts the description part. If a product's margin shows `—`, its description doesn't match any row in `Custos.xlsx`.
- **CMC must always be read alongside the Omie API**: every data refresh must call `carregar_cmc_planilha()` together with the API calls — never skip it or cache it independently. `carregar_dados()` already enforces this by calling both in the same function. Do not refactor this in a way that allows the API data to be returned without the CMC values from the spreadsheet.
- **Omie API has no CMC/stock-cost endpoint** — the `produtos/estoque/` endpoint returns 404 on this account plan. All cost data must come from the spreadsheet.
- **Color coding** used consistently throughout: green < 30 days, yellow 30–60 days, red > 60 days (applied to `dias_sem_comprar` for clients and `dias_atraso` for boletos; for margins: green ≥ 30%, yellow ≥ 10%, red < 10%; for contas a pagar: red = ATRASADO).
- **Supplier name lookup**: `buscar_contas_pagar()` tries `nome_fornecedor` and `razao_social` fields from the Omie response. If neither is present, the dashboard merges `df_pagar` with `df_cli` on `codigo_fornecedor == codigo_cliente` to resolve the name. Suppliers not registered as clients will still show as a numeric code.
- **Updating `Custos.xlsx`**: export fresh report from Omie, save as `Custos.xlsx` in repo root, commit and push — dashboard picks it up on next data refresh.
