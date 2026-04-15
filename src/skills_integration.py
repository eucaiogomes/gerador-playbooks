"""
Integração com Skills da Anthropic
Aplica as melhores práticas de doc-coauthoring e brand-guidelines
"""

from typing import Dict, Any, List
from textwrap import dedent


class DocCoauthoringWorkflow:
    """
    Workflow estruturado de co-autoria de documentos
    Adaptado da skill doc-coauthoring da Anthropic
    """

    @staticmethod
    def get_stage1_prompt(doc_type: str, audience: str) -> str:
        """
        Stage 1: Context Gathering
        Coleta contexto sobre o documento
        """
        return dedent(f"""
        ## Stage 1: Context Gathering

        Você está analisando um documento para transformação em playbook.

        **Tipo de documento**: {doc_type}
        **Público-alvo**: {audience}

        Sua tarefa é extrair e organizar:
        1. **Propósito principal** do documento
        2. **Seções e subtítulos** identificados
        3. **Procedimentos passo-a-passo** (se houver)
        4. **Tabelas e dados estruturados**
        5. **Imagens e referências visuais**
        6. **Informações críticas** que não podem ser perdidas

        Formato de saída esperado:
        ```json
        {{
            "title": "Título do Playbook",
            "purpose": "Propósito em 2-3 frases",
            "sections": [
                {{"title": "Nome da Seção", "level": 1, "content_summary": "..."}}
            ],
            "procedures": [
                {{"title": "Procedimento", "steps": ["passo 1", "passo 2"]}}
            ],
            "key_images": ["descrição da imagem 1", "..."],
            "critical_notes": ["nota importante 1", "..."]
        }}
        ```
        """)

    @staticmethod
    def get_stage2_prompt(section_name: str, context: str) -> str:
        """
        Stage 2: Refinement & Structure
        Reescreve uma seção específica
        """
        return dedent(f"""
        ## Stage 2: Refinement & Structure
        ### Seção: {section_name}

        **Contexto original**:
        {context}

        **Sua tarefa**:
        Reescrever este conteúdo mantendo 100% da informação original,
        mas transformando em linguagem humana, clara e acessível.

        **Diretrizes**:
        1. ✅ Use frases curtas e diretas
        2. ✅ Substitua jargões por termos do dia-a-dia
        3. ✅ Use voz ativa
        4. ✅ Crie transições suaves
        5. ✅ Mantenha TODOS os passos, números e detalhes
        6. ✅ Preserve referências a sistemas, telas e botões

        **PROIBIDO**:
        - ❌ Adicionar informações que não existam no original
        - ❌ Remover etapas ou detalhes
        - ❌ Mudar o sentido das instruções
        - ❌ Inventar nomes de telas, botões ou campos

        **Saída**: Texto reescrito da seção
        """)

    @staticmethod
    def get_stage3_prompt(content: str) -> str:
        """
        Stage 3: Reader Testing
        Verifica se o documento funciona para leitores
        """
        return dedent(f"""
        ## Stage 3: Reader Testing

        **Conteúdo a testar**:
        {content}

        **Sua tarefa**: Verificar se este playbook responde a:
        1. O que este documento explica?
        2. Quem deve usar este playbook?
        3. Qual o primeiro passo?
        4. Há alguma informação confusa ou ambígua?
        5. O que este documento assume que o leitor já sabe?
        6. Há contradições ou inconsistências?

        **Saída**: Relatório de leitura com problemas encontrados (se houver)
        """)


class BrandGuidelines:
    """
    Aplica diretrizes de marca da Lector
    Adaptado da skill brand-guidelines da Anthropic
    """

    # Cores Lector extraídas do site
    COLORS = {
        "primary_dark": "#1E3A5F",
        "primary_bright": "#2563EB",
        "primary_medium": "#3B82F6",
        "accent_orange": "#D97757",
        "white": "#FFFFFF",
        "light_gray": "#F7FAFC",
        "border_gray": "#E2E8F0",
        "text_dark": "#2D3748",
        "text_secondary": "#4A5568",
        "success": "#38A169",
        "info_bg": "#EBF8FF",
        "warning_bg": "#FFF5EB",
    }

    # Fontes recomendadas
    FONTS = {
        "heading": "Calibri",
        "body": "Calibri",
        "fallback_heading": "Arial",
        "fallback_body": "Georgia",
    }

    # Elementos de UI
    UI_ELEMENTS = {
        "border_radius": 4,
        "shadow_opacity": 0.1,
        "section_spacing": 24,
        "paragraph_spacing": 12,
    }

    @classmethod
    def get_info_box_style(cls) -> Dict[str, str]:
        """Estilo para caixas de informação"""
        return {
            "border_left": f"4px solid {cls.COLORS['primary_bright']}",
            "background": cls.COLORS["info_bg"],
            "padding": "12px",
            "margin": "12px 0",
        }

    @classmethod
    def get_warning_box_style(cls) -> Dict[str, str]:
        """Estilo para caixas de alerta"""
        return {
            "border_left": f"4px solid {cls.COLORS['accent_orange']}",
            "background": cls.COLORS["warning_bg"],
            "padding": "12px",
            "margin": "12px 0",
        }

    @classmethod
    def get_heading_style(cls, level: int) -> Dict[str, Any]:
        """Retorna estilo para headings baseado no nível"""
        styles = {
            1: {
                "font_size": 32,
                "color": cls.COLORS["primary_dark"],
                "bold": True,
                "space_before": 24,
                "space_after": 12,
            },
            2: {
                "font_size": 26,
                "color": cls.COLORS["primary_dark"],
                "bold": True,
                "space_before": 20,
                "space_after": 10,
            },
            3: {
                "font_size": 20,
                "color": cls.COLORS["primary_bright"],
                "bold": True,
                "space_before": 16,
                "space_after": 8,
            },
        }
        return styles.get(level, styles[3])


class PlaybookTemplates:
    """
    Templates para diferentes tipos de playbooks
    """

    @staticmethod
    def get_header_template(title: str) -> str:
        """Template para header do playbook"""
        return dedent(f"""
        ╔════════════════════════════════════════════════════════════════╗
        ║                                                                ║
        ║                    LECTOR PLAYBOOK SERIES                      ║
        ║                                                                ║
        ║              {title.upper():^50}        ║
        ║                                                                ║
        ╚════════════════════════════════════════════════════════════════╝
        """)

    @staticmethod
    def get_summary_template(purpose: str) -> str:
        """Template para sumário executivo"""
        return dedent(f"""
        🎯 SOBRE ESTE PLAYBOOK

        {purpose}

        Este guia foi criado para ser prático, direto e fácil de seguir.
        Siga os passos na ordem apresentada para obter os melhores resultados.
        """)

    @staticmethod
    def get_step_template(number: int, title: str, description: str) -> str:
        """Template para passos numerados"""
        return dedent(f"""
        ┌─────────────────────────────────────────────────────────────────┐
        │ PASSO {number:02d}: {title.upper()}
        ├─────────────────────────────────────────────────────────────────┤
        │ {description:<64} │
        └─────────────────────────────────────────────────────────────────┘
        """)

    @staticmethod
    def get_tip_box(tip_text: str) -> str:
        """Caixa de dica"""
        return dedent(f"""
        💡 DICA PRO
        {tip_text}
        """)

    @staticmethod
    def get_warning_box(warning_text: str) -> str:
        """Caixa de atenção"""
        return dedent(f"""
        ⚠️ ATENÇÃO
        {warning_text}
        """)


class QualityChecklist:
    """
    Checklist de qualidade baseado nas skills da Anthropic
    """

    CHECKLIST_ITEMS = [
        ("Integridade", "Todo o conteúdo original está presente?"),
        ("Precisão", "Nenhuma informação foi alterada ou inventada?"),
        ("Estrutura", "A hierarquia de informações está lógica?"),
        ("Imagens", "Todas as imagens foram preservadas?"),
        ("Clareza", "O texto está mais legível que o original?"),
        ("Tom de Voz", "A voz da marca Lector está consistente?"),
        ("Formatação", "Há erros de formatação ou estrutura?"),
        ("Usabilidade", "Um novo leitor consegue seguir o playbook?"),
    ]

    @classmethod
    def generate_report(cls, scores: Dict[str, int]) -> str:
        """Gera relatório de qualidade"""
        report = ["## 📊 Relatório de Qualidade\n"]
        total = 0

        for item, score in scores.items():
            status = "✅" if score >= 8 else "⚠️" if score >= 6 else "❌"
            report.append(f"{status} {item}: {score}/10")
            total += score

        average = total / len(scores) if scores else 0
        report.append(f"\n### Média Geral: {average:.1f}/10")

        if average >= 8:
            report.append("\n🎉 **Status: APROVADO** - O playbook está pronto!")
        else:
            report.append("\n📝 **Status: REPROVADO** - Revisar itens marcados com ⚠️ ou ❌")

        return "\n".join(report)


# Instâncias globais
doc_workflow = DocCoauthoringWorkflow()
brand = BrandGuidelines()
templates = PlaybookTemplates()
quality = QualityChecklist()
