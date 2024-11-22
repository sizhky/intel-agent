"""Configuration management for the Competitive Intelligence Agent."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the application."""
    
    def __init__(self):
        """Initialize configuration with environment variables."""
        self.openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
        self.search_api_key: Optional[str] = os.getenv("SEARCH_API_KEY")
        self.search_engine_id: Optional[str] = os.getenv("SEARCH_ENGINE_ID")
        
        # Project paths
        self.project_root: Path = Path(__file__).parent.parent.parent.parent
        self.reports_dir: Path = self.project_root / "reports"
        self.cache_dir: Path = self.project_root / "cache"
        
        # Ensure directories exist
        self.reports_dir.mkdir(exist_ok=True)
        self.cache_dir.mkdir(exist_ok=True)
    
    def validate(self) -> bool:
        """Validate that all required configuration is present."""
        required_vars = {
            "OPENAI_API_KEY": "openai_api_key",
            "SEARCH_API_KEY": "search_api_key",
            "SEARCH_ENGINE_ID": "search_engine_id"
        }
        missing_vars = [
            env_var for env_var, attr_name in required_vars.items()
            if not getattr(self, attr_name)
        ]
        
        if missing_vars:
            print(f"Missing required environment variables: {', '.join(missing_vars)}")
            print("Please set them in your .env file or environment")
            return False
        return True

# Global config instance
config = Config()
