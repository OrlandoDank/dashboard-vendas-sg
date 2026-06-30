import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path
import base64
from omie_api import carregar_dados

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
    page_title="Dashboard SG Soluções",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# CSS GLOBAL
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Fundo geral branco */
  [data-testid="stAppViewContainer"] { background: #f0f4f8; }
  [data-testid="stHeader"]           { background: transparent; }
  [data-testid="stSidebar"]          { background: #1a1f36; }
  [data-testid="stSidebar"] * { color: #c8ccd8 !important; }
  [data-testid="stSidebar"] .stRadio label { color: #c8ccd8 !important; font-size: 15px; }
  [data-testid="stSidebar"] .stRadio div[data-testid="stMarkdownContainer"] p { color: #888 !important; font-size: 12px; }

  /* Cards KPI */
  .kpi {
    background: white;
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 4px;
  }
  .kpi-icon {
    width: 52px; height: 52px;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; flex-shrink: 0;
  }
  .kpi-body { flex: 1; min-width: 0; }
  .kpi-label { color: #8892a4; font-size: 12px; margin: 0; font-weight: 500; text-transform: uppercase; letter-spacing: .5px; }
  .kpi-value { color: #1a1f36; font-size: 21px; font-weight: 700; margin: 2px 0 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .kpi-sub   { color: #56c4a8; font-size: 12px; margin: 2px 0 0; }

  /* Cards de seção */
  .card {
    background: white;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    margin-bottom: 16px;
  }
  .card-title { color: #1a1f36; font-size: 15px; font-weight: 600; margin: 0 0 16px; }

  /* Badges de status */
  .badge-green  { background:#e6f9f4; color:#06d6a0; border-radius:6px; padding:3px 10px; font-size:12px; font-weight:600; }
  .badge-yellow { background:#fff8e6; color:#ffc107; border-radius:6px; padding:3px 10px; font-size:12px; font-weight:600; }
  .badge-red    { background:#ffeef2; color:#ef476f; border-radius:6px; padding:3px 10px; font-size:12px; font-weight:600; }
  .badge-gray   { background:#f0f4f8; color:#8892a4; border-radius:6px; padding:3px 10px; font-size:12px; font-weight:600; }

  /* Bloco de título de página */
  .page-header { margin-bottom: 24px; }
  .page-header h2 { color: #1a1f36; font-size: 22px; font-weight: 700; margin: 0; }
  .page-header p  { color: #8892a4; font-size: 13px; margin: 4px 0 0; }

  /* Mobile */
  @media (max-width: 768px) {
    .kpi-value { font-size: 17px; }
    [data-testid="column"] { width:100% !important; flex:1 1 100% !important; min-width:100% !important; }
    .block-container { padding-left:1rem !important; padding-right:1rem !important; }
  }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def brl(v):
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

def mes_soma(df, col_data, col_val):
    h = pd.Timestamp.today()
    m = (df[col_data].dt.year == h.year) & (df[col_data].dt.month == h.month)
    return df.loc[m, col_val].sum()

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

CORES = ["#00b4d8","#06d6a0","#ffd166","#ef476f","#a78bfa","#fb8500"]
MES   = datetime.now().strftime("%b/%Y")



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
            <p style="color:#8892a4;font-size:11px;margin:0;">Dashboard de Vendas</p>
          </div>
        </div>
        <div style="margin-bottom:20px;"></div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='color:white;font-size:18px;margin-bottom:4px;'>SG Bichos</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#666;font-size:12px;margin-bottom:24px;'>Dashboard de Vendas</p>", unsafe_allow_html=True)

    pagina = st.radio("Navegação", [
        "🏠  Visão Geral",
        "👥  Clientes",
        "📦  Produtos",
        "🔴  Boletos em Atraso",
        "💰  Financeiro",
    ], label_visibility="collapsed")

    st.markdown("---")
    if st.button("🔄 Atualizar dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown(f"<p style='color:#555;font-size:11px;margin-top:8px;'>Atualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#555;font-size:11px;'>Cache: 5 min</p>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# DADOS
# ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def get_dados():
    return carregar_dados()

with st.spinner("Buscando dados do Omie..."):
    df_ped, df_lin, df_cli, df_ind, df_prod, df_bol, saldo_cash, df_pagar, df_receber = get_dados()


# ─────────────────────────────────────────────────────────────
# MÉTRICAS GLOBAIS
# ─────────────────────────────────────────────────────────────
_hoje_ts = pd.Timestamp.today().normalize()
# Seg–dom da semana atual; se hoje é domingo, usa a próxima semana
if _hoje_ts.weekday() == 6:
    _ini_semana = _hoje_ts + pd.Timedelta(days=1)        # segunda-feira seguinte
else:
    _ini_semana = _hoje_ts - pd.Timedelta(days=_hoje_ts.weekday())  # segunda desta semana
_fim_semana = _ini_semana + pd.Timedelta(days=6)

if not df_pagar.empty:
    _mask_sem       = (df_pagar["data_vencimento"] >= _ini_semana) & (df_pagar["data_vencimento"] <= _fim_semana)
    df_pagar_semana = df_pagar[_mask_sem].copy()
else:
    df_pagar_semana = pd.DataFrame()

total_pagar_semana = df_pagar_semana["valor"].sum() if not df_pagar_semana.empty else 0.0
qtd_pagar_semana   = len(df_pagar_semana)

# Boletos/títulos formais (A VENCER + ATRASADO) com previsão nesta semana
_cols_rec = ["codigo_cliente","numero_documento","parcela","data_vencimento","valor","status"]
_partes = [df for df in [df_receber, df_bol] if not df.empty and all(c in df.columns for c in _cols_rec)]
_df_todas_rec = pd.concat([d[_cols_rec] for d in _partes]).reset_index(drop=True) if _partes else pd.DataFrame()

if not _df_todas_rec.empty:
    _mask_rec_sem     = (_df_todas_rec["data_vencimento"] >= _ini_semana) & (_df_todas_rec["data_vencimento"] <= _fim_semana)
    df_receber_semana = _df_todas_rec[_mask_rec_sem].copy()
else:
    df_receber_semana = pd.DataFrame()

# Pedidos com data de previsão nesta semana (previsões de vendas — igual ao relatório Omie)
if not df_ped.empty:
    _ped_sem = df_ped[
        (df_ped["data_pedido"] >= _ini_semana) &
        (df_ped["data_pedido"] <= _fim_semana)
    ].merge(df_cli[["codigo_cliente","nome_cliente"]], on="codigo_cliente", how="left").copy()
    _ped_rec = pd.DataFrame({
        "codigo_cliente":  _ped_sem["codigo_cliente"],
        "numero_documento": _ped_sem["numero_pedido"].astype(str),
        "parcela":         "",
        "data_vencimento": _ped_sem["data_pedido"],
        "valor":           _ped_sem["valor_total"],
        "status":          "PEDIDO",
    }) if not _ped_sem.empty else pd.DataFrame()
else:
    _ped_rec = pd.DataFrame()

# Combina boletos + pedidos para o total da semana
_rec_partes = [df for df in [df_receber_semana, _ped_rec] if not df.empty]
df_receber_semana = pd.concat(_rec_partes).reset_index(drop=True) if _rec_partes else pd.DataFrame()

total_receber_semana = df_receber_semana["valor"].sum() if not df_receber_semana.empty else 0.0
qtd_receber_semana   = len(df_receber_semana)

fat_total     = df_ped["valor_total"].sum()
fat_mes       = mes_soma(df_ped, "data_pedido", "valor_total")
ped_total     = len(df_ped)
ped_mes       = int(df_ped[(df_ped["data_pedido"].dt.year==datetime.now().year)&(df_ped["data_pedido"].dt.month==datetime.now().month)].shape[0])
ticket_total  = fat_total / ped_total if ped_total else 0
ticket_mes    = fat_mes   / ped_mes   if ped_mes   else 0
cli_ativos    = int((df_ind["num_pedidos"]>0).sum())
cli_verdes    = int(((df_ind["num_pedidos"]>0)&(df_ind["dias_sem_comprar"]<30)).sum())
cli_amarelos  = int(((df_ind["num_pedidos"]>0)&(df_ind["dias_sem_comprar"].between(30,60))).sum())
cli_vermelhos = int(((df_ind["num_pedidos"]>0)&(df_ind["dias_sem_comprar"]>60)).sum())
total_atraso  = df_bol["valor"].sum() if not df_bol.empty else 0


# ═══════════════════════════════════════════════════════════════
# PÁGINA: VISÃO GERAL
# ═══════════════════════════════════════════════════════════════
if pagina == "🏠  Visão Geral":
    st.markdown(f"""<div class="page-header">
      <h2>Visão Geral</h2>
      <p>Resumo executivo de vendas · {MES}</p>
    </div>""", unsafe_allow_html=True)

    # KPIs
    k1,k2,k3,k4 = st.columns(4)
    k1.markdown(kpi_card("💰","#e8f8ff","Total Faturado", brl(fat_total), f"Mês: {brl(fat_mes)}"), unsafe_allow_html=True)
    k2.markdown(kpi_card("📦","#e8fff5","Total de Pedidos", str(ped_total), f"Mês: {ped_mes}"), unsafe_allow_html=True)
    k3.markdown(kpi_card("🎯","#fff8e8","Ticket Médio", brl(ticket_total), f"Mês: {brl(ticket_mes)}"), unsafe_allow_html=True)
    k4.markdown(kpi_card("🏦","#eef2ff","Omie.CASH", brl(saldo_cash), "Saldo disponível"), unsafe_allow_html=True)

    st.write("")
    k5,k6,k7,k8 = st.columns(4)
    k5.markdown(kpi_card("🟢","#e8fff5","Clientes Ativos", str(cli_verdes), "< 30 dias"), unsafe_allow_html=True)
    k6.markdown(kpi_card("🟡","#fff8e8","Em Atenção", str(cli_amarelos), "30 a 60 dias"), unsafe_allow_html=True)
    k7.markdown(kpi_card("🔴","#fff0f3","Inativos", str(cli_vermelhos), "> 60 dias"), unsafe_allow_html=True)
    k8.markdown(kpi_card("⚠️","#fff0f3","Em Atraso", brl(total_atraso), f"{len(df_bol)} boletos"), unsafe_allow_html=True)

    st.write("")

    # Card: Contas a pagar da semana
    st.markdown('<div class="card">', unsafe_allow_html=True)
    cp1, cp2 = st.columns([1, 3])
    with cp1:
        st.markdown(kpi_card("💸","#fff0f3","Esta semana", brl(total_pagar_semana), f"{_ini_semana.strftime('%d/%m')} – {_fim_semana.strftime('%d/%m')} · {qtd_pagar_semana} contas"), unsafe_allow_html=True)
    with cp2:
        if not df_pagar_semana.empty:
            _cli_lkp = df_cli[["codigo_cliente","nome_cliente"]].rename(columns={"codigo_cliente":"codigo_fornecedor","nome_cliente":"_nome"})
            df_ps_show = df_pagar_semana.merge(_cli_lkp, on="codigo_fornecedor", how="left")
            df_ps_show["nome_fornecedor"] = df_ps_show["_nome"].fillna(df_ps_show["nome_fornecedor"])
            df_ps_show = df_ps_show[["nome_fornecedor","numero_documento","data_vencimento","valor","status"]].copy()
            df_ps_show.columns = ["Fornecedor","Documento","Vencimento","Valor (R$)","Status"]
            df_ps_show["Vencimento"] = df_ps_show["Vencimento"].dt.strftime("%d/%m/%Y")
            df_ps_show["Valor (R$)"] = df_ps_show["Valor (R$)"].apply(brl)
            st.dataframe(df_ps_show.head(3), use_container_width=True, hide_index=True, height=143)
        else:
            st.info("Nenhuma conta a pagar esta semana.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Card: Recebimentos da semana
    st.markdown('<div class="card">', unsafe_allow_html=True)
    cr1, cr2 = st.columns([1, 3])
    with cr1:
        st.markdown(kpi_card("💚","#e8fff5","Esta semana", brl(total_receber_semana), f"{_ini_semana.strftime('%d/%m')} – {_fim_semana.strftime('%d/%m')} · {qtd_receber_semana} recebimentos"), unsafe_allow_html=True)
    with cr2:
        if not df_receber_semana.empty:
            df_rs_show = df_receber_semana.merge(
                df_cli[["codigo_cliente","nome_cliente"]], on="codigo_cliente", how="left"
            ).sort_values("data_vencimento")
            df_rs_show = df_rs_show[["nome_cliente","numero_documento","data_vencimento","valor","status"]].copy()
            df_rs_show.columns = ["Cliente","Documento","Vencimento","Valor (R$)","Tipo"]
            df_rs_show["Vencimento"] = df_rs_show["Vencimento"].dt.strftime("%d/%m/%Y")
            df_rs_show["Valor (R$)"] = df_rs_show["Valor (R$)"].apply(brl)
            st.dataframe(df_rs_show.head(3), use_container_width=True, hide_index=True, height=143)
        else:
            st.info("Nenhum recebimento previsto esta semana.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    # Gráfico de faturamento mensal (área)
    g1, g2 = st.columns([3,2])
    with g1:
        st.markdown('<div class="card"><p class="card-title">📈 Faturamento Mensal</p>', unsafe_allow_html=True)
        if not df_ped.empty:
            df_mes = (
                df_ped.dropna(subset=["data_pedido"])
                .assign(mes=lambda x: x["data_pedido"].dt.to_period("M").astype(str))
                .groupby("mes")["valor_total"].sum().reset_index()
            )
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=df_mes["mes"], y=df_mes["valor_total"],
                marker_color="#00b4d8",
                text=[f"R${v/1000:.0f}k" for v in df_mes["valor_total"]],
                textposition="outside",
                textfont=dict(size=10),
            ))
            fig.update_layout(
                margin=dict(t=30,b=0,l=0,r=0), height=240,
                plot_bgcolor="white", paper_bgcolor="white",
                bargap=0.35,
                xaxis=dict(showgrid=False, tickfont=dict(size=11)),
                yaxis=dict(showgrid=True, gridcolor="#f0f4f8", tickfont=dict(size=11), tickprefix="R$"),
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with g2:
        st.markdown('<div class="card"><p class="card-title">👥 Retenção de Clientes</p>', unsafe_allow_html=True)
        total_c = cli_verdes + cli_amarelos + cli_vermelhos
        if total_c > 0:
            fig2 = go.Figure(go.Pie(
                labels=["Ativos","Atenção","Inativos"],
                values=[cli_verdes, cli_amarelos, cli_vermelhos],
                hole=0.65,
                marker_colors=["#06d6a0","#ffd166","#ef476f"],
                textinfo="percent",
                textfont_size=12,
            ))
            fig2.update_layout(
                margin=dict(t=0,b=0,l=0,r=0), height=240,
                paper_bgcolor="white",
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, font=dict(size=11)),
                annotations=[dict(text=f"<b>{total_c}</b><br>clientes", x=0.5,y=0.5, showarrow=False, font=dict(size=13, color="#1a1f36"))],
            )
            st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Top 5 clientes + Top 5 produtos
    t1, t2 = st.columns(2)
    with t1:
        st.markdown('<div class="card"><p class="card-title">🏆 Top 10 Clientes</p>', unsafe_allow_html=True)
        top10 = df_ind[df_ind["total_comprado"]>0].head(10).copy()
        top10["nome_curto"] = top10["nome_cliente"].str[:25]
        fig3 = px.bar(top10.sort_values("total_comprado"), x="total_comprado", y="nome_curto",
                      orientation="h", color_discrete_sequence=["#00b4d8"], text_auto=".2s")
        fig3.update_layout(margin=dict(t=0,b=0,l=0,r=0), height=380,
                           plot_bgcolor="white", paper_bgcolor="white",
                           xaxis=dict(showgrid=True, gridcolor="#f0f4f8", title=""),
                           yaxis=dict(title=""))
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with t2:
        st.markdown('<div class="card"><p class="card-title">📦 Top 10 Produtos</p>', unsafe_allow_html=True)
        top10p = df_prod.head(10).copy()
        top10p["desc_curta"] = top10p["descricao"].str[:25]
        fig4 = px.bar(top10p.sort_values("quantidade_vendida"), x="quantidade_vendida", y="desc_curta",
                      orientation="h", color_discrete_sequence=["#06d6a0"], text_auto=True)
        fig4.update_layout(margin=dict(t=0,b=0,l=0,r=0), height=380,
                           plot_bgcolor="white", paper_bgcolor="white",
                           xaxis=dict(showgrid=True, gridcolor="#f0f4f8", title=""),
                           yaxis=dict(title=""))
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# PÁGINA: CLIENTES
# ═══════════════════════════════════════════════════════════════
elif pagina == "👥  Clientes":
    st.markdown('<div class="page-header"><h2>Clientes</h2><p>Histórico de compras e retenção</p></div>', unsafe_allow_html=True)

    fc1,fc2,fc3 = st.columns([3,2,2])
    with fc1: busca = st.text_input("🔍 Buscar", placeholder="Nome do cliente...")
    with fc2: status_f = st.selectbox("Status", ["Todos","🟢 Ativos (<30d)","🟡 Atenção (30–60d)","🔴 Inativos (>60d)","⚪ Nunca compraram"])
    with fc3: ordem = st.selectbox("Ordenar por", ["Total comprado","Dias sem comprar","Nº pedidos","Nome"])

    df_tab = df_ind.copy()
    if busca:
        df_tab = df_tab[df_tab["nome_cliente"].str.contains(busca, case=False, na=False)]
    if status_f == "🟢 Ativos (<30d)":
        df_tab = df_tab[(df_tab["num_pedidos"]>0)&(df_tab["dias_sem_comprar"]<30)]
    elif status_f == "🟡 Atenção (30–60d)":
        df_tab = df_tab[(df_tab["num_pedidos"]>0)&(df_tab["dias_sem_comprar"].between(30,60))]
    elif status_f == "🔴 Inativos (>60d)":
        df_tab = df_tab[(df_tab["num_pedidos"]>0)&(df_tab["dias_sem_comprar"]>60)]
    elif status_f == "⚪ Nunca compraram":
        df_tab = df_tab[df_tab["num_pedidos"]==0]

    mapa = {"Total comprado":("total_comprado",False),"Dias sem comprar":("dias_sem_comprar",True),"Nº pedidos":("num_pedidos",False),"Nome":("nome_cliente",True)}
    c,a = mapa[ordem]
    df_tab = df_tab.sort_values(c, ascending=a)

    def fmt_cli(df):
        out = df[["nome_cliente","cidade","estado","total_comprado","num_pedidos","ticket_medio","ultima_compra","dias_sem_comprar"]].copy()
        out.columns = ["Cliente","Cidade","Estado","Total (R$)","Pedidos","Ticket Médio (R$)","Última Compra","Dias s/ comprar"]
        out["Total (R$)"]       = out["Total (R$)"].apply(lambda v: brl(v) if v>0 else "—")
        out["Ticket Médio (R$)"]= out["Ticket Médio (R$)"].apply(lambda v: brl(v) if v>0 else "—")
        out["Última Compra"]    = pd.to_datetime(out["Última Compra"]).dt.strftime("%d/%m/%Y").fillna("—")
        out["Dias s/ comprar"]  = out["Dias s/ comprar"].apply(lambda d: "—" if d==9999 else str(d))
        return out

    def cor_cli(row):
        d = row["Dias s/ comprar"]
        if d=="—": cor="#f8f9fa"
        else:
            dias=int(d)
            cor="#e8fff5" if dias<30 else "#fff8e8" if dias<=60 else "#fff0f3"
        return [f"background-color:{cor}" if col in ("Dias s/ comprar","Última Compra") else "" for col in row.index]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(fmt_cli(df_tab).style.apply(cor_cli, axis=1), use_container_width=True, hide_index=True, height=520)
    st.caption(f"{len(df_tab)} clientes  ·  🟢 {cli_verdes}  🟡 {cli_amarelos}  🔴 {cli_vermelhos}")
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# PÁGINA: PRODUTOS
# ═══════════════════════════════════════════════════════════════
elif pagina == "📦  Produtos":
    st.markdown('<div class="page-header"><h2>Produtos</h2><p>Vendas e margem por produto</p></div>', unsafe_allow_html=True)

    p1,p2 = st.columns(2)
    with p1:
        st.markdown('<div class="card"><p class="card-title">Qtd vendida — Top 10</p>', unsafe_allow_html=True)
        tq = df_prod.head(10).copy()
        tq["d"] = tq["descricao"].str[:28]
        fig = px.bar(tq.sort_values("quantidade_vendida"), x="quantidade_vendida", y="d",
                     orientation="h", color_discrete_sequence=["#06d6a0"], text_auto=True)
        fig.update_layout(margin=dict(t=0,b=0,l=0,r=0), height=300,
                          plot_bgcolor="white", paper_bgcolor="white",
                          xaxis=dict(showgrid=True, gridcolor="#f0f4f8", title=""),
                          yaxis=dict(title=""))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with p2:
        st.markdown('<div class="card"><p class="card-title">Receita — Top 10</p>', unsafe_allow_html=True)
        tr = df_prod.sort_values("receita_total",ascending=False).head(10).copy()
        tr["d"] = tr["descricao"].str[:28]
        fig2 = px.bar(tr.sort_values("receita_total"), x="receita_total", y="d",
                      orientation="h", color_discrete_sequence=["#00b4d8"], text_auto=".2s")
        fig2.update_layout(margin=dict(t=0,b=0,l=0,r=0), height=300,
                           plot_bgcolor="white", paper_bgcolor="white",
                           xaxis=dict(showgrid=True, gridcolor="#f0f4f8", title=""),
                           yaxis=dict(title=""))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    ord_p = st.radio("Ordenar tabela por:", ["Qtd vendida","Receita","Margem %"], horizontal=True)
    mapa_p = {"Qtd vendida":"quantidade_vendida","Receita":"receita_total","Margem %":"margem_pct"}
    df_pe = df_prod.sort_values(mapa_p[ord_p], ascending=False).copy()

    def fmt_prod(df):
        out = df[["descricao","unidade","quantidade_vendida","preco_medio_venda","receita_total","num_pedidos","cmc_unitario","margem_pct"]].copy()
        out.columns=["Produto","Un.","Qtd","Preço Médio (R$)","Receita (R$)","Pedidos","CMC (R$)","Margem %"]
        out["Preço Médio (R$)"]=out["Preço Médio (R$)"].apply(brl)
        out["Receita (R$)"]=out["Receita (R$)"].apply(brl)
        out["CMC (R$)"]=out["CMC (R$)"].apply(lambda v: brl(v) if v>0 else "—")
        out["Margem %"]=out["Margem %"].apply(lambda v: f"{v:.1f}%" if pd.notna(v) else "—")
        return out

    def cor_margem(row):
        m=row["Margem %"]
        if m=="—": cor=""
        else:
            v=float(m.replace("%",""))
            cor="#e8fff5" if v>=30 else "#fff8e8" if v>=10 else "#fff0f3"
        return [f"background-color:{cor}" if col=="Margem %" else "" for col in row.index]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(fmt_prod(df_pe).style.apply(cor_margem,axis=1), use_container_width=True, hide_index=True, height=480)
    st.caption(f"{len(df_prod)} produtos  ·  {int((df_prod['cmc_unitario']>0).sum())} com CMC cadastrado")
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# PÁGINA: BOLETOS EM ATRASO
# ═══════════════════════════════════════════════════════════════
elif pagina == "🔴  Boletos em Atraso":
    st.markdown('<div class="page-header"><h2>Boletos em Atraso</h2><p>Contas a receber vencidas</p></div>', unsafe_allow_html=True)

    if df_bol.empty:
        st.success("Nenhum boleto em atraso no momento.")
    else:
        df_b = df_bol.merge(df_cli[["codigo_cliente","nome_cliente"]], on="codigo_cliente", how="left")
        b1,b2,b3 = st.columns(3)
        b1.markdown(kpi_card("💸","#fff0f3","Total em Atraso", brl(df_b["valor"].sum())), unsafe_allow_html=True)
        b2.markdown(kpi_card("📄","#fff8e8","Boletos Vencidos", str(len(df_b))), unsafe_allow_html=True)
        b3.markdown(kpi_card("👤","#fff0f3","Clientes Devedores", str(df_b["codigo_cliente"].nunique())), unsafe_allow_html=True)

        st.write("")

        # Gráfico por cliente
        st.markdown('<div class="card"><p class="card-title">Valor em atraso por cliente</p>', unsafe_allow_html=True)
        df_bc = df_b.groupby("nome_cliente")["valor"].sum().sort_values(ascending=False).head(10).reset_index()
        df_bc["nome_curto"] = df_bc["nome_cliente"].str[:30]
        fig = px.bar(df_bc.sort_values("valor"), x="valor", y="nome_curto",
                     orientation="h", color_discrete_sequence=["#ef476f"], text_auto=".2s")
        fig.update_layout(margin=dict(t=0,b=0,l=0,r=0), height=250,
                          plot_bgcolor="white", paper_bgcolor="white",
                          xaxis=dict(showgrid=True, gridcolor="#f0f4f8", title=""),
                          yaxis=dict(title=""))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        def fmt_bol(df):
            out = df[["nome_cliente","numero_documento","parcela","data_vencimento","dias_atraso","valor"]].copy()
            out.columns=["Cliente","Nº Documento","Parcela","Vencimento","Dias em Atraso","Valor (R$)"]
            out["Vencimento"]=out["Vencimento"].dt.strftime("%d/%m/%Y")
            out["Valor (R$)"]=out["Valor (R$)"].apply(brl)
            return out

        def cor_bol(row):
            d=row["Dias em Atraso"]
            cor="#e8fff5" if d<30 else "#fff8e8" if d<=60 else "#fff0f3"
            return [f"background-color:{cor}" if col in ("Dias em Atraso","Vencimento") else "" for col in row.index]

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.dataframe(fmt_bol(df_b).style.apply(cor_bol,axis=1), use_container_width=True, hide_index=True, height=450)
        st.caption(f"🟢 <30d  🟡 30–60d  🔴 >60d")
        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# PÁGINA: FINANCEIRO
# ═══════════════════════════════════════════════════════════════
elif pagina == "💰  Financeiro":
    st.markdown('<div class="page-header"><h2>Financeiro</h2><p>Resumo financeiro e pedidos recentes</p></div>', unsafe_allow_html=True)

    f1,f2,f3 = st.columns(3)
    f1.markdown(kpi_card("💰","#e8f8ff","Faturamento Total", brl(fat_total), f"Mês: {brl(fat_mes)}"), unsafe_allow_html=True)
    f2.markdown(kpi_card("🏦","#eef2ff","Omie.CASH", brl(saldo_cash), "Saldo disponível"), unsafe_allow_html=True)
    f3.markdown(kpi_card("⚠️","#fff0f3","Em Atraso", brl(total_atraso), f"{len(df_bol)} boletos"), unsafe_allow_html=True)

    st.write("")

    # Faturamento por mês (barras)
    st.markdown('<div class="card"><p class="card-title">📊 Faturamento por mês</p>', unsafe_allow_html=True)
    if not df_ped.empty:
        df_mes = (
            df_ped.dropna(subset=["data_pedido"])
            .assign(mes=lambda x: x["data_pedido"].dt.to_period("M").astype(str))
            .groupby("mes").agg(faturamento=("valor_total","sum"), pedidos=("numero_pedido","count")).reset_index()
        )
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_mes["mes"], y=df_mes["faturamento"], name="Faturamento",
            marker_color="#00b4d8", yaxis="y1",
            text=[f"R${v/1000:.0f}k" for v in df_mes["faturamento"]],
            textposition="outside", textfont=dict(size=10),
        ))
        fig.add_trace(go.Scatter(
            x=df_mes["mes"], y=df_mes["pedidos"], name="Pedidos",
            mode="lines+markers", line=dict(color="#ffd166",width=2),
            marker=dict(size=6), yaxis="y2",
        ))
        fig.update_layout(
            margin=dict(t=40,b=0,l=0,r=0), height=300,
            plot_bgcolor="white", paper_bgcolor="white",
            bargap=0.35,
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            yaxis=dict(showgrid=True, gridcolor="#f0f4f8", title="R$", tickprefix="R$"),
            yaxis2=dict(overlaying="y", side="right", title="Pedidos", showgrid=False),
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Contas a pagar
    st.markdown('<div class="card"><p class="card-title">💸 Contas a Pagar</p>', unsafe_allow_html=True)
    periodo = st.radio("Período:", ["Esta semana", "Este mês", "Este ano"], horizontal=True, key="radio_pagar")

    if not df_pagar.empty:
        _h = pd.Timestamp.today().normalize()
        if periodo == "Esta semana":
            _ini = _h - pd.Timedelta(days=_h.weekday())
            _fim = _ini + pd.Timedelta(days=6)
        elif periodo == "Este mês":
            _ini = _h.replace(day=1)
            _fim = (_ini + pd.DateOffset(months=1)) - pd.Timedelta(days=1)
        else:
            _ini = _h.replace(month=1, day=1)
            _fim = _h.replace(month=12, day=31)

        df_pf = df_pagar[(df_pagar["data_vencimento"] >= _ini) & (df_pagar["data_vencimento"] <= _fim)].copy()

        pc1, pc2, pc3 = st.columns(3)
        _atrasadas = df_pf[df_pf["status"] == "ATRASADO"]
        pc1.markdown(kpi_card("💸","#fff0f3","Total a Pagar", brl(df_pf["valor"].sum()), f"{len(df_pf)} contas"), unsafe_allow_html=True)
        pc2.markdown(kpi_card("⚠️","#fff8e8","Em Atraso", brl(_atrasadas["valor"].sum()), f"{len(_atrasadas)} contas"), unsafe_allow_html=True)
        pc3.markdown(kpi_card("✅","#e8fff5","Em Aberto", brl(df_pf[df_pf["status"]=="ABERTO"]["valor"].sum()), f"{len(df_pf[df_pf['status']=='ABERTO'])} contas"), unsafe_allow_html=True)

        st.write("")

        if not df_pf.empty:
            _cli_lkp2 = df_cli[["codigo_cliente","nome_cliente"]].rename(columns={"codigo_cliente":"codigo_fornecedor","nome_cliente":"_nome"})
            df_pf = df_pf.merge(_cli_lkp2, on="codigo_fornecedor", how="left")
            df_pf["nome_fornecedor"] = df_pf["_nome"].fillna(df_pf["nome_fornecedor"])
            df_pt = df_pf[["nome_fornecedor","numero_documento","parcela","data_vencimento","valor","status"]].copy()
            df_pt.columns = ["Fornecedor","Documento","Parcela","Vencimento","Valor (R$)","Status"]
            df_pt["Vencimento"] = df_pt["Vencimento"].dt.strftime("%d/%m/%Y")
            df_pt["Valor (R$)"] = df_pt["Valor (R$)"].apply(brl)

            def cor_pagar(row):
                cor = "#fff0f3" if row["Status"] == "ATRASADO" else ""
                return [f"background-color:{cor}" if col in ("Status","Vencimento") else "" for col in row.index]

            st.dataframe(df_pt.style.apply(cor_pagar, axis=1), use_container_width=True, hide_index=True, height=400)
            st.caption(f"{len(df_pf)} contas · Total: {brl(df_pf['valor'].sum())}")
        else:
            st.info("Nenhuma conta a pagar no período selecionado.")
    else:
        st.info("Nenhuma conta a pagar encontrada.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    # Contas a receber
    st.markdown('<div class="card"><p class="card-title">💚 Contas a Receber</p>', unsafe_allow_html=True)
    periodo_rec = st.radio("Período:", ["Esta semana", "Este mês", "Este ano"], horizontal=True, key="radio_receber")

    if not df_receber.empty:
        _h = pd.Timestamp.today().normalize()
        if periodo_rec == "Esta semana":
            _ini_r = _h - pd.Timedelta(days=_h.weekday())
            _fim_r = _ini_r + pd.Timedelta(days=6)
        elif periodo_rec == "Este mês":
            _ini_r = _h.replace(day=1)
            _fim_r = (_ini_r + pd.DateOffset(months=1)) - pd.Timedelta(days=1)
        else:
            _ini_r = _h.replace(month=1, day=1)
            _fim_r = _h.replace(month=12, day=31)

        df_rf = df_receber[(df_receber["data_vencimento"] >= _ini_r) & (df_receber["data_vencimento"] <= _fim_r)].copy()

        pr1, pr2 = st.columns(2)
        pr1.markdown(kpi_card("💚","#e8fff5","Total a Receber", brl(df_rf["valor"].sum()), f"{len(df_rf)} títulos"), unsafe_allow_html=True)
        pr2.markdown(kpi_card("📄","#e8f8ff","Títulos", str(len(df_rf["codigo_cliente"].unique() if not df_rf.empty else [])), "clientes"), unsafe_allow_html=True)

        st.write("")

        if not df_rf.empty:
            df_rf_show = df_rf.merge(df_cli[["codigo_cliente","nome_cliente"]], on="codigo_cliente", how="left")
            df_rt = df_rf_show[["nome_cliente","numero_documento","parcela","data_vencimento","valor","status"]].copy()
            df_rt.columns = ["Cliente","Documento","Parcela","Vencimento","Valor (R$)","Status"]
            df_rt["Vencimento"] = df_rt["Vencimento"].dt.strftime("%d/%m/%Y")
            df_rt["Valor (R$)"] = df_rt["Valor (R$)"].apply(brl)
            st.dataframe(df_rt, use_container_width=True, hide_index=True, height=400)
            st.caption(f"{len(df_rf)} títulos · Total: {brl(df_rf['valor'].sum())}")
        else:
            st.info("Nenhum recebimento no período selecionado.")
    else:
        st.info("Nenhuma conta a receber encontrada.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    # Pedidos recentes
    st.markdown('<div class="card"><p class="card-title">📋 Pedidos recentes</p>', unsafe_allow_html=True)
    df_pr = (
        df_ped.merge(df_cli[["codigo_cliente","nome_cliente"]], on="codigo_cliente", how="left")
        .sort_values("data_pedido", ascending=False).head(50)
    )[["numero_pedido","data_pedido","nome_cliente","valor_total","quantidade_itens"]].copy()
    df_pr.columns=["Nº Pedido","Data","Cliente","Valor (R$)","Itens"]
    df_pr["Data"]=pd.to_datetime(df_pr["Data"]).dt.strftime("%d/%m/%Y")
    df_pr["Valor (R$)"]=df_pr["Valor (R$)"].apply(brl)
    df_pr["Etapa"]="Faturado"
    st.dataframe(df_pr, use_container_width=True, hide_index=True, height=420)
    st.markdown('</div>', unsafe_allow_html=True)
