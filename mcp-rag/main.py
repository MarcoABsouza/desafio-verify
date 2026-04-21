from mcp.server.fastmcp import FastMCP
import json
import os

mcp = FastMCP("Servidor-RAG", host="0.0.0.0", port=8002)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_DB = os.path.join(BASE_DIR, "mock_db.json")

try:
    with open(CAMINHO_DB, "r", encoding="utf-8") as f:
        DATABASE = json.load(f)
except FileNotFoundError:
    DATABASE = []

@mcp.tool()
def consultar_exames(texto_ocr: str) -> list[dict]:
    """
    Ferramenta MCP (RAG): Recebe o texto sujo do OCR e recupera os 
    códigos oficiais e detalhes dos exames correspondentes na base.
    """
    if not texto_ocr:
        return []

    exames_encontrados = []
    texto_limpo = texto_ocr.lower()
    
    for exame in DATABASE:
        if exame["nome"].lower() in texto_limpo:
            exames_encontrados.append({
                "codigo": exame["codigo"],
                "nome": exame["nome"]
            })
            
    return exames_encontrados

if __name__ == "__main__":
    mcp.run(transport='sse')