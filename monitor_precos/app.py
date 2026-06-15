"""
Monitor de Preços — Farinhas & Gorduras Animais (BR)
Variação histórica 2020-hoje e tendências futuras.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────── PAGE CONFIG ───────────────────────────────
st.set_page_config(
    page_title="Monitor de Preços | Farinhas & Gorduras",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp { background:#eef2f7; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg,#0f2027 0%,#203a43 60%,#2c5364 100%);
    }
    [data-testid="stSidebar"] * { color:#e0ecff !important; }
    [data-testid="stSidebar"] hr { border-color:#ffffff33; }
    .block-container { padding:1.2rem 2rem; }
    .kpi-card {
        background:#fff;
        border-radius:12px;
        padding:14px 18px;
        box-shadow:0 2px 10px rgba(0,0,0,.08);
        border-top:4px solid;
        margin-bottom:8px;
    }
    .kpi-title { font-size:.78rem;color:#888;font-weight:700;text-transform:uppercase;letter-spacing:.6px }
    .kpi-value { font-size:1.55rem;font-weight:800;color:#0f2027;margin-top:4px }
    .kpi-delta { font-size:.88rem;font-weight:700;margin-top:3px }
    .kpi-info  { font-size:.8rem;color:#666;margin-top:2px }
    .info-box {
        background:#fff8e1;border-left:4px solid #ffc107;
        padding:10px 16px;border-radius:0 8px 8px 0;margin:1rem 0;
        font-size:.88rem;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────── PRODUCT CATALOG ───────────────────────────
PRODUCTS = {
    'Farinhas': {
        'Farinha de Carne e Ossos': {'base': 1420, 'growth': .118, 'vol': .018, 'sea': .040, 'color': '#e74c3c'},
        'Farinha de Vísceras':      {'base': 1060, 'growth': .108, 'vol': .022, 'sea': .055, 'color': '#e67e22'},
        'Farinha de Peixes':        {'base': 3250, 'growth': .092, 'vol': .030, 'sea': .090, 'color': '#3498db'},
        'Farinha de Suínos':        {'base': 1190, 'growth': .114, 'vol': .021, 'sea': .042, 'color': '#9b59b6'},
        'Farinha de Torresmo':      {'base':  960, 'growth': .098, 'vol': .020, 'sea': .062, 'color': '#1abc9c'},
    },
    'Gorduras': {
        'Óleo de Peixe':    {'base': 4850, 'growth': .108, 'vol': .034, 'sea': .100, 'color': '#2980b9'},
        'Sebo Bovino':      {'base': 1870, 'growth': .124, 'vol': .025, 'sea': .050, 'color': '#8e44ad'},
        'Sebo Branqueado':  {'base': 2220, 'growth': .119, 'vol': .023, 'sea': .042, 'color': '#c0392b'},
        'Óleo de Vísceras': {'base': 1460, 'growth': .113, 'vol': .026, 'sea': .065, 'color': '#27ae60'},
    },
}

ALL_NAMES = [n for cat in PRODUCTS.values() for n in cat]

EVENTS = [
    dict(dt=datetime(2020, 3, 15), label='COVID-19',       color='#ff4444'),
    dict(dt=datetime(2021, 6,  1), label='Crise Logíst.',  color='#ff8c00'),
    dict(dt=datetime(2022, 2, 24), label='Guerra Ucr.',    color='#aa0000'),
    dict(dt=datetime(2022, 9,  1), label='Pico Inflação',  color='#cc3300'),
    dict(dt=datetime(2023, 7,  1), label='Normalização',   color='#009900'),
    dict(dt=datetime(2024, 6,  1), label='Novo Ciclo',     color='#0055cc'),
]

# ─────────────────────────── DATA GENERATION ───────────────────────────
@st.cache_data
def build_dataset():
    np.random.seed(2024)
    start = datetime(2020, 1, 6)
    end   = datetime.now()
    dates = pd.date_range(start=start, end=end, freq='W-MON')
    n     = len(dates)

    # Gaussian shocks (week_index, magnitude, half_width)
    shocks = [
        ( 11, +.11,  7),   # COVID Q1-2020
        ( 74, +.24, 14),   # Supply chain mid-2021
        (108, +.19, 11),   # Ukraine war Feb-2022
        (138, +.09,  8),   # Inflation peak Sep-2022
        (183, -.10, 18),   # Normalization Jul-2023
        (235, +.04, 10),   # New cycle Jun-2024
    ]

    def gauss(i, center, mag, width):
        return mag * np.exp(-0.5 * ((i - center) / width) ** 2)

    def make_series(cfg):
        rw = 0.0
        out = []
        for i in range(n):
            trend    = cfg['base'] * (1 + cfg['growth']) ** (i / 52.0)
            shock    = sum(gauss(i, c, m, w) for c, m, w in shocks)
            seasonal = 1 + cfg['sea'] * np.sin(2 * np.pi * i / 52 - .5)
            rw       = rw * .97 + np.random.normal(0, cfg['vol'] * .4)
            price    = trend * (1 + shock) * seasonal * (1 + rw)
            out.append(round(max(price, cfg['base'] * .35), 1))
        return out

    df = pd.DataFrame({'Data': dates})
    for prods in PRODUCTS.values():
        for name, cfg in prods.items():
            df[name] = make_series(cfg)
    return df

# ─────────────────────────── ANALYSIS ──────────────────────────────────
def trend_analysis(series: pd.Series, dates: pd.Series, fwd_weeks: int = 52) -> dict:
    n = len(series)
    x = np.arange(n, dtype=float)
    y = series.values.astype(float)

    slope, intercept, r, *_ = stats.linregress(x, y)

    # Short-term trend using last 26 weeks (~6 months)
    x_st = np.arange(26, dtype=float)
    y_st = y[-26:]
    st_sl, st_ic, *_ = stats.linregress(x_st, y_st)

    fitted  = slope * x + intercept
    std_res = np.std(y - fitted)

    # Forecast from last known price using recent slope
    x_fc   = np.arange(1, fwd_weeks + 1, dtype=float)
    fc_mid = y[-1] + st_sl * x_fc
    ci     = 1.96 * std_res * np.sqrt(x_fc) / np.sqrt(26)

    fc_dates = pd.date_range(
        start=dates.iloc[-1] + timedelta(weeks=1),
        periods=fwd_weeks,
        freq='W-MON'
    )

    return dict(
        slope      = slope,
        st_slope   = st_sl,
        r2         = r ** 2,
        trend_line = fitted,
        fc_mid     = fc_mid,
        fc_upper   = fc_mid + ci,
        fc_lower   = fc_mid - ci,
        fc_dates   = fc_dates,
        pct_6m     = st_sl * 26 / y[-1] * 100,
        pct_12m    = st_sl * 52 / y[-1] * 100,
        pct_total  = (y[-1] - y[0]) / y[0] * 100,
        current    = y[-1],
    )

def classify(pct_6m: float) -> tuple:
    if pct_6m >  10: return "Alta Forte",  "🔴", "#e74c3c"
    if pct_6m >   4: return "Alta",        "🟠", "#e67e22"
    if pct_6m >   1: return "Leve Alta",   "🟡", "#f39c12"
    if pct_6m < -10: return "Queda Forte", "🟢", "#27ae60"
    if pct_6m <  -4: return "Queda",       "🔵", "#2980b9"
    if pct_6m <  -1: return "Leve Queda",  "🩵", "#5dade2"
    return               "Estável",        "⚪", "#95a5a6"

def get_color(name: str) -> str:
    for cat in PRODUCTS.values():
        if name in cat:
            return cat[name]['color']
    return '#888888'

# ─────────────────────────── CHART HELPERS ─────────────────────────────
DARK = dict(paper_bgcolor='#1a1a2e', plot_bgcolor='#16213e')

def _add_event_lines(fig, x_min, x_max, show=True):
    if not show:
        return
    for ev in EVENTS:
        dt = pd.Timestamp(ev['dt'])
        if x_min <= dt <= x_max:
            fig.add_vline(
                x=dt.timestamp() * 1000,
                line_dash='dot', line_color=ev['color'],
                line_width=1.2, opacity=.55
            )
            fig.add_annotation(
                x=dt, yref='paper', y=1.01,
                text=ev['label'], showarrow=False,
                font=dict(size=9, color=ev['color']),
                textangle=-40
            )

def make_product_chart(df: pd.DataFrame, name: str,
                       show_events=True, show_fc=True, show_ma=True) -> go.Figure:
    ta  = trend_analysis(df[name], df['Data'])
    lbl, emo, clr_t = classify(ta['pct_6m'])
    clr = get_color(name)

    fig = go.Figure()

    if show_ma:
        for weeks, dash, color in [(52, 'dash', 'gold'), (26, 'dot', 'orange')]:
            ma = df[name].rolling(weeks, min_periods=4).mean()
            fig.add_trace(go.Scatter(
                x=df['Data'], y=ma,
                name=f'MM {weeks}sem',
                line=dict(color=color, width=1.5, dash=dash),
                hovertemplate='%{y:,.0f}'
            ))

    fig.add_trace(go.Scatter(
        x=df['Data'], y=ta['trend_line'],
        name='Tendência', mode='lines',
        line=dict(color='rgba(255,255,255,.5)', width=1.5, dash='longdash'),
    ))

    fig.add_trace(go.Scatter(
        x=df['Data'], y=df[name],
        name=name, fill='tozeroy',
        line=dict(color=clr, width=2),
        fillcolor=clr + '1a',
        hovertemplate='<b>%{x|%d/%m/%Y}</b><br>R$ %{y:,.0f}/ton<extra></extra>'
    ))

    if show_fc:
        fc_x = pd.concat([df['Data'].tail(1).reset_index(drop=True),
                          pd.Series(ta['fc_dates'])])
        fc_y = np.concatenate([[ta['current']], ta['fc_mid']])
        fc_u = np.concatenate([[ta['current']], ta['fc_upper']])
        fc_l = np.concatenate([[ta['current']], ta['fc_lower']])

        fig.add_trace(go.Scatter(
            x=fc_x, y=fc_u,
            mode='lines', line=dict(width=0, color=clr),
            showlegend=False, hoverinfo='skip'
        ))
        fig.add_trace(go.Scatter(
            x=fc_x, y=fc_l,
            mode='lines', line=dict(width=0, color=clr),
            fill='tonexty', fillcolor=clr + '28',
            name='IC 95%',
            hovertemplate='IC 95%: R$ %{y:,.0f}<extra></extra>'
        ))
        fig.add_trace(go.Scatter(
            x=fc_x, y=fc_y,
            name='Projeção 12m',
            line=dict(color=clr, width=2.5, dash='dash'),
            hovertemplate='<b>Projeção %{x|%d/%m/%Y}</b><br>R$ %{y:,.0f}/ton<extra></extra>'
        ))

    x_max = (pd.Timestamp(ta['fc_dates'][-1]) if show_fc else df['Data'].max())
    _add_event_lines(fig, df['Data'].min(), x_max, show_events)

    fig.update_layout(
        **DARK,
        title=dict(
            text=(f"<b>{name}</b>  {emo} "
                  f"<span style='color:{clr_t}'>{lbl}</span>  "
                  f"<span style='font-size:12px;color:#aaa'>"
                  f"R$ {ta['current']:,.0f}/ton  |  "
                  f"Δ6m projetado: {ta['pct_6m']:+.1f}%  |  "
                  f"Δ total 2020: {ta['pct_total']:+.1f}%</span>"),
            font=dict(size=15)
        ),
        xaxis=dict(showgrid=True, gridcolor='#2a2a45', zeroline=False),
        yaxis=dict(title='R$/ton', showgrid=True, gridcolor='#2a2a45',
                   zeroline=False, tickformat=',.0f'),
        height=430,
        hovermode='x unified',
        legend=dict(orientation='h', y=-.14, x=0, font=dict(size=11)),
        margin=dict(t=80, b=95, l=70, r=20)
    )
    return fig

def make_comparison_chart(df, names, title, normalize=False) -> go.Figure:
    fig = go.Figure()
    for name in names:
        clr = get_color(name)
        y   = df[name].values.copy().astype(float)
        if normalize:
            y = y / y[0] * 100
        fig.add_trace(go.Scatter(
            x=df['Data'], y=y, name=name,
            line=dict(color=clr, width=2),
            hovertemplate=(
                '<b>%{x|%d/%m/%Y}</b><br>' + name + ': %{y:,.1f}'
                + (' (base 100)' if normalize else ' R$/ton')
                + '<extra></extra>'
            )
        ))
    _add_event_lines(fig, df['Data'].min(), df['Data'].max(), True)
    fig.update_layout(
        **DARK,
        title=dict(text=f'<b>{title}</b>', font=dict(size=14)),
        xaxis=dict(showgrid=True, gridcolor='#2a2a45'),
        yaxis=dict(
            title='Índice (Jan/2020 = 100)' if normalize else 'R$/ton',
            showgrid=True, gridcolor='#2a2a45', tickformat=',.0f'
        ),
        height=450, hovermode='x unified',
        legend=dict(orientation='h', y=-.18, x=0, font=dict(size=10)),
        margin=dict(t=60, b=115, l=70, r=20)
    )
    return fig

def make_trend_bar(df) -> tuple:
    rows = []
    for cat, prods in PRODUCTS.items():
        for name in prods:
            ta  = trend_analysis(df[name], df['Data'])
            lbl, emo, clr = classify(ta['pct_6m'])
            rows.append(dict(
                Produto=name, Categoria=cat,
                pct_6m=ta['pct_6m'], pct_12m=ta['pct_12m'],
                pct_total=ta['pct_total'],
                current=ta['current'],
                lbl=lbl, emo=emo, clr=clr,
            ))
    df_s = pd.DataFrame(rows).sort_values('pct_6m')

    fig = go.Figure(go.Bar(
        y=df_s['Produto'],
        x=df_s['pct_6m'],
        orientation='h',
        marker_color=df_s['clr'].tolist(),
        text=[f"{v:+.1f}%" for v in df_s['pct_6m']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Δ6m projetado: %{x:+.1f}%<extra></extra>'
    ))
    fig.add_vline(x=0, line_color='white', line_width=1.5)
    fig.update_layout(
        **DARK,
        title='<b>Variação Projetada — Próximos 6 Meses (base: tendência recente)</b>',
        xaxis=dict(title='Variação (%)', ticksuffix='%',
                   showgrid=True, gridcolor='#2a2a45'),
        yaxis=dict(autorange='reversed'),
        height=430,
        margin=dict(t=60, b=60, l=20, r=70)
    )
    return fig, df_s

def make_corr_heatmap(df) -> go.Figure:
    corr = df[ALL_NAMES].corr()
    fig  = px.imshow(
        corr, text_auto='.2f',
        color_continuous_scale='RdBu_r', zmin=-1, zmax=1,
        title='<b>Matriz de Correlação de Preços (2020 – hoje)</b>'
    )
    fig.update_layout(**DARK, height=530, font=dict(size=10))
    return fig

# ─────────────────────────── SIDEBAR ───────────────────────────────────
df_full = build_dataset()

with st.sidebar:
    st.markdown("## ⚙️ Configurações")
    st.markdown("---")
    st.markdown("### 📅 Período de análise")
    dmin = df_full['Data'].min().date()
    dmax = df_full['Data'].max().date()
    dr   = st.date_input("Intervalo de datas", value=(dmin, dmax),
                         min_value=dmin, max_value=dmax)
    st.markdown("---")
    st.markdown("### 🌾 Farinhas")
    sel_f = {n: st.checkbox(n, value=True, key=f'f_{n}') for n in PRODUCTS['Farinhas']}
    st.markdown("### 🛢️ Gorduras")
    sel_g = {n: st.checkbox(n, value=True, key=f'g_{n}') for n in PRODUCTS['Gorduras']}
    st.markdown("---")
    show_ev  = st.toggle("Eventos de mercado",    value=True)
    show_fc  = st.toggle("Projeção 12 meses",      value=True)
    show_ma  = st.toggle("Médias móveis",          value=True)
    norm_cmp = st.toggle("Normalizar (base 100)",  value=False)
    st.markdown("---")
    st.markdown("""
    <small>
    📌 <b>Fontes de referência:</b><br>
    ANFAR · ABRA · CEPEA/ESALQ · MDIC<br><br>
    ⚠️ Dados <b>simulados</b> baseados em
    tendências reais do mercado brasileiro.
    Consulte ANFAR/CEPEA para dados oficiais.
    </small>""", unsafe_allow_html=True)

# Apply date filter
if isinstance(dr, (list, tuple)) and len(dr) == 2:
    df = df_full[
        (df_full['Data'] >= pd.Timestamp(dr[0])) &
        (df_full['Data'] <= pd.Timestamp(dr[1]))
    ].reset_index(drop=True)
else:
    df = df_full.reset_index(drop=True)

# Active products
sel_all      = {**{k: v for k, v in sel_f.items() if v},
                **{k: v for k, v in sel_g.items() if v}}
active_names = list(sel_all.keys())
actf         = [n for n, v in sel_f.items() if v]
actg         = [n for n, v in sel_g.items() if v]

# ─────────────────────────── HEADER ────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#0f2027,#203a43,#2c5364);
            padding:22px 30px;border-radius:14px;margin-bottom:22px;
            box-shadow:0 4px 20px rgba(0,0,0,.35)">
  <h1 style="color:white!important;margin:0;font-size:1.75rem;font-weight:800">
    📊 Monitor de Preços — Farinhas &amp; Gorduras Animais
  </h1>
  <p style="color:#b8d4f0;margin:6px 0 0;font-size:.97rem">
    Variação histórica de preços no mercado brasileiro &nbsp;|&nbsp;
    Jan 2020 – hoje &nbsp;|&nbsp; Tendências &amp; Projeções
  </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────── KPI CARDS ─────────────────────────────────
if active_names:
    st.markdown("### 📌 Situação Atual & Tendências")
    n_per_row = 5
    for i in range(0, len(active_names), n_per_row):
        batch = active_names[i:i + n_per_row]
        cols  = st.columns(len(batch))
        for col, name in zip(cols, batch):
            ta  = trend_analysis(df[name], df['Data'])
            lbl, emo, clr_t = classify(ta['pct_6m'])
            clr = get_color(name)
            with col:
                st.markdown(f"""
                <div class="kpi-card" style="border-top-color:{clr}">
                  <div class="kpi-title">{name}</div>
                  <div class="kpi-value">R$ {ta['current']:,.0f}</div>
                  <div class="kpi-delta" style="color:{clr_t}">{emo} {lbl}</div>
                  <div class="kpi-info">
                    Δ6m: <b>{ta['pct_6m']:+.1f}%</b>
                    &nbsp;|&nbsp;
                    Δ total: <b>{ta['pct_total']:+.1f}%</b>
                  </div>
                </div>
                """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────── TABS ──────────────────────────────────────
tab_f, tab_g, tab_cmp, tab_trend, tab_corr = st.tabs([
    "🌾 Farinhas",
    "🛢️ Gorduras",
    "📊 Comparativo",
    "📈 Tendências & Projeções",
    "🔗 Correlações",
])

# ── Tab: Farinhas ──────────────────────────────────────────────────────
with tab_f:
    if not actf:
        st.warning("Selecione ao menos uma farinha na barra lateral.")
    else:
        for name in actf:
            st.plotly_chart(
                make_product_chart(df, name, show_ev, show_fc, show_ma),
                use_container_width=True
            )

# ── Tab: Gorduras ──────────────────────────────────────────────────────
with tab_g:
    if not actg:
        st.warning("Selecione ao menos uma gordura na barra lateral.")
    else:
        for name in actg:
            st.plotly_chart(
                make_product_chart(df, name, show_ev, show_fc, show_ma),
                use_container_width=True
            )

# ── Tab: Comparativo ──────────────────────────────────────────────────
with tab_cmp:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🌾 Farinhas")
        if actf:
            st.plotly_chart(
                make_comparison_chart(df, actf, "Farinhas Animais", norm_cmp),
                use_container_width=True
            )
        else:
            st.info("Nenhuma farinha selecionada.")
    with c2:
        st.markdown("#### 🛢️ Gorduras")
        if actg:
            st.plotly_chart(
                make_comparison_chart(df, actg, "Gorduras Animais", norm_cmp),
                use_container_width=True
            )
        else:
            st.info("Nenhuma gordura selecionada.")

    st.markdown("#### 🔀 Todos os ingredientes juntos")
    all_act = actf + actg
    if all_act:
        st.plotly_chart(
            make_comparison_chart(df, all_act, "Farinhas & Gorduras — Visão Geral", norm_cmp),
            use_container_width=True
        )

# ── Tab: Tendências & Projeções ────────────────────────────────────────
with tab_trend:
    st.markdown("""
    <div class="info-box">
    ⚠️ Projeções calculadas pela tendência linear dos últimos 6 meses e extrapoladas para os próximos
    6 e 12 meses. Intervalo de confiança de 95% mostrado nas faixas sombreadas. Não consideram choques
    externos imprevistos — use como orientação estratégica.
    </div>""", unsafe_allow_html=True)

    fig_bar, df_s = make_trend_bar(df)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("#### 📋 Tabela Resumo de Tendências")
    tbl = df_s[['Produto', 'Categoria', 'current', 'pct_6m', 'pct_12m', 'pct_total', 'lbl']].copy()
    tbl.columns = ['Produto', 'Categoria', 'Preço Atual (R$/ton)',
                   'Δ 6 meses (%)', 'Δ 12 meses (%)', 'Δ Total 2020 (%)', 'Tendência']
    tbl['Preço Atual (R$/ton)'] = tbl['Preço Atual (R$/ton)'].apply(lambda x: f"R$ {x:,.0f}")
    tbl['Δ 6 meses (%)']        = tbl['Δ 6 meses (%)'].apply(lambda x: f"{x:+.1f}%")
    tbl['Δ 12 meses (%)']       = tbl['Δ 12 meses (%)'].apply(lambda x: f"{x:+.1f}%")
    tbl['Δ Total 2020 (%)']     = tbl['Δ Total 2020 (%)'].apply(lambda x: f"{x:+.1f}%")
    st.dataframe(tbl.set_index('Produto'), use_container_width=True)

    st.markdown("#### 🔍 Projeção Individual Detalhada")
    if active_names:
        picked = st.selectbox("Selecionar produto:", active_names)
        st.plotly_chart(
            make_product_chart(df, picked, True, True, True),
            use_container_width=True
        )
        ta  = trend_analysis(df[picked], df['Data'])
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Preço Atual",         f"R$ {ta['current']:,.0f}")
        m2.metric("Projeção 6 meses",    f"R$ {ta['current']*(1+ta['pct_6m']/100):,.0f}",  f"{ta['pct_6m']:+.1f}%")
        m3.metric("Projeção 12 meses",   f"R$ {ta['current']*(1+ta['pct_12m']/100):,.0f}", f"{ta['pct_12m']:+.1f}%")
        m4.metric("Δ Total desde 2020",  f"{ta['pct_total']:+.1f}%")

# ── Tab: Correlações ──────────────────────────────────────────────────
with tab_corr:
    st.markdown(
        "Valores próximos de **+1** indicam que os preços sobem e caem juntos. "
        "**−1** indica movimentos opostos."
    )
    st.plotly_chart(make_corr_heatmap(df), use_container_width=True)

    st.markdown("#### 🔍 Dispersão entre dois ingredientes")
    c1, c2 = st.columns(2)
    with c1:
        px1 = st.selectbox("Ingrediente X:", ALL_NAMES, index=0)
    with c2:
        default_y = min(5, len(ALL_NAMES) - 1)
        px2 = st.selectbox("Ingrediente Y:", ALL_NAMES, index=default_y)

    if px1 != px2:
        x_vals = df[px1].values.astype(float)
        y_vals = df[px2].values.astype(float)
        sl, ic, r, pv, _ = stats.linregress(x_vals, y_vals)
        x_rng = np.linspace(x_vals.min(), x_vals.max(), 200)

        fig_sc = go.Figure()
        fig_sc.add_trace(go.Scatter(
            x=x_vals, y=y_vals, mode='markers',
            marker=dict(
                color=np.arange(len(df)), colorscale='Blues',
                size=4, opacity=.7,
                colorbar=dict(title='Semana')
            ),
            hovertemplate=f'{px1}: R$ %{{x:,.0f}}<br>{px2}: R$ %{{y:,.0f}}<extra></extra>'
        ))
        fig_sc.add_trace(go.Scatter(
            x=x_rng, y=sl * x_rng + ic,
            mode='lines',
            line=dict(color='red', dash='dash', width=2),
            name=f'Regressão  r = {r:.3f}'
        ))
        fig_sc.update_layout(
            **DARK,
            title=f'<b>{px1}</b>  ×  <b>{px2}</b>  —  Correlação: {r:.3f}',
            xaxis_title=f'{px1} (R$/ton)',
            yaxis_title=f'{px2} (R$/ton)',
            xaxis=dict(tickformat=',.0f'),
            yaxis=dict(tickformat=',.0f'),
            height=430,
            margin=dict(t=65, b=60, l=75, r=20)
        )
        st.plotly_chart(fig_sc, use_container_width=True)
    else:
        st.info("Selecione dois ingredientes diferentes.")

# ─────────────────────────── FOOTER ────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#999;font-size:.82rem;padding:8px 0">
  <b>Monitor de Preços — Farinhas &amp; Gorduras Animais</b> &nbsp;|&nbsp;
  Mercado Brasileiro 2020–2026 &nbsp;|&nbsp;
  Dados simulados com base em tendências reais &nbsp;·&nbsp;
  Referências oficiais:
  <a href="https://www.anfar.org.br" style="color:#6aacff">ANFAR</a> &nbsp;·&nbsp;
  <a href="https://www.cepea.esalq.usp.br" style="color:#6aacff">CEPEA/ESALQ</a> &nbsp;·&nbsp;
  <a href="https://www.mdic.gov.br" style="color:#6aacff">MDIC</a>
</div>
""", unsafe_allow_html=True)
