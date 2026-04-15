# 🏗️ Arquitetura do Lector Playbook Converter

## Visão Geral

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         SISTEMA DE ENTRADA                               │
│                    Arquivos .docx do usuário                            │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        CAMADA DE EXTRAÇÃO                              │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                     DOCX Reader Tool                             │   │
│  │  • Extrai texto com formatação                                 │   │
│  │  • Preserva hierarquia de títulos                              │   │
│  │  • Extrai imagens (salva em /images)                           │   │
│  │  • Identifica tabelas e listas                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    ORQUESTRADOR CREWAI (Multi-Agente)                   │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐   │
│  │  AGENTE 1: EXTRATOR (Context Gathering)                          │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │  • Identifica seções e subtítulos                        │    │   │
│  │  │  • Classifica tipo de conteúdo (procedimento, info)      │    │   │
│  │  │  • Preserva estrutura hierárquica                        │    │   │
│  │  │  • Extrai elementos visuais                              │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  └───────────────────────────────────────────────────────────────────┘   │
│                                   │                                     │
│                                   ▼                                     │
│  ┌───────────────────────────────────────────────────────────────────┐   │
│  │  AGENTE 2: REESCRITOR (Refinement)                                 │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │  UX Writing Guidelines:                                  │    │   │
│  │  │  • Frases curtas (< 20 palavras)                        │    │   │
│  │  │  • Voz ativa                                             │    │   │
│  │  │  • Jargões → linguagem humana                            │    │   │
│  │  │  • Transições suaves                                     │    │   │
│  │  │  • GARANTIA: 100% conteúdo preservado                    │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  └───────────────────────────────────────────────────────────────────┘   │
│                                   │                                     │
│                                   ▼                                     │
│  ┌───────────────────────────────────────────────────────────────────┐   │
│  │  AGENTE 3: DESIGNER (Brand Application)                            │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │  Identidade Visual Lector:                               │    │   │
│  │  │  • Cores: #1E3A5F, #2563EB, #D97757                    │    │   │
│  │  │  • Tipografia: Calibri                                   │    │   │
│  │  │  • Caixas de info: 🎯 💡 ⚠️                              │    │   │
│  │  │  • Elementos: passos, checklists, tabelas                │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  └───────────────────────────────────────────────────────────────────┘   │
│                                   │                                     │
│                                   ▼                                     │
│  ┌───────────────────────────────────────────────────────────────────┐   │
│  │  AGENTE 4: REVISOR (Reader Testing)                                │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │  Checklist de Qualidade (8 critérios):                   │    │   │
│  │  │  • Integridade, Precisão, Estrutura                      │    │   │
│  │  │  • Imagens, Clareza, Tom de Voz                          │    │   │
│  │  │  • Formatação, Usabilidade                               │    │   │
│  │  │  Score: ≥ 8.0 = Aprovado                                 │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  └───────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        CAMADA DE SAÍDA                                  │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                     DOCX Writer Tool                               │   │
│  │  • Gera arquivo .docx formatado                                  │   │
│  │  • Aplica estilos Lector (cores, fontes)                         │   │
│  │  • Insere imagens extraídas                                      │   │
│  │  • Valida estrutura do documento                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         PLAYBOOK FINAL                                  │
│                    output/PLAYBOOK_[nome].docx                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Integração de Skills

```
┌─────────────────────────────────────────────────────────────────┐
│                    SKILLS INTEGRATION MODULE                     │
│                    (src/skills_integration.py)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────┐  ┌───────────────────┐                │
│  │  DocCoauthoring   │  │  BrandGuidelines    │                │
│  │  Workflow         │  │  (Lector)           │                │
│  │                   │  │                     │                │
│  │  • Stage 1:       │  │  • Cores extraídas  │                │
│  │    Context        │  │    do site          │                │
│  │    Gathering      │  │  • Tipografia       │                │
│  │                   │  │  • Elementos UI     │                │
│  │  • Stage 2:       │  │                     │                │
│  │    Refinement     │  └───────────────────┘                │
│  │                   │                                        │
│  │  • Stage 3:       │  ┌───────────────────┐                │
│  │    Reader Testing │  │  PlaybookTemplates│                │
│  │                   │  │                   │                │
│  └───────────────────┘  │  • Headers        │                │
│                         │  • Info boxes     │                │
│  ┌───────────────────┐  │  • Steps          │                │
│  │  QualityChecklist │  │  • Checklists     │                │
│  │                   │  └───────────────────┘                │
│  │  • 8 critérios    │                                        │
│  │  • Scoring        │  ┌───────────────────┐                │
│  │  • Relatório      │  │  Theme Factory    │                │
│  │                   │  │  (10 temas)       │                │
│  └───────────────────┘  └───────────────────┘                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Fluxo de Dados

```
Entrada (.docx)
      │
      ▼
┌─────────────┐
│   Parse     │──┐
│   XML       │  │
└─────────────┘  │
      │          │
      ▼          │
┌─────────────┐  │
│   Extrair   │  │
│   Texto     │  │
└─────────────┘  │
      │          │
      ▼          │
┌─────────────┐  │
│   Extrair   │  │
│   Imagens   │◀─┘
└─────────────┘
      │
      ▼
┌──────────────────────────────────────┐
│         ESTRUTURA JSON               │
│  {                                   │
│    "title": "...",                   │
│    "sections": [...],                │
│    "images": [...],                   │
│    "tables": [...]                    │
│  }                                   │
└──────────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────────┐
│         CREWAI PROCESSING           │
│  Extrator ──▶ Reescritor            │
│      │                              │
│      ▼                              │
│  Designer ──▶ Revisor               │
└──────────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────────┐
│      INSTRUÇÕES DE DESIGN            │
│  • Ordem de elementos                 │
│  • Estilos a aplicar                  │
│  • Posicionamento de imagens          │
└──────────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────────┐
│         DOCX Writer                  │
│  • Aplica estilos                     │
│  • Insere imagens                     │
│  • Gera documento final               │
└──────────────────────────────────────┘
      │
      ▼
 Saída (.docx)
```

## Camadas de Abstração

```
┌─────────────────────────────────────────────────────────────┐
│  CAMADA 4: UI / CLI                                          │
│  • Click (argumentos de linha de comando)                   │
│  • Rich (interface colorida no terminal)                    │
│  • Progress bars e status updates                           │
├─────────────────────────────────────────────────────────────┤
│  CAMADA 3: Orquestração                                      │
│  • CrewAI (gerenciamento de agentes)                        │
│  • Tasks (definição de tarefas)                             │
│  • Processamento sequencial                                 │
├─────────────────────────────────────────────────────────────┤
│  CAMADA 2: Agentes                                           │
│  • ExtractorAgent (extração estruturada)                    │
│  • RewriterAgent (reescrita UX)                             │
│  • DesignerAgent (aplicação de marca)                       │
│  • ReviewerAgent (qualidade)                              │
├─────────────────────────────────────────────────────────────┤
│  CAMADA 1: Ferramentas                                       │
│  • DocxReader (leitura de Word)                             │
│  • DocxWriter (escrita de Word)                             │
│  • ImageExtractor (gerenciamento de imagens)                │
├─────────────────────────────────────────────────────────────┤
│  CAMADA 0: Skills Integration                                │
│  • DocCoauthoringWorkflow (3 estágios)                     │
│  • BrandGuidelines (cores Lector)                          │
│  • PlaybookTemplates (estruturas)                          │
│  • QualityChecklist (verificação)                          │
└─────────────────────────────────────────────────────────────┘
```

## Diagrama de Sequência

```
Usuário    CLI    Extractor    Rewriter    Designer    Reviewer    Writer   Output
   │         │         │           │           │           │          │       │
   │──run──▶│         │           │           │           │          │       │
   │         │──init──▶│           │           │           │          │       │
   │         │         │──extrair─▶│           │           │          │       │
   │         │         │           │           │           │          │       │
   │         │         │◀─estrutura│           │           │          │       │
   │         │         │           │           │           │          │       │
   │         │         │────reescr─▶│           │           │          │       │
   │         │         │           │           │           │          │       │
   │         │         │◀─texto claro         │           │          │       │
   │         │         │           │           │           │          │       │
   │         │         │──────────design───────▶│           │          │       │
   │         │         │           │           │           │          │       │
   │         │         │◀─instruções design                │          │       │
   │         │         │           │           │           │          │       │
   │         │         │─────────────────────revisão─────▶│          │       │
   │         │         │           │           │           │          │       │
   │         │         │◀─aprovado (score 8.5)            │          │       │
   │         │         │           │           │           │          │       │
   │         │         │────────────────────────────────────gerar─────▶│       │
   │         │         │           │           │           │          │       │
   │         │         │           │           │           │◀─docx────│       │
   │         │         │           │           │           │          │       │
   │         │         │           │           │           │────salvar───────▶│
   │         │         │           │           │           │          │       │
   │◀──OK────│         │           │           │           │          │       │
   │         │         │           │           │           │          │       │
```

## Componentes Reutilizáveis

```
┌─────────────────────────────────────────────────────────────┐
│                    BIBLIOTECA DE COMPONENTES                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  COMPONENTES VISUAIS                               │   │
│  │                                                     │   │
│  │  • TitleBox(title)                                 │   │
│  │  • InfoBox(type, content)    [tip|warning|info]   │   │
│  │  • StepBox(number, title, desc)                  │   │
│  │  • Checklist(items)                                │   │
│  │  • Table(data, headers)                            │   │
│  │  • Separator()                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  COMPONENTES DE TEXTO                               │   │
│  │                                                     │   │
│  │  • Heading1(text)                                   │   │
│  │  • Heading2(text)                                 │   │
│  │  • Heading3(text)                                   │   │
│  │  • Paragraph(text, style)                           │   │
│  │  • BulletList(items)                                │   │
│  │  • NumberedList(items)                              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  COMPONENTES DE LAYOUT                              │   │
│  │                                                     │   │
│  │  • PageBreak()                                      │   │
│  │  • ColumnBreak()                                    │   │
│  │  • Header(text)                                     │   │
│  │  • Footer(text)                                     │   │
│  │  • Margin(top, bottom, left, right)                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Configuração de Marca

```
┌─────────────────────────────────────────────────────────────┐
│              IDENTIDADE VISUAL LECTOR                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  CORES:                                                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  #1E3A5F  │  #2563EB  │  #D97757  │  #2D3748       │   │
│  │  Azul     │  Azul     │  Coral    │  Cinza         │   │
│  │  Escuro   │  Brilhante│           │  Escuro        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  TIPOGRAFIA:                                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Headings: Calibri, Bold, 32/26/20pt                │   │
│  │  Body:     Calibri, Regular, 11pt                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ESPAÇAMENTO:                                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Line height: 1.15                                  │   │
│  │  Paragraph:   12pt                                  │   │
│  │  Section:    24pt                                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ELEMENTOS:                                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  🎯 Info Box:    border-left 4px #2563EB          │   │
│  │  ⚠️ Warning Box: border-left 4px #D97757          │   │
│  │  💡 Tip Box:     border-left 4px #2563EB          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

**Arquitetura projetada para escalabilidade, manutenção e reutilização.**
