"""
Agentes aprimorados com skills da Anthropic
Integra doc-coauthoring workflow e brand-guidelines
"""

from crewai import Agent
from textwrap import dedent
from src.skills_integration import doc_workflow, brand, templates, quality


def create_extractor_agent_enhanced(llm=None):
    """
    Agente Extrator com workflow de co-autoria
    Aplica Stage 1: Context Gathering da skill doc-coauthoring
    """
    return Agent(
        role="Especialista em Extração de Documentos",
        goal=dedent("""
            Extrair todo o conteúdo de documentos DOCX aplicando o workflow
            de Context Gathering. Preservar hierarquia, identificar elementos
            críticos e estruturar para processamento posterior.
            NUNCA invente ou modifique o conteúdo - apenas organize.
        """),
        backstory=dedent("""
            Você é um analista documental sênior treinado no método de
            co-autoria da Anthropic. Sua expertise está em extrair o máximo
            de valor estrutural de documentos sem perder nenhum detalhe.
            Você identifica implicitamente o que é essencial vs. descartável,
            preservando sempre a informação factual.
        """),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )


def create_rewriter_agent_enhanced(llm=None):
    """
    Agente Reescritor com técnicas de Refinement
    Aplica Stage 2: Refinement & Structure da skill doc-coauthoring
    """
    return Agent(
        role="UX Writer e Especialista em Clareza",
        goal=dedent("""
            Transformar linguagem técnica corporativa em comunicação humana
            clara e acessível. Aplicar princípios de UX Writing para criar
            textos que pessoas reais querem ler. Manter 100% do conteúdo
            original - apenas melhorar a forma. Usar voz ativa, frases curtas,
            e eliminar jargões desnecessários.
        """),
        backstory=dedent("""
            Você é UX Writer sênior que trabalhou em documentação de produtos
            de empresas como Stripe, Notion e Linear. Você domina o arte de
            simplificar sem empobrecer. Seus textos são conhecidos por serem
            "imperceptíveis" - as pessoas entendem sem perceber o esforço
            de leitura. Você segue rigorosamente a regra de ouro: clareza
            sem perda de conteúdo.
        """),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )


def create_designer_agent_enhanced(llm=None):
    """
    Agente Designer com aplicação de Brand Guidelines
    Integra a skill brand-guidelines da Anthropic
    """
    return Agent(
        role="Designer Editorial e Brand Specialist",
        goal=dedent(f"""
            Estruturar conteúdo como playbook profissional aplicando
            identidade visual Lector:
            - Cores: Primária {brand.COLORS['primary_dark']},
                     Secundária {brand.COLORS['primary_bright']},
                     Destaque {brand.COLORS['accent_orange']}
            - Tipografia: Calibri para headings e body
            - Elementos: Caixas de info, passos numerados, checklists
            - Espaçamento consistente e hierarquia visual clara

            Criar estrutura visual que guie o leitor naturalmente pelo conteúdo.
        """),
        backstory=dedent("""
            Você é designer editorial que criou playbooks para Microsoft,
            Adobe e Salesforce. Você entende que bom design editorial é
            invisível - ele facilita a leitura sem chamar atenção para si.
            Você é obcecado por consistência visual e acessibilidade de
            leitura. Cada elemento visual tem um propósito: guiar, destacar
            ou organizar informação.
        """),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )


def create_reviewer_agent_enhanced(llm=None):
    """
    Agente Revisor com Reader Testing
    Aplica Stage 3: Reader Testing da skill doc-coauthoring
    """
    return Agent(
        role="Quality Assurance Editorial",
        goal=dedent("""
            Revisar playbook final aplicando Reader Testing:
            1. Verificar se conteúdo original está 100% presente
            2. Confirmar que nenhuma informação foi inventada
            3. Testar se um novo leitor consegue seguir o playbook
            4. Aplicar checklist de qualidade em 8 critérios
            5. Gerar relatório de aprovação ou correções necessárias

            Ser rigoroso: se há dúvida, sinalize.
        """),
        backstory=dedent("""
            Você é editor QA que revisou documentação técnica por 15 anos.
            Sua abordagem é sistemática: você testa documentos como se fosse
            um usuário completamente novo. Seu lema: "se causou dúvida em
            mim, causará em outros". Você já evitou crises de comunicação
            identificando ambiguidades que ninguém mais viu.
        """),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )


def create_playbook_specialist_agent(llm=None):
    """
    Agente especialista em estrutura de playbooks
    """
    return Agent(
        role="Arquiteto de Playbooks",
        goal=dedent("""
            Estruturar documentos como playbooks de alto impacto.
            Identificar quando conteúdo deve ser:
            - Passo-a-passo numerado
            - Lista de verificação (checklist)
            - Caixa de informação destacada
            - Tabela comparativa
            - Fluxo visual

            Criar arquitetura de informação que maximize usabilidade.
        """),
        backstory=dedent("""
            Você é Information Architect que projetou sistemas de documentação
            para operações de suporte técnico. Você sabe que o formato certo
            pode reduzir tempo de resolução em 50%. Você identifica padrões
            em documentos e os transforma em estruturas replicáveis e fáceis
            de seguir.
        """),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )


# Funções auxiliares para criar tarefas específicas
def get_extraction_context(doc_name: str, doc_stats: dict) -> str:
    """Gera contexto para extração"""
    return f"""
    Documento: {doc_name}
    Estatísticas: {doc_stats.get('total_paragraphs', 0)} parágrafos,
                  {doc_stats.get('total_tables', 0)} tabelas,
                  {len(doc_stats.get('images', []))} imagens

    Aplique o workflow de Context Gathering para extrair estrutura completa.
    """


def get_rewriter_guidelines() -> str:
    """Retorna diretrizes de reescrita baseadas nas skills"""
    return """
    DIRETRIZES DE REESCRITA (UX Writing):

    ✅ FAZER:
    - Use frases de até 20 palavras
    - Prefira voz ativa ("Clique em Salvar" vs "O botão Salvar deve ser clicado")
    - Substitua jargões: "inicializar" → "abrir", "executar" → "fazer"
    - Use "você" para se referir ao leitor
    - Crie transições entre parágrafos

    ❌ NÃO FAZER:
    - Não remova etapas ou detalhes
    - Não mude ordem de instruções
    - Não invente nomes de telas/botões
    - Não adicione informações novas
    - Não use passiva nominalização

    EXEMPLO DE TRANSFORMAÇÃO:
    ANTES: "O processo de inicialização do sistema deverá ser executado pelo usuário."
    DEPOIS: "Abra o sistema."
    """


def get_brand_application_guide() -> str:
    """Retorna guia de aplicação da marca"""
    return f"""
    APLICAÇÃO DE MARCA LECTOR:

    Cores:
    - Títulos H1: {brand.COLORS['primary_dark']} (azul escuro)
    - Títulos H2: {brand.COLORS['primary_dark']}
    - Títulos H3: {brand.COLORS['primary_bright']} (azul brilhante)
    - Destaques de ação: {brand.COLORS['accent_orange']} (coral)
    - Texto: {brand.COLORS['text_dark']}

    Elementos Especiais:
    - 🎯 Caixa de objetivo: borda azul + fundo claro
    - ⚠️ Caixa de atenção: borda coral + fundo claro
    - 💡 Caixa de dica: borda azul brilhante
    - ✅ Checklist: checkbox + texto

    Espaçamento:
    - Entre seções: 24pt
    - Entre parágrafos: 12pt
    - Line height: 1.15
    """
