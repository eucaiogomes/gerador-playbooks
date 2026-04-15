"""
Agente Extrator - Lê e estrutura o conteúdo dos documentos DOCX
"""

from crewai import Agent
from textwrap import dedent


def create_extractor_agent(llm=None):
    """
    Cria o agente extrator que analisa documentos Word
    e extrai conteúdo estruturado mantendo a hierarquia original
    """
    return Agent(
        role="Especialista em Extração de Documentos",
        goal=dedent("""
            Extrair todo o conteúdo de documentos DOCX de forma estruturada,
            preservando a hierarquia de títulos, a ordem do conteúdo,
            e identificando imagens, tabelas e elementos visuais.
            NÃO inventar ou modificar o conteúdo, apenas organizá-lo.
        """),
        backstory=dedent("""
            Você é um especialista em análise documental com anos de experiência
            em processamento de documentos corporativos. Sua habilidade única é
            identificar a estrutura lógica de qualquer documento, separando
            títulos, seções, procedimentos e elementos visuais sem perder nenhum
            detalhe do conteúdo original.
        """),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
