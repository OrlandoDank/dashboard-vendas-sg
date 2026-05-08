import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path
import base64
from condominios_data import carregar_dados_condominios, agregar_clientes, agregar_produtos

# ─────────────────────────────────────────────────────────────
# LOGO
# ─────────────────────────────────────────────────────────────
def _logo_b64() -> str:
    p = Path(__file__).parent / "logo.jpg"
    if p.exists():
        return base64.b64encode(p.read_bytes()).decode()
    return ""

_LOGO = _logo_b64()

# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Condomínios",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# CSS GLOBAL
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stAppViewContainer"] { background: #f0f4f8; }
  [data-testid="stHeader"]           { background: transparent; }
  [data-testid="stSidebar"]          { background: #1a1f36; }
  [data-testid="stSidebar"] * { color: #c8ccd8 !important; }
  [data-testid="stSidebar"] .stRadio label { color: #c8ccd8 !important; font-size: 15px; }

  .kpi {
    background: white; border-radius: 14px; padding: 18px 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    display: flex; align-items: center; gap: 16px; margin-bottom: 4px;
  }
  .kpi-icon { width:52px; height:52px; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:22px; flex-shrink:0; }
  .kpi-body { flex:1; min-width:0; }
  .kpi-label { color:#8892a4; font-size:12px; margin:0; font-weight:500; text-transform:uppercase; letter-spacing:.5px; }
  .kpi-value { color:#1a1f36; font-size:21px; font-weight:700; margin:2px 0 0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .kpi-sub   { color:#56c4a8; font-size:12px; margin:2px 0 0; }

  .card { background:white; border-radius:14px; padding:20px; box-shadow:0 2px 12px rgba(0,0,0,0.07); margin-bottom:16px; }
  .card-title { color:#1a1f36; font-size:15px; font-weight:600; margin:0 0 16px; }

  .page-header { margin-bottom:24px; }
  .page-header h2 { color:#1a1f36; font-size:22px; font-weight:700; margin:0; }
  .page-header p  { color:#8892a4; font-size:13px; margin:4px 0 0; }

  @media (max-width:768px) {
    .kpi-value { font-size:17px; }
    [data-testid="column"] { width:100% !important; flex:1 1 100% !important; min-width:100% !important; }
    .block-container { padding-left:1rem !important; padding-right:1rem !important; }
  }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def brl(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def kpi_card(icon, bg, label, value, sub=""):
    return f"""
    <div class="kpi">
      <div class="kpi-icon" style="background:{bg};">{icon}</div>
      <div class="kpi-body">
        <p class="kpi-label">{label}</p>
        <p class="kpi-value">{value}</p>
        {"<p class='kpi-sub'>"+sub+"</p>" if sub else ""}
      </div>
    </div>"""

def bar_h(df, x, y, cor, title, text_fmt=None):
    kw = dict(text_auto=text_fmt) if text_fmt else dict(text_auto=True)
    fig = px.bar(df.sort_values(x), x=x, y=y, orientation="h",
                 color_discrete_sequence=[cor], **kw)
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        height=max(240, len(df) * 28),
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="#f0f4f8", title=""),
        yaxis=dict(title=""),
    )
    return fig

COND_CORES = {
    "Flexaccanto":      "#00b4d8",
    "Cosenza":          "#06d6a0",
    "Fit Marumbi":      "#ffd166",
    "Castellamare":     "#ef476f",
    "Cambirella":       "#a78bfa",
    "Helbor Visionist": "#fb8500",
    "Outros":           "#8892a4",
}
MES = datetime.now().strftime("%b/%Y")


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    if _LOGO:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:4px;">
          <img src="data:image/jpeg;base64,{_LOGO}"
               style="width:48px;height:48px;object-fit:contain;border-radius:10px;background:white;padding:3px;flex-shrink:0;">
          <div>
            <p style="color:white;font-size:17px;font-weight:700;margin:0;line-height:1.2;">SG Bichos</p>
            <p style="color:#8892a4;font-size:11px;margin:0;">Condomínios</p>
          </div>
        </div>
        <div style="margin-bottom:20px;"></div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='color:white;font-size:18px;margin-bottom:4px;'>SG Bichos</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#666;font-size:12px;margin-bottom:24px;'>Condomínios</p>", unsafe_allow_html=True)

    pagina = st.radio("Navegação", [
        "🏠  Visão Geral",
        "🏢  Por Condomínio",
        "👥  Clientes",
        "📦  Produtos",
    ], label_visibility="collapsed")

    st.markdown("---")
    if st.button("🔄 Atualizar dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown(
        f"<p style='color:#555;font-size:11px;margin-top:8px;'>Atualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<p style='color:#555;font-size:11px;'>Cache: 5 min</p>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# DADOS
# ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def get_dados():
    df      = carregar_dados_condominios()
    df_cli  = agregar_clientes(df)
    df_prod = agregar_produtos(df)
    return df, df_cli, df_prod

with st.spinner("Carregando dados da planilha..."):
    df_raw, df_cli, df_prod = get_dados()

fat_total   = df_raw["receita"].sum()
lucro_total = df_raw["lucro"].sum()
margem_geral = (lucro_total / fat_total * 100) if fat_total > 0 else 0
n_clientes  = df_raw["cliente"].nunique()

condominios = sorted([c for c in df_raw["condominio"].unique() if c != "Outros"])


# ═══════════════════════════════════════════════════════════════
# PÁGINA: VISÃO GERAL
# ═══════════════════════════════════════════════════════════════
if pagina == "🏠  Visão Geral":
    st.markdown("""<div class="page-header">
      <h2>Visão Geral</h2>
      <p>Resumo consolidado de vendas por condomínio · Todos os períodos</p>
    </div>""", unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi_card("💰", "#e8f8ff", "Total Faturado",  brl(fat_total)), unsafe_allow_html=True)
    k2.markdown(kpi_card("📊", "#e8fff5", "Margem Geral",    f"{margem_geral:.1f}%", f"Lucro: {brl(lucro_total)}"), unsafe_allow_html=True)
    k3.markdown(kpi_card("👥", "#fff8e8", "Clientes Únicos", str(n_clientes)), unsafe_allow_html=True)
    k4.markdown(kpi_card("🏢", "#eef2ff", "Condomínios",     str(len(condominios))), unsafe_allow_html=True)

    st.write("")

    # Faturamento por condomínio (barras) + donut de distribuição
    g1, g2 = st.columns([3, 2])

    df_cond = (
        df_raw[df_raw["condominio"] != "Outros"]
        .groupby("condominio")
        .agg(faturamento=("receita", "sum"), clientes=("cliente", "nunique"))
        .sort_values("faturamento", ascending=False)
        .reset_index()
    )

    with g1:
        st.markdown('<div class="card"><p class="card-title">📊 Faturamento por Condomínio</p>', unsafe_allow_html=True)
        fig = px.bar(
            df_cond.sort_values("faturamento"), x="faturamento", y="condominio",
            orientation="h", text_auto=".2s",
            color="condominio", color_discrete_map=COND_CORES,
        )
        fig.update_layout(
            margin=dict(t=0, b=0, l=0, r=0), height=280,
            plot_bgcolor="white", paper_bgcolor="white", showlegend=False,
            xaxis=dict(showgrid=True, gridcolor="#f0f4f8", title="R$"),
            yaxis=dict(title=""),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with g2:
        st.markdown('<div class="card"><p class="card-title">🥧 Distribuição de Faturamento</p>', unsafe_allow_html=True)
        fig2 = go.Figure(go.Pie(
            labels=df_cond["condominio"],
            values=df_cond["faturamento"],
            hole=0.6,
            marker_colors=[COND_CORES.get(c, "#8892a4") for c in df_cond["condominio"]],
            textinfo="percent",
            textfont_size=11,
        ))
        fig2.update_layout(
            margin=dict(t=0, b=0, l=0, r=0), height=280,
            paper_bgcolor="white",
            legend=dict(orientation="h", yanchor="bottom", y=-0.35, font=dict(size=10)),
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Faturamento mensal por condomínio (área empilhada)
    st.markdown('<div class="card"><p class="card-title">📈 Faturamento Mensal por Condomínio</p>', unsafe_allow_html=True)
    df_mes = (
        df_raw[df_raw["condominio"] != "Outros"]
        .assign(mes=lambda x: x["data"].dt.to_period("M").astype(str))
        .groupby(["mes", "condominio"])["receita"].sum().reset_index()
    )
    fig3 = px.area(
        df_mes, x="mes", y="receita", color="condominio",
        color_discrete_map=COND_CORES,
        labels={"receita": "Faturamento (R$)", "mes": "Mês", "condominio": "Condomínio"},
    )
    fig3.update_layout(
        margin=dict(t=10, b=0, l=0, r=0), height=260,
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#f0f4f8"),
        legend=dict(orientation="h", yanchor="bottom", y=1.01),
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Top 10 clientes e top 10 produtos (global)
    t1, t2 = st.columns(2)

    with t1:
        st.markdown('<div class="card"><p class="card-title">🏆 Top 10 Clientes (Global)</p>', unsafe_allow_html=True)
        top_cli = (
            df_cli[df_cli["condominio"] != "Outros"]
            .groupby("cliente")["total_comprado"].sum()
            .sort_values(ascending=False).head(10).reset_index()
        )
        top_cli["nome"] = top_cli["cliente"].str[:30]
        st.plotly_chart(
            bar_h(top_cli, "total_comprado", "nome", "#00b4d8", "Top clientes", ".2s"),
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with t2:
        st.markdown('<div class="card"><p class="card-title">📦 Top 10 Produtos (Global)</p>', unsafe_allow_html=True)
        top_prod = (
            df_prod[df_prod["condominio"] != "Outros"]
            .groupby("produto")["quantidade_vendida"].sum()
            .sort_values(ascending=False).head(10).reset_index()
        )
        top_prod["desc"] = top_prod["produto"].str[:30]
        st.plotly_chart(
            bar_h(top_prod, "quantidade_vendida", "desc", "#06d6a0", "Top produtos"),
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# PÁGINA: POR CONDOMÍNIO
# ═══════════════════════════════════════════════════════════════
elif pagina == "🏢  Por Condomínio":
    cond_sel = st.selectbox("Selecionar Condomínio", condominios, key="sel_cond")
    cor_cond = COND_CORES.get(cond_sel, "#00b4d8")

    df_c  = df_raw[df_raw["condominio"] == cond_sel]
    df_cl = df_cli[df_cli["condominio"] == cond_sel].sort_values("total_comprado", ascending=False)
    df_pr = df_prod[df_prod["condominio"] == cond_sel]

    fat_c    = df_c["receita"].sum()
    lucro_c  = df_c["lucro"].sum()
    margem_c = (lucro_c / fat_c * 100) if fat_c > 0 else 0

    st.markdown(f"""<div class="page-header">
      <h2>🏢 {cond_sel}</h2>
      <p>Análise detalhada do condomínio · Todos os períodos</p>
    </div>""", unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi_card("💰", "#e8f8ff", "Total Faturado", brl(fat_c)), unsafe_allow_html=True)
    k2.markdown(kpi_card("📊", "#e8fff5", "Margem",        f"{margem_c:.1f}%", f"Lucro: {brl(lucro_c)}"), unsafe_allow_html=True)
    k3.markdown(kpi_card("👥", "#fff8e8", "Clientes",      str(df_c["cliente"].nunique())), unsafe_allow_html=True)
    k4.markdown(kpi_card("📦", "#eef2ff", "Produtos",      str(df_c["produto"].nunique())), unsafe_allow_html=True)

    st.write("")

    # ── Quem compra mais (do maior para menor) ─────────────────
    st.markdown('<div class="card"><p class="card-title">🏆 Clientes — do maior para o menor comprador</p>', unsafe_allow_html=True)
    top_cl = df_cl.head(20).copy()

    def _badge_dias(d):
        cor = "#e8fff5;color:#06d6a0" if d < 30 else "#fff8e8;color:#ffc107" if d <= 60 else "#ffeef2;color:#ef476f"
        return f'<span style="background:{cor.split(";")[0]};color:{cor.split(";")[1]};border-radius:5px;padding:2px 8px;font-size:12px;font-weight:600;">{d}d</span>'

    top_cl["nome_dias"] = top_cl["cliente"].str[:35] + "  " + top_cl["dias_sem_comprar"].astype(str) + "d"
    fig = px.bar(
        top_cl.sort_values("total_comprado"), x="total_comprado", y="nome_dias",
        orientation="h", color_discrete_sequence=[cor_cond], text_auto=".2s",
    )
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0), height=max(260, len(top_cl) * 30),
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="#f0f4f8", title="Total comprado (R$)"),
        yaxis=dict(title=""),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("🟢 <30d sem comprar  🟡 30–60d  🔴 >60d")
    st.markdown("</div>", unsafe_allow_html=True)

    p1, p2 = st.columns(2)

    with p1:
        # ── Qual produto vende mais (do maior para menor) ───────
        st.markdown('<div class="card"><p class="card-title">📦 Produtos — mais vendidos (quantidade)</p>', unsafe_allow_html=True)
        top_pq = df_pr.sort_values("quantidade_vendida", ascending=False).head(15).copy()
        top_pq["desc"] = top_pq["produto"].str[:30]
        fig2 = px.bar(
            top_pq.sort_values("quantidade_vendida"), x="quantidade_vendida", y="desc",
            orientation="h", color_discrete_sequence=["#06d6a0"], text_auto=True,
        )
        fig2.update_layout(
            margin=dict(t=0, b=0, l=0, r=0), height=max(260, len(top_pq) * 30),
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(showgrid=True, gridcolor="#f0f4f8", title="Quantidade"),
            yaxis=dict(title=""),
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with p2:
        # ── Qual produto tem melhor margem (do maior para menor) ─
        st.markdown('<div class="card"><p class="card-title">📊 Produtos — melhor margem</p>', unsafe_allow_html=True)
        top_pm = (
            df_pr[df_pr["margem_pct"].notna()]
            .sort_values("margem_pct", ascending=False)
            .head(15)
            .copy()
        )
        top_pm["desc"] = top_pm["produto"].str[:30]
        top_pm_plot = top_pm.sort_values("margem_pct")

        fig3 = px.bar(
            top_pm_plot, x="margem_pct", y="desc",
            orientation="h",
            color="margem_pct",
            color_continuous_scale=[
                [0.0,   "#ef476f"],
                [0.333, "#ffd166"],
                [0.666, "#06d6a0"],
                [1.0,   "#06d6a0"],
            ],
            text=top_pm_plot["margem_pct"].apply(lambda v: f"{v:.1f}%"),
        )
        fig3.update_layout(
            margin=dict(t=0, b=0, l=0, r=0), height=max(260, len(top_pm) * 30),
            plot_bgcolor="white", paper_bgcolor="white",
            coloraxis_showscale=False,
            xaxis=dict(showgrid=True, gridcolor="#f0f4f8", title="Margem (%)"),
            yaxis=dict(title=""),
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# PÁGINA: CLIENTES
# ═══════════════════════════════════════════════════════════════
elif pagina == "👥  Clientes":
    st.markdown('<div class="page-header"><h2>Clientes</h2><p>Ranking de compras por cliente e condomínio</p></div>', unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns([2, 2, 2])
    with fc1: busca     = st.text_input("🔍 Buscar cliente", placeholder="Nome...")
    with fc2: cond_f    = st.selectbox("Condomínio", ["Todos"] + condominios)
    with fc3: ordem_cli = st.selectbox("Ordenar por", ["Total comprado", "Dias s/ comprar", "Margem %", "Nome"])

    df_tab = df_cli[df_cli["condominio"] != "Outros"].copy()
    if busca:
        df_tab = df_tab[df_tab["cliente"].str.contains(busca, case=False, na=False)]
    if cond_f != "Todos":
        df_tab = df_tab[df_tab["condominio"] == cond_f]

    mapa_c = {
        "Total comprado":   ("total_comprado",   False),
        "Dias s/ comprar":  ("dias_sem_comprar", True),
        "Margem %":         ("margem_pct",       False),
        "Nome":             ("cliente",          True),
    }
    col_c, asc_c = mapa_c[ordem_cli]
    df_tab = df_tab.sort_values(col_c, ascending=asc_c)

    def fmt_cli(df):
        out = df[[
            "cliente", "condominio", "total_comprado", "total_custo",
            "total_lucro", "qtd_itens", "ultima_compra", "dias_sem_comprar", "margem_pct",
        ]].copy()
        out.columns = [
            "Cliente", "Condomínio", "Total (R$)", "Custo (R$)",
            "Lucro (R$)", "Itens", "Última Compra", "Dias s/ comprar", "Margem %",
        ]
        out["Total (R$)"]     = out["Total (R$)"].apply(brl)
        out["Custo (R$)"]     = out["Custo (R$)"].apply(brl)
        out["Lucro (R$)"]     = out["Lucro (R$)"].apply(brl)
        out["Última Compra"]  = pd.to_datetime(out["Última Compra"]).dt.strftime("%d/%m/%Y").fillna("—")
        out["Dias s/ comprar"] = out["Dias s/ comprar"].apply(lambda d: "—" if d == 9999 else str(d))
        out["Margem %"]       = out["Margem %"].apply(lambda v: f"{v:.1f}%" if pd.notna(v) else "—")
        return out

    def cor_cli_row(row):
        d   = row["Dias s/ comprar"]
        cor_d = "#e8fff5" if d < 30 else "#fff8e8" if d <= 60 else "#fff0f3"
        m   = row["Margem %"]
        if m == "—":
            cor_m = ""
        else:
            v = float(m.replace("%", ""))
            cor_m = "#e8fff5" if v >= 30 else "#fff8e8" if v >= 10 else "#fff0f3"
        return [
            f"background-color:{cor_d}" if col in ("Dias s/ comprar", "Última Compra")
            else f"background-color:{cor_m}" if col == "Margem %"
            else ""
            for col in row.index
        ]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(
        fmt_cli(df_tab).style.apply(cor_cli_row, axis=1),
        use_container_width=True, hide_index=True, height=520,
    )
    st.caption(f"{len(df_tab)} clientes · {n_clientes} no total  ·  🟢 <30d  🟡 30–60d  🔴 >60d")
    st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# PÁGINA: PRODUTOS
# ═══════════════════════════════════════════════════════════════
elif pagina == "📦  Produtos":
    st.markdown('<div class="page-header"><h2>Produtos</h2><p>Vendas e margem por produto</p></div>', unsafe_allow_html=True)

    fp1, fp2, fp3 = st.columns([2, 2, 3])
    with fp1: busca_p  = st.text_input("🔍 Buscar produto", placeholder="Nome...")
    with fp2: cond_fp  = st.selectbox("Condomínio", ["Todos"] + condominios, key="cond_prod")
    with fp3: ordem_p  = st.radio("Ordenar por", ["Qtd vendida", "Receita", "Margem %"], horizontal=True)

    df_pe = df_prod[df_prod["condominio"] != "Outros"].copy()
    if cond_fp != "Todos":
        df_pe = df_pe[df_pe["condominio"] == cond_fp]
    if busca_p:
        df_pe = df_pe[df_pe["produto"].str.contains(busca_p, case=False, na=False)]

    # Ao mostrar "Todos", agrupa por produto eliminando a coluna condominio
    if cond_fp == "Todos":
        df_pe = (
            df_pe.groupby("produto")
            .agg(
                quantidade_vendida=("quantidade_vendida", "sum"),
                receita_total     =("receita_total",      "sum"),
                custo_total       =("custo_total",        "sum"),
                lucro_total       =("lucro_total",        "sum"),
                preco_medio       =("preco_medio",        "mean"),
                cmc_medio         =("cmc_medio",          "mean"),
                num_clientes      =("num_clientes",       "sum"),
            )
            .reset_index()
        )
        df_pe["margem_pct"] = (df_pe["lucro_total"] / df_pe["receita_total"] * 100).round(1)
        df_pe.loc[df_pe["receita_total"] <= 0, "margem_pct"] = None

    mapa_p = {"Qtd vendida": "quantidade_vendida", "Receita": "receita_total", "Margem %": "margem_pct"}
    df_pe = df_pe.sort_values(mapa_p[ordem_p], ascending=False)

    # Gráficos Top 10
    p1, p2 = st.columns(2)
    with p1:
        st.markdown('<div class="card"><p class="card-title">Quantidade vendida — Top 10</p>', unsafe_allow_html=True)
        tq = df_pe.sort_values("quantidade_vendida", ascending=False).head(10).copy()
        tq["d"] = tq["produto"].str[:30]
        fig = px.bar(tq.sort_values("quantidade_vendida"), x="quantidade_vendida", y="d",
                     orientation="h", color_discrete_sequence=["#06d6a0"], text_auto=True)
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=290,
                          plot_bgcolor="white", paper_bgcolor="white",
                          xaxis=dict(showgrid=True, gridcolor="#f0f4f8", title=""),
                          yaxis=dict(title=""))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with p2:
        st.markdown('<div class="card"><p class="card-title">Receita — Top 10</p>', unsafe_allow_html=True)
        tr = df_pe.sort_values("receita_total", ascending=False).head(10).copy()
        tr["d"] = tr["produto"].str[:30]
        fig2 = px.bar(tr.sort_values("receita_total"), x="receita_total", y="d",
                      orientation="h", color_discrete_sequence=["#00b4d8"], text_auto=".2s")
        fig2.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=290,
                           plot_bgcolor="white", paper_bgcolor="white",
                           xaxis=dict(showgrid=True, gridcolor="#f0f4f8", title=""),
                           yaxis=dict(title=""))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Tabela completa
    def fmt_prod(df):
        has_cond = "condominio" in df.columns
        base_cols = ["produto"] + (["condominio"] if has_cond else []) + [
            "quantidade_vendida", "preco_medio", "receita_total",
            "custo_total", "lucro_total", "num_clientes", "margem_pct",
        ]
        out = df[base_cols].copy()
        rename = {
            "produto":            "Produto",
            "condominio":         "Condomínio",
            "quantidade_vendida": "Qtd",
            "preco_medio":        "Preço Médio (R$)",
            "receita_total":      "Receita (R$)",
            "custo_total":        "Custo (R$)",
            "lucro_total":        "Lucro (R$)",
            "num_clientes":       "Clientes",
            "margem_pct":         "Margem %",
        }
        out = out.rename(columns=rename)
        out["Preço Médio (R$)"] = out["Preço Médio (R$)"].apply(brl)
        out["Receita (R$)"]     = out["Receita (R$)"].apply(brl)
        out["Custo (R$)"]       = out["Custo (R$)"].apply(brl)
        out["Lucro (R$)"]       = out["Lucro (R$)"].apply(brl)
        out["Margem %"]         = out["Margem %"].apply(lambda v: f"{v:.1f}%" if pd.notna(v) else "—")
        return out

    def cor_margem_prod(row):
        m = row["Margem %"]
        if m == "—":
            cor = ""
        else:
            v = float(m.replace("%", ""))
            cor = "#e8fff5" if v >= 30 else "#fff8e8" if v >= 10 else "#fff0f3"
        return [f"background-color:{cor}" if col == "Margem %" else "" for col in row.index]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(
        fmt_prod(df_pe).style.apply(cor_margem_prod, axis=1),
        use_container_width=True, hide_index=True, height=480,
    )
    st.caption(f"{len(df_pe)} produtos")
    st.markdown("</div>", unsafe_allow_html=True)
