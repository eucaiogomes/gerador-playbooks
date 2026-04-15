"""
Ferramenta para extrair e gerenciar imagens de documentos
"""

import hashlib
import os
from pathlib import Path
from typing import List, Dict, Optional
from PIL import Image as PILImage
import io

from .docx_reader import DocumentImage


class ImageExtractor:
    """Gerencia extração e salvamento de imagens"""

    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.images_dir = self.output_dir / "images"
        self.images_dir.mkdir(parents=True, exist_ok=True)

    def save_images(self, images: List[DocumentImage]) -> Dict[str, Path]:
        """Salva imagens extraídas e retorna mapeamento hash -> caminho"""
        saved_paths = {}

        for img in images:
            # Criar subdiretório baseado na primeira letra do hash
            subdir = self.images_dir / img.hash[0]
            subdir.mkdir(exist_ok=True)

            # Caminho final
            img_path = subdir / img.filename

            # Salvar imagem
            with open(img_path, "wb") as f:
                f.write(img.image_data)

            saved_paths[img.hash] = img_path

        return saved_paths

    def get_image_info(self, image_data: bytes) -> Dict[str, any]:
        """Retorna informações da imagem"""
        try:
            img = PILImage.open(io.BytesIO(image_data))
            return {
                "format": img.format,
                "width": img.width,
                "height": img.height,
                "mode": img.mode,
                "size_bytes": len(image_data),
            }
        except Exception as e:
            return {
                "format": None,
                "width": None,
                "height": None,
                "error": str(e),
            }

    def optimize_image(self, image_data: bytes, max_width: int = 1200) -> bytes:
        """Otimiza imagem para uso em documentos"""
        try:
            img = PILImage.open(io.BytesIO(image_data))

            # Converter para RGB se necessário
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Redimensionar se muito grande
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), PILImage.Resampling.LANCZOS)

            # Salvar em buffer
            output = io.BytesIO()
            img.save(output, format="JPEG", quality=85, optimize=True)
            return output.getvalue()

        except Exception as e:
            print(f"Erro ao otimizar imagem: {e}")
            return image_data
