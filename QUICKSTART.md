# 🚀 Quick Start - Lector Playbook Converter

## Instalação (2 minutos)

### 1. Instale as dependências

```bash
cd "C:\Users\Lector\lector-playbook-converter"

pip install -r requirements.txt
```

Se tiver problemas, instale individualmente:

```bash
pip install crewai crewai-tools python-docx click rich pydantic pillow python-dotenv
```

### 2. Verifique a instalação

```bash
python test_system.py
```

Deve mostrar:
```
[OK] Imports
[OK] Estrutura
[OK] Config de Marca
[OK] Arquivos Input
```

### 3. Execute o conversor

```bash
python run.py
```

## 📋 O que vai acontecer

1. **Agente Extrator** vai ler seus arquivos `.docx`
2. **Agente Reescritor** vai transformar em linguagem humana
3. **Agente Designer** vai aplicar identidade visual Lector
4. **Agente Revisor** vai verificar qualidade
5. **Playbooks** serão salvos em `output/`

## 🎨 Cores da Marca (Já Configuradas)

| Cor | Hex | Uso |
|-----|-----|-----|
| Azul Escuro | `#1E3A5F` | Títulos, Header |
| Azul Brilhante | `#2563EB` | Links, Destaques |
| Coral | `#D97757` | CTAs, Alertas |

Extraídas do screenshot do site www.lector.com.br

## 📝 Arquivos Encontrados

O sistema detectou automaticamente:
- ✅ Processo Onboarding.docx (0.77 MB)
- ✅ Processos Cigam.docx (2.14 MB)

## 🔧 Comandos Úteis

### Basico
```bash
python run.py
```

### Com cores personalizadas
```bash
python run.py -p "#1E3A5F" --secondary-color "#2563EB"
```

### Pasta diferente
```bash
python run.py -i "C:\outra\pasta\docs"
```

### Modo debug (mais detalhes)
```bash
python run.py --debug
```

## 📁 Estrutura de Saída

```
output/
├── PLAYBOOK_Processo Onboarding.docx
├── PLAYBOOK_Processos Cigam.docx
└── images/
    ├── img_a1b2c3d4.png
    └── img_e5f6g7h8.jpg
```

## ❓ Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Nenhum arquivo encontrado"
Verifique se os arquivos estão em:
`C:\Users\Lector\Desktop\Documentações`

### Imagens não aparecem
As imagens são extraídas para `output/images/` e referenciadas no documento.

## 🎓 Documentação Completa

- `README.md` - Documentação geral
- `LECTOR_BRAND.md` - Guia de identidade visual
- `SKILLS_INTEGRATION.md` - Como as skills Anthropic foram integradas

---

**Pronto para usar!** Execute `python run.py` e seus playbooks serão gerados! 🎉
