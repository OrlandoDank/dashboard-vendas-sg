from pathlib import Path
import pandas as pd

PLANILHA_COND = Path(__file__).parent.parent / "Condominios" / "condominios.xlsx"
PLANILHA_END  = Path(__file__).parent.parent / "CondominiosDash" / "Endereços.xlsx"


def carregar_enderecos() -> pd.DataFrame:
    """Lê Endereços.xlsx e retorna DataFrame com nome_norm → telefone."""
    df_raw = pd.read_excel(PLANILHA_END, header=None)
    header_row = next(i for i, row in df_raw.iterrows() if any("Telefone" in str(v) for v in row.values))
    df_raw.columns = df_raw.iloc[header_row]
    df = df_raw.iloc[header_row + 1:].copy().reset_index(drop=True)
    col_nome = next(c for c in df.columns if "Social" in str(c) or "Nome Completo" in str(c))
    col_tel  = next(c for c in df.columns if "Telefone" in str(c))
    df = df[[col_nome, col_tel]].copy()
    df.columns = ["nome", "telefone"]
    df = df.dropna(subset=["nome"])
    df["nome_norm"] = df["nome"].astype(str).str.strip().str.upper()
    df["telefone"]  = df["telefone"].astype(str).str.strip().replace("nan", "")
    return df[["nome_norm", "telefone"]].drop_duplicates("nome_norm")


def carregar_dados_condominios() -> pd.DataFrame:
    """Lê condominios.xlsx e retorna DataFrame limpo com todas as linhas de venda."""
    df = pd.read_excel(PLANILHA_COND, header=1)
    df.columns = [
        "data", "cliente", "produto", "tags",
        "quantidade", "cmc_unit", "preco_unit", "total_merc", "desconto",
    ]

    df["data"]    = pd.to_datetime(df["data"], errors="coerce").ffill()
    df["cliente"] = df["cliente"].ffill()

    df["condominio"] = (
        df["tags"]
        .str.extract(r"Cliente,\s*(.+)", expand=False)
        .str.strip()
        .fillna("Outros")
    )

    for col in ["quantidade", "cmc_unit", "preco_unit", "total_merc", "desconto"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["receita"] = df["total_merc"] - df["desconto"]
    df["custo"]   = df["cmc_unit"] * df["quantidade"]
    df["lucro"]   = df["receita"] - df["custo"]

    df = df[df["produto"].notna() & (df["produto"].astype(str).str.strip() != "")].copy()
    df["produto"] = df["produto"].astype(str).str.strip()
    df["cliente"] = df["cliente"].astype(str).str.strip()

    return df.reset_index(drop=True)


def agregar_clientes(df: pd.DataFrame) -> pd.DataFrame:
    hoje = pd.Timestamp.today().normalize()
    resumo = (
        df.groupby(["condominio", "cliente"])
        .agg(
            total_comprado=("receita",    "sum"),
            total_custo   =("custo",      "sum"),
            total_lucro   =("lucro",      "sum"),
            qtd_itens     =("quantidade", "sum"),
            ultima_compra =("data",       "max"),
        )
        .reset_index()
    )
    # Datas futuras (entregas pré-agendadas) não contam como "última compra"
    ultimas_passadas = (
        df[df["data"] <= hoje]
        .groupby(["condominio", "cliente"])["data"]
        .max()
        .rename("ultima_compra_real")
        .reset_index()
    )
    resumo = resumo.merge(ultimas_passadas, on=["condominio", "cliente"], how="left")
    # Clientes sem nenhuma compra passada ficam com ultima_compra = NaT e dias = 9999
    resumo["ultima_compra"] = resumo["ultima_compra_real"]
    resumo = resumo.drop(columns=["ultima_compra_real"])
    resumo["dias_sem_comprar"] = (hoje - resumo["ultima_compra"]).dt.days.fillna(9999).astype(int)
    resumo["margem_pct"] = (
        resumo["total_lucro"] / resumo["total_comprado"] * 100
    ).round(1)
    resumo.loc[resumo["total_comprado"] <= 0, "margem_pct"] = None

    # Merge telefone da planilha de endereços
    df_end = carregar_enderecos()
    resumo["nome_norm"] = resumo["cliente"].str.strip().str.upper()
    resumo = resumo.merge(df_end, on="nome_norm", how="left")
    resumo["telefone"] = resumo["telefone"].fillna("")
    resumo = resumo.drop(columns=["nome_norm"])

    return resumo.sort_values("total_comprado", ascending=False).reset_index(drop=True)


def agregar_produtos(df: pd.DataFrame) -> pd.DataFrame:
    resumo = (
        df.groupby(["condominio", "produto"])
        .agg(
            quantidade_vendida=("quantidade", "sum"),
            receita_total     =("receita",    "sum"),
            custo_total       =("custo",      "sum"),
            lucro_total       =("lucro",      "sum"),
            preco_medio       =("preco_unit", "mean"),
            cmc_medio         =("cmc_unit",   "mean"),
            num_clientes      =("cliente",    "nunique"),
        )
        .reset_index()
    )
    resumo["margem_pct"] = (resumo["lucro_total"] / resumo["receita_total"] * 100).round(1)
    resumo.loc[resumo["receita_total"] <= 0, "margem_pct"] = None
    return resumo.sort_values("quantidade_vendida", ascending=False).reset_index(drop=True)
