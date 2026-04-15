#!/usr/bin/env python3
"""
Lector Playbook Converter - Conversão em Massa
Converte todos os DOCX de uma pasta em mini-apps HTML interativos.

Uso:
  python batch_convert.py
  python batch_convert.py --input "C:/caminho/docs" --output "C:/saida"
  python batch_convert.py --input pasta --output saida --logo logo.svg
"""

import sys
import importlib.util
from pathlib import Path
from datetime import datetime

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, MofNCompleteColumn
from rich.panel import Panel
from rich import box

ROOT    = Path(__file__).parent
SRC     = ROOT / "src"
TOOLS   = SRC / "tools"
console = Console()


# ── Carregamento direto dos módulos (evita imports relativos) ────────────────
def _load_mod(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_html_mod  = _load_mod("html_writer", TOOLS / "html_writer.py")
_docx_mod  = _load_mod("docx_reader", TOOLS / "docx_reader.py")
HTMLWriter = _html_mod.HTMLWriter
DocxReader = _docx_mod.DocxReader

DEFAULT_INPUT  = Path(r"C:\Users\Lector\Desktop\Documentações")
DEFAULT_OUTPUT = ROOT / "output"
DEFAULT_LOGO   = Path(r"C:\Users\Lector\Downloads\logo\logo-lector.svg")


# ── Funções auxiliares ───────────────────────────────────────────────────────

def load_logo(logo_path: Path) -> str:
    if logo_path.exists():
        return logo_path.read_text(encoding='utf-8')
    console.print(f"[yellow]Aviso: logo nao encontrada em {logo_path}[/yellow]")
    return ""


def convert_one(docx_path: Path, output_dir: Path, logo_svg: str) -> dict:
    """Converte um DOCX para HTML e retorna resultado."""
    result = {"file": docx_path.name, "status": "error",
              "html_path": None, "sections": 0, "error": ""}
    try:
        reader      = DocxReader(docx_path)
        doc_content = reader.read()

        html_name   = f"PLAYBOOK_{docx_path.stem}.html"
        html_path   = output_dir / html_name

        writer = HTMLWriter(
            output_path=html_path,
            title=docx_path.stem,
            logo_svg=logo_svg,
        )
        writer.build_from_doc_content(doc_content)
        writer.save()

        result["status"]    = "success"
        result["html_path"] = str(html_path)
        result["sections"]  = len(writer._sections)
        st = writer._stats()
        result["cl_items"]  = st["cl_items"]
        result["tables"]    = st["tables"]
    except Exception as e:
        result["error"] = str(e)
    return result


def generate_index(output_dir: Path, results: list, logo_svg: str) -> Path:
    """Gera um index.html com cards para todos os playbooks."""
    ok = [r for r in results if r["status"] == "success"]
    now = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Logo para o index
    if logo_svg:
        import re
        logo_html = re.sub(r'<svg ', '<svg style="height:38px;width:auto" ', logo_svg.strip(), count=1)
    else:
        logo_html = '<span style="font-size:20px;font-weight:800;color:#fff"><span style="color:#EF6315">iT</span> Lector</span>'

    cards = ""
    for r in ok:
        name     = r["file"].replace(".docx", "")
        html_f   = Path(r["html_path"]).name
        sections = r.get("sections", 0)
        cl_items = r.get("cl_items", 0)
        tables   = r.get("tables", 0)
        cards += f"""
        <a href="{html_f}" class="card">
          <div class="card-icon">📋</div>
          <div class="card-body">
            <h3 class="card-title">{name}</h3>
            <div class="card-meta">
              <span>📑 {sections} seções</span>
              <span>☑ {cl_items} tarefas</span>
              <span>📊 {tables} tabelas</span>
            </div>
          </div>
          <div class="card-arrow">→</div>
        </a>"""

    errors = [r for r in results if r["status"] == "error"]
    err_rows = ""
    for r in errors:
        err_rows += f'<tr><td>{r["file"]}</td><td class="err">{r.get("error","")[:80]}</td></tr>'
    err_section = ""
    if err_rows:
        err_section = f"""
        <div class="err-block">
          <h2>Arquivos com Erro ({len(errors)})</h2>
          <table class="err-tbl"><thead><tr><th>Arquivo</th><th>Erro</th></tr></thead>
          <tbody>{err_rows}</tbody></table>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Lector Playbooks</title>
<style>
:root {{
  --navy:#00347E; --navy-dark:#001C66; --orange:#EF6315; --orange2:#FF930F;
  --white:#fff; --gray-50:#F7FAFC; --gray-200:#E2E8F0; --gray-700:#4A5568;
  --r:10px; --sh:0 2px 8px rgba(0,0,0,.1);
}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',Calibri,Arial,sans-serif;background:var(--gray-50);color:var(--gray-700)}}
.hdr{{background:var(--navy-dark);padding:0 32px;height:64px;display:flex;align-items:center;gap:14px;box-shadow:0 2px 8px rgba(0,0,0,.3)}}
.hdr svg{{height:34px;width:auto}}
.hdr-div{{width:1px;height:26px;background:rgba(255,255,255,.15)}}
.hdr-title{{font-size:14px;font-weight:500;color:rgba(255,255,255,.75);flex:1}}
.hdr-date{{font-size:12px;color:rgba(255,255,255,.4)}}
.hero{{background:linear-gradient(135deg,var(--navy-dark) 0%,var(--navy) 100%);padding:48px 32px 40px;text-align:center;color:var(--white)}}
.hero h1{{font-size:32px;font-weight:700;margin-bottom:8px}}
.hero p{{font-size:15px;color:rgba(255,255,255,.7);margin-bottom:24px}}
.hero-stats{{display:inline-flex;gap:32px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.12);border-radius:var(--r);padding:14px 32px}}
.hstat{{text-align:center}}
.hstat-val{{font-size:26px;font-weight:700;color:var(--orange);display:block}}
.hstat-lbl{{font-size:11px;color:rgba(255,255,255,.55);text-transform:uppercase;letter-spacing:.5px}}
.content{{max-width:1100px;margin:0 auto;padding:40px 24px}}
.section-title{{font-size:13px;font-weight:700;color:var(--gray-700);text-transform:uppercase;letter-spacing:.8px;margin-bottom:16px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px;margin-bottom:40px}}
.card{{display:flex;align-items:center;gap:16px;background:var(--white);border-radius:var(--r);padding:20px;box-shadow:var(--sh);border:1px solid var(--gray-200);text-decoration:none;color:inherit;transition:all .2s ease}}
.card:hover{{box-shadow:0 6px 20px rgba(0,0,0,.12);transform:translateY(-2px);border-color:var(--orange)}}
.card-icon{{font-size:28px;flex-shrink:0}}
.card-body{{flex:1;min-width:0}}
.card-title{{font-size:15px;font-weight:600;color:var(--navy);margin-bottom:5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.card-meta{{display:flex;gap:10px;font-size:12px;color:var(--gray-700);flex-wrap:wrap}}
.card-arrow{{font-size:18px;color:var(--orange);flex-shrink:0;font-weight:700}}
.err-block{{margin-top:32px}}
.err-block h2{{font-size:16px;font-weight:600;color:#E53E3E;margin-bottom:12px}}
.err-tbl{{width:100%;border-collapse:collapse;font-size:13px;background:var(--white);border-radius:var(--r);overflow:hidden;box-shadow:var(--sh)}}
.err-tbl th{{background:#FFF5F5;color:#E53E3E;padding:10px 14px;text-align:left;font-size:11px;text-transform:uppercase}}
.err-tbl td{{padding:9px 14px;border-bottom:1px solid var(--gray-200)}}
.err{{color:#E53E3E;font-size:12px}}
.footer{{text-align:center;padding:24px;font-size:12px;color:#A0AEC0;border-top:1px solid var(--gray-200)}}
@media(max-width:600px){{.hero{{padding:32px 16px 28px}}.hero-stats{{gap:20px;padding:12px 20px}}.content{{padding:24px 14px}}.cards{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<header class="hdr">
  {logo_html}
  <div class="hdr-div"></div>
  <span class="hdr-title">Central de Playbooks</span>
  <span class="hdr-date">{now}</span>
</header>
<div class="hero">
  <h1>Central de Playbooks</h1>
  <p>Documentação interativa da equipe Lector Tecnologia</p>
  <div class="hero-stats">
    <div class="hstat"><span class="hstat-val">{len(ok)}</span><span class="hstat-lbl">Playbooks</span></div>
    <div class="hstat"><span class="hstat-val">{sum(r.get('sections',0) for r in ok)}</span><span class="hstat-lbl">Seções</span></div>
    <div class="hstat"><span class="hstat-val">{sum(r.get('cl_items',0) for r in ok)}</span><span class="hstat-lbl">Tarefas</span></div>
  </div>
</div>
<div class="content">
  <div class="section-title">Playbooks Disponíveis ({len(ok)})</div>
  <div class="cards">{cards}</div>
  {err_section}
</div>
<footer class="footer">© Lector Tecnologia · Gerado em {now}</footer>
</body>
</html>"""

    index_path = output_dir / "index.html"
    index_path.write_text(html, encoding='utf-8')
    return index_path


# ── CLI ──────────────────────────────────────────────────────────────────────

@click.command()
@click.option('--input',  '-i', 'input_dir',  default=str(DEFAULT_INPUT),
              type=click.Path(), show_default=True, help='Pasta com arquivos .docx')
@click.option('--output', '-o', 'output_dir', default=str(DEFAULT_OUTPUT),
              type=click.Path(), show_default=True, help='Pasta de saída')
@click.option('--logo',   '-l', 'logo_path',  default=str(DEFAULT_LOGO),
              type=click.Path(), show_default=True, help='Arquivo SVG da logo Lector')
@click.option('--pattern', '-p', default='**/*.docx',
              show_default=True, help='Glob pattern para encontrar arquivos')
def main(input_dir, output_dir, logo_path, pattern):
    """
    Converte todos os arquivos DOCX em mini-apps HTML interativos com identidade Lector.
    Gera tambem um index.html com links para todos os playbooks.
    """
    input_path  = Path(input_dir)
    output_path = Path(output_dir)
    logo_file   = Path(logo_path)

    console.print(Panel.fit(
        "[bold cyan]Lector Playbook Converter[/bold cyan] — [dim]Modo Lote[/dim]",
        border_style="cyan"
    ))

    if not input_path.exists():
        console.print(f"[red]Pasta de entrada nao encontrada: {input_path}[/red]")
        raise SystemExit(1)

    output_path.mkdir(parents=True, exist_ok=True)
    logo_svg = load_logo(logo_file)

    docx_files = sorted(input_path.glob(pattern))
    if not docx_files:
        console.print(f"[yellow]Nenhum .docx encontrado em: {input_path}[/yellow]")
        raise SystemExit(0)

    console.print(f"[blue]Encontrados:[/blue] {len(docx_files)} arquivo(s)\n")

    results = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}", table_column=None),
        BarColumn(bar_width=30),
        MofNCompleteColumn(),
        console=console,
    ) as prog:
        task = prog.add_task("Convertendo...", total=len(docx_files))
        for f in docx_files:
            prog.update(task, description=f"[cyan]{f.name[:40]}[/cyan]")
            r = convert_one(f, output_path, logo_svg)
            results.append(r)
            prog.advance(task)

    # Index page
    idx = generate_index(output_path, results, logo_svg)

    # Summary table
    table = Table(title="Resultado", box=box.ROUNDED)
    table.add_column("Arquivo",  style="cyan",  max_width=40)
    table.add_column("Status",   justify="center", width=8)
    table.add_column("Secoes",   justify="center", width=7)
    table.add_column("Tarefas",  justify="center", width=8)
    table.add_column("Saida")

    for r in results:
        st  = "[green]OK[/green]"   if r["status"] == "success" else "[red]ERRO[/red]"
        sec = str(r.get("sections", "-"))
        cl  = str(r.get("cl_items", "-"))
        out = Path(r["html_path"]).name if r["html_path"] else (r.get("error","")[:35])
        table.add_row(r["file"], st, sec, cl, out)

    console.print()
    console.print(table)

    ok  = sum(1 for r in results if r["status"] == "success")
    err = len(results) - ok
    console.print(f"\n[green]{ok} convertidos[/green]", end="")
    if err:
        console.print(f"  [red]{err} com erro[/red]", end="")
    console.print(f"\n[dim]Saida:[/dim] {output_path.resolve()}")
    console.print(f"[bold]Indice:[/bold] {idx.resolve()}\n")


if __name__ == "__main__":
    main()
