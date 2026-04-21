from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List
import uuid

app = FastAPI(
    title="API de Agendamento Laboratorial",
    description="Recebe a confirmação de exames processados pelo Agente via RAG e efetiva o agendamento.",
    version="1.0.0"
)

class ExameItem(BaseModel):
    codigo: str = Field(
        ..., 
        description="Código oficial do exame recuperado na base RAG.", 
        example="EX-1045"
    )
    nome: str = Field(
        ..., 
        description="Nome do exame extraído via OCR.", 
        example="Hemograma Completo"
    )

class AgendamentoRequest(BaseModel):
    exames: List[ExameItem] = Field(
        ..., 
        min_length=1, 
        description="Lista de exames a serem agendados."
    )

class AgendamentoResponse(BaseModel):
    agendamento_id: str
    status: str
    mensagem: str
    exames_confirmados: List[str]

@app.post(
    "/agendamentos",
    response_model=AgendamentoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo agendamento",
    tags=["Agendamentos"]
)
async def criar_agendamento(request: AgendamentoRequest):
    """
    Recebe uma lista de exames e simula a persistência de um agendamento.
    Retorna o ID gerado e a confirmação dos códigos processados.
    """
    if not request.exames:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="A lista de exames não pode estar vazia."
        )

    agendamento_id = str(uuid.uuid4())
    
    codigos_confirmados = [exame.codigo for exame in request.exames]

    return AgendamentoResponse(
        agendamento_id=agendamento_id,
        status="Sucesso",
        mensagem="Agendamento processado e confirmado.",
        exames_confirmados=codigos_confirmados
    )