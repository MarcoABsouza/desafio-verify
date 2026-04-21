import json
import os

exames_base = [
    ("Hemograma", "Avaliação das células sanguíneas"),
    ("Glicemia", "Medição de açúcar no sangue"),
    ("Colesterol", "Perfil lipídico"),
    ("Triglicerídeos", "Avaliação de gordura no sangue"),
    ("TGO (AST)", "Enzima hepática"),
    ("TGP (ALT)", "Enzima hepática"),
    ("Ureia", "Avaliação da função renal"),
    ("Creatinina", "Avaliação da função renal"),
    ("Ácido Úrico", "Produto do metabolismo das purinas"),
    ("Sódio", "Eletrólito sérico"),
    ("Potássio", "Eletrólito sérico"),
    ("Cálcio", "Mineral circulante"),
    ("TSH", "Hormônio estimulante da tireoide"),
    ("T4 Livre", "Hormônio tireoidiano"),
    ("Vitamina D", "Avaliação vitamínica"),
]

db = []
contador = 1

for exame, desc in exames_base:
    variacoes = ["", " de Jejum", " Pós-Prandial", " Total", " Frações", " Sérico", " Urinário"]
    for var in variacoes:
        nome_final = f"{exame}{var}".strip()
        db.append({
            "codigo": f"EX-{contador:04d}",
            "nome": nome_final,
            "descricao": f"{desc} ({nome_final})"
        })
        contador += 1

caminho_db = os.path.join("mcp-rag", "mock_db.json")

with open(caminho_db, "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=4)

print(f"Base de dados gerada com sucesso! Total de exames: {len(db)}")