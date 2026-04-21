from mcp.server.fastmcp import FastMCP
import cv2
import fitz
import pytesseract
import os

mcp = FastMCP("Servidor-OCR", host="0.0.0.0", port=8001)

@mcp.tool()
def extrair_texto_pedido(caminho_arquivo: str) -> str:
    """
    Ferramenta MCP: Extrai texto bruto de pedidos médicos.
    Suporta imagens fotográficas/scans e documentos PDF.
    """
    if not os.path.exists(caminho_arquivo):
        return f"Erro: Arquivo não encontrado em {caminho_arquivo}"

    try:
        if caminho_arquivo.lower().endswith('.pdf'):
            doc = fitz.open(caminho_arquivo)
            texto = "\n".join([page.get_text() for page in doc])
            return texto if texto.strip() else "Nenhum texto legível encontrado no PDF."
        
        img = cv2.imread(caminho_arquivo)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        processada = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        texto = pytesseract.image_to_string(processada, lang='por')
        return texto

    except Exception as e:
         return f"Falha na extração OCR: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport='sse')