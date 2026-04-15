#!/usr/bin/env python3
"""
Lector Playbook Converter - Orquestrador Principal
CLI para converter documentos DOCX em playbooks profissionais
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Optional

import click
from crewai import Crew, Process
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import box

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent))

from config import config, BrandIdentity
from tools import DocxReader, DocxWriter, HTMLWriter, ImageExtractor
from agents import (
    create_extractor_agent,
    create_rewriter_agent,
    create_designer_agent,
    create_reviewer_agent,
)
from tasks import (
    create_extraction_task,
    create_rewrite_task,
    create_design_task,
    create_review_task,
)

console = Console()


def print_banner():
    """Mostra banner inicial"""
    console.print(Panel.fit(
        "[bold cyan]Lector Playbook Converter[/bold cyan]\n"
        "[dim]Transforme documentos Word em playbooks profissionais[/dim]\n"
        "[green]Powered by CrewAI + Claude[/green]",
        border_style="cyan",
        box=box.ROUNDED
    ))


def find_docx_files(input_dir: Path) -> List[Path]:
    """Encontra todos os arquivos .docx no diretório"""
    return list(input_dir.glob("**/*.docx"))


def process_single_document(
    file_path: Path,
    output_dir: Path,
    brand: BrandIdentity,
    console: Console,
    skip_review: bool = False
) -> dict:
    """Processa um único documento através do pipeline de agentes"""

    results = {
        "file": file_path.name,
        "status": "pending",
        "output_path": None,
        "review_score": None,
    }

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:

        # Task 1: Extração
        task = progress.add_task(f"📄 Extraindo {file_path.name}...", total=None)

        reader = DocxReader(file_path)
        doc_content = reader.read()

        # Salvar imagens extraídas
        image_extractor = ImageExtractor(output_dir)
        saved_images = image_extractor.save_images(doc_content["images"])

        progress.update(task, completed=True)

        # Criar agentes
        extractor_agent = create_extractor_agent()
        rewriter_agent = create_rewriter_agent()
        designer_agent = create_designer_agent()
        reviewer_agent = create_rewriter_agent() if not skip_review else None

        # Task 2: Extração Estruturada (CrewAI)
        task = progress.add_task("🔍 Agente: Analisando estrutura...", total=None)

        extraction_task = create_extraction_task(
            extractor_agent,
            doc_content
        )

        crew_extract = Crew(
            agents=[extractor_agent],
            tasks=[extraction_task],
            process=Process.sequential,
            verbose=config.debug,
        )

        extracted_result = crew_extract.kickoff()

        progress.update(task, completed=True)

        # Task 3: Reescrita (CrewAI)
        task = progress.add_task("✨ Agente: Reescrevendo em linguagem humana...", total=None)

        rewrite_task = create_rewrite_task(
            rewriter_agent,
            extracted_result.raw
        )

        crew_rewrite = Crew(
            agents=[rewriter_agent],
            tasks=[rewrite_task],
            process=Process.sequential,
            verbose=config.debug,
        )

        rewritten_result = crew_rewrite.kickoff()

        progress.update(task, completed=True)

        # Task 4: Design (CrewAI)
        task = progress.add_task("🎨 Agente: Aplicando design Lector...", total=None)

        brand_colors = {
            "primary": brand.primary_color,
            "secondary": brand.secondary_color,
            "accent": brand.accent_color,
        }

        design_task = create_design_task(
            designer_agent,
            rewritten_result.raw,
            brand_colors
        )

        crew_design = Crew(
            agents=[designer_agent],
            tasks=[design_task],
            process=Process.sequential,
            verbose=config.debug,
        )

        design_result = crew_design.kickoff()

        progress.update(task, completed=True)

        # Task 5: Revisão (opcional)
        review_score = None
        if not skip_review and reviewer_agent:
            task = progress.add_task("🔍 Agente: Revisando qualidade...", total=None)

            review_task = create_review_task(
                reviewer_agent,
                json.dumps(doc_content, default=str),
                design_result.raw
            )

            crew_review = Crew(
                agents=[reviewer_agent],
                tasks=[review_task],
                process=Process.sequential,
                verbose=config.debug,
            )

            review_result = crew_review.kickoff()
            review_score = review_result.raw

            progress.update(task, completed=True)

        # Gerar documento final
        task = progress.add_task("💾 Gerando DOCX final...", total=None)

        output_filename = f"PLAYBOOK_{file_path.stem}.docx"
        output_path = output_dir / output_filename

        writer = DocxWriter(brand, output_path)

        # Processar resultado e gerar documento
        try:
            # Parse do resultado de design para estruturar o DOCX
            generate_docx_from_design(writer, design_result.raw, doc_content, saved_images)
            writer.save()
            results["output_path"] = str(output_path)
            results["status"] = "success"
        except Exception as e:
            console.print(f"[red]Erro ao gerar documento: {e}[/red]")
            results["status"] = "error"
            results["error"] = str(e)

        progress.update(task, completed=True)

        # Gerar mini-app HTML interativo
        task = progress.add_task("Gerando mini-app HTML interativo...", total=None)
        try:
            html_filename = f"PLAYBOOK_{file_path.stem}.html"
            html_path = output_dir / html_filename
            logo_svg = ""
            logo_file = Path(r"C:\Users\Lector\Downloads\logo\logo-lector.svg")
            if logo_file.exists():
                logo_svg = logo_file.read_text(encoding='utf-8')
            html_writer = HTMLWriter(output_path=html_path, title=file_path.stem, logo_svg=logo_svg)
            html_writer.build_from_doc_content(doc_content)
            html_writer.save()
            results["html_path"] = str(html_path)
            console.print(f"[green]Mini-app HTML:[/green] [dim]{html_filename}[/dim]")
        except Exception as e:
            console.print(f"[yellow]HTML nao gerado: {e}[/yellow]")

        progress.update(task, completed=True)

    return results


def generate_docx_from_design(
    writer: DocxWriter,
    design_instructions: str,
    original_content: dict,
    saved_images: dict
):
    """Gera DOCX a partir das instruções de design"""

    # Título
    writer.add_title(original_content["file_name"].replace(".docx", ""))

    # Processar elementos originais
    for element in original_content.get("elements", []):
        if element["type"] == "heading":
            level = element.get("level", 1)
            writer.add_heading(element["content"], level=level)

        elif element["type"] == "paragraph":
            content = element["content"]
            if content.strip():
                # Verificar se é lista
                if content.startswith(("- ", "* ", "• ")):
                    items = [line.strip()[2:] for line in content.split("\n") if line.strip().startswith(("- ", "* ", "• "))]
                    if items:
                        writer.add_bullet_list(items)
                    else:
                        writer.add_paragraph(content)
                elif content[0:2].replace(".", "").isdigit():
                    # Lista numerada
                    writer.add_paragraph(content)
                else:
                    writer.add_paragraph(content)

        elif element["type"] == "table":
            writer.add_table(element["content"])

    # Adicionar imagens no final (ou intercaladas se possível)
    if config.preserve_images and saved_images:
        writer.add_heading("Imagens de Referência", level=2)
        for img_hash, img_path in saved_images.items():
            try:
                with open(img_path, "rb") as f:
                    img_data = f.read()
                writer.add_image(img_data, width=5.5)
            except Exception as e:
                console.print(f"[yellow]Aviso: Não foi possível adicionar imagem {img_path}: {e}[/yellow]")


@click.command()
@click.option(
    "--input", "-i",
    type=click.Path(exists=True, path_type=Path),
    default=config.input_dir,
    help="Diretório com os arquivos .docx"
)
@click.option(
    "--output", "-o",
    type=click.Path(path_type=Path),
    default=config.output_dir,
    help="Diretório de saída para os playbooks"
)
@click.option(
    "--skip-review", "-s",
    is_flag=True,
    default=False,
    help="Pular etapa de revisão de qualidade"
)
@click.option(
    "--primary-color", "-p",
    default=config.brand.primary_color,
    help="Cor primária da marca (hex)"
)
@click.option(
    "--secondary-color",
    default=config.brand.secondary_color,
    help="Cor secundária da marca (hex)"
)
@click.version_option(version="1.0.0", prog_name="lector-playbook")
def cli(input: Path, output: Path, skip_review: bool, primary_color: str, secondary_color: str):
    """
    🚀 Lector Playbook Converter

    Transforme documentos Word em playbooks profissionais com identidade visual Lector.
    Usa agentes de IA para estruturar, reescrever e formatar seus documentos.
    """
    print_banner()

    # Atualizar configurações
    config.input_dir = input
    config.output_dir = output
    config.brand.primary_color = primary_color
    config.brand.secondary_color = secondary_color

    # Criar diretório de saída
    output.mkdir(parents=True, exist_ok=True)

    # Encontrar arquivos
    docx_files = find_docx_files(input)

    if not docx_files:
        console.print(f"[yellow]⚠️ Nenhum arquivo .docx encontrado em {input}[/yellow]")
        return

    console.print(f"\n[blue]📁 Encontrados {len(docx_files)} arquivo(s) para processar:[/blue]\n")

    for i, f in enumerate(docx_files, 1):
        console.print(f"  {i}. {f.name}")

    console.print()

    # Processar cada arquivo
    results = []
    for file_path in docx_files:
        console.print(f"\n[bold cyan]Processando: {file_path.name}[/bold cyan]")
        console.print("─" * 60)

        result = process_single_document(
            file_path=file_path,
            output_dir=output,
            brand=config.brand,
            console=console,
            skip_review=skip_review
        )
        results.append(result)

    # Resumo final
    console.print("\n")
    console.print("=" * 60)
    console.print("[bold green]📊 RESUMO DA CONVERSÃO[/bold green]")
    console.print("=" * 60)

    table = Table(title="Playbooks Gerados", box=box.ROUNDED)
    table.add_column("Documento", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Arquivo de Saída", style="dim")

    for result in results:
        status = result["status"]
        status_text = "✅ Sucesso" if status == "success" else "❌ Erro"
        status_style = "green" if status == "success" else "red"

        output_file = result.get("output_path", "N/A")
        if output_file != "N/A":
            output_file = Path(output_file).name

        table.add_row(
            result["file"],
            f"[{status_style}]{status_text}[/{status_style}]",
            output_file
        )

    console.print(table)
    console.print(f"\n[dim]📂 Playbooks salvos em: {output.absolute()}[/dim]\n")


if __name__ == "__main__":
    cli()
