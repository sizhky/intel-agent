"""Competitor analysis module using OpenAI."""

import json
from typing import Dict, List, Optional

from openai import OpenAI
from rich.console import Console

from .config import config
from .search import GoogleSearchClient

console = Console()

class CompetitorAnalyzer:
    """Analyzes competitors using OpenAI's API."""

    def __init__(self):
        """Initialize the analyzer with API configurations."""
        self.search_client = GoogleSearchClient(
            api_key=config.search_api_key,
            cx=config.search_engine_id
        )
        self.openai_client = OpenAI(api_key=config.openai_api_key)

    def analyze_domain(self, domain: str, num_competitors: int = 5) -> Dict:
        """Analyze competitors in a specific domain.
        
        Args:
            domain: The business domain to analyze (e.g., "AI chatbot companies")
            num_competitors: Number of competitors to analyze
            
        Returns:
            Dict containing analysis results
        """
        # Search for competitors
        console.print(f"\n[bold blue]Searching for competitors in {domain}...[/]")
        competitors = self.search_client.search_competitors(domain, num_results=num_competitors)
        
        # Analyze each competitor
        analysis = []
        for comp in competitors:
            console.print(f"\n[yellow]Analyzing {comp['title']}...[/]")
            
            # Prepare competitor info for analysis
            comp_info = {
                "name": comp["title"],
                "url": comp["link"],
                "description": comp["snippet"]
            }
            
            # Get AI analysis
            analysis_prompt = f"""
            Analyze this competitor in the {domain} space:
            Company: {comp_info['name']}
            Website: {comp_info['url']}
            Description: {comp_info['description']}
            
            Provide analysis in JSON format with these fields:
            - key_strengths: List of main competitive advantages
            - target_market: Primary target audience/market
            - unique_selling_points: What sets them apart
            - potential_weaknesses: Areas where they might be vulnerable
            """
            
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a competitive intelligence analyst."},
                        {"role": "user", "content": analysis_prompt}
                    ],
                    temperature=0.7
                )
                
                # Parse AI analysis
                ai_analysis = json.loads(response.choices[0].message.content)
                comp_info.update(ai_analysis)
                analysis.append(comp_info)
                
            except Exception as e:
                console.print(f"[red]Error analyzing {comp['title']}: {str(e)}[/]")
                continue
        
        return {
            "domain": domain,
            "competitors": analysis,
            "analysis_summary": self._generate_summary(domain, analysis)
        }
    
    def _generate_summary(self, domain: str, analyses: List[Dict]) -> Dict:
        """Generate an overall summary of the competitive landscape.
        
        Args:
            domain: The business domain
            analyses: List of competitor analyses
            
        Returns:
            Dict containing summary insights
        """
        if not analyses:
            return {"error": "No competitor analyses available"}
        
        summary_prompt = f"""
        Based on the analysis of {len(analyses)} competitors in the {domain} space:
        {json.dumps(analyses, indent=2)}
        
        Provide a market summary in JSON format with these fields:
        - market_trends: Key trends in the market
        - common_strengths: Strengths shared by multiple competitors
        - market_gaps: Potential opportunities/gaps in the market
        - entry_barriers: Key barriers to entering this market
        - recommendations: Strategic recommendations for entering/competing
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a competitive intelligence analyst."},
                    {"role": "user", "content": summary_prompt}
                ],
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            console.print(f"[red]Error generating summary: {str(e)}[/]")
            return {"error": f"Failed to generate summary: {str(e)}"}
