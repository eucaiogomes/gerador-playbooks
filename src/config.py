"""
Configurações do sistema e identidade visual Lector
"""

import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()


@dataclass
class BrandIdentity:
    """Identidade visual da marca Lector - Extraída do site oficial"""
    # Cores Principais (do screenshot do site)
    primary_color: str = os.getenv("LECTOR_PRIMARY_COLOR", "#1E3A5F")  # Azul escuro header
    secondary_color: str = os.getenv("LECTOR_SECONDARY_COLOR", "#2563EB")  # Azul brilhante
    accent_color: str = os.getenv("LECTOR_ACCENT_COLOR", "#D97757")  # Laranja/Coral CTA
    background_color: str = os.getenv("LECTOR_BACKGROUND_COLOR", "#FFFFFF")
    text_color: str = os.getenv("LECTOR_TEXT_COLOR", "#2D3748")

    # Cores de Suporte
    light_gray: str = "#F7FAFC"
    border_color: str = "#E2E8F0"
    text_secondary: str = "#4A5568"
    info_blue: str = "#EBF8FF"
    warning_orange: str = "#FFF5EB"
    success_green: str = "#38A169"

    # Fontes (baseado em análise do site)
    heading_font: str = os.getenv("LECTOR_FONT_HEADING", "Calibri")
    body_font: str = os.getenv("LECTOR_FONT_BODY", "Calibri")

    # Estilos de título (hierarquia Lector)
    title_size: int = 32  # pt - Título principal
    heading1_size: int = 26  # pt - Seções principais
    heading2_size: int = 20  # pt - Subseções
    heading3_size: int = 16  # pt - Tópicos
    body_size: int = 11  # pt - Corpo de texto

    # Espaçamento
    line_spacing: float = 1.15
    paragraph_spacing: float = 12  # pt
    section_spacing: float = 24  # pt

    # Bordas e UI
    border_radius: int = 4  # px equivalente
    shadow_color: str = "#000000"


@dataclass
class AppConfig:
    """Configurações da aplicação"""
    # Diretórios
    input_dir: Path = Path(os.getenv("INPUT_DIR", r"C:\Users\Lector\Desktop\Documentações"))
    output_dir: Path = Path(os.getenv("OUTPUT_DIR", r"C:\Users\Lector\lector-playbook-converter\output"))

    # Modelo LLM
    model: str = os.getenv("MODEL", "claude-3-sonnet-20240229")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")

    # Configurações de processamento
    max_workers: int = int(os.getenv("MAX_WORKERS", "3"))
    preserve_images: bool = os.getenv("PRESERVE_IMAGES", "true").lower() == "true"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Identidade visual
    brand: BrandIdentity = None

    def __post_init__(self):
        self.brand = BrandIdentity()
        # Criar diretório de saída se não existir
        self.output_dir.mkdir(parents=True, exist_ok=True)


# Instância global de configuração
config = AppConfig()
