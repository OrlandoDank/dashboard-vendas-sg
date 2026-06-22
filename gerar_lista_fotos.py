import json, re
from pathlib import Path

js = Path(__file__).parent / "sg-bichos/js/produtos.js"
content = js.read_text(encoding="utf-8")
match = re.search(r"const produtos = (\[.*?\]);", content, re.DOTALL)
prods = json.loads(match.group(1))

linhas = ["Categoria,Nome do Produto,Arquivo esperado (colocar em sg-bichos/images/produtos/)"]
for p in prods:
    nome = p["nome"].replace(",", ";")
    arquivo = p["imagem"].replace("images/produtos/", "")
    linhas.append(f"{p['categoria']},{nome},{arquivo}")

saida = Path(__file__).parent / "sg-bichos" / "lista-fotos.csv"
saida.write_text("\n".join(linhas), encoding="utf-8-sig")
print(f"Gerado: {saida}")
print(f"{len(prods)} produtos")
