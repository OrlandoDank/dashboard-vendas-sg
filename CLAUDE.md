# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This repository contains three products for SG Bichos (pet shop brand of SG Soluções):

1. **Sales dashboard** (`dashboard.py`) — internal Streamlit app with Omie ERP data. Deployed on Streamlit Community Cloud. Port 8501.
2. **CFO dashboard** (`dashboard_cfo.py`) — strategic financial planning dashboard. Local only (port 8502). Do NOT modify `dashboard.py` when working on CFO features.
3. **Loja virtual** (`sg-bichos/`) — public static e-commerce site (HTML/CSS/JS) for deploy on Hostinger. No backend required.

## Running locally

```powershell
# Install dependencies
& "C:\Users\orlan\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m pip install -r requirements.txt

# Sales dashboard (operacional)
& "C:\Users\orlan\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m streamlit run dashboard.py --server.port 8501

# CFO dashboard (planejamento financeiro)
& "C:\Users\orlan\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m streamlit run dashboard_cfo.py --server.port 8502
```

Credentials are loaded from `.streamlit/secrets.toml` locally (gitignored). See `.streamlit/secrets.toml` format:
```toml
OMIE_APP_KEY = "..."
OMIE_APP_SECRET = "..."
```

## Deploying changes

### Dashboard (Streamlit Cloud)
After editing, commit and push via GitHub Desktop or:
```bash
git add dashboard.py omie_api.py
git commit -m "description"
git push origin master
```
Streamlit Cloud auto-redeploys within ~2 minutes of a push to `master`.

### Loja virtual (Hostinger)
Upload the entire `sg-bichos/` folder to `public_html` via Hostinger File Manager or FTP.
See `sg-bichos/README.md` for full step-by-step instructions.

## Architecture

---

## Loja Virtual — sg-bichos/

Static HTML/CSS/JS e-commerce site. No server or PHP required. WhatsApp is used instead of a payment gateway.

### Updating the product catalog

Run `gerar_catalogo.py` to pull the live catalog from Omie and regenerate `sg-bichos/js/produtos.js`:

```powershell
& "C:\Users\orlan\AppData\Local\Python\pythoncore-3.14-64\python.exe" gerar_catalogo.py
```

### Testing locally

```powershell
& "C:\Users\orlan\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m http.server 8080
# Access: http://localhost:8080/sg-bichos/
```

### File structure

| File | Purpose |
|---|---|
| `sg-bichos/index.html` | Home page |
| `sg-bichos/categoria.html` | Category listing (`?cat=petiscos-secos`) |
| `sg-bichos/produto.html` | Product detail (`?id=<id>`) |
| `sg-bichos/contato.html` | Contact page (form opens WhatsApp) |
| `sg-bichos/css/style.css` | All styles. CSS variables: `--verde #2C1A08`, `--laranja #F5A800` |
| `sg-bichos/js/produtos.js` | Generated catalog — **do not edit manually**, run `gerar_catalogo.py` instead |
| `sg-bichos/js/main.js` | Cart, carousel, search, nav rendering, WhatsApp redirect |
| `sg-bichos/images/logo-sg-bichos.jpg` | Brand logo (copy of `logo.jpg` in repo root) |
| `sg-bichos/images/produtos/<codigo>.jpg` | Product photos — named after Omie internal code |
| `gerar_catalogo.py` | Fetches Omie catalog → writes `sg-bichos/js/produtos.js` |
| `gerar_lista_fotos.py` | Generates `sg-bichos/lista-fotos.csv` with product→filename mapping |

### Catalog filtering

`gerar_catalogo.py` excludes these Omie families (edit `FAMILIAS_EXCLUIR` to change):
`inativo, laços, Limpeza, Papeis, Coleira, Gravatas, Bonificações, Gargantilhas, Apliques, Bandanas, Adesivos`

Current catalog: **145 produtos** — Petiscos Secos (98), Higiene e Limpeza (30), Ração Seca (17).

### Product photos

- Place photos in `sg-bichos/images/produtos/` named `<codigo_interno>.jpg` (e.g. `PRD00117.jpg`)
- Run `gerar_lista_fotos.py` to regenerate `lista-fotos.csv` with the full product→filename mapping
- Missing photos fall back to a branded placeholder automatically
- Ideal size: 600×600 px

### Home page highlights (vitrine)

Set `"destaque": true` on chosen products in `sg-bichos/js/produtos.js`. If none are marked, the first 8 products are shown. Re-run `gerar_catalogo.py` resets all to `false`, so mark destaques after generating.

### WhatsApp number

Defined in `sg-bichos/js/produtos.js` as `const WHATSAPP = "5541987109563"`.

---

## Dashboard — dashboard.py

Two files do all the work:

**`omie_api.py`** — data layer. All Omie API calls live here. Key functions:
- `carregar_dados()` — single entry point called by the dashboard; returns a 9-tuple: `(df_pedidos, df_linhas, df_clientes, df_ind, df_prod, df_boletos, saldo_cash, df_pagar, df_receber)`
- `_paginar()` — generic paginator for all Omie list endpoints (50 records/page)
- `buscar_pedidos_e_linhas()` — fetches orders filtered by `infoCadastro`: only `faturado=S`, excludes `cancelado=S` and `devolvido=S`. The `etapa` field is NOT used for filtering (it's a custom workflow stage, not a reliable status indicator).
- `calcular_indicadores()` — left-joins all clients against order history; clients with no orders get `dias_sem_comprar=9999`
- `calcular_produtos()` — aggregates order line items, filters out `FAMILIAS_EXCLUIR` (laços, adesivos, limpeza, etc.) via `buscar_catalogo_produtos()`, then merges CMC costs using `_normalizar_desc()` which handles HTML entities (`&quot;`→`"`), removes accents and strips `(ZOOMIES)` suffix before matching
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

## CFO Dashboard — dashboard_cfo.py

Separate from `dashboard.py`. Never edit `dashboard.py` when working on CFO features.

**Structure:**
- **Aba 1 — Painel Financeiro:** KPIs atuais, projeção Jul-Dez/2026, composição de receita por unidade, análise de produtos (Top 10 margem, Top 10 valor vendido, tabela completa)
- **Aba 2 — Plano de Ação:** GAP analysis, 4 alavancas financeiras, plano de publicidade por unidade (B&T / Distribuidora / Lojas), checklist de execução

**Inputs manuais (sidebar):**
- Receita de cada loja de condomínio (5 lojas — não estão no Omie)
- Receita da B&T Loja de acessórios
- Parâmetros de crescimento por unidade (sliders)
- Total de despesas fixas

**8 fontes de receita do grupo:**
1. Distribuidora (B2B) — lida do Omie automaticamente
2. B&T Serviço — R$ 7.840/mês base, 90% margem
3. B&T Loja Acessórios — manual, R$ 100 atual, R$ 20k capacidade
4. Flex (condo) — manual, R$ 2.000 atual
5. Boutique do Dog (condo) — manual, R$ 1.000 atual (loja variada)
6. Cambirella (condo) — manual, R$ 500 atual
7. Castellamare (condo) — manual, R$ 500 atual
8. Cozensa (condo) — manual, R$ 500 atual

**Projeção configurada para:** crescimento 8%/mês dist. + B&T svc; INCOFAP extra R$ 4.500/mês; retirada progressiva R$ 0→R$ 18k em Dez/2026.

## Important constraints

- **CMC matching**: uses `_normalizar_desc()` on both sides before merging — removes HTML entities (`&quot;`→`"`), strips accents via NFKD, removes `(ZOOMIES)` brand suffix, uppercases. Format in spreadsheet is `"CODE - DESCRIPTION (UNIT)"` — the regex `^\S+\s*-\s*(.+?)\s*\(\w+\)$` extracts the description part. If a product's margin shows `—`, its description doesn't match any row in `Custos.xlsx` even after normalization.
- **Order filtering**: `buscar_pedidos_e_linhas()` uses `infoCadastro.faturado/cancelado/devolvido` fields — NOT `etapa`. The `etapa` field is a custom workflow stage configured per company and is unreliable as a status filter. Cancelled orders have `cancelado=S`; use this field exclusively.
- **Product family filtering**: `calcular_produtos()` calls `buscar_catalogo_produtos()` and excludes families in `FAMILIAS_EXCLUIR` (laços, adesivos, limpeza, papéis, coleira, gravatas, bonificações, gargantilhas, apliques, bandanas, inativo). Same list as `gerar_catalogo.py`.
- **CMC must always be read alongside the Omie API**: every data refresh must call `carregar_cmc_planilha()` together with the API calls — never skip it or cache it independently. `carregar_dados()` already enforces this by calling both in the same function. Do not refactor this in a way that allows the API data to be returned without the CMC values from the spreadsheet.
- **Omie API has no CMC/stock-cost endpoint** — the `produtos/estoque/`, `produtos/cmv/`, `produtos/posicaoestoque/` and all stock/CMV-related endpoints return 404 on this account plan. All cost data must come from `Custos.xlsx`. Do not retry these endpoints — confirmed blocked as of Jul/2026.
- **Color coding** used consistently throughout: green < 30 days, yellow 30–60 days, red > 60 days (applied to `dias_sem_comprar` for clients and `dias_atraso` for boletos; for margins: green ≥ 30%, yellow ≥ 10%, red < 10%; for contas a pagar: red = ATRASADO).
- **Supplier name lookup**: `buscar_contas_pagar()` tries `nome_fornecedor` and `razao_social` fields from the Omie response. If neither is present, the dashboard merges `df_pagar` with `df_cli` on `codigo_fornecedor == codigo_cliente` to resolve the name. Suppliers not registered as clients will still show as a numeric code.
- **Updating `Custos.xlsx`**: export fresh report from Omie, save as `Custos.xlsx` in repo root, commit and push — dashboard picks it up on next data refresh.
