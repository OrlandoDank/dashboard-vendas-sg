/* ===== CONFIGURAÇÃO ===== */
const CONFIG = { whatsapp: WHATSAPP };

/* ===== CARRINHO ===== */
let cart = JSON.parse(localStorage.getItem('sgbichos_cart') || '[]');

function saveCart() {
  localStorage.setItem('sgbichos_cart', JSON.stringify(cart));
}

function addToCart(id) {
  const prod = produtos.find(p => p.id === id);
  if (!prod) return;
  const item = cart.find(i => i.id === id);
  if (item) {
    item.qty++;
  } else {
    cart.push({ id: prod.id, nome: prod.nome, preco: prod.preco, imagem: prod.imagem, qty: 1 });
  }
  saveCart();
  updateCartBadge();
  renderCartItems();
  showToast('🛒 ' + prod.nome.substring(0, 28) + '... adicionado!');
}

function removeFromCart(id) {
  cart = cart.filter(i => i.id !== id);
  saveCart();
  updateCartBadge();
  renderCartItems();
}

function updateQty(id, delta) {
  const item = cart.find(i => i.id === id);
  if (!item) return;
  item.qty = Math.max(1, item.qty + delta);
  saveCart();
  renderCartItems();
}

function clearCart() {
  cart = [];
  saveCart();
  updateCartBadge();
  renderCartItems();
}

function getCartTotal() {
  return cart.reduce((sum, i) => sum + i.preco * i.qty, 0);
}

function getCartCount() {
  return cart.reduce((sum, i) => sum + i.qty, 0);
}

function updateCartBadge() {
  const count = getCartCount();
  document.querySelectorAll('.cart-badge').forEach(el => {
    el.textContent = count;
    el.style.display = count > 0 ? 'flex' : 'none';
  });
}

function renderCartItems() {
  const container = document.getElementById('cart-items');
  if (!container) return;
  if (cart.length === 0) {
    container.innerHTML = `
      <div class="cart-empty">
        <div class="cart-empty-icon">🛒</div>
        <p>Seu carrinho está vazio.</p>
        <p style="font-size:0.82rem;color:#999">Adicione produtos para continuar.</p>
      </div>`;
    return;
  }
  container.innerHTML = cart.map(item => `
    <div class="cart-item" data-id="${item.id}">
      <img class="cart-item-img" src="${item.imagem}" alt="${item.nome}"
           onerror="this.src='https://placehold.co/60x60/4A7C59/FFFFFF?text=🐾'">
      <div class="cart-item-info">
        <div class="cart-item-name">${item.nome}</div>
        <div class="cart-item-price">R$ ${fmtPreco(item.preco)}</div>
        <div class="cart-item-qty">
          <button class="qty-btn" onclick="updateQty(${item.id}, -1)" aria-label="Diminuir">−</button>
          <span class="qty-num">${item.qty}</span>
          <button class="qty-btn" onclick="updateQty(${item.id}, +1)" aria-label="Aumentar">+</button>
        </div>
      </div>
      <button class="cart-item-remove" onclick="removeFromCart(${item.id})" aria-label="Remover item">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6"/>
        </svg>
      </button>
    </div>
  `).join('');

  const totalEl = document.getElementById('cart-total');
  if (totalEl) totalEl.textContent = 'R$ ' + fmtPreco(getCartTotal());
}

/* ===== WHATSAPP ===== */
function fmtPreco(v) {
  return v.toFixed(2).replace('.', ',');
}

function buildCartMsg() {
  if (cart.length === 0) return '';
  let lines = cart.map(i => `🐾 ${i.nome} — R$ ${fmtPreco(i.preco)} (x${i.qty})`).join('\n');
  const total = getCartTotal();
  return `Olá! Gostaria de fazer um pedido:\n\n${lines}\n\n*Total: R$ ${fmtPreco(total)}*\n\nPode me ajudar com o pedido?`;
}

function checkoutWhatsApp() {
  const msg = buildCartMsg();
  if (!msg) return;
  window.open(`https://wa.me/${CONFIG.whatsapp}?text=${encodeURIComponent(msg)}`, '_blank');
}

function buyProductWhatsApp(id) {
  const prod = produtos.find(p => p.id === id);
  if (!prod) return;
  const msg = `Olá! Tenho interesse em comprar:\n\n🐾 *${prod.nome}*\nPreço: R$ ${fmtPreco(prod.preco)}\n\nPoderia me ajudar?`;
  window.open(`https://wa.me/${CONFIG.whatsapp}?text=${encodeURIComponent(msg)}`, '_blank');
}

/* ===== SIDE CART ===== */
function openCart() {
  document.getElementById('cart-overlay').classList.add('open');
  document.getElementById('cart-panel').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeCart() {
  document.getElementById('cart-overlay').classList.remove('open');
  document.getElementById('cart-panel').classList.remove('open');
  document.body.style.overflow = '';
}

/* ===== CARROSSEL ===== */
let carouselIndex = 0;
let carouselInterval = null;

function initCarousel() {
  const track = document.getElementById('carousel-track');
  if (!track) return;
  const slides = track.querySelectorAll('.slide');
  const dots = document.querySelectorAll('.dot');
  if (slides.length === 0) return;

  function goTo(n) {
    carouselIndex = (n + slides.length) % slides.length;
    track.style.transform = `translateX(-${carouselIndex * 100}%)`;
    dots.forEach((d, i) => d.classList.toggle('active', i === carouselIndex));
  }

  document.getElementById('carousel-prev')?.addEventListener('click', () => {
    goTo(carouselIndex - 1);
    resetInterval();
  });
  document.getElementById('carousel-next')?.addEventListener('click', () => {
    goTo(carouselIndex + 1);
    resetInterval();
  });
  dots.forEach((d, i) => d.addEventListener('click', () => { goTo(i); resetInterval(); }));

  function resetInterval() {
    clearInterval(carouselInterval);
    carouselInterval = setInterval(() => goTo(carouselIndex + 1), 5000);
  }

  goTo(0);
  resetInterval();
}

/* ===== BUSCA ===== */
function initSearch() {
  const input = document.getElementById('search-input');
  const results = document.getElementById('search-results');
  if (!input || !results) return;

  input.addEventListener('input', () => {
    const q = input.value.trim().toLowerCase();
    if (q.length < 2) { results.classList.remove('show'); return; }
    const matches = produtos.filter(p =>
      p.nome.toLowerCase().includes(q) || p.categoria.toLowerCase().includes(q)
    ).slice(0, 5);
    if (matches.length === 0) { results.classList.remove('show'); return; }
    results.innerHTML = matches.map(p => `
      <div class="search-result-item" onclick="location.href='produto.html?id=${p.id}'">
        <img class="search-result-img" src="${p.imagem}" alt="${p.nome}"
             onerror="this.src='https://placehold.co/42x42/4A7C59/FFFFFF?text=🐾'">
        <div>
          <div class="search-result-name">${p.nome}</div>
          <div class="search-result-price">R$ ${fmtPreco(p.preco)}</div>
        </div>
      </div>
    `).join('');
    results.classList.add('show');
  });

  input.addEventListener('keydown', e => {
    if (e.key === 'Escape') { results.classList.remove('show'); input.blur(); }
    if (e.key === 'Enter') {
      const q = input.value.trim();
      if (q) location.href = `categoria.html?busca=${encodeURIComponent(q)}`;
    }
  });

  document.addEventListener('click', e => {
    if (!input.contains(e.target) && !results.contains(e.target)) {
      results.classList.remove('show');
    }
  });
}

/* ===== RENDERIZAR PRODUTOS ===== */
function createProductCard(prod) {
  const placeholder = `https://placehold.co/400x400/2C1A08/F5A800?text=SG+Bichos`;
  const catLabel = categorias.find(c => c.id === prod.categoria)?.label || prod.categoria;
  return `
    <article class="product-card">
      <div class="product-img-wrap">
        ${prod.destaque ? '<span class="product-badge">Destaque</span>' : ''}
        <img src="${prod.imagem}" alt="${prod.nome}" loading="lazy"
             onerror="this.src='${placeholder}'">
      </div>
      <div class="product-body">
        <div class="product-cat">${catLabel}</div>
        <div class="product-name">${prod.nome}</div>
        <div class="product-desc">${prod.descricao}</div>
        <div class="product-price">R$ ${fmtPreco(prod.preco)}</div>
      </div>
      <div class="product-actions">
        <button class="btn-add" onclick="addToCart(${prod.id})">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
          </svg>
          Adicionar
        </button>
        <button class="btn-wpp" onclick="buyProductWhatsApp(${prod.id})" aria-label="Comprar via WhatsApp">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347"/>
          </svg>
        </button>
      </div>
    </article>
  `;
}

function renderHomeProducts() {
  const grid = document.getElementById('products-grid');
  if (!grid) return;
  const destaques = produtos.filter(p => p.destaque);
  const lista = destaques.length ? destaques : produtos.slice(0, 8);
  grid.innerHTML = lista.map(createProductCard).join('');
}

function renderAllProducts(filter) {
  const grid = document.getElementById('products-grid');
  if (!grid) return;
  const list = filter ? produtos.filter(filter) : produtos;
  grid.innerHTML = list.length
    ? list.map(createProductCard).join('')
    : '<p style="text-align:center;color:#999;padding:40px 0;grid-column:1/-1">Nenhum produto encontrado.</p>';
}

/* ===== NAV DINÂMICO ===== */
function renderNav() {
  const desktopSlot = document.getElementById('nav-cats');
  const mobileSlot  = document.getElementById('mobile-nav-cats');
  if (!categorias.length) return;

  if (desktopSlot) {
    desktopSlot.innerHTML = categorias.map(c =>
      `<div class="nav-item">
        <a href="categoria.html?cat=${c.id}" class="nav-link">${c.icone} ${c.label}</a>
       </div>`
    ).join('');
  }

  if (mobileSlot) {
    mobileSlot.innerHTML = categorias.map(c =>
      `<a href="categoria.html?cat=${c.id}" class="nav-link">${c.icone} ${c.label}</a>`
    ).join('');
  }
}

/* ===== GRID CATEGORIAS (home) ===== */
function renderCategoryGrid() {
  const grid = document.getElementById('cat-grid');
  if (!grid || !categorias.length) return;
  const placeholder = 'https://placehold.co/600x400/2C1A08/F5A800?text=';
  grid.innerHTML = categorias.map(c => `
    <a href="categoria.html?cat=${c.id}" class="cat-card">
      <img src="${c.imagem}" alt="${c.label}" loading="lazy"
           onerror="this.src='${placeholder}${encodeURIComponent(c.label)}'">
      <div class="cat-card-overlay">
        <div class="cat-card-icon">${c.icone}</div>
        <div class="cat-card-name">${c.label}</div>
        <div class="cat-card-count">${produtos.filter(p => p.categoria === c.id).length} produtos</div>
      </div>
    </a>
  `).join('');
}

/* ===== MOBILE MENU ===== */
function initMobileMenu() {
  const btn = document.getElementById('mobile-menu-btn');
  const nav = document.getElementById('mobile-nav');
  if (!btn || !nav) return;
  btn.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
  });
  nav.querySelectorAll('.nav-link').forEach(link => {
    if (link.nextElementSibling?.classList.contains('dropdown')) {
      link.addEventListener('click', e => {
        e.preventDefault();
        link.nextElementSibling.classList.toggle('open');
      });
    }
  });
}

/* ===== TOAST ===== */
function showToast(msg) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = msg;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 2800);
}

/* ===== INIT ===== */
document.addEventListener('DOMContentLoaded', () => {
  updateCartBadge();
  renderCartItems();
  initCarousel();
  initSearch();
  renderNav();
  renderCategoryGrid();
  initMobileMenu();
  renderHomeProducts();

  document.getElementById('cart-btn')?.addEventListener('click', openCart);
  document.getElementById('cart-overlay')?.addEventListener('click', closeCart);
  document.getElementById('cart-close')?.addEventListener('click', closeCart);
  document.getElementById('btn-checkout')?.addEventListener('click', checkoutWhatsApp);
  document.getElementById('btn-clear-cart')?.addEventListener('click', () => {
    if (confirm('Limpar o carrinho?')) clearCart();
  });
});
