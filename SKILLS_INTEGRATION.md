# 🤖 Integração com Skills Anthropic

Este documento descreve como as skills oficiais da Anthropic foram integradas ao Lector Playbook Converter.

## 📚 Skills Integradas

### 1. doc-coauthoring
**Fonte**: `/skills/doc-coauthoring/SKILL.md`

**Aplicação**: Workflow de três estágios para criação de documentos

- **Stage 1: Context Gathering**
  - Extração estruturada do conteúdo DOCX
  - Identificação de elementos críticos
  - Preservação de hierarquia

- **Stage 2: Refinement & Structure**
  - Reescrita iterativa por seções
  - Brainstorming de opções
  - Validação com usuário

- **Stage 3: Reader Testing**
  - Verificação de ambiguidades
  - Teste com "fresh eyes"
  - Validação de usabilidade

**Implementação**: `src/skills_integration.py` - `DocCoauthoringWorkflow`

---

### 2. brand-guidelines
**Fonte**: `/skills/brand-guidelines/SKILL.md`

**Aplicação**: Sistema de cores e tipografia da Lector

**Cores extraídas do site**:
```python
COLORS = {
    "primary_dark": "#1E3A5F",      # Azul escuro (header)
    "primary_bright": "#2563EB",    # Azul brilhante (CTAs)
    "accent_orange": "#D97757",     # Coral (alertas)
    "text_dark": "#2D3748",         # Texto principal
    "light_gray": "#F7FAFC",        # Backgrounds
}
```

**Tipografia**:
- Headings: Calibri (fallback: Arial)
- Body: Calibri (fallback: Georgia)

**Implementação**: `src/skills_integration.py` - `BrandGuidelines`

---

### 3. docx
**Fonte**: `/skills/docx/SKILL.md`

**Aplicação**: Técnicas avançadas de manipulação DOCX

**Aprendizados aplicados**:
- Uso de `python-docx` para estrutura XML
- Estilos pré-definidos para consistência
- Preservação de metadados
- Manipulação de runs e parágrafos
- Inserção de imagens com proporção

**Implementação**: `src/tools/docx_writer.py` - `DocxWriter`

---

### 4. theme-factory
**Fonte**: `/skills/theme-factory/SKILL.md`

**Aplicação**: Temas visuais consistentes

**Tema Lector customizado**:
- Nome: "Lector Corporate"
- Base: Azul corporativo + Laranja energia
- Aplicação: Playbooks profissionais

**Implementação**: `src/skills_integration.py` - `PlaybookTemplates`

---

## 🏗️ Arquitetura dos Agentes

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORQUESTRADOR PRINCIPAL                        │
│                      (src/main.py)                               │
└───────────────────────────────┬───────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   EXTRACTOR   │───▶│    REWRITER     │───▶│    DESIGNER    │
│    AGENT      │    │     AGENT       │    │     AGENT      │
└───────────────┘    └─────────────────┘    └─────────────────┘
       │                     │                     │
       │                     │                     │
       ▼                     ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│              SKILLS INTEGRATION MODULE                          │
│         (src/skills_integration.py)                             │
│                                                                  │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│   │ DocCoauthor  │  │   Brand      │  │  Templates   │          │
│   │   Workflow   │  │  Guidelines  │  │              │          │
│   └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      REVIEWER AGENT                              │
│              (Quality Assurance + Reader Testing)                │
└───────────────────────────────┬───────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      OUTPUT DOCS                                 │
│              Playbooks DOCX formatados                          │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 Workflow de Processamento

### 1. Entrada
- Lê arquivos `.docx` da pasta configurada
- Extrai texto, imagens, tabelas e formatação
- Preserva estrutura original

### 2. Extração (Stage 1)
```python
# Aplica doc-coauthoring Stage 1
extraction_task = create_extraction_task(agent, doc_content)
# Resultado: JSON estruturado com hierarquia completa
```

### 3. Reescrita (Stage 2)
```python
# Aplica doc-coauthoring Stage 2
rewrite_task = create_rewrite_task(agent, extracted_content)
# Diretrizes UX Writing aplicadas:
# - Frases curtas (< 20 palavras)
# - Voz ativa
# - Jargões → Linguagem humana
```

### 4. Design (Brand Guidelines)
```python
# Aplica brand-guidelines
design_task = create_design_task(agent, content, brand_colors)
# Elementos aplicados:
# - Cores Lector extraídas do site
# - Hierarquia tipográfica
# - Caixas de informação estilizadas
```

### 5. Revisão (Stage 3)
```python
# Aplica doc-coauthoring Stage 3
review_task = create_review_task(agent, original, final)
# Reader Testing:
# - Verifica se novo leitor entende
# - Identifica ambiguidades
# - Gera score de qualidade
```

### 6. Saída
- Gera DOCX com `python-docx`
- Aplica estilos customizados
- Insere imagens preservadas
- Salva em pasta de output

## 🎨 Aplicação de Marca

### Cores Lector (Extraídas do Site)

| Elemento | Cor | Hex |
|----------|-----|-----|
| Título Principal | Azul Escuro | `#1E3A5F` |
| Títulos Secundários | Azul Escuro | `#1E3A5F` |
| Destaques/Links | Azul Brilhante | `#2563EB` |
| CTAs/Avisos | Coral | `#D97757` |
| Texto Principal | Cinza Escuro | `#2D3748` |
| Background | Branco | `#FFFFFF` |

### Tipografia

- **Headings**: Calibri, Bold
- **Body**: Calibri, Regular
- **Fallbacks**: Arial (headings), Georgia (body)

### Elementos Visuais

```
┌──────────────────────────────────────────────────────────────┐
│ 🎯 SOBRE ESTE PLAYBOOK                                       │
│ ─────────────────────────────────────────────────────────── │
│ Caixa de informação com borda azul e fundo leve              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ ⚠️ ATENÇÃO                                                   │
│ ─────────────────────────────────────────────────────────── │
│ Caixa de alerta com borda coral e fundo leve                 │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ 💡 DICA PRO                                                  │
│ ─────────────────────────────────────────────────────────── │
│ Caixa de dica com borda azul brilhante                       │
└──────────────────────────────────────────────────────────────┘
```

## ✅ Checklist de Qualidade

Baseado na skill doc-coauthoring, aplicamos 8 critérios:

1. **Integridade** - Conteúdo original preservado?
2. **Precisão** - Nenhuma informação inventada?
3. **Estrutura** - Hierarquia lógica?
4. **Imagens** - Todas preservadas?
5. **Clareza** - Mais legível que original?
6. **Tom de Voz** - Consistente com Lector?
7. **Formatação** - Erros estruturais?
8. **Usabilidade** - Novo leitor entende?

**Score**: 
- ≥ 8.0: Aprovado
- 6.0-7.9: Aprovado com observações
- < 6.0: Reprovação (revisar)

## 🚀 Uso

### Básico
```bash
python run.py
```

### Com opções de marca
```bash
python run.py \
  --primary-color "#1E3A5F" \
  --secondary-color "#2563EB" \
  --accent-color "#D97757"
```

### Debug (verbose)
```bash
python run.py --debug
```

## 📁 Estrutura de Arquivos

```
lector-playbook-converter/
├── skills/                      # Skills da Anthropic copiadas
│   ├── brand-guidelines/
│   ├── doc-coauthoring/
│   ├── docx/
│   └── theme-factory/
├── src/
│   ├── skills_integration.py    # Módulo de integração
│   ├── agents_enhanced.py       # Agentes com skills
│   ├── config.py                # Config com cores Lector
│   └── ...
├── LECTOR_BRAND.md              # Guia visual completo
└── SKILLS_INTEGRATION.md        # Este arquivo
```

## 🔧 Personalização

Para ajustar cores ou comportamento:

1. **Editar `.env`**:
   ```bash
   LECTOR_PRIMARY_COLOR=#sua_cor
   LECTOR_SECONDARY_COLOR=#sua_cor
   ```

2. **Ou passar via CLI**:
   ```bash
   python run.py -p "#cor" -s "#cor"
   ```

3. **Modificar `src/config.py`**:
   - Alterar valores default em `BrandIdentity`

## 📝 Notas Técnicas

### Por que CrewAI?
- Framework open-source líder para orquestração de agentes
- Suporte nativo a múltiplos LLMs (Claude, GPT, etc.)
- Ferramentas customizáveis
- Processamento sequencial e hierárquico

### Por que python-docx?
- Biblioteca oficial da Microsoft para DOCX
- Preserva compatibilidade com Word
- Permite estilos customizados
- Suporta imagens, tabelas, formatação

### Integração com Skills
- Skills fornecem **diretrizes e workflows**
- CrewAI fornece **orquestração**
- Resultado: **sistema robusto e profissional**

## 🎓 Créditos

- **Anthropic Skills**: github.com/anthropics/skills
- **CrewAI**: github.com/joaomdmoura/crewai
- **python-doc**: github.com/python-openxml/python-docx

---

**Desenvolvido para Lector** | *Sistema de Conversão de Playbooks*
