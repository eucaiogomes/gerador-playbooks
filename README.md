# 🚀 Lector Playbook Converter

Sistema multi-agente powered by [CrewAI](https://github.com/joaomdmoura/crewai) para converter documentos Word em playbooks profissionais com identidade visual Lector.

## ✨ O que faz?

- 📄 **Extrai** conteúdo de documentos .docx mantendo estrutura e imagens
- ✨ **Reescreve** em linguagem humana e clara (sem inventar conteúdo)
- 🎨 **Aplica** identidade visual da marca Lector automaticamente
- 🔍 **Revisa** qualidade antes da entrega

## 🛠️ Instalação

### 1. Clone ou copie o projeto

```bash
cd lector-playbook-converter
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

Ou usando o pyproject:

```bash
pip install -e .
```

### 3. Configure as cores da marca

Edite o arquivo `.env` e substitua as cores pelas cores reais do site Lector:

```bash
# Inspecione o site https://www.lector.com.br/ no DevTools (F12)
# ou me peça para extrair as cores
LECTOR_PRIMARY_COLOR=#SEU_CODIGO
LECTOR_SECONDARY_COLOR=#SEU_CODIGO
LECTOR_ACCENT_COLOR=#SEU_CODIGO
```

## 🚀 Uso

### Modo básico (recomendado):

```bash
python run.py
```

### Usando a CLI completa:

```bash
# Com os documentos em outra pasta
python run.py -i "C:\caminho\para\documentos"

# Salvando em pasta específica
python run.py -o "C:\caminho\para\playbooks"

# Definindo cores da marca
python run.py -p "#1E3A5F" --secondary-color "#00C9A7"

# Pulando revisão (mais rápido)
python run.py --skip-review
```

## 📁 Estrutura do Projeto

```
lector-playbook-converter/
├── src/
│   ├── agents/          # Agentes CrewAI especializados
│   │   ├── extractor_agent.py    # Extrai conteúdo estruturado
│   │   ├── rewriter_agent.py     # Reescreve em linguagem humana
│   │   ├── designer_agent.py     # Aplica design Lector
│   │   └── reviewer_agent.py     # Revisa qualidade
│   ├── tools/           # Ferramentas de processamento
│   │   ├── docx_reader.py        # Leitor de DOCX
│   │   ├── docx_writer.py        # Escritor com estilo Lector
│   │   └── image_extractor.py    # Gerenciamento de imagens
│   ├── config.py        # Configurações e identidade visual
│   ├── tasks.py         # Tarefas dos agentes
│   └── main.py          # Orquestrador CLI
├── input/               # Coloque seus .docx aqui (ou use -i)
├── output/              # Playbooks gerados (ou use -o)
├── run.py               # Script de execução simples
├── requirements.txt     # Dependências
└── .env                 # Configurações
```

## 🤖 Agentes do Sistema

### 1. 🔍 Extrator
Analisa documentos Word e extrai:
- Títulos e hierarquia
- Texto com formatação
- Tabelas
- Imagens (preservadas)

### 2. ✨ Reescritor
Transforma linguagem técnica em humana:
- Frases curtas e diretas
- Voz ativa
- Sem jargões desnecessários
- **Garantia**: não inventa conteúdo!

### 3. 🎨 Designer
Aplica estrutura de playbook:
- Sumário executivo
- Caixas de informação (⚠️ 💡 🎯)
- Etapas numeradas
- Checklists
- Identidade visual Lector

### 4. 🔍 Revisor
Garante qualidade:
- Compara com original
- Verifica integridade
- Pontua clareza (1-10)
- Aprova ou solicita correções

## 🎨 Personalização Visual

Para descobrir as cores exatas do site Lector:

1. Abra https://www.lector.com.br/
2. Pressione `F12` (DevTools)
3. Vá na aba "Elements" ou "Inspector"
4. Use o seletor de cor 🖱️ para capturar:
   - Cor primária (provavelmente azul/corporate)
   - Cor secundária (verde/destaque)
   - Cor de alerta/acento (laranja/vermelho)

Ou... **me mande uma screenshot do site** que extraio as cores para você!

## 📝 Formatos Suportados

### Entrada:
- ✅ Arquivos .docx (Word moderno)
- ✅ Imagens embutidas (preservadas)
- ✅ Tabelas
- ✅ Listas formatadas
- ⚠️ .doc (Word antigo) - converta antes para .docx

### Saída:
- ✅ Playbook .docx formatado
- ✅ Imagens em pasta separada `output/images/`
- ✅ Estilos personalizados Lector

## ⚙️ Configurações Avançadas

No arquivo `.env`:

```bash
# Modelo de IA (requer API key da Anthropic)
ANTHROPIC_API_KEY=sua_chave_aqui
MODEL=claude-3-sonnet-20240229

# Ou use modelos locais via Ollama (grátis, mas mais lento)
# MODEL=ollama/mistral

# Processamento
MAX_WORKERS=3              # Documentos simultâneos
PRESERVE_IMAGES=true       # Manter imagens originais
DEBUG=false                # Logs detalhados
```

## 🐛 Troubleshooting

### Erro "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Documentos não aparecem
Verifique se são `.docx` (não `.doc`). Converta: Abrir no Word → Salvar Como → .docx

### Imagens não preservadas
Verifique `PRESERVE_IMAGES=true` no `.env`

### Qualidade da reescrita
- Sem API key: usa heurísticas locais (rápido, menos refinado)
- Com API key: usa Claude (mais inteligente, requer créditos)

## 📜 Licença

Projeto interno Lector. Uso livre dentro da organização.

## 🤝 Suporte

Encontrou um bug? Quer uma feature?
- Abra uma issue no repositório
- Ou me chame: "Oi Claude, preciso de ajuda com o playbook converter"

---

**Feito com ❤️ usando CrewAI + Python**
"# gerador-playbooks" 
