import os
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path

URL_BASE     = "https://app.omie.com.br/api/v1/"
PLANILHA_CMC = Path(__file__).parent / "Custos.xlsx"


def _credenciais():
    """Lê APP_KEY e APP_SECRET em tempo de execução (não na importação)."""
    try:
        import streamlit as st
        return st.secrets["OMIE_APP_KEY"], st.secrets["OMIE_APP_SECRET"]
    except Exception:
        return os.environ.get("OMIE_APP_KEY", ""), os.environ.get("OMIE_APP_SECRET", "")


def _post(endpoint: str, call: str, param: dict) -> dict:
    app_key, app_secret = _credenciais()
    payload = {
        "app_key":    app_key,
        "app_secret": app_secret,
        "call":       call,
        "param":      [param],
    }
    r = requests.post(URL_BASE + endpoint, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()


def _paginar(endpoint: str, call: str, param_base: dict, chave_lista: str) -> list:
    itens = []
    pagina = 1
    while True:
        resp = _post(endpoint, call, {**param_base, "pagina": pagina, "registros_por_pagina": 50})
        lista = resp.get(chave_lista, [])
        if not lista:
            break
        itens.extend(lista)
        if pagina >= resp.get("total_de_paginas", 1):
            break
        pagina += 1
    return itens


# ── CMC DA PLANILHA ───────────────────────────────────────────────────────────

def carregar_cmc_planilha() -> pd.DataFrame:
    """
    Lê Custos.xlsx (Posição de Estoque) e retorna DataFrame com
    descricao_limpa (uppercase, sem código/unidade) e cmc_unitario.
    Sempre relê o arquivo para capturar atualizações.
    """
    df_raw = pd.read_excel(PLANILHA_CMC, sheet_name=0, header=None)

    # Encontrar linha de cabeçalho (contém "Soma de CMC")
    header_row = None
    for i, row in df_raw.iterrows():
        if any("CMC" in str(v) for v in row.values):
            header_row = i
            break
    if header_row is None:
        return pd.DataFrame(columns=["descricao_limpa", "cmc_unitario"])

    df_raw.columns = df_raw.iloc[header_row]
    df = df_raw.iloc[header_row + 1:].copy().reset_index(drop=True)

    # Identificar colunas pelo conteúdo do cabeçalho
    col_desc = df.columns[0]
    col_cmc  = next((c for c in df.columns if "CMC Unit" in str(c)), None)
    if col_cmc is None:
        return pd.DataFrame(columns=["descricao_limpa", "cmc_unitario"])

    df = df[[col_desc, col_cmc]].copy()
    df.columns = ["descricao_planilha", "cmc_unitario"]
    df = df.dropna(subset=["descricao_planilha"])
    df = df[df["descricao_planilha"].astype(str).str.strip() != ""]

    # Extrair descrição limpa: "002 - PRODUTO XYZ (UN)" → "PRODUTO XYZ"
    df["descricao_limpa"] = (
        df["descricao_planilha"]
        .astype(str)
        .str.extract(r"^\S+\s*-\s*(.+?)\s*\(\w+\)$", expand=False)
        .fillna(df["descricao_planilha"].astype(str))
        .str.strip()
        .str.upper()
    )
    df["cmc_unitario"] = pd.to_numeric(df["cmc_unitario"], errors="coerce").fillna(0)

    return df[["descricao_limpa", "cmc_unitario"]].drop_duplicates("descricao_limpa")


# ── SALDO OMIE.CASH ───────────────────────────────────────────────────────────

def buscar_saldo_omie_cash() -> float:
    hoje = datetime.today().strftime("%d/%m/%Y")
    try:
        data = _post("financas/extrato/", "ListarExtrato", {
            "nCodCC":           3311955703,
            "dPeriodoInicial":  "01/01/2020",
            "dPeriodoFinal":    hoje,
        })
        return float(data.get("nSaldoDisponivel", 0) or 0)
    except Exception:
        return 0.0


# ── CLIENTES ──────────────────────────────────────────────────────────────────

def buscar_clientes() -> pd.DataFrame:
    raw = _paginar("geral/clientes/", "ListarClientes", {}, "clientes_cadastro")
    registros = []
    for c in raw:
        registros.append({
            "codigo_cliente": c.get("codigo_cliente_omie"),
            "nome_cliente":   c.get("razao_social") or c.get("nome_fantasia", ""),
            "cidade":         c.get("cidade", ""),
            "estado":         c.get("estado", ""),
            "email":          c.get("email", ""),
            "telefone":       c.get("telefone1_numero", ""),
            "cnpj_cpf":       c.get("cnpj_cpf", ""),
        })
    df = pd.DataFrame(registros)
    df["codigo_cliente"] = pd.to_numeric(df["codigo_cliente"], errors="coerce")
    return df


# ── PEDIDOS + LINHAS ──────────────────────────────────────────────────────────

def buscar_pedidos_e_linhas() -> tuple:
    raw = _paginar("produtos/pedido/", "ListarPedidos", {}, "pedido_venda_produto")
    pedidos = []
    linhas  = []
    for p in raw:
        cab   = p.get("cabecalho", {})
        total = p.get("total_pedido", {})
        num   = cab.get("numero_pedido")
        data  = cab.get("data_previsao")

        pedidos.append({
            "numero_pedido":    num,
            "data_pedido":      data,
            "codigo_cliente":   cab.get("codigo_cliente"),
            "valor_total":      float(total.get("valor_total_pedido", 0) or 0),
            "valor_produtos":   float(total.get("valor_mercadorias",  0) or 0),
            "valor_desconto":   float(total.get("valor_descontos",    0) or 0),
            "etapa":            cab.get("etapa", ""),
            "quantidade_itens": int(cab.get("quantidade_itens", 0) or 0),
        })

        for item in p.get("det", []):
            prod = item.get("produto", {})
            linhas.append({
                "numero_pedido":     num,
                "data_pedido":       data,
                "codigo_produto":    prod.get("codigo_produto", ""),
                "codigo_interno":    prod.get("codigo", ""),
                "descricao":         prod.get("descricao", ""),
                "unidade":           prod.get("unidade", ""),
                "quantidade":        float(prod.get("quantidade",     0) or 0),
                "valor_unitario":    float(prod.get("valor_unitario", 0) or 0),
                "valor_desconto":    float(prod.get("valor_desconto", 0) or 0),
                "valor_total_linha": float(prod.get("valor_total",    0) or 0),
            })

    df_ped = pd.DataFrame(pedidos)
    df_lin = pd.DataFrame(linhas)

    if not df_ped.empty:
        df_ped["data_pedido"]    = pd.to_datetime(df_ped["data_pedido"], format="%d/%m/%Y", errors="coerce")
        df_ped["valor_total"]    = pd.to_numeric(df_ped["valor_total"], errors="coerce")
        df_ped["codigo_cliente"] = pd.to_numeric(df_ped["codigo_cliente"], errors="coerce")

    if not df_lin.empty:
        df_lin["data_pedido"] = pd.to_datetime(df_lin["data_pedido"], format="%d/%m/%Y", errors="coerce")

    return df_ped, df_lin


# ── CATÁLOGO DE PRODUTOS ──────────────────────────────────────────────────────

def buscar_catalogo_produtos() -> pd.DataFrame:
    raw = _paginar("geral/produtos/", "ListarProdutos",
                   {"filtrar_apenas_omiepdv": "N"}, "produto_servico_cadastro")
    registros = []
    for p in raw:
        registros.append({
            "codigo_produto": p.get("codigo_produto"),
            "codigo_interno": p.get("codigo", ""),
            "descricao":      p.get("descricao", ""),
            "valor_venda":    float(p.get("valor_unitario", 0) or 0),
        })
    df = pd.DataFrame(registros)
    df["codigo_produto"] = pd.to_numeric(df["codigo_produto"], errors="coerce")
    return df


# ── AGREGAÇÕES DE PRODUTOS ────────────────────────────────────────────────────

def calcular_produtos(df_linhas: pd.DataFrame, df_cmc: pd.DataFrame) -> pd.DataFrame:
    if df_linhas.empty:
        return pd.DataFrame()

    resumo = (
        df_linhas.groupby(["codigo_produto", "descricao"])
        .agg(
            quantidade_vendida  = ("quantidade",        "sum"),
            receita_total       = ("valor_total_linha", "sum"),
            desconto_total      = ("valor_desconto",    "sum"),
            num_pedidos         = ("numero_pedido",     "nunique"),
            unidade             = ("unidade",           "first"),
        )
        .reset_index()
    )

    # Normalizar descrição para match com planilha
    resumo["descricao_norm"] = resumo["descricao"].str.strip().str.upper()

    if not df_cmc.empty:
        resumo = resumo.merge(
            df_cmc.rename(columns={"descricao_limpa": "descricao_norm"}),
            on="descricao_norm", how="left"
        )
        resumo["cmc_unitario"] = resumo["cmc_unitario"].fillna(0)
    else:
        resumo["cmc_unitario"] = 0.0

    resumo["custo_total"] = resumo["cmc_unitario"] * resumo["quantidade_vendida"]
    resumo["lucro_bruto"] = resumo["receita_total"] - resumo["custo_total"]

    def margem(row):
        if row["cmc_unitario"] > 0 and row["receita_total"] > 0:
            return round((row["lucro_bruto"] / row["receita_total"]) * 100, 1)
        return None

    resumo["margem_pct"]        = resumo.apply(margem, axis=1)
    resumo["preco_medio_venda"] = resumo["receita_total"] / resumo["quantidade_vendida"]

    return resumo.sort_values("quantidade_vendida", ascending=False).reset_index(drop=True)


# ── INDICADORES DE CLIENTES ───────────────────────────────────────────────────

def calcular_indicadores(df_pedidos: pd.DataFrame, df_clientes: pd.DataFrame) -> pd.DataFrame:
    hoje = pd.Timestamp.today().normalize()

    resumo = (
        df_pedidos.groupby("codigo_cliente")
        .agg(
            total_comprado  = ("valor_total", "sum"),
            num_pedidos     = ("numero_pedido", "count"),
            ultima_compra   = ("data_pedido", "max"),
            primeira_compra = ("data_pedido", "min"),
        )
        .reset_index()
    )
    resumo["dias_sem_comprar"] = (hoje - resumo["ultima_compra"]).dt.days
    resumo["ticket_medio"]     = resumo["total_comprado"] / resumo["num_pedidos"]

    df = df_clientes.merge(resumo, on="codigo_cliente", how="left")
    df["total_comprado"]   = df["total_comprado"].fillna(0)
    df["num_pedidos"]      = df["num_pedidos"].fillna(0).astype(int)
    df["ticket_medio"]     = df["ticket_medio"].fillna(0)
    df["dias_sem_comprar"] = df["dias_sem_comprar"].fillna(9999).astype(int)

    return df.sort_values("total_comprado", ascending=False).reset_index(drop=True)


# ── CONTAS A RECEBER (ABERTO + ATRASADO) ─────────────────────────────────────

def buscar_contas_receber() -> pd.DataFrame:
    """Retorna contas a receber em aberto e atrasadas (ignora RECEBIDO, PAGO e CANCELADO)."""
    raw = _paginar(
        "financas/contareceber/", "ListarContasReceber",
        {},
        "conta_receber_cadastro",
    )
    hoje = pd.Timestamp.today().normalize()
    registros = []
    for r in raw:
        status = r.get("status_titulo", "")
        if status in ("RECEBIDO", "PAGO", "CANCELADO"):
            continue
        dv = r.get("data_vencimento", "")
        try:
            dt_venc = pd.to_datetime(dv, format="%d/%m/%Y")
        except Exception:
            continue
        dp = r.get("data_previsao") or dv
        try:
            dt_prev = pd.to_datetime(dp, format="%d/%m/%Y")
        except Exception:
            dt_prev = dt_venc
        registros.append({
            "codigo_cliente":    r.get("codigo_cliente_fornecedor"),
            "numero_documento":  r.get("numero_documento", ""),
            "parcela":           r.get("numero_parcela", ""),
            "data_vencimento":   dt_prev,   # usa data_previsao (campo PREVISÃO do Omie)
            "dias_atraso":       (hoje - dt_venc).days if status == "ATRASADO" else 0,
            "valor":             float(r.get("valor_documento", 0) or 0),
            "status":            status,
            "codigo_lancamento": r.get("codigo_lancamento_omie"),
        })
    df = pd.DataFrame(registros)
    if not df.empty:
        df["codigo_cliente"] = pd.to_numeric(df["codigo_cliente"], errors="coerce")
        df = df.sort_values(["codigo_cliente", "data_vencimento"]).reset_index(drop=True)
    return df


# ── CONTAS A PAGAR ────────────────────────────────────────────────────────────

def buscar_contas_pagar() -> pd.DataFrame:
    raw = _paginar(
        "financas/contapagar/", "ListarContasPagar",
        {},
        "conta_pagar_cadastro",
    )
    registros = []
    for r in raw:
        status = r.get("status_titulo", "")
        if status in ("CANCELADO", "PAGO", "LIQUIDADO"):
            continue
        dv = r.get("data_vencimento", "")
        try:
            dt_venc = pd.to_datetime(dv, format="%d/%m/%Y")
        except Exception:
            continue
        dp = r.get("data_previsao") or dv
        try:
            dt_prev = pd.to_datetime(dp, format="%d/%m/%Y")
        except Exception:
            dt_prev = dt_venc
        nome = (
            r.get("nome_fornecedor")
            or r.get("razao_social")
            or str(r.get("codigo_cliente_fornecedor", ""))
        )
        registros.append({
            "codigo_fornecedor": r.get("codigo_cliente_fornecedor"),
            "nome_fornecedor":   nome,
            "numero_documento":  r.get("numero_documento", ""),
            "parcela":           r.get("numero_parcela", ""),
            "data_vencimento":   dt_prev,   # usa data_previsao (campo PREVISÃO do Omie)
            "valor":             float(r.get("valor_documento", 0) or 0),
            "status":            status,
        })
    df = pd.DataFrame(registros)
    if not df.empty:
        df = df.sort_values("data_vencimento").reset_index(drop=True)
    return df


# ── ENTRADA PRINCIPAL ─────────────────────────────────────────────────────────

def carregar_dados():
    """Retorna (df_pedidos, df_linhas, df_clientes, df_ind, df_prod, df_boletos, saldo_cash, df_pagar, df_receber)."""
    df_clientes           = buscar_clientes()
    df_pedidos, df_linhas = buscar_pedidos_e_linhas()
    df_cmc                = carregar_cmc_planilha()        # lê planilha sempre atualizada
    df_indicadores        = calcular_indicadores(df_pedidos, df_clientes)
    df_produtos           = calcular_produtos(df_linhas, df_cmc)
    df_todas_receber      = buscar_contas_receber()
    saldo_cash            = buscar_saldo_omie_cash()
    df_pagar              = buscar_contas_pagar()

    _empty = pd.DataFrame()
    df_boletos = df_todas_receber[df_todas_receber["status"] == "ATRASADO"].copy()    if not df_todas_receber.empty else _empty
    df_receber = df_todas_receber[df_todas_receber["status"] != "ATRASADO"].copy()   if not df_todas_receber.empty else _empty

    return df_pedidos, df_linhas, df_clientes, df_indicadores, df_produtos, df_boletos, saldo_cash, df_pagar, df_receber
