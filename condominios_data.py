from pathlib import Path
import pandas as pd

PLANILHA_COND      = Path(__file__).parent.parent / "Condominios" / "condominios.xlsx"
PLANILHA_END       = Path(__file__).parent.parent / "CondominiosDash" / "Endereços.xlsx"
PLANILHA_ABC       = Path(__file__).parent.parent / "CondominiosDash" / "Curva ABC quantidade.xlsx"
PLANILHA_ABC_VALOR = Path(__file__).parent.parent / "CondominiosDash" / "Curva ABC valor.xlsx"


def carregar_curva_abc() -> pd.DataFrame:
    """Lê curva ABC quantidade.xlsx e retorna descricao_norm → curva_abc, quantidade_abc."""
    df_raw = pd.read_excel(PLANILHA_ABC, header=None)
    header_row = next(i for i, row in df_raw.iterrows() if any("Ordem" in str(v) for v in row.values))
    df_raw.columns = df_raw.iloc[header_row]
    df = df_raw.iloc[header_row + 1:].copy().reset_index(drop=True)
    df = df[df["Ordem"].notna() & df["Descrição (completa)"].notna()].copy()
    df["curva_abc"] = df["ABC"].ffill().str.extract(r"^([ABC])", expand=False)
    df["quantidade_abc"] = pd.to_numeric(df["Quantidade Faturada"], errors="coerce").fillna(0)
    df["descricao_norm"] = (
        df["Descrição (completa)"]
        .astype(str)
        .str.extract(r"^\S+\s*-\s*(.+)$", expand=False)
        .fillna(df["Descrição (completa)"].astype(str))
        .str.strip().str.upper()
    )
    return df[["descricao_norm", "curva_abc", "quantidade_abc"]].drop_duplicates("descricao_norm")


def carregar_curva_abc_valor() -> pd.DataFrame:
    """Lê Curva ABC valor.xlsx e retorna descricao_norm → curva_abc_valor, valor_abc."""
    df_raw = pd.read_excel(PLANILHA_ABC_VALOR, header=None)
    header_row = next(i for i, row in df_raw.iterrows() if any("Ordem" in str(v) for v in row.values))
    df_raw.columns = df_raw.iloc[header_row]
    df = df_raw.iloc[header_row + 1:].copy().reset_index(drop=True)
    df = df[df["Ordem"].notna() & df["Descrição (completa)"].notna()].copy()
    df["curva_abc_valor"] = df["ABC"].ffill().str.extract(r"^([ABC])", expand=False)
    col_valor = next(c for c in df.columns if "Valor" in str(c) or "Faturamento" in str(c) or "Receita" in str(c))
    df["valor_abc"] = pd.to_numeric(df[col_valor], errors="coerce").fillna(0)
    df["descricao_norm"] = (
        df["Descrição (completa)"]
        .astype(str)
        .str.extract(r"^\S+\s*-\s*(.+)$", expand=False)
        .fillna(df["Descrição (completa)"].astype(str))
        .str.strip().str.upper()
    )
    return df[["descricao_norm", "curva_abc_valor", "valor_abc"]].drop_duplicates("descricao_norm")


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

    resumo["descricao_norm"] = resumo["produto"].str.strip().str.upper()

    df_abc = carregar_curva_abc()
    resumo = resumo.merge(df_abc, on="descricao_norm", how="left")
    resumo["curva_abc"]      = resumo["curva_abc"].fillna("—")
    resumo["quantidade_abc"] = resumo["quantidade_abc"].fillna(0)

    df_abc_val = carregar_curva_abc_valor()
    resumo = resumo.merge(df_abc_val, on="descricao_norm", how="left")
    resumo["curva_abc_valor"] = resumo["curva_abc_valor"].fillna("—")
    resumo["valor_abc"]       = resumo["valor_abc"].fillna(0)

    resumo = resumo.drop(columns=["descricao_norm"])

    return resumo.sort_values("quantidade_vendida", ascending=False).reset_index(drop=True)
