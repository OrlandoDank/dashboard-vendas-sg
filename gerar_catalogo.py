#!/usr/bin/env python3
"""
Gera sg-bichos/js/produtos.js com os produtos do catálogo Omie.
Uso: python gerar_catalogo.py

O arquivo gerado substitui o catálogo placeholder pelo catálogo real da loja.
Execute novamente sempre que quiser atualizar preços ou adicionar produtos.
"""
import json
import re
import unicodedata
from pathlib import Path
import requests

# ── Credenciais ────────────────────────────────────────────────────────────────

def ler_secrets():
    secrets = Path(__file__).parent / ".streamlit" / "secrets.toml"
    import tomllib
    with open(secrets, "rb") as f:
        s = tomllib.load(f)
    return s["OMIE_APP_KEY"], s["OMIE_APP_SECRET"]

# ── Omie API ───────────────────────────────────────────────────────────────────

URL_BASE = "https://app.omie.com.br/api/v1/"

def _post(endpoint, call, param):
    key, secret = ler_secrets()
    r = requests.post(URL_BASE + endpoint, json={
        "app_key": key, "app_secret": secret,
        "call": call, "param": [param],
    }, timeout=30)
    r.raise_for_status()
    return r.json()

def _paginar(endpoint, call, param_base, chave_lista):
    itens, pagina = [], 1
    while True:
        resp = _post(endpoint, call, {**param_base, "pagina": pagina, "registros_por_pagina": 50})
        lista = resp.get(chave_lista, [])
        if not lista:
            break
        itens.extend(lista)
        if pagina >= resp.get("total_de_paginas", 1):
            break
        pagina += 1
        print(f"    página {pagina - 1}/{resp.get('total_de_paginas', 1)}", end="\r")
    print()
    return itens

# ── Configuração ───────────────────────────────────────────────────────────────

WHATSAPP = "5541987109563"

# Famílias a excluir (comparação case-insensitive, sem acentos)
FAMILIAS_EXCLUIR = {
    "lacos", "limpeza", "papeis", "coleira", "gravatas",
    "bonificacoes", "bonificacao", "gargantilhas", "apliques", "bandanas", "adesivos",
    "inativo",
}

# Ícones por família (slugificado) — adicione mais conforme aparecerem
ICONES = {
    "racao":     "🥣",
    "racoes":    "🥣",
    "petiscos":  "🦴",
    "acessorios":"🎀",
    "higiene":   "🛁",
    "brinquedos":"🎾",
    "roupas":    "👕",
    "camas":     "🛏",
    "transporte":"🧳",
    "saude":     "💊",
}

def slugify(texto):
    """'Ração Cães' → 'racao-caes'"""
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = texto.encode("ascii", "ignore").decode("ascii")
    texto = texto.lower().strip()
    texto = re.sub(r"[^a-z0-9\s-]", "", texto)
    texto = re.sub(r"[\s_]+", "-", texto)
    texto = re.sub(r"-+", "-", texto).strip("-")
    return texto

def slugify_simples(texto):
    """Versão sem hífens para comparar com FAMILIAS_EXCLUIR."""
    return slugify(texto).replace("-", "")

# ── Busca produtos ─────────────────────────────────────────────────────────────

def buscar_produtos():
    print("Buscando catálogo de produtos no Omie...")
    raw = _paginar("geral/produtos/", "ListarProdutos",
                   {"filtrar_apenas_omiepdv": "N"}, "produto_servico_cadastro")
    print(f"  Total bruto: {len(raw)} produtos")

    produtos = []
    familias_map = {}   # slug → label original
    excluidos   = {}

    for p in raw:
        # Filtrar inativos
        if p.get("inativo", "N") == "S":
            excluidos["[inativo]"] = excluidos.get("[inativo]", 0) + 1
            continue

        familia_label = (p.get("descricao_familia") or "").strip()

        # Sem família → ignorar
        if not familia_label:
            excluidos["[sem família]"] = excluidos.get("[sem família]", 0) + 1
            continue

        # Filtrar famílias excluídas
        slug_simples = slugify_simples(familia_label)
        if slug_simples in FAMILIAS_EXCLUIR:
            excluidos[familia_label] = excluidos.get(familia_label, 0) + 1
            continue

        preco = float(p.get("valor_unitario") or 0)
        if preco <= 0:
            excluidos["[sem preço]"] = excluidos.get("[sem preço]", 0) + 1
            continue

        codigo   = str(p.get("codigo", "")).strip()
        descricao = (p.get("descricao") or "").strip()
        cat_slug  = slugify(familia_label)
        familias_map[cat_slug] = familia_label

        produtos.append({
            "id":           int(p.get("codigo_produto") or 0),
            "nome":         descricao,
            "categoria":    cat_slug,
            "subcategoria": cat_slug,
            "preco":        round(preco, 2),
            "imagem":       f"images/produtos/{codigo}.jpg",
            "descricao":    descricao,
            "destaque":     False,
        })

    produtos.sort(key=lambda x: x["nome"])

    print(f"\n  OK Incluidos: {len(produtos)} produtos")
    if excluidos:
        print("  Excluidos:")
        for k, v in sorted(excluidos.items(), key=lambda x: -x[1]):
            print(f"       {k}: {v}")

    # Construir lista de categorias
    categorias = []
    for slug in sorted(familias_map):
        label = familias_map[slug]
        icone = ICONES.get(slug.split("-")[0], "\U0001F43E")
        qtd   = sum(1 for p in produtos if p["categoria"] == slug)
        categorias.append({
            "id":     slug,
            "label":  label,
            "icone":  icone,
            "imagem": f"images/cat-{slug}.jpg",
            "sub":    [],
        })
        print(f"       {label} ({qtd} produtos) -> id: \"{slug}\"")

    return produtos, categorias

# ── Gerar JS ───────────────────────────────────────────────────────────────────

def gerar_js(produtos, categorias):
    saida = Path(__file__).parent / "sg-bichos" / "js" / "produtos.js"

    conteudo = (
        f'const WHATSAPP = "{WHATSAPP}";\n\n'
        f'const produtos = {json.dumps(produtos, ensure_ascii=False, indent=2)};\n\n'
        f'const categorias = {json.dumps(categorias, ensure_ascii=False, indent=2)};\n'
    )

    saida.write_text(conteudo, encoding="utf-8")
    print(f"\nArquivo gerado: {saida}")
    print(f"  {len(produtos)} produtos | {len(categorias)} categorias")
    print("\nProximos passos:")
    print("  1. Adicione fotos em sg-bichos/images/produtos/<codigo>.jpg")
    print("  2. Marque destaque:true nos produtos que quer na vitrine da home")
    print("  3. Execute novamente para atualizar precos")

if __name__ == "__main__":
    produtos, categorias = buscar_produtos()
    gerar_js(produtos, categorias)
