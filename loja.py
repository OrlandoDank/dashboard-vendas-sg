import streamlit as st
import urllib.parse
import base64
from pathlib import Path
from omie_api import buscar_catalogo_produtos
import datetime

WHATSAPP = "5541987109563"

def _logo_b64() -> str:
    p = Path(__file__).parent / "logo.jpg"
    return base64.b64encode(p.read_bytes()).decode() if p.exists() else ""

st.set_page_config(
    page_title="SG Bichos — Loja",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

_LOGO = _logo_b64()

st.markdown("""
<style>
  [data-testid="stAppViewContainer"] { background: #f5f5f5; }
  [data-testid="stHeader"] { background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
  section[data-testid="stSidebar"],
  [data-testid="stSidebarCollapsedControl"] { display: none !important; }
  footer, #MainMenu { visibility: hidden; }
  .block-container { padding-top: 1.5rem !important; max-width: 1180px; }

  /* Header */
  .loja-header {
    display: flex; align-items: center; gap: 18px;
    padding: 18px 24px;
    background: white;
    border-radius: 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    margin-bottom: 28px;
  }
  .loja-nome  { font-size: 23px; font-weight: 800; color: #1a1f36; margin: 0; }
  .loja-sub   { font-size: 12px; color: #8892a4; margin: 2px 0 0; }

  /* Banner de WhatsApp */
  .wa-banner {
    background: linear-gradient(135deg,#25D366,#128C7E);
    border-radius: 14px;
    padding: 18px 24px;
    color: white;
    display: flex; align-items: center; gap: 16px;
    margin-bottom: 28px;
    text-decoration: none !important;
  }
  .wa-banner-txt { font-size: 15px; font-weight: 700; }
  .wa-banner-sub { font-size: 12px; opacity: 0.88; margin: 2px 0 0; }

  /* Título de seção */
  .sec-title {
    font-size: 17px; font-weight: 700; color: #1a1f36;
    margin: 0 0 20px; padding-bottom: 10px;
    border-bottom: 2px solid #eee;
    display: flex; align-items: baseline; gap: 10px;
  }
  .sec-count { font-size: 13px; font-weight: 400; color: #aaa; }

  /* Card de produto */
  .prod-card {
    background: white;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    margin-bottom: 20px;
    display: flex; flex-direction: column;
  }
  .prod-thumb {
    height: 150px;
    display: flex; align-items: center; justify-content: center;
    font-size: 52px;
  }
  .prod-body { padding: 14px 16px 16px; flex: 1; display: flex; flex-direction: column; }
  .prod-nome {
    font-size: 13px; font-weight: 600; color: #1a1f36;
    line-height: 1.35; margin: 0 0 4px; min-height: 36px;
    display: -webkit-box; -webkit-line-clamp: 2;
    -webkit-box-orient: vertical; overflow: hidden;
  }
  .prod-cod  { font-size: 11px; color: #bbb; margin: 0 0 10px; }
  .prod-preco { font-size: 22px; font-weight: 800; color: #1a1f36; margin: 0 0 14px; flex: 1; }
  .prod-btn {
    display: block;
    padding: 11px 12px;
    background: #25D366;
    color: white !important;
    border-radius: 9px;
    font-size: 13px; font-weight: 700;
    text-align: center; text-decoration: none !important;
    letter-spacing: 0.2px;
  }
  .prod-btn:hover { background: #1fb85a; }

  /* Empty state */
  .empty { text-align: center; padding: 60px 20px; color: #aaa; }

  /* Footer */
  .loja-footer {
    margin-top: 48px; padding: 28px;
    background: #1a1f36; color: #8892a4;
    text-align: center; border-radius: 16px; font-size: 13px; line-height: 1.9;
  }
  .loja-footer a { color: #25D366; text-decoration: none; font-weight: 600; }

  @media (max-width: 768px) {
    .block-container { padding-left: 0.8rem !important; padding-right: 0.8rem !important; }
  }
</style>
""", unsafe_allow_html=True)


# ── HEADER ─────────────────────────────────────────────────────
logo_tag = (
    f'<img src="data:image/jpeg;base64,{_LOGO}" '
    'style="width:54px;height:54px;object-fit:contain;border-radius:10px;'
    'background:#f5f5f5;padding:4px;flex-shrink:0;">'
    if _LOGO else '<span style="font-size:40px;">🐾</span>'
)
st.markdown(f"""
<div class="loja-header">
  {logo_tag}
  <div>
    <p class="loja-nome">SG Bichos</p>
    <p class="loja-sub">Tudo para o seu pet com qualidade e carinho 🐾</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── BANNER WHATSAPP ─────────────────────────────────────────────
wa_banner = f"https://wa.me/{WHATSAPP}?text={urllib.parse.quote('Olá! Gostaria de saber mais sobre os produtos da SG Bichos.')}"
st.markdown(f"""
<a href="{wa_banner}" target="_blank" class="wa-banner">
  <span style="font-size:30px;">💬</span>
  <div>
    <p class="wa-banner-txt">Atendimento via WhatsApp</p>
    <p class="wa-banner-sub">Tire suas dúvidas com nossos especialistas · +55 41 98710-9563</p>
  </div>
  <span style="margin-left:auto;font-size:22px;">→</span>
</a>
""", unsafe_allow_html=True)


# ── DADOS ───────────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def _get_catalogo():
    return buscar_catalogo_produtos()

with st.spinner("Carregando produtos..."):
    df = _get_catalogo()

import unicodedata as _ud

def _norm(s: str) -> str:
    return _ud.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().strip()

_FAMILIAS_EXCLUIR = {_norm(f) for f in [
    "Laços", "Limpeza", "Inativos", "Papeis", "Coleira",
    "Gravatas", "Bonificação", "Gargantilhas", "Bandanas", "Apliques",
]}

df = df[
    (df["valor_venda"] > 0) &
    (df["inativo"] != "S") &
    (~df["familia"].apply(lambda f: _norm(str(f)) in _FAMILIAS_EXCLUIR))
].reset_index(drop=True)


# ── BUSCA ───────────────────────────────────────────────────────
busca = st.text_input(
    "", placeholder="🔍  Buscar produto...",
    label_visibility="collapsed",
)
if busca:
    df = df[df["descricao"].str.contains(busca, case=False, na=False)].reset_index(drop=True)

st.markdown(
    f'<div class="sec-title">Nossos Produtos <span class="sec-count">{len(df)} itens</span></div>',
    unsafe_allow_html=True,
)


# ── HELPERS ─────────────────────────────────────────────────────
def _thumb(nome: str) -> tuple:
    n = nome.lower()
    if any(w in n for w in ["ração", "racao", "alimento", "snack", "petisco", "trato"]):
        return "🍖", "linear-gradient(135deg,#fff3e0,#ffe0b2)"
    if any(w in n for w in ["coleira", "guia", "peitoral", "cinto"]):
        return "🦮", "linear-gradient(135deg,#e8f5e9,#c8e6c9)"
    if any(w in n for w in ["brinquedo", "bola", "corda", "pelúcia"]):
        return "🎾", "linear-gradient(135deg,#e3f2fd,#bbdefb)"
    if any(w in n for w in ["cama", "canil", "manta", "coberta", "almofad"]):
        return "🛏️", "linear-gradient(135deg,#f3e5f5,#e1bee7)"
    if any(w in n for w in ["shampoo", "condicionador", "banho", "higiene", "perfume"]):
        return "🚿", "linear-gradient(135deg,#e0f7fa,#b2ebf2)"
    if any(w in n for w in ["vacina", "vermifugo", "medicament", "antiparasit", "remedio"]):
        return "💊", "linear-gradient(135deg,#fce4ec,#f8bbd0)"
    if any(w in n for w in ["gato", "cat", "felino"]):
        return "🐱", "linear-gradient(135deg,#fff8e1,#ffecb3)"
    if any(w in n for w in ["peixe", "aquario", "aquário"]):
        return "🐠", "linear-gradient(135deg,#e0f7fa,#b2ebf2)"
    if any(w in n for w in ["passaro", "pássaro", "ave"]):
        return "🐦", "linear-gradient(135deg,#e8f5e9,#c8e6c9)"
    return "🐾", "linear-gradient(135deg,#fce4ec,#f8bbd0)"


def _brl(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _wa_url(prod: dict) -> str:
    cod = prod["codigo_interno"] or str(prod["codigo_produto"])
    msg = (
        f"Olá! Tenho interesse em comprar:\n\n"
        f"*{prod['descricao']}*\n"
        f"Código: {cod}\n"
        f"Preço: {_brl(prod['valor_venda'])}\n\n"
        "Poderia me ajudar? 😊"
    )
    return f"https://wa.me/{WHATSAPP}?text={urllib.parse.quote(msg)}"


# ── GRID DE PRODUTOS ────────────────────────────────────────────
if df.empty:
    st.markdown('<div class="empty"><p style="font-size:48px">🔍</p><p>Nenhum produto encontrado.</p></div>', unsafe_allow_html=True)
else:
    COLS = 4
    produtos = df.to_dict("records")
    for i in range(0, len(produtos), COLS):
        cols = st.columns(COLS)
        for j, prod in enumerate(produtos[i : i + COLS]):
            with cols[j]:
                emoji, grad = _thumb(prod["descricao"])
                wa = _wa_url(prod)
                cod_display = prod["codigo_interno"] or str(prod["codigo_produto"])
                st.markdown(f"""
<div class="prod-card">
  <div class="prod-thumb" style="background:{grad};">{emoji}</div>
  <div class="prod-body">
    <p class="prod-nome">{prod['descricao']}</p>
    <p class="prod-cod">Cód: {cod_display}</p>
    <p class="prod-preco">{_brl(prod['valor_venda'])}</p>
    <a href="{wa}" target="_blank" class="prod-btn">📲 Pedir via WhatsApp</a>
  </div>
</div>
""", unsafe_allow_html=True)


# ── FOOTER ──────────────────────────────────────────────────────
ano = datetime.date.today().year
wa_home = f"https://wa.me/{WHATSAPP}"
st.markdown(f"""
<div class="loja-footer">
  <p style="font-size:16px;font-weight:800;color:white;margin:0 0 6px;">SG Bichos</p>
  <p>Fale conosco: <a href="{wa_home}">WhatsApp +55 41 98710-9563</a></p>
  <p style="margin:0;font-size:11px;opacity:0.6;">© {ano} SG Bichos. Todos os direitos reservados.</p>
</div>
""", unsafe_allow_html=True)
