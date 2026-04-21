import re

def mascarar_dados_sensiveis(texto_bruto: str) -> str:
    """
    Guarda-costas (Guardrail) de PII: Analisa o texto extraído pelo OCR
    e mascara informações sensíveis antes que estas cheguem ao LLM ou RAG.
    """
    if not texto_bruto:
        return ""

    texto_sanitizado = texto_bruto

    padrao_email = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    texto_sanitizado = re.sub(padrao_email, '[EMAIL_REMOVIDO]', texto_sanitizado)

    padrao_telefone = r'(\+?\d{2,3}?)?[\s-]?\(?\d{2,3}\)?[\s-]?\d{4,5}[\s-]?\d{4}'
    texto_sanitizado = re.sub(padrao_telefone, '[TELEFONE_REMOVIDO]', texto_sanitizado)

    padrao_documento = r'\b\d{3}[\.\s-]?\d{3}[\.\s-]?\d{3}[-\s]?\d{2}\b|\b\d{9}\b'
    texto_sanitizado = re.sub(padrao_documento, '[DOC_MASCARADO]', texto_sanitizado)

    padrao_conselho = r'\b(?:CRM|OM|CRO)[-\s]?[A-Z]{0,2}[-\s]?\d{4,6}\b'
    texto_sanitizado = re.sub(padrao_conselho, '[LICENCA_MEDICA_OCULTA]', texto_sanitizado, flags=re.IGNORECASE)

    padroes_nome = [
        r'(?i)(paciente\s*:?\s*)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
        r'(?i)(nome\s*:?\s*)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
        r'(?i)(sr\.|sra\.)\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)'
    ]
    
    for padrao in padroes_nome:
        texto_sanitizado = re.sub(padrao, r'\1[NOME_PACIENTE_MASCARADO]', texto_sanitizado)

    return texto_sanitizado
    