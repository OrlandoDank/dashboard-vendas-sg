import streamlit as st
import urllib.parse
import base64
import unicodedata as _ud
from pathlib import Path
from omie_api import buscar_catalogo_produtos
import datetime

WHATSAPP  = "5541987109563"
ROOT      = Path(__file__).parent
IMGS_DIR  = ROOT / "imagens"
IMGS_DIR.mkdir(exist_ok=True)


# ── CONFIG ──────────────────────────────────────────────────────
def _logo_b64() -> str:
    p = ROOT / "logo.jpg"
    return base64.b64encode(p.read_bytes()).decode() if p.exists() else ""

st.set_page_config(
    page_title="SG Bichos",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

_LOGO = _logo_b64()


# ── CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* ── reset ── */
  [data-testid="stAppViewContainer"] { background: #ffffff; font-family: 'Segoe UI', Arial, sans-serif; }
  [data-testid="stHeader"] { background: #ffffff; }
  section[data-testid="stSidebar"],
  [data-testid="stSidebarCollapsedControl"] { display: none !important; }
  footer, #MainMenu { visibility: hidden; }
  .block-container { padding: 0 !important; max-width: 100% !important; }
  div[data-testid="stVerticalBlock"] > div { gap: 0 !important; }

  /* ── barra topo navy ── */
  .top-bar {
    background: #1a2538;
    color: #c8ccd8;
    text-align: center;
    font-size: 12px;
    padding: 8px 16px;
    letter-spacing: 0.4px;
  }
  .top-bar a { color: #a8e6bf; text-decoration: none; font-weight: 600; }

  /* ── header ── */
  .site-header {
    background: #ffffff;
    border-bottom: 1px solid #eee;
    padding: 20px 48px;
    display: flex;
    align-items: center;
    gap: 20px;
  }
  .site-logo {
    width: 56px; height: 56px;
    object-fit: contain;
    border-radius: 8px;
    flex-shrink: 0;
  }
  .site-title { font-size: 22px; font-weight: 800; color: #1a2538; margin: 0; line-height: 1.1; }
  .site-sub   { font-size: 11px; color: #999; margin: 3px 0 0; letter-spacing: 0.3px; }

  /* ── barra de benefícios ── */
  .benefits {
    background: #f8f4ef;
    display: flex;
    justify-content: center;
    gap: 0;
    padding: 0;
  }
  .benefit-item {
    flex: 1;
    display: flex; align-items: center; gap: 14px;
    padding: 18px 32px;
    border-right: 1px solid #ece8e2;
  }
  .benefit-item:last-child { border-right: none; }
  .benefit-icon { font-size: 26px; flex-shrink: 0; }
  .benefit-title { font-size: 13px; font-weight: 700; color: #1a2538; margin: 0; }
  .benefit-sub   { font-size: 11px; color: #888; margin: 2px 0 0; }

  /* ── área de produtos ── */
  .produtos-area {
    max-width: 1280px;
    margin: 0 auto;
    padding: 32px 32px 64px;
  }
  .produtos-header {
    display: flex; align-items: baseline; justify-content: space-between;
    margin-bottom: 24px;
    padding-bottom: 12px;
    border-bottom: 1px solid #eee;
  }
  .produtos-titulo { font-size: 18px; font-weight: 700; color: #1a2538; margin: 0; }
  .produtos-count  { font-size: 13px; color: #aaa; }

  /* ── busca ── */
  .stTextInput > div > div > input {
    border: 1.5px solid #e0e0e0 !important;
    border-radius: 6px !important;
    padding: 10px 14px !important;
    font-size: 14px !important;
    background: #fafafa !important;
    color: #1a2538 !important;
    box-shadow: none !important;
  }
  .stTextInput > div > div > input:focus {
    border-color: #1a2538 !important;
    background: #fff !important;
  }

  /* ── card de produto ── */
  .prod-card {
    background: #ffffff;
    cursor: pointer;
    margin-bottom: 28px;
  }
  .prod-img-wrap {
    width: 100%;
    aspect-ratio: 1 / 1;
    overflow: hidden;
    background: #f5f0ea;
    position: relative;
  }
  .prod-img-wrap img {
    width: 100%; height: 100%;
    object-fit: cover;
    transition: transform 0.35s ease;
    display: block;
  }
  .prod-card:hover .prod-img-wrap img { transform: scale(1.05); }
  .prod-img-placeholder {
    width: 100%; height: 100%;
    display: flex; align-items: center; justify-content: center;
    font-size: 64px;
  }
  .prod-info { padding: 12px 2px 0; }
  .prod-nome {
    font-size: 13px; font-weight: 500; color: #1a1a1a;
    line-height: 1.35; margin: 0 0 5px;
    min-height: 36px;
    display: -webkit-box; -webkit-line-clamp: 2;
    -webkit-box-orient: vertical; overflow: hidden;
  }
  .prod-cod  { font-size: 10px; color: #ccc; margin: 0 0 6px; letter-spacing: 0.3px; }
  .prod-preco { font-size: 15px; font-weight: 700; color: #1a2538; margin: 0 0 12px; }
  .prod-btn {
    display: block;
    padding: 9px 12px;
    background: #1a2538;
    color: #ffffff !important;
    text-align: center;
    font-size: 11px; font-weight: 700;
    text-decoration: none !important;
    letter-spacing: 1px;
    text-transform: uppercase;
    border-radius: 3px;
    transition: background 0.2s;
  }
  .prod-btn:hover { background: #25D366; }

  /* ── empty state ── */
  .empty-state {
    text-align: center; padding: 80px 20px; color: #bbb;
    font-size: 14px;
  }

  /* ── footer ── */
  .site-footer {
    background: #1a2538;
    color: #8892a4;
    text-align: center;
    padding: 40px 32px;
    font-size: 13px;
    line-height: 2;
  }
  .site-footer-title { font-size: 18px; font-weight: 800; color: #fff; margin: 0 0 8px; }
  .site-footer a { color: #a8e6bf; text-decoration: none; font-weight: 600; }
  .site-footer-copy { font-size: 11px; opacity: 0.45; margin: 12px 0 0; }

  @media (max-width: 900px) {
    .site-header { padding: 14px 16px; }
    .produtos-area { padding: 20px 12px 48px; }
    .benefit-item { padding: 14px 16px; }
  }
</style>
""", unsafe_allow_html=True)


# ── BARRA TOPO ──────────────────────────────────────────────────
wa_home = f"https://wa.me/{WHATSAPP}"
st.markdown(f"""
<div class="top-bar">
  Atendimento via WhatsApp &nbsp;·&nbsp;
  <a href="{wa_home}" target="_blank">+55 41 98710-9563</a>
  &nbsp;·&nbsp; Entregamos para todo o Brasil 🐾
</div>
""", unsafe_allow_html=True)


# ── HEADER ──────────────────────────────────────────────────────
logo_img = (
    f'<img class="site-logo" src="data:image/jpeg;base64,{_LOGO}">'
    if _LOGO else '<span style="font-size:48px;">🐾</span>'
)
st.markdown(f"""
<div class="site-header">
  {logo_img}
  <div>
    <p class="site-title">SG Bichos</p>
    <p class="site-sub">PRODUTOS PARA PETS COM QUALIDADE E CARINHO</p>
  </div>
</div>
""", unsafe_allow_html=True)


# ── BENEFÍCIOS ──────────────────────────────────────────────────
st.markdown(f"""
<div class="benefits">
  <div class="benefit-item">
    <span class="benefit-icon">🚚</span>
    <div>
      <p class="benefit-title">Entregamos em todo o Brasil</p>
      <p class="benefit-sub">Receba com agilidade e comodidade</p>
    </div>
  </div>
  <div class="benefit-item">
    <span class="benefit-icon">💬</span>
    <div>
      <p class="benefit-title">Fale com a gente</p>
      <p class="benefit-sub">Atendimento via WhatsApp</p>
    </div>
  </div>
  <div class="benefit-item">
    <span class="benefit-icon">🐾</span>
    <div>
      <p class="benefit-title">Produtos selecionados</p>
      <p class="benefit-sub">Qualidade e cuidado para seu pet</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── DADOS ───────────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def _get_catalogo():
    return buscar_catalogo_produtos()

with st.spinner("Carregando produtos..."):
    df = _get_catalogo()

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


# ── HELPERS ─────────────────────────────────────────────────────
def _thumb(nome: str) -> tuple:
    n = nome.lower()
    if any(w in n for w in ["ração", "racao", "alimento", "snack", "petisco", "trato"]):
        return "🍖", "#fff3e0"
    if any(w in n for w in ["shampoo", "condicionador", "banho", "higiene", "perfume"]):
        return "🚿", "#e0f7fa"
    if any(w in n for w in ["brinquedo", "bola", "corda", "pelúcia"]):
        return "🎾", "#e3f2fd"
    if any(w in n for w in ["cama", "canil", "manta", "coberta", "almofad"]):
        return "🛏️", "#f3e5f5"
    if any(w in n for w in ["vacina", "vermifugo", "medicament", "antiparasit"]):
        return "💊", "#fce4ec"
    if any(w in n for w in ["gato", "cat", "felino"]):
        return "🐱", "#fff8e1"
    if any(w in n for w in ["peixe", "aquario", "aquário"]):
        return "🐠", "#e0f7fa"
    return "🐾", "#f5f0ea"


def _brl(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _img_tag(codigo: str, emoji: str, bg: str) -> str:
    """Retorna tag <img> com foto real ou placeholder colorido com emoji."""
    for ext in ("jpg", "jpeg", "png", "webp"):
        p = IMGS_DIR / f"{codigo}.{ext}"
        if p.exists():
            mime = "png" if ext == "png" else "webp" if ext == "webp" else "jpeg"
            b64 = base64.b64encode(p.read_bytes()).decode()
            return f'<img src="data:image/{mime};base64,{b64}" alt="">'
    return f'<div class="prod-img-placeholder" style="background:{bg};">{emoji}</div>'


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


# ── ÁREA DE PRODUTOS ────────────────────────────────────────────
st.markdown('<div class="produtos-area">', unsafe_allow_html=True)

busca = st.text_input("", placeholder="🔍  Buscar produto...", label_visibility="collapsed")
if busca:
    df = df[df["descricao"].str.contains(busca, case=False, na=False)].reset_index(drop=True)

st.markdown(f"""
<div class="produtos-header">
  <p class="produtos-titulo">Nossos Produtos</p>
  <span class="produtos-count">{len(df)} itens</span>
</div>
""", unsafe_allow_html=True)

if df.empty:
    st.markdown('<div class="empty-state">🔍<br>Nenhum produto encontrado.</div>', unsafe_allow_html=True)
else:
    COLS = 4
    produtos = df.to_dict("records")
    for i in range(0, len(produtos), COLS):
        cols = st.columns(COLS, gap="medium")
        for j, prod in enumerate(produtos[i : i + COLS]):
            with cols[j]:
                emoji, bg   = _thumb(prod["descricao"])
                cod         = prod["codigo_interno"] or str(prod["codigo_produto"])
                img_content = _img_tag(cod, emoji, bg)
                wa          = _wa_url(prod)
                st.markdown(f"""
<div class="prod-card">
  <div class="prod-img-wrap">{img_content}</div>
  <div class="prod-info">
    <p class="prod-nome">{prod['descricao']}</p>
    <p class="prod-cod">CÓD. {cod}</p>
    <p class="prod-preco">{_brl(prod['valor_venda'])}</p>
    <a href="{wa}" target="_blank" class="prod-btn">Comprar via WhatsApp</a>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # fecha produtos-area


# ── FOOTER ──────────────────────────────────────────────────────
ano = datetime.date.today().year
st.markdown(f"""
<div class="site-footer">
  <p class="site-footer-title">SG Bichos</p>
  <p>Fale conosco: <a href="{wa_home}" target="_blank">WhatsApp +55 41 98710-9563</a></p>
  <p class="site-footer-copy">© {ano} SG Bichos. Todos os direitos reservados.</p>
</div>
""", unsafe_allow_html=True)
