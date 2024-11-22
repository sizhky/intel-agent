"""Command-line interface for the Competitive Intelligence Agent."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from intel_agent.core.config import config

app = typer.Typer(
    name="intel-agent",
    help="Competitive Intelligence Agent - AI-powered competitor research tool.",
    add_completion=False,
)
console = Console()

@app.command()
def analyze(
    domain: str = typer.Argument(..., help="Domain/industry to analyze"),
    output: Path = typer.Option(
        "report.md",
        "--output", "-o",
        help="Output file for the competitive analysis report",
    ),
):
    """Analyze competitors in the specified domain."""
    if not config.validate():
        raise typer.Exit(code=1)
    
    console.print(f"[bold green]Analyzing competitors in domain:[/] {domain}")
    console.print("[yellow]This feature is coming soon![/]")

@app.command()
def configure():
    """Configure the Intel Agent with API keys and settings."""
    console.print("[bold]Configuration Setup[/]")
    console.print(
        "\nPlease set up your environment variables in the .env file:"
    )
    console.print("1. [blue]OPENAI_API_KEY[/] - Your OpenAI API key")
    console.print("2. [blue]SEARCH_API_KEY[/] - Your Search API key")

def main():
    """Main entry point for the CLI."""
    app()
