"""
Ferramentas para processamento de documentos
"""

from .docx_reader import DocxReader
from .docx_writer import DocxWriter
from .html_writer import HTMLWriter
from .image_extractor import ImageExtractor

__all__ = ["DocxReader", "DocxWriter", "HTMLWriter", "ImageExtractor"]
