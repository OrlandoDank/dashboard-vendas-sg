import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from omie_api import carregar_dados

# ─────────────────────────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard de Vendas – SG Soluções",
    page_icon="📊",
    layout="wide",
)

st.markdown("""
<style>
  .kpi-card {
    background: #1e293b;
    border-radius: 10px;
    padding: 12px 16px;
    text-align: center;
    height: 100%;
  }
  .kpi-card .label  { color: #94a3b8; font-size: 12px; margin: 0; }
  .kpi-card .total  { color: #f1f5f9; font-size: 20px; font-weight: 700; margin: 4px 0 2px; }
  .kpi-card .mes    { color: #60a5fa; font-size: 13px; margin: 0; }
  .kpi-card .sub    { color: #64748b; font-size: 11px; margin: 0; }
  .status-bar { display:flex; gap:8px; margin-bottom: 4px; }
  .badge { border-radius:6px; padding: 4px 12px; font-size:13px; font-weight:600; }
  .verde    { background:#d4edda; color:#155724; }
  .amarelo  { background:#fff3cd; color:#856404; }
  .vermelho { background:#f8d7da; color:#721c24; }
  .cinza    { background:#e2e8f0; color:#475569; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# DADOS
# ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def get_dados():
    return carregar_dados()

col_title, col_btn = st.columns([5, 1])
with col_title:
    st.title("📊 Dashboard de Vendas – SG Soluções")
with col_btn:
    st.write("")
    if st.button("🔄 Atualizar", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

with st.spinner("Buscando dados do Omie..."):
    df_pedidos, df_linhas, df_clientes, df_ind, df_prod, df_boletos, saldo_cash = get_dados()

st.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}  |  Cache renova a cada 5 min")
st.divider()


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def brl(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def mes_atual(df, col_data, col_valor):
    hoje = pd.Timestamp.today()
    mask = (df[col_data].dt.year == hoje.year) & (df[col_data].dt.month == hoje.month)
    return df.loc[mask, col_valor].sum()

MES = datetime.now().strftime("%b/%Y")


# ─────────────────────────────────────────────────────────────
# LINHA 1 – KPIs COMPACTOS (total + mês na mesma caixinha)
# ─────────────────────────────────────────────────────────────
fat_total = df_pedidos["valor_total"].sum()
fat_mes   = mes_atual(df_pedidos, "data_pedido", "valor_total")

ped_total = len(df_pedidos)
ped_mes   = int(df_pedidos[
    (df_pedidos["data_pedido"].dt.year  == datetime.now().year) &
    (df_pedidos["data_pedido"].dt.month == datetime.now().month)
].shape[0])

ticket_total = fat_total / ped_total if ped_total else 0
ticket_mes   = fat_mes   / ped_mes   if ped_mes   else 0

cli_ativos   = int((df_ind["num_pedidos"] > 0).sum())
cli_verdes   = int(((df_ind["num_pedidos"] > 0) & (df_ind["dias_sem_comprar"] <  30)).sum())
cli_amarelos = int(((df_ind["num_pedidos"] > 0) & (df_ind["dias_sem_comprar"].between(30, 60))).sum())
cli_vermelhos= int(((df_ind["num_pedidos"] > 0) & (df_ind["dias_sem_comprar"] >  60)).sum())
cli_nunca    = int((df_ind["num_pedidos"] == 0).sum())

c1, c2, c3, c4, c5, c6 = st.columns(6)

def card(col, icon, label, total_val, mes_val, sub=""):
    col.markdown(f"""
    <div class="kpi-card">
      <p class="label">{icon} {label}</p>
      <p class="total">{total_val}</p>
      <p class="mes">📅 {MES}: {mes_val}</p>
      {'<p class="sub">' + sub + '</p>' if sub else ''}
    </div>
    """, unsafe_allow_html=True)

card(c1, "💰", "Total Faturado",  brl(fat_total),        brl(fat_mes))
card(c2, "📦", "Pedidos",         str(ped_total),        str(ped_mes))
card(c3, "🎯", "Ticket Médio",    brl(ticket_total),     brl(ticket_mes))
card(c4, "👥", "Clientes Ativos", str(cli_ativos),       f"{cli_verdes} ativos hoje", sub="com ao menos 1 compra")
card(c5, "⚠️", "Retenção",
     f"🟢 {cli_verdes}  🟡 {cli_amarelos}  🔴 {cli_vermelhos}",
     f"⚪ {cli_nunca} nunca compraram",
     sub="verde <30d · amarelo 30-60d · vermelho >60d")
c6.markdown(f"""
<div class="kpi-card" style="border: 1px solid #22c55e;">
  <p class="label">🏦 Omie.CASH</p>
  <p class="total" style="color:#4ade80;">{brl(saldo_cash)}</p>
  <p class="mes">Saldo disponível</p>
</div>
""", unsafe_allow_html=True)

st.write("")
st.divider()


# ─────────────────────────────────────────────────────────────
# BOLETOS EM ATRASO
# ─────────────────────────────────────────────────────────────
st.subheader("🔴 Boletos em atraso")

if df_boletos.empty:
    st.success("Nenhum boleto em atraso no momento.")
else:
    # Juntar nome do cliente
    df_bol = df_boletos.merge(
        df_clientes[["codigo_cliente", "nome_cliente"]],
        on="codigo_cliente", how="left"
    )

    total_atraso    = df_bol["valor"].sum()
    qtd_boletos     = len(df_bol)
    qtd_clientes    = df_bol["codigo_cliente"].nunique()

    ba1, ba2, ba3 = st.columns(3)
    ba1.metric("💸 Total em atraso",   brl(total_atraso))
    ba2.metric("📄 Boletos vencidos",  str(qtd_boletos))
    ba3.metric("👤 Clientes devedores", str(qtd_clientes))

    st.write("")

    # Formatar tabela
    df_bol_exib = df_bol[[
        "nome_cliente", "numero_documento", "parcela",
        "data_vencimento", "dias_atraso", "valor"
    ]].copy()
    df_bol_exib.columns = [
        "Cliente", "Nº Documento", "Parcela",
        "Vencimento", "Dias em Atraso", "Valor (R$)"
    ]
    df_bol_exib["Vencimento"]  = df_bol_exib["Vencimento"].dt.strftime("%d/%m/%Y")
    df_bol_exib["Valor (R$)"]  = df_bol_exib["Valor (R$)"].apply(brl)

    def colorir_atraso(row):
        d = row["Dias em Atraso"]
        cor = "#d4edda" if d < 30 else "#fff3cd" if d <= 60 else "#f8d7da"
        return [
            f"background-color:{cor}" if col in ("Dias em Atraso", "Vencimento") else ""
            for col in row.index
        ]

    st.dataframe(
        df_bol_exib.style.apply(colorir_atraso, axis=1),
        use_container_width=True, hide_index=True, height=400
    )
    st.caption(
        f"{qtd_boletos} boletos vencidos · {qtd_clientes} clientes · "
        f"Total: {brl(total_atraso)}  |  "
        "🟢 <30 dias  🟡 30–60 dias  🔴 >60 dias"
    )

st.divider()


# ─────────────────────────────────────────────────────────────
# GRÁFICOS
# ─────────────────────────────────────────────────────────────
g1, g2 = st.columns(2)

with g1:
    st.subheader("📈 Faturamento por mês")
    if not df_pedidos.empty:
        df_mes = (
            df_pedidos.dropna(subset=["data_pedido"])
            .assign(mes=lambda x: x["data_pedido"].dt.to_period("M").astype(str))
            .groupby("mes")["valor_total"].sum()
            .reset_index()
        )
        fig = px.bar(df_mes, x="mes", y="valor_total",
                     labels={"mes": "Mês", "valor_total": "Faturamento (R$)"},
                     color_discrete_sequence=["#3b82f6"], text_auto=".2s")
        fig.update_layout(margin=dict(t=10, b=10), height=300)
        st.plotly_chart(fig, use_container_width=True)

with g2:
    st.subheader("🏆 Top 10 clientes por valor")
    top10 = df_ind[df_ind["total_comprado"] > 0].head(10).copy()
    top10["nome_curto"] = top10["nome_cliente"].str[:28]
    fig2 = px.bar(
        top10.sort_values("total_comprado"),
        x="total_comprado", y="nome_curto", orientation="h",
        color="total_comprado", color_continuous_scale="Blues",
        labels={"total_comprado": "Total (R$)", "nome_curto": ""},
        text_auto=".2s",
    )
    fig2.update_layout(margin=dict(t=10, b=10), height=300, coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()


# ─────────────────────────────────────────────────────────────
# PRODUTOS MAIS VENDIDOS
# ─────────────────────────────────────────────────────────────
st.subheader("📦 Produtos mais vendidos")

if not df_prod.empty:
    p1, p2 = st.columns(2)

    with p1:
        top_qtd = df_prod.head(10).copy()
        top_qtd["desc_curta"] = top_qtd["descricao"].str[:30]
        fig_p = px.bar(
            top_qtd.sort_values("quantidade_vendida"),
            x="quantidade_vendida", y="desc_curta", orientation="h",
            color="quantidade_vendida", color_continuous_scale="Greens",
            labels={"quantidade_vendida": "Qtd vendida", "desc_curta": ""},
            text_auto=True,
        )
        fig_p.update_layout(title="Top 10 por quantidade", margin=dict(t=30, b=10),
                            height=300, coloraxis_showscale=False)
        st.plotly_chart(fig_p, use_container_width=True)

    with p2:
        top_rec = df_prod.sort_values("receita_total", ascending=False).head(10).copy()
        top_rec["desc_curta"] = top_rec["descricao"].str[:30]
        fig_r = px.bar(
            top_rec.sort_values("receita_total"),
            x="receita_total", y="desc_curta", orientation="h",
            color="receita_total", color_continuous_scale="Blues",
            labels={"receita_total": "Receita (R$)", "desc_curta": ""},
            text_auto=".2s",
        )
        fig_r.update_layout(title="Top 10 por receita", margin=dict(t=30, b=10),
                            height=300, coloraxis_showscale=False)
        st.plotly_chart(fig_r, use_container_width=True)

    # Tabela completa de produtos com margem
    st.markdown("##### Todos os produtos – quantidade · receita · margem")

    tem_custo = df_prod["margem_pct"].notna().any()
    if not tem_custo:
        st.info("💡 **Margem indisponível:** cadastre o preço de custo dos produtos no Omie "
                "(Cadastros → Produtos → campo Custo) para habilitar esta coluna automaticamente.")

    ord_prod = st.radio("Ordenar por:", ["Qtd vendida", "Receita", "Margem %"],
                        horizontal=True, key="ord_prod")

    df_prod_exib = df_prod.copy()
    if ord_prod == "Qtd vendida":
        df_prod_exib = df_prod_exib.sort_values("quantidade_vendida", ascending=False)
    elif ord_prod == "Receita":
        df_prod_exib = df_prod_exib.sort_values("receita_total", ascending=False)
    else:
        df_prod_exib = df_prod_exib.sort_values("margem_pct", ascending=False)

    def fmt_prod(df):
        out = df[[
            "descricao", "unidade", "quantidade_vendida",
            "preco_medio_venda", "receita_total", "num_pedidos",
            "cmc_unitario", "margem_pct"
        ]].copy()
        out.columns = [
            "Produto", "Un.", "Qtd Vendida",
            "Preço Médio (R$)", "Receita Total (R$)", "Nº Pedidos",
            "Custo Unit. (R$)", "Margem %"
        ]
        out["Preço Médio (R$)"]   = out["Preço Médio (R$)"].apply(brl)
        out["Receita Total (R$)"] = out["Receita Total (R$)"].apply(brl)
        out["Custo Unit. (R$)"]   = out["Custo Unit. (R$)"].apply(
            lambda v: brl(v) if v > 0 else "—")
        out["Margem %"] = out["Margem %"].apply(
            lambda v: f"{v:.1f}%" if pd.notna(v) else "—")
        return out

    def colorir_margem(row):
        m = row["Margem %"]
        if m == "—":
            cor = ""
        else:
            val = float(m.replace("%",""))
            cor = "#d4edda" if val >= 30 else "#fff3cd" if val >= 10 else "#f8d7da"
        return [f"background-color:{cor}" if col == "Margem %" else "" for col in row.index]

    df_fmt = fmt_prod(df_prod_exib)
    st.dataframe(
        df_fmt.style.apply(colorir_margem, axis=1),
        use_container_width=True, hide_index=True, height=420
    )
    st.caption(f"Total: {len(df_prod)} produtos diferentes vendidos")

st.divider()


# ─────────────────────────────────────────────────────────────
# TODOS OS CLIENTES
# ─────────────────────────────────────────────────────────────
st.subheader("👥 Todos os clientes")

fc1, fc2, fc3, fc4 = st.columns([3, 2, 2, 2])
with fc1:
    busca = st.text_input("🔍 Buscar cliente", placeholder="Digite o nome...")
with fc2:
    status_filtro = st.selectbox("Status", [
        "Todos", "🟢 Ativos (<30d)", "🟡 Atenção (30–60d)",
        "🔴 Inativos (>60d)", "⚪ Nunca compraram"])
with fc3:
    ordenar_por = st.selectbox("Ordenar por", [
        "Total comprado", "Dias sem comprar", "Nº pedidos", "Nome"])
with fc4:
    top_n = st.selectbox("Mostrar", ["Todos", "Top 10", "Top 20", "Top 50"])

df_tab = df_ind.copy()
if busca:
    df_tab = df_tab[df_tab["nome_cliente"].str.contains(busca, case=False, na=False)]
if status_filtro == "🟢 Ativos (<30d)":
    df_tab = df_tab[(df_tab["num_pedidos"] > 0) & (df_tab["dias_sem_comprar"] < 30)]
elif status_filtro == "🟡 Atenção (30–60d)":
    df_tab = df_tab[(df_tab["num_pedidos"] > 0) & (df_tab["dias_sem_comprar"].between(30, 60))]
elif status_filtro == "🔴 Inativos (>60d)":
    df_tab = df_tab[(df_tab["num_pedidos"] > 0) & (df_tab["dias_sem_comprar"] > 60)]
elif status_filtro == "⚪ Nunca compraram":
    df_tab = df_tab[df_tab["num_pedidos"] == 0]

ordem_map = {
    "Total comprado":   ("total_comprado",    False),
    "Dias sem comprar": ("dias_sem_comprar",   True),
    "Nº pedidos":       ("num_pedidos",        False),
    "Nome":             ("nome_cliente",       True),
}
col_ord, asc_ord = ordem_map[ordenar_por]
df_tab = df_tab.sort_values(col_ord, ascending=asc_ord)
if top_n != "Todos":
    df_tab = df_tab.head(int(top_n.replace("Top ", "")))


def formatar_clientes(df):
    out = df[[
        "nome_cliente", "cidade", "estado",
        "total_comprado", "num_pedidos", "ticket_medio",
        "ultima_compra", "dias_sem_comprar",
    ]].copy()
    out.columns = [
        "Cliente", "Cidade", "Estado",
        "Total Comprado (R$)", "Nº Pedidos", "Ticket Médio (R$)",
        "Última Compra", "Dias sem comprar",
    ]
    out["Total Comprado (R$)"] = out["Total Comprado (R$)"].apply(
        lambda v: brl(v) if v > 0 else "—")
    out["Ticket Médio (R$)"] = out["Ticket Médio (R$)"].apply(
        lambda v: brl(v) if v > 0 else "—")
    out["Última Compra"] = pd.to_datetime(out["Última Compra"]).dt.strftime("%d/%m/%Y").fillna("—")
    out["Dias sem comprar"] = out["Dias sem comprar"].apply(
        lambda d: "—" if d == 9999 else str(d))
    return out


def colorir_cliente(row):
    d = row["Dias sem comprar"]
    if d == "—":
        cor = "#f0f0f0"
    else:
        dias = int(d)
        cor  = "#d4edda" if dias < 30 else "#fff3cd" if dias <= 60 else "#f8d7da"
    return [
        f"background-color:{cor}" if col in ("Dias sem comprar", "Última Compra") else ""
        for col in row.index
    ]


df_cli_fmt = formatar_clientes(df_tab)
st.dataframe(
    df_cli_fmt.style.apply(colorir_cliente, axis=1),
    use_container_width=True, hide_index=True, height=500
)
st.caption(f"Exibindo {len(df_tab)} clientes")

st.divider()


# ─────────────────────────────────────────────────────────────
# PEDIDOS RECENTES
# ─────────────────────────────────────────────────────────────
st.subheader("📋 Pedidos recentes")

df_ped_exib = (
    df_pedidos
    .merge(df_clientes[["codigo_cliente", "nome_cliente"]], on="codigo_cliente", how="left")
    .sort_values("data_pedido", ascending=False)
    .head(50)
)[["numero_pedido", "data_pedido", "nome_cliente", "valor_total", "quantidade_itens", "etapa"]].copy()

df_ped_exib.columns = ["Nº Pedido", "Data", "Cliente", "Valor (R$)", "Itens", "Etapa"]
df_ped_exib["Data"]       = pd.to_datetime(df_ped_exib["Data"]).dt.strftime("%d/%m/%Y")
df_ped_exib["Valor (R$)"] = df_ped_exib["Valor (R$)"].apply(brl)
etapa_map = {"10":"Novo","20":"Em análise","30":"Aprovado","40":"Em produção",
             "50":"Pronto","60":"Enviado","70":"Entregue"}
df_ped_exib["Etapa"] = df_ped_exib["Etapa"].map(etapa_map).fillna(df_ped_exib["Etapa"])

st.dataframe(df_ped_exib, use_container_width=True, hide_index=True, height=400)

st.divider()
st.caption("Dados em tempo real via API Omie · Cache 5 min · Clique em 🔄 para forçar atualização")
