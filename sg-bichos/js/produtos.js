const WHATSAPP = "5541987109563";

const produtos = [
  {
    "id": 3313738836,
    "nome": "CAIXA BEEFLEX DE CARNE 70G C/20 Un",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 39.0,
    "imagem": "images/produtos/PRD00117.jpg",
    "descricao": "CAIXA BEEFLEX DE CARNE 70G C/20 Un",
    "destaque": false
  },
  {
    "id": 3313738887,
    "nome": "CAIXA C/ 10UN DE CHIPS PULMÃO BRUPET",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 108.5,
    "imagem": "images/produtos/PRD00146.jpg",
    "descricao": "CAIXA C/ 10UN DE CHIPS PULMÃO BRUPET",
    "destaque": false
  },
  {
    "id": 3313738840,
    "nome": "CAIXA C/ 20Un DE PALITO FLEXÍVEL - BACON",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 188.0,
    "imagem": "images/produtos/PRD00124.jpg",
    "descricao": "CAIXA C/ 20Un DE PALITO FLEXÍVEL - BACON",
    "destaque": false
  },
  {
    "id": 3313738842,
    "nome": "CAIXA C/ 20Un. DE PALITO FLEXÍVEL - LEITE - Brupet",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 188.0,
    "imagem": "images/produtos/PRD00125.jpg",
    "descricao": "CAIXA C/ 20Un. DE PALITO FLEXÍVEL - LEITE - Brupet",
    "destaque": false
  },
  {
    "id": 3313738731,
    "nome": "CAIXA C/ 4 DE PALITO 605 - 1KG",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 67.5,
    "imagem": "images/produtos/PRD00055.jpg",
    "descricao": "CAIXA C/ 4 DE PALITO 605 - 1KG",
    "destaque": false
  },
  {
    "id": 3313738723,
    "nome": "CAIXA C/20 Un. DE PALITO FLEXÍVEL - MENTA",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 188.0,
    "imagem": "images/produtos/PRD00051.jpg",
    "descricao": "CAIXA C/20 Un. DE PALITO FLEXÍVEL - MENTA",
    "destaque": false
  },
  {
    "id": 3313738891,
    "nome": "CAIXA C/4 UN PALITO 805 1KG - Brupet",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 64.0,
    "imagem": "images/produtos/PRD00147.jpg",
    "descricao": "CAIXA C/4 UN PALITO 805 1KG - Brupet",
    "destaque": false
  },
  {
    "id": 3313738755,
    "nome": "CAIXA DE BIFINHO SABOR CARNE 800g  c/5 Un - BRUPET",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 152.5,
    "imagem": "images/produtos/PRD00067.jpg",
    "descricao": "CAIXA DE BIFINHO SABOR CARNE 800g  c/5 Un - BRUPET",
    "destaque": false
  },
  {
    "id": 3313738747,
    "nome": "CAIXA DE BIFINHO SABOR FRANGO 400g  c/10 Un.- BRUPET",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 165.0,
    "imagem": "images/produtos/PRD00063.jpg",
    "descricao": "CAIXA DE BIFINHO SABOR FRANGO 400g  c/10 Un.- BRUPET",
    "destaque": false
  },
  {
    "id": 3313738735,
    "nome": "CAIXA DE BIFINHO SABOR FRANGO 50g c/ 20Un.- BRUPET",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 56.0,
    "imagem": "images/produtos/PRD00057.jpg",
    "descricao": "CAIXA DE BIFINHO SABOR FRANGO 50g c/ 20Un.- BRUPET",
    "destaque": false
  },
  {
    "id": 3313738753,
    "nome": "CAIXA DE BIFINHO SABOR FRANGO 800g c/5un. - BRUPET",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 152.5,
    "imagem": "images/produtos/PRD00066.jpg",
    "descricao": "CAIXA DE BIFINHO SABOR FRANGO 800g c/5un. - BRUPET",
    "destaque": false
  },
  {
    "id": 3313738743,
    "nome": "CAIXA DE BIFINHOS DE CARNE 400g  C/10Un.- BRUPET",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 165.0,
    "imagem": "images/produtos/PRD00061.jpg",
    "descricao": "CAIXA DE BIFINHOS DE CARNE 400g  C/10Un.- BRUPET",
    "destaque": false
  },
  {
    "id": 3313738739,
    "nome": "CAIXA DE BIFINHOS DE CARNE 50g c/ 20Un.- BRUPET",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 56.0,
    "imagem": "images/produtos/PRD00059.jpg",
    "descricao": "CAIXA DE BIFINHOS DE CARNE 50g c/ 20Un.- BRUPET",
    "destaque": false
  },
  {
    "id": 3313738715,
    "nome": "CAIXA DE CASCO BOVINO 15Un. - BRUPET",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 119.0,
    "imagem": "images/produtos/PRD00047.jpg",
    "descricao": "CAIXA DE CASCO BOVINO 15Un. - BRUPET",
    "destaque": false
  },
  {
    "id": 3313738719,
    "nome": "CAIXA DE PALITO 805 C/ 9 UN. CX C/20 PCT",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 40.0,
    "imagem": "images/produtos/PRD00049.jpg",
    "descricao": "CAIXA DE PALITO 805 C/ 9 UN. CX C/20 PCT",
    "destaque": false
  },
  {
    "id": 3313738711,
    "nome": "CAIXA DE PÉ DE FRANGO 10un - BRUPET",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 64.0,
    "imagem": "images/produtos/PRD00045.jpg",
    "descricao": "CAIXA DE PÉ DE FRANGO 10un - BRUPET",
    "destaque": false
  },
  {
    "id": 3313738935,
    "nome": "CAIXA ORELHA DESIDRATADA BOVINA c/ 8un.",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 32.0,
    "imagem": "images/produtos/SG0027.jpg",
    "descricao": "CAIXA ORELHA DESIDRATADA BOVINA c/ 8un.",
    "destaque": false
  },
  {
    "id": 3313738933,
    "nome": "CAIXA ORELHA DESIDRATADA DE SUINO C/ 8Un. - BRUPET",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 44.0,
    "imagem": "images/produtos/SG0026.jpg",
    "descricao": "CAIXA ORELHA DESIDRATADA DE SUINO C/ 8Un. - BRUPET",
    "destaque": false
  },
  {
    "id": 3313738939,
    "nome": "CAIXA OSSO DESIDRATADO FEMUR SUINO C/15Un.",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 103.5,
    "imagem": "images/produtos/SG0029.jpg",
    "descricao": "CAIXA OSSO DESIDRATADO FEMUR SUINO C/15Un.",
    "destaque": false
  },
  {
    "id": 3314162132,
    "nome": "CAIXA OSSO DESIDRATADO MEIO FEMUR SUINO C/30 Un.",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 115.7,
    "imagem": "images/produtos/PRD00154.jpg",
    "descricao": "CAIXA OSSO DESIDRATADO MEIO FEMUR SUINO C/30 Un.",
    "destaque": false
  },
  {
    "id": 3313738727,
    "nome": "CAIXA c/20 UN. DE MEIO CHIFRE BOVINO",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 83.0,
    "imagem": "images/produtos/PRD00053.jpg",
    "descricao": "CAIXA c/20 UN. DE MEIO CHIFRE BOVINO",
    "destaque": false
  },
  {
    "id": 3313738652,
    "nome": "COLONIA PET ANGEL 480ML",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 148.9,
    "imagem": "images/produtos/PRD00029.jpg",
    "descricao": "COLONIA PET ANGEL 480ML",
    "destaque": false
  },
  {
    "id": 3313740149,
    "nome": "COLONIA PET HIPO PELES SENSIVEIS 250 ML",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 98.9,
    "imagem": "images/produtos/PA0011.jpg",
    "descricao": "COLONIA PET HIPO PELES SENSIVEIS 250 ML",
    "destaque": false
  },
  {
    "id": 3313738650,
    "nome": "COLONIA PET INVICTOS  480ML",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 148.9,
    "imagem": "images/produtos/PRD00028.jpg",
    "descricao": "COLONIA PET INVICTOS  480ML",
    "destaque": false
  },
  {
    "id": 3313740145,
    "nome": "COLONIA PET UNISSEX 250 ML",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 88.9,
    "imagem": "images/produtos/PA0010.jpg",
    "descricao": "COLONIA PET UNISSEX 250 ML",
    "destaque": false
  },
  {
    "id": 3313738885,
    "nome": "Caixa Traqueia - Brupet c/ 1 un e cx com 10Un..",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 54.0,
    "imagem": "images/produtos/PRD00145.jpg",
    "descricao": "Caixa Traqueia - Brupet c/ 1 un e cx com 10Un..",
    "destaque": false
  },
  {
    "id": 3314157505,
    "nome": "Caixa Traqueia - Brupet c/ 2 un. Cx c/ 10 Un",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 104.0,
    "imagem": "images/produtos/PRD00152.jpg",
    "descricao": "Caixa Traqueia - Brupet c/ 2 un. Cx c/ 10 Un",
    "destaque": false
  },
  {
    "id": 3313740141,
    "nome": "DERMO ACELERADOR DE SECAGEM SPRAY 500 ML",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 95.9,
    "imagem": "images/produtos/PA0009.jpg",
    "descricao": "DERMO ACELERADOR DE SECAGEM SPRAY 500 ML",
    "destaque": false
  },
  {
    "id": 3313738654,
    "nome": "DERMO CAUTERIZADOR HIDRATANTE SPRAY 500ML",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 82.8,
    "imagem": "images/produtos/PRD00034.jpg",
    "descricao": "DERMO CAUTERIZADOR HIDRATANTE SPRAY 500ML",
    "destaque": false
  },
  {
    "id": 3313740133,
    "nome": "DERMO CONDICIONADOR RESTAURADOR 1000 ML",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 95.9,
    "imagem": "images/produtos/PA0007.jpg",
    "descricao": "DERMO CONDICIONADOR RESTAURADOR 1000 ML",
    "destaque": false
  },
  {
    "id": 3313738997,
    "nome": "DERMO CONDICIONADOR RESTAURADOR 5000 ML",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 344.9,
    "imagem": "images/produtos/PA0008.jpg",
    "descricao": "DERMO CONDICIONADOR RESTAURADOR 5000 ML",
    "destaque": false
  },
  {
    "id": 3313738981,
    "nome": "DERMO DESEMBARACANTE SPRAY 500 ML",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 89.9,
    "imagem": "images/produtos/PA0001.jpg",
    "descricao": "DERMO DESEMBARACANTE SPRAY 500 ML",
    "destaque": false
  },
  {
    "id": 3313738674,
    "nome": "DERMO FINALIZADOR BRILHO INTENSO SPRAY 500ml",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 139.9,
    "imagem": "images/produtos/PA0017.jpg",
    "descricao": "DERMO FINALIZADOR BRILHO INTENSO SPRAY 500ml",
    "destaque": false
  },
  {
    "id": 3313738985,
    "nome": "DERMO LIMPEZA DE OUVIDOS 500 ML",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 98.8,
    "imagem": "images/produtos/PA0002.jpg",
    "descricao": "DERMO LIMPEZA DE OUVIDOS 500 ML",
    "destaque": false
  },
  {
    "id": 3313738640,
    "nome": "DERMO MASCARA HIDRATANTE  1000ML",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 149.9,
    "imagem": "images/produtos/PRD00023.jpg",
    "descricao": "DERMO MASCARA HIDRATANTE  1000ML",
    "destaque": false
  },
  {
    "id": 3313738646,
    "nome": "DERMO SHAMPOO  ILUMINADOR  DE PELOS 1000ML",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 139.9,
    "imagem": "images/produtos/PRD00026.jpg",
    "descricao": "DERMO SHAMPOO  ILUMINADOR  DE PELOS 1000ML",
    "destaque": false
  },
  {
    "id": 3313738644,
    "nome": "DERMO SHAMPOO ANTIRESIDUO 1000ML",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 139.9,
    "imagem": "images/produtos/PRD00025.jpg",
    "descricao": "DERMO SHAMPOO ANTIRESIDUO 1000ML",
    "destaque": false
  },
  {
    "id": 3313738648,
    "nome": "DERMO SHAMPOO ILUMINADOR DE PELOS  5LT",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 373.9,
    "imagem": "images/produtos/PRD00027.jpg",
    "descricao": "DERMO SHAMPOO ILUMINADOR DE PELOS  5LT",
    "destaque": false
  },
  {
    "id": 3313738989,
    "nome": "DERMO SHAMPOO NEUTRALIZADOR DE ODORES 1000 ML",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 149.9,
    "imagem": "images/produtos/PA0003.jpg",
    "descricao": "DERMO SHAMPOO NEUTRALIZADOR DE ODORES 1000 ML",
    "destaque": false
  },
  {
    "id": 3313740123,
    "nome": "DERMO SHAMPOO NEUTRALIZADOR DE ODORES 5000 ML",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 373.9,
    "imagem": "images/produtos/PA0004.jpg",
    "descricao": "DERMO SHAMPOO NEUTRALIZADOR DE ODORES 5000 ML",
    "destaque": false
  },
  {
    "id": 3313738993,
    "nome": "DERMO SHAMPOO NEUTRO HIDRATANTE 1000 ML",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 119.9,
    "imagem": "images/produtos/PA0005.jpg",
    "descricao": "DERMO SHAMPOO NEUTRO HIDRATANTE 1000 ML",
    "destaque": false
  },
  {
    "id": 3313740127,
    "nome": "DERMO SHAMPOO NEUTRO HIDRATANTE 5000 ML",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 324.9,
    "imagem": "images/produtos/PA0006.jpg",
    "descricao": "DERMO SHAMPOO NEUTRO HIDRATANTE 5000 ML",
    "destaque": false
  },
  {
    "id": 3318084077,
    "nome": "LIFE ESPECIAL FILHOTE 10 kg",
    "categoria": "racao-seca",
    "subcategoria": "racao-seca",
    "preco": 114.0,
    "imagem": "images/produtos/PRD00164.jpg",
    "descricao": "LIFE ESPECIAL FILHOTE 10 kg",
    "destaque": false
  },
  {
    "id": 3318084065,
    "nome": "LIFE ESPECIAL GATO ADULTO 10,1kg",
    "categoria": "racao-seca",
    "subcategoria": "racao-seca",
    "preco": 117.0,
    "imagem": "images/produtos/PRD00163.jpg",
    "descricao": "LIFE ESPECIAL GATO ADULTO 10,1kg",
    "destaque": false
  },
  {
    "id": 3318084043,
    "nome": "LIFE ESPECIAL GATO CASTRADO  kg",
    "categoria": "racao-seca",
    "subcategoria": "racao-seca",
    "preco": 131.0,
    "imagem": "images/produtos/PRD00162.jpg",
    "descricao": "LIFE ESPECIAL GATO CASTRADO  kg",
    "destaque": false
  },
  {
    "id": 3318084196,
    "nome": "LIFE ESPECIAL MEDIAS E GRANDES 15kg",
    "categoria": "racao-seca",
    "subcategoria": "racao-seca",
    "preco": 133.0,
    "imagem": "images/produtos/PRD00166.jpg",
    "descricao": "LIFE ESPECIAL MEDIAS E GRANDES 15kg",
    "destaque": false
  },
  {
    "id": 3318084140,
    "nome": "LIFE ESPECIAL PEQUENAS RAÇAS 10,1kg",
    "categoria": "racao-seca",
    "subcategoria": "racao-seca",
    "preco": 107.0,
    "imagem": "images/produtos/PRD00165.jpg",
    "descricao": "LIFE ESPECIAL PEQUENAS RAÇAS 10,1kg",
    "destaque": false
  },
  {
    "id": 3313738913,
    "nome": "ORELHA DESIDRATADA DE BOVINO",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 4.0,
    "imagem": "images/produtos/SG0009.jpg",
    "descricao": "ORELHA DESIDRATADA DE BOVINO",
    "destaque": false
  },
  {
    "id": 3313738911,
    "nome": "ORELHA DESIDRATADA DE SUINO UNIDADE - BRUPET",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 5.7,
    "imagem": "images/produtos/SG0008.jpg",
    "descricao": "ORELHA DESIDRATADA DE SUINO UNIDADE - BRUPET",
    "destaque": false
  },
  {
    "id": 3313738909,
    "nome": "OSSO DESIDRATADO DE BOVINO",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 6.8,
    "imagem": "images/produtos/SG0007.jpg",
    "descricao": "OSSO DESIDRATADO DE BOVINO",
    "destaque": false
  },
  {
    "id": 3313738931,
    "nome": "OSSO DESIDRATADO DE BOVINO - COSTELA BOVINA Cx c/8Un.",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 54.4,
    "imagem": "images/produtos/SG0025.jpg",
    "descricao": "OSSO DESIDRATADO DE BOVINO - COSTELA BOVINA Cx c/8Un.",
    "destaque": false
  },
  {
    "id": 3313738917,
    "nome": "OSSO DESIDRATADO FEMUR SUINO",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 6.9,
    "imagem": "images/produtos/SG0001.jpg",
    "descricao": "OSSO DESIDRATADO FEMUR SUINO",
    "destaque": false
  },
  {
    "id": 3313738897,
    "nome": "OSSO DESIDRATADO MEIO FEMUR SUINO",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 3.9,
    "imagem": "images/produtos/PRD00150.jpg",
    "descricao": "OSSO DESIDRATADO MEIO FEMUR SUINO",
    "destaque": false
  },
  {
    "id": 3313738790,
    "nome": "OSSO NÓ 2x3&quot; Cartela - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 5.1,
    "imagem": "images/produtos/PRD00094.jpg",
    "descricao": "OSSO NÓ 2x3&quot; Cartela - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738830,
    "nome": "OSSO NÓ 2x3&quot; Cartela CAXIA - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 51.0,
    "imagem": "images/produtos/PRD00114.jpg",
    "descricao": "OSSO NÓ 2x3&quot; Cartela CAXIA - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738792,
    "nome": "OSSO NÓ 3x4&quot; Cartela - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 5.1,
    "imagem": "images/produtos/PRD00095.jpg",
    "descricao": "OSSO NÓ 3x4&quot; Cartela - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738832,
    "nome": "OSSO NÓ 3x4&quot; Cartela CAIXA - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 51.0,
    "imagem": "images/produtos/PRD00115.jpg",
    "descricao": "OSSO NÓ 3x4&quot; Cartela CAIXA - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738881,
    "nome": "Osso Nó 2x3&quot; n.2 com 50Un. - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 70.0,
    "imagem": "images/produtos/PRD00142.jpg",
    "descricao": "Osso Nó 2x3&quot; n.2 com 50Un. - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738856,
    "nome": "PALITO 06X5mm C/12 Un. - BRUPET",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 2.3,
    "imagem": "images/produtos/PRD00132.jpg",
    "descricao": "PALITO 06X5mm C/12 Un. - BRUPET",
    "destaque": false
  },
  {
    "id": 3313738869,
    "nome": "PALITO 10X5MM CARNE DEFUMADA PC 1kg - CAIXA c/4 - Brupet",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 78.0,
    "imagem": "images/produtos/PRD00140.jpg",
    "descricao": "PALITO 10X5MM CARNE DEFUMADA PC 1kg - CAIXA c/4 - Brupet",
    "destaque": false
  },
  {
    "id": 3313738865,
    "nome": "PALITO 10X5MM CARNE DEFUMADA PC C/7 UN - Brupet",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 2.3,
    "imagem": "images/produtos/PRD00137.jpg",
    "descricao": "PALITO 10X5MM CARNE DEFUMADA PC C/7 UN - Brupet",
    "destaque": false
  },
  {
    "id": 3313738867,
    "nome": "PALITO 10X5MM CARNE DEFUMADA PC C/7 UN - CAIXA C20 PCT - Brupet",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 44.0,
    "imagem": "images/produtos/PRD00138.jpg",
    "descricao": "PALITO 10X5MM CARNE DEFUMADA PC C/7 UN - CAIXA C20 PCT - Brupet",
    "destaque": false
  },
  {
    "id": 3313738854,
    "nome": "PALITO 10X5mm CARNE DEFUMADA 1Kg - Brupet",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 20.0,
    "imagem": "images/produtos/PRD00131.jpg",
    "descricao": "PALITO 10X5mm CARNE DEFUMADA 1Kg - Brupet",
    "destaque": false
  },
  {
    "id": 3313738860,
    "nome": "PALITO 605MM PC C/12 UN",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 2.3,
    "imagem": "images/produtos/PRD00135.jpg",
    "descricao": "PALITO 605MM PC C/12 UN",
    "destaque": false
  },
  {
    "id": 3313738862,
    "nome": "PALITO 605MM PC C/12 UN CAIXA C/20 pco",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 40.0,
    "imagem": "images/produtos/PRD00136.jpg",
    "descricao": "PALITO 605MM PC C/12 UN CAIXA C/20 pco",
    "destaque": false
  },
  {
    "id": 3313738844,
    "nome": "PALITO 805 1KG - Brupet",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 16.0,
    "imagem": "images/produtos/PRD00126.jpg",
    "descricao": "PALITO 805 1KG - Brupet",
    "destaque": false
  },
  {
    "id": 3313738850,
    "nome": "PALITO FLEX SABOR MISTO PC 1 KG - Brupet",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 42.0,
    "imagem": "images/produtos/PRD00129.jpg",
    "descricao": "PALITO FLEX SABOR MISTO PC 1 KG - Brupet",
    "destaque": false
  },
  {
    "id": 3313738858,
    "nome": "PALITO FLEX SABOR MISTO PC 1 KG CAIXA C/4 - Brupet",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 122.0,
    "imagem": "images/produtos/PRD00134.jpg",
    "descricao": "PALITO FLEX SABOR MISTO PC 1 KG CAIXA C/4 - Brupet",
    "destaque": false
  },
  {
    "id": 3313738782,
    "nome": "Palito 6mmx5&quot; 1 kg - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 14.5,
    "imagem": "images/produtos/PRD00090.jpg",
    "descricao": "Palito 6mmx5&quot; 1 kg - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738814,
    "nome": "Palito 6mmx5&quot; 1 kg CAIXA c/10 Un. - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 124.0,
    "imagem": "images/produtos/PRD00106.jpg",
    "descricao": "Palito 6mmx5&quot; 1 kg CAIXA c/10 Un. - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738810,
    "nome": "Palito 6mmx5&quot; Natural CAIXA c/10Un. - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 28.64,
    "imagem": "images/produtos/PRD00104.jpg",
    "descricao": "Palito 6mmx5&quot; Natural CAIXA c/10Un. - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738760,
    "nome": "Palito 6mmx5&quot; Natural Cartela- Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 2.86,
    "imagem": "images/produtos/PRD00079.jpg",
    "descricao": "Palito 6mmx5&quot; Natural Cartela- Ricosso",
    "destaque": false
  },
  {
    "id": 3313738878,
    "nome": "Palito 8mm5&quot; Colorido 1kg- Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 13.1,
    "imagem": "images/produtos/PRD00141.jpg",
    "descricao": "Palito 8mm5&quot; Colorido 1kg- Ricosso",
    "destaque": false
  },
  {
    "id": 3313738784,
    "nome": "Palito 8mmx5&quot; 1 kg - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 12.6,
    "imagem": "images/produtos/PRD00091.jpg",
    "descricao": "Palito 8mmx5&quot; 1 kg - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738820,
    "nome": "Palito 8mmx5&quot; 1 kg CAIXA c/ 10 Un.- Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 126.0,
    "imagem": "images/produtos/PRD00109.jpg",
    "descricao": "Palito 8mmx5&quot; 1 kg CAIXA c/ 10 Un.- Ricosso",
    "destaque": false
  },
  {
    "id": 3313738788,
    "nome": "Palito 8mmx5&quot; 1 kg Carne - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 13.1,
    "imagem": "images/produtos/PRD00093.jpg",
    "descricao": "Palito 8mmx5&quot; 1 kg Carne - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738816,
    "nome": "Palito 8mmx5&quot; 1 kg Carne CAIXA C/10Un. - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 131.0,
    "imagem": "images/produtos/PRD00107.jpg",
    "descricao": "Palito 8mmx5&quot; 1 kg Carne CAIXA C/10Un. - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738786,
    "nome": "Palito 8mmx5&quot; 1 kg Menta - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 13.1,
    "imagem": "images/produtos/PRD00092.jpg",
    "descricao": "Palito 8mmx5&quot; 1 kg Menta - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738818,
    "nome": "Palito 8mmx5&quot; 1 kg Menta CAIXA C/ 10 Un. - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 131.0,
    "imagem": "images/produtos/PRD00108.jpg",
    "descricao": "Palito 8mmx5&quot; 1 kg Menta CAIXA C/ 10 Un. - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738764,
    "nome": "Palito 8mmx5&quot; Carne Cartela - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 2.86,
    "imagem": "images/produtos/PRD00081.jpg",
    "descricao": "Palito 8mmx5&quot; Carne Cartela - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738800,
    "nome": "Palito 8mmx5&quot; Carne FARDO c/ 10 Un.- Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 28.64,
    "imagem": "images/produtos/PRD00099.jpg",
    "descricao": "Palito 8mmx5&quot; Carne FARDO c/ 10 Un.- Ricosso",
    "destaque": false
  },
  {
    "id": 3313738766,
    "nome": "Palito 8mmx5&quot; Menta Cartelado - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 2.86,
    "imagem": "images/produtos/PRD00082.jpg",
    "descricao": "Palito 8mmx5&quot; Menta Cartelado - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738762,
    "nome": "Palito 8mmx5&quot; Natural Cartelado- Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 2.86,
    "imagem": "images/produtos/PRD00080.jpg",
    "descricao": "Palito 8mmx5&quot; Natural Cartelado- Ricosso",
    "destaque": false
  },
  {
    "id": 3313738804,
    "nome": "Palito 8mmx5&quot; Natural FARDO c/ 10 Un.- Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 28.64,
    "imagem": "images/produtos/PRD00101.jpg",
    "descricao": "Palito 8mmx5&quot; Natural FARDO c/ 10 Un.- Ricosso",
    "destaque": false
  },
  {
    "id": 3313738802,
    "nome": "Palito 8mmx5&quot; cartelado Menta CAIXA C/10 Un. - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 28.64,
    "imagem": "images/produtos/PRD00100.jpg",
    "descricao": "Palito 8mmx5&quot; cartelado Menta CAIXA C/10 Un. - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738778,
    "nome": "Palito Flexivel Carne Cartela - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 3.2,
    "imagem": "images/produtos/PRD00088.jpg",
    "descricao": "Palito Flexivel Carne Cartela - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738826,
    "nome": "Palito Flexivel Carne Cartela CAIXA - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 32.0,
    "imagem": "images/produtos/PRD00112.jpg",
    "descricao": "Palito Flexivel Carne Cartela CAIXA - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738776,
    "nome": "Palito Flexivel Menta Cartela - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 3.2,
    "imagem": "images/produtos/PRD00087.jpg",
    "descricao": "Palito Flexivel Menta Cartela - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738822,
    "nome": "Palito Flexivel Menta Cartela CAIXA - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 32.0,
    "imagem": "images/produtos/PRD00110.jpg",
    "descricao": "Palito Flexivel Menta Cartela CAIXA - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738774,
    "nome": "Palito Flexivel Natural Cartela - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 3.2,
    "imagem": "images/produtos/PRD00086.jpg",
    "descricao": "Palito Flexivel Natural Cartela - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738824,
    "nome": "Palito Flexivel Natural Cartela CAIXA - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 32.0,
    "imagem": "images/produtos/PRD00111.jpg",
    "descricao": "Palito Flexivel Natural Cartela CAIXA - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738772,
    "nome": "Palito Flexível Carne 1 Kg - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 23.0,
    "imagem": "images/produtos/PRD00085.jpg",
    "descricao": "Palito Flexível Carne 1 Kg - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738828,
    "nome": "Palito Flexível Carne 1 Kg CAIXA c/10 Un. - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 233.0,
    "imagem": "images/produtos/PRD00113.jpg",
    "descricao": "Palito Flexível Carne 1 Kg CAIXA c/10 Un. - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738780,
    "nome": "Palito Flexível Carne 500 Gramas - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 12.4,
    "imagem": "images/produtos/PRD00089.jpg",
    "descricao": "Palito Flexível Carne 500 Gramas - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738812,
    "nome": "Palito Flexível Carne 500 Gramas CAIXA c/10 Un.- Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 124.0,
    "imagem": "images/produtos/PRD00105.jpg",
    "descricao": "Palito Flexível Carne 500 Gramas CAIXA c/10 Un.- Ricosso",
    "destaque": false
  },
  {
    "id": 3313738768,
    "nome": "Palito Flexível Menta 1 Kg - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 23.0,
    "imagem": "images/produtos/PRD00083.jpg",
    "descricao": "Palito Flexível Menta 1 Kg - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738806,
    "nome": "Palito Flexível Menta 1 Kg CAIXA - Ricossa",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 233.0,
    "imagem": "images/produtos/PRD00102.jpg",
    "descricao": "Palito Flexível Menta 1 Kg CAIXA - Ricossa",
    "destaque": false
  },
  {
    "id": 3313738770,
    "nome": "Palito Flexível Natural 1 Kg  - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 23.0,
    "imagem": "images/produtos/PRD00084.jpg",
    "descricao": "Palito Flexível Natural 1 Kg  - Ricosso",
    "destaque": false
  },
  {
    "id": 3313738808,
    "nome": "Palito Flexível Natural 1 Kg  CAIXA c/10 Un. - Ricosso",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 233.0,
    "imagem": "images/produtos/PRD00103.jpg",
    "descricao": "Palito Flexível Natural 1 Kg  CAIXA c/10 Un. - Ricosso",
    "destaque": false
  },
  {
    "id": 3318084814,
    "nome": "ROBUSTUS CAO AD DIA A DIA 15 KG",
    "categoria": "racao-seca",
    "subcategoria": "racao-seca",
    "preco": 76.51,
    "imagem": "images/produtos/PRD00178.jpg",
    "descricao": "ROBUSTUS CAO AD DIA A DIA 15 KG",
    "destaque": false
  },
  {
    "id": 3318084810,
    "nome": "ROBUSTUS CAO AD DIA A DIA 25 KG",
    "categoria": "racao-seca",
    "subcategoria": "racao-seca",
    "preco": 125.44,
    "imagem": "images/produtos/PRD00177.jpg",
    "descricao": "ROBUSTUS CAO AD DIA A DIA 25 KG",
    "destaque": false
  },
  {
    "id": 3318084768,
    "nome": "ROBUSTUS CAO AD PEQ. RACAS 10,1 KG",
    "categoria": "racao-seca",
    "subcategoria": "racao-seca",
    "preco": 81.47,
    "imagem": "images/produtos/PRD00175.jpg",
    "descricao": "ROBUSTUS CAO AD PEQ. RACAS 10,1 KG",
    "destaque": false
  },
  {
    "id": 3318084631,
    "nome": "ROBUSTUS CAO AD PEQ. RACAS 20 KG",
    "categoria": "racao-seca",
    "subcategoria": "racao-seca",
    "preco": 153.2,
    "imagem": "images/produtos/PRD00174.jpg",
    "descricao": "ROBUSTUS CAO AD PEQ. RACAS 20 KG",
    "destaque": false
  },
  {
    "id": 3318084805,
    "nome": "ROBUSTUS CAO AD RACAS MED E GDE 15 KG",
    "categoria": "racao-seca",
    "subcategoria": "racao-seca",
    "preco": 89.28,
    "imagem": "images/produtos/PRD00176.jpg",
    "descricao": "ROBUSTUS CAO AD RACAS MED E GDE 15 KG",
    "destaque": false
  },
  {
    "id": 3318084593,
    "nome": "ROBUSTUS CAO FILHOTE 10,1 KG",
    "categoria": "racao-seca",
    "subcategoria": "racao-seca",
    "preco": 89.03,
    "imagem": "images/produtos/PRD00173.jpg",
    "descricao": "ROBUSTUS CAO FILHOTE 10,1 KG",
    "destaque": false
  },
  {
    "id": 3318084252,
    "nome": "ROBUSTUS GATO AD DIA A DIA 15KG",
    "categoria": "racao-seca",
    "subcategoria": "racao-seca",
    "preco": 100.0,
    "imagem": "images/produtos/PRD00167.jpg",
    "descricao": "ROBUSTUS GATO AD DIA A DIA 15KG",
    "destaque": false
  },
  {
    "id": 3318084585,
    "nome": "ROBUSTUS GATO ADULTO 10,1 KG",
    "categoria": "racao-seca",
    "subcategoria": "racao-seca",
    "preco": 89.84,
    "imagem": "images/produtos/PRD00172.jpg",
    "descricao": "ROBUSTUS GATO ADULTO 10,1 KG",
    "destaque": false
  },
  {
    "id": 3318084536,
    "nome": "ROBUSTUS GATO ADULTO 20 KG",
    "categoria": "racao-seca",
    "subcategoria": "racao-seca",
    "preco": 172.39,
    "imagem": "images/produtos/PRD00171.jpg",
    "descricao": "ROBUSTUS GATO ADULTO 20 KG",
    "destaque": false
  },
  {
    "id": 3318084424,
    "nome": "ROBUSTUS GATO CASTRADO FRANGO 10,1 KG",
    "categoria": "racao-seca",
    "subcategoria": "racao-seca",
    "preco": 101.8,
    "imagem": "images/produtos/PRD00170.jpg",
    "descricao": "ROBUSTUS GATO CASTRADO FRANGO 10,1 KG",
    "destaque": false
  },
  {
    "id": 3318084262,
    "nome": "ROBUSTUS GATO CASTRADO FRANGO 3 KG",
    "categoria": "racao-seca",
    "subcategoria": "racao-seca",
    "preco": 35.0,
    "imagem": "images/produtos/PRD00168.jpg",
    "descricao": "ROBUSTUS GATO CASTRADO FRANGO 3 KG",
    "destaque": false
  },
  {
    "id": 3318084418,
    "nome": "ROBUSTUS GATO CASTRADO SALMAO 10,1 KG",
    "categoria": "racao-seca",
    "subcategoria": "racao-seca",
    "preco": 101.8,
    "imagem": "images/produtos/PRD00169.jpg",
    "descricao": "ROBUSTUS GATO CASTRADO SALMAO 10,1 KG",
    "destaque": false
  },
  {
    "id": 3313738921,
    "nome": "STEAK DE FRANGO (ZOOMIES)",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 7.5,
    "imagem": "images/produtos/SG0020.jpg",
    "descricao": "STEAK DE FRANGO (ZOOMIES)",
    "destaque": false
  },
  {
    "id": 3313738943,
    "nome": "STEAK DE FRANGO CAIXA c/ 10Un.",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 75.0,
    "imagem": "images/produtos/SG0031.jpg",
    "descricao": "STEAK DE FRANGO CAIXA c/ 10Un.",
    "destaque": false
  },
  {
    "id": 3313738895,
    "nome": "TAPETE DOGHOOD 7Un. FARDO COM 50",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 595.0,
    "imagem": "images/produtos/RC00450.jpg",
    "descricao": "TAPETE DOGHOOD 7Un. FARDO COM 50",
    "destaque": false
  },
  {
    "id": 3313738875,
    "nome": "TAPETE DOGHOOD CARVÃO ATIVADO 30Un.",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 49.5,
    "imagem": "images/produtos/RC002U.jpg",
    "descricao": "TAPETE DOGHOOD CARVÃO ATIVADO 30Un.",
    "destaque": false
  },
  {
    "id": 3313738873,
    "nome": "TAPETE DOGHOOD CARVÃO ATIVADO 30Un. FARDO C/8",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 356.0,
    "imagem": "images/produtos/RC002.jpg",
    "descricao": "TAPETE DOGHOOD CARVÃO ATIVADO 30Un. FARDO C/8",
    "destaque": false
  },
  {
    "id": 3313738893,
    "nome": "TAPETE DOGHOOD F7Un. FARDO COM 25",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 322.5,
    "imagem": "images/produtos/RC00425.jpg",
    "descricao": "TAPETE DOGHOOD F7Un. FARDO COM 25",
    "destaque": false
  },
  {
    "id": 3313738871,
    "nome": "TAPETE DOGHOOD TRADICIONAL 30Un.",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 44.5,
    "imagem": "images/produtos/RC003U.jpg",
    "descricao": "TAPETE DOGHOOD TRADICIONAL 30Un.",
    "destaque": false
  },
  {
    "id": 3313740030,
    "nome": "TAPETE DOGHOOD TRADICIONAL 30Un. FARDO C/8",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 316.0,
    "imagem": "images/produtos/RC003.jpg",
    "descricao": "TAPETE DOGHOOD TRADICIONAL 30Un. FARDO C/8",
    "destaque": false
  },
  {
    "id": 3313738883,
    "nome": "TAPETE DOGHOOD TRADICIONAL 50Un.",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 66.9,
    "imagem": "images/produtos/RC001U.jpg",
    "descricao": "TAPETE DOGHOOD TRADICIONAL 50Un.",
    "destaque": false
  },
  {
    "id": 3313740036,
    "nome": "TAPETE DOGHOOD TRADICIONAL 50Un. FARDO C/6",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 376.0,
    "imagem": "images/produtos/RC001.jpg",
    "descricao": "TAPETE DOGHOOD TRADICIONAL 50Un. FARDO C/6",
    "destaque": false
  },
  {
    "id": 3313740038,
    "nome": "TAPETE DOGHOOD c/ 7Un.",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 13.9,
    "imagem": "images/produtos/RC004U.jpg",
    "descricao": "TAPETE DOGHOOD c/ 7Un.",
    "destaque": false
  },
  {
    "id": 3313739828,
    "nome": "TOALHA DESCARTÁVEL",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 144.0,
    "imagem": "images/produtos/PRD00074.jpg",
    "descricao": "TOALHA DESCARTÁVEL",
    "destaque": false
  },
  {
    "id": 3313739628,
    "nome": "Tonalizante pelos claros 1lt",
    "categoria": "higiene-e-limpeza",
    "subcategoria": "higiene-e-limpeza",
    "preco": 147.9,
    "imagem": "images/produtos/PA0012.jpg",
    "descricao": "Tonalizante pelos claros 1lt",
    "destaque": false
  },
  {
    "id": 3313738794,
    "nome": "Traqueia - Brupet c/ 1 un.",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 5.6,
    "imagem": "images/produtos/PRD00096.jpg",
    "descricao": "Traqueia - Brupet c/ 1 un.",
    "destaque": false
  },
  {
    "id": 3313738899,
    "nome": "Traqueia - Brupet c/ 2 un.",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 10.75,
    "imagem": "images/produtos/PRD00151.jpg",
    "descricao": "Traqueia - Brupet c/ 2 un.",
    "destaque": false
  },
  {
    "id": 3313738834,
    "nome": "UNIDADE BEEFLEX DE CARNE 70G",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 1.95,
    "imagem": "images/produtos/PRD00116.jpg",
    "descricao": "UNIDADE BEEFLEX DE CARNE 70G",
    "destaque": false
  },
  {
    "id": 3313738758,
    "nome": "UNIDADE DE BIFINHO SABOR CARNE 800g - BRUPET",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 30.5,
    "imagem": "images/produtos/PRD00068.jpg",
    "descricao": "UNIDADE DE BIFINHO SABOR CARNE 800g - BRUPET",
    "destaque": false
  },
  {
    "id": 3313738749,
    "nome": "UNIDADE DE BIFINHO SABOR FRANGO 400g - BRUPET",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 16.5,
    "imagem": "images/produtos/PRD00064.jpg",
    "descricao": "UNIDADE DE BIFINHO SABOR FRANGO 400g - BRUPET",
    "destaque": false
  },
  {
    "id": 3313738737,
    "nome": "UNIDADE DE BIFINHO SABOR FRANGO 50g - BRUPET",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 2.9,
    "imagem": "images/produtos/PRD00058.jpg",
    "descricao": "UNIDADE DE BIFINHO SABOR FRANGO 50g - BRUPET",
    "destaque": false
  },
  {
    "id": 3313738751,
    "nome": "UNIDADE DE BIFINHO SABOR FRANGO 800g - BRUPET",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 30.5,
    "imagem": "images/produtos/PRD00065.jpg",
    "descricao": "UNIDADE DE BIFINHO SABOR FRANGO 800g - BRUPET",
    "destaque": false
  },
  {
    "id": 3313738745,
    "nome": "UNIDADE DE BIFINHOS DE CARNE 400g - BRUPET",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 16.5,
    "imagem": "images/produtos/PRD00062.jpg",
    "descricao": "UNIDADE DE BIFINHOS DE CARNE 400g - BRUPET",
    "destaque": false
  },
  {
    "id": 3313738741,
    "nome": "UNIDADE DE BIFINHOS DE CARNE 50g - BRUPET",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 2.9,
    "imagem": "images/produtos/PRD00060.jpg",
    "descricao": "UNIDADE DE BIFINHOS DE CARNE 50g - BRUPET",
    "destaque": false
  },
  {
    "id": 3313738717,
    "nome": "UNIDADE DE CASCO BOVINO - Brupet",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 8.0,
    "imagem": "images/produtos/PRD00048.jpg",
    "descricao": "UNIDADE DE CASCO BOVINO - Brupet",
    "destaque": false
  },
  {
    "id": 3313738729,
    "nome": "UNIDADE DE MEIO CHIFRE BOVINO - Brupet",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 4.2,
    "imagem": "images/produtos/PRD00054.jpg",
    "descricao": "UNIDADE DE MEIO CHIFRE BOVINO - Brupet",
    "destaque": false
  },
  {
    "id": 3313738733,
    "nome": "UNIDADE DE PALITO 605 - 1KG - Brupet",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 18.75,
    "imagem": "images/produtos/PRD00056.jpg",
    "descricao": "UNIDADE DE PALITO 605 - 1KG - Brupet",
    "destaque": false
  },
  {
    "id": 3313738721,
    "nome": "UNIDADE DE PALITO 805 C/ 9 UNIDADES - Brupet",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 2.3,
    "imagem": "images/produtos/PRD00050.jpg",
    "descricao": "UNIDADE DE PALITO 805 C/ 9 UNIDADES - Brupet",
    "destaque": false
  },
  {
    "id": 3313738838,
    "nome": "UNIDADE DE PALITO FLEXÍVEL - BACON - Brupet",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 9.4,
    "imagem": "images/produtos/PRD00123.jpg",
    "descricao": "UNIDADE DE PALITO FLEXÍVEL - BACON - Brupet",
    "destaque": false
  },
  {
    "id": 3313738846,
    "nome": "UNIDADE DE PALITO FLEXÍVEL - LEITE - Brupet",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 9.4,
    "imagem": "images/produtos/PRD00127.jpg",
    "descricao": "UNIDADE DE PALITO FLEXÍVEL - LEITE - Brupet",
    "destaque": false
  },
  {
    "id": 3313738725,
    "nome": "UNIDADE DE PALITO FLEXÍVEL - MENTA - Brupet",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 9.4,
    "imagem": "images/produtos/PRD00052.jpg",
    "descricao": "UNIDADE DE PALITO FLEXÍVEL - MENTA - Brupet",
    "destaque": false
  },
  {
    "id": 3315711096,
    "nome": "UNIDADE DE PALITO FLEXÍVEL c/ 10 Un. ZD - MENTA - Brupet",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 5.5,
    "imagem": "images/produtos/PRD00160.jpg",
    "descricao": "UNIDADE DE PALITO FLEXÍVEL c/ 10 Un. ZD - MENTA - Brupet",
    "destaque": false
  },
  {
    "id": 3315710970,
    "nome": "UNIDADE DE PALITO FLEXÍVEL c/ 10 Un. ZD- LEITE - Brupet",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 5.5,
    "imagem": "images/produtos/PRD00159.jpg",
    "descricao": "UNIDADE DE PALITO FLEXÍVEL c/ 10 Un. ZD- LEITE - Brupet",
    "destaque": false
  },
  {
    "id": 3315711118,
    "nome": "UNIDADE DE PALITO FLEXÍVEL c/10 Un. ZD - BACON - Brupet",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 5.5,
    "imagem": "images/produtos/PRD00161.jpg",
    "descricao": "UNIDADE DE PALITO FLEXÍVEL c/10 Un. ZD - BACON - Brupet",
    "destaque": false
  },
  {
    "id": 3313738713,
    "nome": "UNIDADE PÉ DE FRANGO - BRUPET",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 6.5,
    "imagem": "images/produtos/PRD00046.jpg",
    "descricao": "UNIDADE PÉ DE FRANGO - BRUPET",
    "destaque": false
  },
  {
    "id": 3313738848,
    "nome": "Unidade chips pulmão bovino - Brupet",
    "categoria": "petiscos-secos",
    "subcategoria": "petiscos-secos",
    "preco": 11.0,
    "imagem": "images/produtos/PRD00128.jpg",
    "descricao": "Unidade chips pulmão bovino - Brupet",
    "destaque": false
  }
];

const categorias = [
  {
    "id": "higiene-e-limpeza",
    "label": "Higiene e limpeza",
    "icone": "🛁",
    "imagem": "images/cat-higiene-e-limpeza.jpg",
    "sub": []
  },
  {
    "id": "petiscos-secos",
    "label": "Petiscos Secos",
    "icone": "🦴",
    "imagem": "images/cat-petiscos-secos.jpg",
    "sub": []
  },
  {
    "id": "racao-seca",
    "label": "Ração Seca",
    "icone": "🥣",
    "imagem": "images/cat-racao-seca.jpg",
    "sub": []
  }
];
