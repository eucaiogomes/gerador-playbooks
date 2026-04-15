#!/usr/bin/env python3
"""
Script simples para executar o Lector Playbook Converter
"""

import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.main import cli

if __name__ == "__main__":
    cli()
