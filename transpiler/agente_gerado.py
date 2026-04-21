import asyncio
import sys
import os
import httpx

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from security.guardrail import mascarar_dados_sensiveis

import warnings
import logging
warnings.showwarning = lambda *args, **kwargs: None
logging.getLogger().setLevel(logging.ERROR)

from google.adk.agents.llm_agent import LlmAgent
from google.adk.apps import App
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool import McpToolset, SseConnectionParams
from google.adk.tools.function_tool import FunctionTool
from google.genai.types import Content, Part

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

if "GEMINI_API_KEY" not in os.environ:
    print("Aviso: GEMINI_API_KEY não foi encontrada no ambiente. Isso causará um erro ao conectar com a API.")
    os.environ["GEMINI_API_KEY"] = "[ENCRYPTION_KEY]"

API_DESTINO = "http://localhost:8000/agendamentos"
MCP_OCR_URL = "http://localhost:8001/sse"
MCP_RAG_URL = "http://localhost:8002/sse"

async def extrair_e_mascarar(caminho_imagem: str) -> str:
    from mcp.client.sse import sse_client
    from mcp.client.session import ClientSession
    
    async with sse_client(url=MCP_OCR_URL) as (ler_ocr, esc_ocr):
        async with ClientSession(ler_ocr, esc_ocr) as sessao_ocr:
            await sessao_ocr.initialize()
            resultado = await sessao_ocr.call_tool("extrair_texto_pedido", arguments={"caminho_arquivo": caminho_imagem})
            if resultado.isError or not resultado.content:
                return ""
            texto = resultado.content[0].text
            texto = mascarar_dados_sensiveis(texto)
            return texto

def agendar_exames(exames: list[dict]) -> str:
    """Envia os exames para a API de agendamento FastAPI e retorna o resultado. A lista deve conter o codigo e o nome do exame."""
    try:
        resposta = httpx.post(API_DESTINO, json={"exames": exames}, timeout=10.0)
        if resposta.status_code == 201:
            dados = resposta.json()
            return f"Agendamento concluído! ID: {dados.get('agendamento_id')}. Códigos: {dados.get('exames_confirmados')}"
        return f"Erro na API de agendamento: {resposta.text}"
    except Exception as e:
        return f"Falha na conexão com a API: {e}"

async def executar_fluxo(caminho_imagem: str):
    print(f"\nIniciando Agente [AssistenteLaboratorialCLI]")
    print(f"Processando imagem: {caminho_imagem}\n")
    
    print("1. [Extração/Segurança] Lendo imagem via OCR e mascarando PII")
    texto_seguro = await extrair_e_mascarar(caminho_imagem)
    if not texto_seguro:
        print("Nenhum texto pôde ser extraído.")
        return
    
    print("Texto processado pronto para o agente:\n", texto_seguro, "\n")
    
    print("2. [Consulta/Agendamento] Instanciando agente autônomo ADK")
    rag_toolset = McpToolset(connection_params=SseConnectionParams(url=MCP_RAG_URL))
    agendar_tool = FunctionTool(agendar_exames)

    agent = LlmAgent(
        name="AssistenteLaboratorialCLI",
        model="gemini-2.5-flash-lite",
        tools=[rag_toolset, agendar_tool]
    )
    
    app = App(name="AssistenteLaboratorialCLI_app", root_agent=agent)
    session_service = InMemorySessionService()

    prompt = f"""
Você deve seguir o fluxo estritamente sem conversas fiadas ou saudações informais. VÁ DIRETO para a execução das ferramentas.
1. Analise os exames listados neste texto:
{texto_seguro}
2. Use a ferramenta de consultar exames via RAG para obter os códigos exatos dos exames.
3. Chame a ferramenta de agendar_exames para submetê-los à API.
4. Ao final, apresente um resumo contendo apenas o resultado final do agendamento feito.
"""
    
    msg = Content(role="user", parts=[Part.from_text(text=prompt)])
    
    resposta = ""
    async with Runner(app=app, session_service=session_service, auto_create_session=True) as runner:
        async for event in runner.run_async(user_id="cli_user", session_id="cli_session", new_message=msg):
            if hasattr(event, "content") and event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        resposta += part.text

    print("\n=== RESPOSTA DO AGENTE ===")
    print(resposta)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python agente_gerado.py <caminho_para_imagem>")
        sys.exit(1)
    asyncio.run(executar_fluxo(sys.argv[1]))
