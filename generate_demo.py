"""
Script para gerar HTML de demonstração com conteúdo realista de playbook Lector
Rode com: python generate_demo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import only HTMLWriter directly to avoid circular/relative import issues
import importlib.util, types

# Manually load html_writer without the package machinery
spec = importlib.util.spec_from_file_location(
    "html_writer",
    Path(__file__).parent / "src" / "tools" / "html_writer.py"
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
HTMLWriter = mod.HTMLWriter


# ── Estrutura de demo simula o retorno de DocxReader.read() ───────────────────
class E:
    """Simula DocumentElement"""
    def __init__(self, type_, content, level=None):
        self.type    = type_
        self.content = content
        self.level   = level
        self.style   = None
        self.formatting = None


demo_content = {
    "file_name": "Processo de Onboarding.docx",
    "images": [],
    "total_paragraphs": 40,
    "total_tables": 2,
    "elements": [
        # ── Seção 1: Objetivo ───────────────────────────────────────────────
        E("heading", "Objetivo do Processo", 1),
        E("paragraph", "🎯 Objetivo — Garantir que todos os novos colaboradores tenham uma experiência de integração padronizada, produtiva e alinhada com a cultura da Lector IT."),
        E("paragraph", "Este playbook descreve todas as etapas do processo de Onboarding, desde a aprovação da contratação até o fim do período de experiência."),
        E("paragraph", "💡 Dica — Compartilhe este documento com o gestor responsável antes do primeiro dia do colaborador para que tudo esteja preparado com antecedência."),

        # ── Seção 2: Pré-Onboarding ─────────────────────────────────────────
        E("heading", "Pré-Onboarding (Antes do 1º dia)", 1),
        E("paragraph", "As atividades abaixo devem ser realizadas pelo RH e pelo gestor direto com pelo menos 3 dias úteis de antecedência."),

        E("heading", "Responsabilidades do RH", 2),
        E("paragraph", "□ Enviar e-mail de boas-vindas ao novo colaborador"),
        E("paragraph", "□ Criar login no Active Directory"),
        E("paragraph", "□ Provisionar acesso ao Jira, Confluence e e-mail corporativo"),
        E("paragraph", "□ Preparar crachá e equipamentos (notebook, headset)"),
        E("paragraph", "□ Inserir colaborador no grupo do Teams da equipe"),

        E("heading", "Responsabilidades do Gestor", 2),
        E("paragraph", "□ Definir buddy (colega padrinho) para o período de experiência"),
        E("paragraph", "□ Preparar agenda da primeira semana"),
        E("paragraph", "□ Reservar sala para reunião de boas-vindas"),
        E("paragraph", "□ Comunicar a chegada do novo membro para o time"),

        # ── Seção 3: Primeiro Dia ────────────────────────────────────────────
        E("heading", "Primeiro Dia", 1),
        E("paragraph", "O primeiro dia define a percepção inicial do colaborador sobre a empresa. Siga esta sequência:"),

        E("heading", "Cronograma Sugerido", 2),
        E("paragraph", ""),  # spacer
    ],
}

# Adicionar tabela de cronograma
demo_content["elements"].append(
    E("table", [
        ["Horário", "Atividade", "Responsável"],
        ["08:30", "Recepção na portaria e entrega de crachá", "RH"],
        ["09:00", "Reunião de boas-vindas com a equipe", "Gestor"],
        ["10:00", "Apresentação dos sistemas e ferramentas", "TI"],
        ["11:00", "Tour pelo escritório e apresentação pessoal", "Buddy"],
        ["12:00", "Almoço de integração com o time", "Gestor"],
        ["14:00", "Leitura do Código de Conduta e Políticas", "RH"],
        ["15:30", "Configuração de ambiente de trabalho", "TI"],
        ["17:00", "Alinhamento de expectativas e dúvidas", "Gestor"],
    ])
)

demo_content["elements"] += [
    E("paragraph", "⚠️ Atenção — Não agende reuniões operacionais no primeiro dia. O objetivo é ambientação, não produtividade imediata."),

    # ── Seção 4: Primeiros 30 dias ───────────────────────────────────────────
    E("heading", "Acompanhamento — Primeiros 30 Dias", 1),
    E("paragraph", "Durante o primeiro mês, o gestor deve conduzir check-ins semanais de 30 minutos para monitorar a adaptação do colaborador."),

    E("heading", "Checklist — Semana 1", 2),
    E("paragraph", "□ Apresentar o colaborador a todos os stakeholders principais"),
    E("paragraph", "□ Garantir que todos os acessos estão funcionando"),
    E("paragraph", "□ Confirmar entendimento do organograma e dos processos"),
    E("paragraph", "□ Verificar se o buddy está em contato regular"),

    E("heading", "Checklist — Semana 2 a 4", 2),
    E("paragraph", "□ Realizar check-in semanal de alinhamento"),
    E("paragraph", "□ Apresentar o plano de desenvolvimento individual (PDI)"),
    E("paragraph", "□ Avaliar adaptação técnica e cultural"),
    E("paragraph", "□ Coletar feedback do colaborador sobre o processo"),
    E("paragraph", "□ Registrar observações no sistema de RH (CIGAM)"),

    # ── Seção 5: Avaliação de Período de Experiência ─────────────────────────
    E("heading", "Avaliação do Período de Experiência", 1),
    E("paragraph", "Ao final do período de experiência (45 ou 90 dias), deve ser realizada uma avaliação formal entre gestor e colaborador."),
    E("paragraph", "ℹ️ Informação — A avaliação deve ser registrada no CIGAM até 5 dias antes do vencimento do contrato de experiência para garantir o processo de efetivação dentro do prazo legal."),

    E("heading", "Documentos Necessários", 2),
]

demo_content["elements"].append(
    E("table", [
        ["Documento", "Prazo", "Responsável", "Sistema"],
        ["Formulário de Avaliação", "5 dias antes", "Gestor", "CIGAM - RH"],
        ["Feedback 360°", "7 dias antes", "RH", "Formulário Teams"],
        ["Aprovação de Efetivação", "3 dias antes", "Diretoria", "E-mail"],
        ["Aditivo Contratual", "1 dia antes", "RH", "CIGAM - DP"],
    ])
)

demo_content["elements"] += [
    E("paragraph", "□ Formulário de avaliação preenchido pelo gestor"),
    E("paragraph", "□ Autoavaliação preenchida pelo colaborador"),
    E("paragraph", "□ Parecer do buddy registrado"),
    E("paragraph", "□ Decisão de efetivação comunicada formalmente"),
    E("paragraph", "□ Aditivo contratual assinado"),
]


# ── Carregar logo ─────────────────────────────────────────────────────────────
logo_path = Path(r"C:\Users\Lector\Downloads\logo\logo-lector.svg")
logo_svg  = logo_path.read_text(encoding='utf-8') if logo_path.exists() else ""

# ── Gerar HTML ─────────────────────────────────────────────────────────────────
output_path = Path(__file__).parent / "output" / "DEMO_Processo de Onboarding.html"
output_path.parent.mkdir(exist_ok=True)

writer = HTMLWriter(output_path=output_path, title="Processo de Onboarding", logo_svg=logo_svg)
writer.build_from_doc_content(demo_content)
saved = writer.save()

print(f"\nMini-app gerado com sucesso!")
print(f"Abra no navegador: {saved.resolve()}\n")
