# SG Bichos — Loja Virtual

Site estático para pet shop. HTML + CSS + JavaScript puro, sem backend.

---

## Como publicar na Hostinger

1. Acesse [hpanel.hostinger.com](https://hpanel.hostinger.com) e faça login
2. Vá em **Hospedagem** → selecione seu plano → **Gerenciar**
3. Clique em **Gerenciador de Arquivos** (ou use FTP via FileZilla)
4. Navegue até a pasta `public_html`
5. Faça upload de **todos** os arquivos e pastas desta pasta `sg-bichos/`
6. Certifique-se que o `index.html` está na raiz do `public_html`
7. Acesse seu domínio para verificar o site

---

## Configurações obrigatórias antes do upload

### 1. Logo
Substitua o arquivo `images/logo-sg-bichos.png` pelo logo real da SG Bichos.
- Formato recomendado: PNG com fundo transparente
- Altura ideal: 100–120px (será exibido em 52px de altura)

### 2. Número do WhatsApp
O número `5541987109563` já está configurado no arquivo `js/produtos.js`:
```js
const WHATSAPP = "5541987109563";
```
Se o número mudar, altere apenas essa linha.

### 3. Fotos dos produtos
Coloque as fotos reais dos produtos na pasta `images/produtos/`.
Os nomes esperados (definidos em `js/produtos.js`) são:
- `racao-cao.jpg`
- `racao-gato.jpg`
- `coleira.jpg`
- `arranhador.jpg`
- `comedouro.jpg`
- `petisco.jpg`
- `shampoo.jpg`
- `gaiola.jpg`

Enquanto não houver foto real, o site exibe um placeholder verde automaticamente.

### 4. Adicionar ou editar produtos
Edite o array em `js/produtos.js`:
```js
{
  id: 9,                              // ← número único, maior que os existentes
  nome: "Nome do Produto",
  categoria: "caes",                  // caes | gatos | passaros | higiene
  subcategoria: "racao",              // racao | petiscos | acessorios | higiene | arranhadores
  preco: 59.90,                       // sem R$, use ponto como separador decimal
  imagem: "images/produtos/foto.jpg", // caminho relativo
  descricao: "Descrição do produto.",
  destaque: false                     // true = aparece na vitrine da home
}
```

### 5. Banners do carrossel
Os 3 slides em `index.html` usam imagens de fundo via CSS inline:
```html
<div class="slide-bg" style="background-image:url('images/banner-1.jpg');">
```
Substitua `images/banner-1.jpg`, `banner-2.jpg`, `banner-3.jpg` pelas fotos reais.
- Tamanho recomendado: **1400 × 500 px**
- Formato: JPG ou WEBP

### 6. Fotos das categorias
Na home há 4 cards de categoria. As imagens estão configuradas como placeholders.
Para usar fotos reais, substitua as URLs `placehold.co` por:
```html
<img src="images/cat-caes.jpg" alt="Cães" loading="lazy">
```

---

## Estrutura de arquivos

```
sg-bichos/
├── index.html          ← Página inicial
├── categoria.html      ← Listagem por categoria (usa ?cat=caes, ?busca=...)
├── produto.html        ← Página de produto individual (usa ?id=1)
├── contato.html        ← Contato (formulário → WhatsApp)
├── css/
│   └── style.css       ← Todos os estilos
├── js/
│   ├── produtos.js     ← Catálogo de produtos + número WhatsApp
│   └── main.js         ← Carrinho, carrossel, busca, WhatsApp
├── images/
│   ├── logo-sg-bichos.png
│   ├── banner-1.jpg
│   ├── banner-2.jpg
│   ├── banner-3.jpg
│   ├── cat-caes.jpg
│   ├── cat-gatos.jpg
│   ├── cat-passaros.jpg
│   ├── cat-higiene.jpg
│   └── produtos/       ← Fotos dos produtos
└── README.md
```

---

## Funcionalidades

- **Carrinho lateral** — slide-in com contador no header, salvo em localStorage
- **WhatsApp direto** — cada produto tem botão "Comprar via WhatsApp"
- **Checkout via WhatsApp** — mensagem formatada com todos os itens e total
- **Busca em tempo real** — filtra produtos por nome e categoria
- **Carrossel automático** — 3 slides, avança a cada 5 segundos
- **Filtro por categoria** — na página `categoria.html`
- **Responsivo** — mobile-first, funciona em celular, tablet e desktop
- **Botão flutuante** — WhatsApp fixo em todas as páginas

---

## Testar localmente (opcional)

Abra os arquivos diretamente no navegador ou use um servidor local:
```bash
# Python 3
python -m http.server 8080
# Depois acesse http://localhost:8080
```

O carrinho e a busca funcionam normalmente. O redirecionamento para WhatsApp só funciona com número real configurado.
