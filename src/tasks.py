"""
Tarefas do CrewAI para processamento de playbooks
"""

from crewai import Task
from textwrap import dedent
from typing import Dict, Any, List


def create_extraction_task(agent, docx_content: Dict[str, Any]) -> Task:
    """
    Tarefa de extração estruturada do documento
    """
    return Task(
        description=dedent(f"""
            Analise o seguinte conteúdo extraído de um documento DOCX e estruture-o
            de forma organizada, identificando:

            1. **Título principal** do documento
            2. **Seções e subtítulos** (com nível hierárquico)
            3. **Conteúdo de cada seção** (parágrafos, listas)
            4. **Tabelas** (preservando estrutura de dados)
            5. **Imagens** (quantidade e referências)
            6. **Procedimentos passo-a-passo** (se houver)

            CONTÉUDO BRUTO:
            {docx_content}

            Retorne um JSON estruturado com:
            - title: título principal
            - sections: lista de seções com título, nível e conteúdo
            - images: lista de referências de imagens
            - tables: lista de tabelas encontradas
            - steps: lista de procedimentos passo-a-passo

            IMPORTANTE: NÃO modifique o conteúdo textual, apenas organize-o.
        """),
        agent=agent,
        expected_output="JSON estruturado com hierarquia completa do documento",
    )


def create_rewrite_task(agent, extracted_content: str) -> Task:
    """
    Tarefa de reescrita em linguagem humana
    """
    return Task(
        description=dedent(f"""
            Reescreva o seguinte conteúdo estruturado em linguagem humana,
            clara e acessível, mantendo 100% das informações originais:

            CONTÉUDO EXTRAÍDO:
            {extracted_content}

            DIRETRIZES DE REESCRITA:
            1. Use frases curtas e diretas
            2. Substitua jargões técnicos por termos do dia-a-dia
            3. Use voz ativa sempre que possível
            4. Crie transições suaves entre seções
            5. Adicione exemplos práticos se o original tiver
            6. Mantenha TODOS os passos, números e detalhes técnicos
            7. Preserve referências a sistemas, telas e botões exatamente como estão

            PROIBIDO:
            - Adicionar informações que não existam no original
            - Remover etapas ou detalhes
            - Mudar o sentido das instruções
            - Inventar nomes de telas, botões ou campos

            Retorne o conteúdo reescrito mantendo a mesma estrutura JSON.
        """),
        agent=agent,
        expected_output="Conteúdo reescrito em linguagem humana, estrutura JSON mantida",
    )


def create_design_task(agent, rewritten_content: str, brand_colors: Dict[str, str]) -> Task:
    """
    Tarefa de design e estruturação visual
    """
    return Task(
        description=dedent(f"""
            Estruture o seguinte conteúdo como um playbook profissional,
            aplicando elementos de design editorial e UX:

            CONTÉUDO REESCRITO:
            {rewritten_content}

            PALETA DE CORES LECTOR:
            - Primária: {brand_colors.get('primary', '#1E3A5F')}
            - Secundária: {brand_colors.get('secondary', '#00A896')}
            - Destaque: {brand_colors.get('accent', '#FF6B35')}

            ELEMENTOS A ADICIONAR:
            1. **Título principal** com formatação de destaque
            2. **Sumário executivo** (2-3 frases sobre o playbook)
            3. **Caixas de informação**:
               - 🎯 "O que você vai aprender" (no início)
               - ⚠️ "Atenção" (para pontos críticos)
               - 💡 "Dica Pro" (para atalhos ou truques)
            4. **Etapas numeradas** para procedimentos
            5. **Checklists** onde aplicável
            6. **Imagens** marcadas para inserção nos locais originais
            7. **Seções bem definidas** com espaçamento visual

            ESTRUTURA DE SAÍDA:
            Retorne instruções detalhadas para o gerador de documento:
            - ordem de elementos
            - formatação para cada elemento
            - posicionamento de imagens
            - estilos a aplicar
        """),
        agent=agent,
        expected_output="Instruções estruturadas para geração do playbook formatado",
    )


def create_review_task(agent, original_content: str, final_design: str) -> Task:
    """
    Tarefa de revisão de qualidade
    """
    return Task(
        description=dedent(f"""
            Compare o conteúdo original com o design final do playbook
            e gere um relatório de qualidade:

            CONTEÚDO ORIGINAL:
            {original_content}

            DESIGN FINAL:
            {final_design}

            CRITÉRIOS DE AVALIAÇÃO:
            1. **Integridade**: Todo conteúdo original está presente?
            2. **Precisão**: Nenhuma informação foi alterada ou inventada?
            3. **Estrutura**: A hierarquia de informações está lógica?
            4. **Imagens**: Todas as imagens foram preservadas?
            5. **Clareza**: O texto está mais legível que o original?
            6. **Tom**: A voz da marca Lector está consistente?

            FORMATO DO RELATÓRIO:
            ```
            ## Relatório de Qualidade - [Nome do Documento]

            ### ✅ Aprovado / ❌ Reprovação com Correções

            ### Pontuação por Critério (1-10):
            - Integridade: X/10
            - Precisão: X/10
            - Estrutura: X/10
            - Imagens: X/10
            - Clareza: X/10
            - Tom de Voz: X/10

            ### Média Geral: X/10

            ### Problemas Encontrados (se houver):
            1. [descrição]
            - Correção sugerida: [ação]

            ### Recomendação Final:
            [APROVADO / REPROVADO - com justificativa]
            ```

            Se REPROVADO, liste exatamente o que precisa ser corrigido.
        """),
        agent=agent,
        expected_output="Relatório de qualidade completo com aprovação ou lista de correções",
    )
