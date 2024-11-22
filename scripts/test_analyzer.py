"""Test script for competitor analysis."""

import json
from rich.console import Console

from intel_agent.core.analyzer import CompetitorAnalyzer

console = Console()

def test_analysis():
    """Test the competitor analysis functionality."""
    analyzer = CompetitorAnalyzer()
    
    # Test domain - feel free to change this
    test_domain = "Best webUIs for Ollama"
    
    console.print(f"\n[bold green]Analyzing competitors in: {test_domain}[/]")
    console.print("[bold yellow]This may take a few minutes...[/]")
    
    # Run analysis
    results = analyzer.analyze_domain(test_domain, num_competitors=3)
    
    # Save results
    output_file = "analysis_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    console.print(f"\n[bold green]Analysis complete! Results saved to {output_file}[/]")
    
    # Display summary
    console.print("\n[bold blue]Market Summary:[/]")
    summary = results["analysis_summary"]
    
    for key, value in summary.items():
        console.print(f"\n[yellow]{key.replace('_', ' ').title()}:[/]")
        if isinstance(value, list):
            for item in value:
                console.print(f"  • {item}")
        else:
            console.print(f"  {value}")

if __name__ == "__main__":
    if not CompetitorAnalyzer().search_client.api_key:
        console.print("[red]Please configure your API keys in .env file[/]")
    else:
        test_analysis()
