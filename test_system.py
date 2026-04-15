#!/usr/bin/env python3
"""
Script de teste do Lector Playbook Converter
Verifica se todas as dependencias estao instaladas
"""

import sys
from pathlib import Path

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_imports():
    """Testa se todos os imports funcionam"""
    print_section("TESTANDO IMPORTS")

    modules = [
        ("docx", "python-docx"),
        ("crewai", "crewai"),
        ("click", "click"),
        ("rich", "rich"),
        ("PIL", "pillow"),
        ("dotenv", "python-dotenv"),
    ]

    all_ok = True
    for module, package in modules:
        try:
            __import__(module)
            print(f"  [OK] {package}")
        except ImportError:
            print(f"  [ERRO] {package} - NAO INSTALADO")
            all_ok = False

    return all_ok

def test_structure():
    """Testa se a estrutura de arquivos existe"""
    print_section("TESTANDO ESTRUTURA")

    required_files = [
        "src/__init__.py",
        "src/config.py",
        "src/skills_integration.py",
        "src/agents_enhanced.py",
        "src/tools/docx_reader.py",
        "src/tools/docx_writer.py",
        "src/agents/extractor_agent.py",
        "LECTOR_BRAND.md",
        "SKILLS_INTEGRATION.md",
        "requirements.txt",
    ]

    base_path = Path(__file__).parent
    all_ok = True

    for file in required_files:
        path = base_path / file
        if path.exists():
            print(f"  [OK] {file}")
        else:
            print(f"  [ERRO] {file} - NAO ENCONTRADO")
            all_ok = False

    return all_ok

def test_brand_config():
    """Testa configuracao de marca"""
    print_section("TESTANDO CONFIGURACAO DE MARCA")

    sys.path.insert(0, str(Path(__file__).parent / "src"))

    try:
        from config import BrandIdentity
        brand = BrandIdentity()

        colors = [
            ("Primary", brand.primary_color),
            ("Secondary", brand.secondary_color),
            ("Accent", brand.accent_color),
            ("Text", brand.text_color),
        ]

        for name, color in colors:
            print(f"  [OK] {name:12} {color}")

        print(f"\n  Fonte Headings: {brand.heading_font}")
        print(f"  Fonte Body:     {brand.body_font}")

        return True
    except Exception as e:
        print(f"  [ERRO] {e}")
        return False

def test_input_files():
    """Verifica se ha arquivos para processar"""
    print_section("VERIFICANDO ARQUIVOS DE ENTRADA")

    input_dir = Path(r"C:\Users\Lector\Desktop\Documentacoes")

    if not input_dir.exists():
        # Try alternative path
        input_dir = Path(r"C:\Users\Lector\Desktop\Documentações")

    if not input_dir.exists():
        print(f"  [AVISO] Pasta nao encontrada: {input_dir}")
        print(f"  Crie a pasta e coloque arquivos .docx la")
        return False

    docx_files = list(input_dir.glob("**/*.docx"))

    if docx_files:
        print(f"  [OK] {len(docx_files)} arquivo(s) .docx encontrado(s):\n")
        for f in docx_files:
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"     - {f.name} ({size_mb:.2f} MB)")
        return True
    else:
        print(f"  [AVISO] Nenhum arquivo .docx encontrado em {input_dir}")
        return False

def main():
    print("""
    +==============================================================+
    |                                                              |
    |              LECTOR PLAYBOOK CONVERTER - TESTE               |
    |                                                              |
    +==============================================================+
    """)

    results = []

    # Testar imports
    results.append(("Imports", test_imports()))

    # Testar estrutura
    results.append(("Estrutura", test_structure()))

    # Testar configuracao
    results.append(("Config de Marca", test_brand_config()))

    # Verificar arquivos
    results.append(("Arquivos Input", test_input_files()))

    # Resumo
    print("\n" + "="*60)
    print("  RESUMO DOS TESTES")
    print("="*60)

    for name, result in results:
        status = "[OK] PASSOU" if result else "[ERRO] FALHOU"
        print(f"  {status:12} {name}")

    all_passed = all(r for _, r in results)

    print("\n" + "="*60)
    if all_passed:
        print("  [OK] TUDO PRONTO! Execute: python run.py")
    else:
        print("  [ERRO] ALGUNS TESTES FALHARAM")
        print("     Instale dependencias: pip install -r requirements.txt")
    print("="*60 + "\n")

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
