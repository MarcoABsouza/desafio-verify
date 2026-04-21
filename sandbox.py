import asyncio
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool import McpToolset, SseConnectionParams

async def test():
    ocr_toolset = await McpToolset.create(
        connection_params=SseConnectionParams(url="http://localhost:8001/sse")
    )
    rag_toolset = await McpToolset.create(
        connection_params=SseConnectionParams(url="http://localhost:8002/sse")
    )
    
    agent = LlmAgent(
        model="gemini-2.5-flash",
        tools=[*ocr_toolset.tools, *rag_toolset.tools]
    )
    print("Agent created:", agent)

asyncio.run(test())
