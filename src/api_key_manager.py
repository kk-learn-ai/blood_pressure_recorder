from typing import Optional
import os
from pathlib import Path
from dotenv import load_dotenv

class APIKeyError(Exception):
    """Custom exception for API key related errors"""
    pass

class APIKeyManager:
    """Manages API key loading and validation"""
    
    def __init__(self, env_path: Optional[Path] = None) -> None:
        """
        Initialize API Key Manager.
        
        Args:
            env_path: Optional path to .env file
            
        Raises:
            FileNotFoundError: If env_path is provided but file doesn't exist
        """
        if env_path and not env_path.exists():
            raise FileNotFoundError(f"Environment file not found at: {env_path}")
        load_dotenv(dotenv_path=env_path)
        
    def load_api_key(self) -> str:
        """
        Load and validate OpenAI API key from environment variables.
        
        Returns:
            str: Valid OpenAI API key
            
        Raises:
            APIKeyError: If API key is missing or invalid
        """
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise APIKeyError("OpenAI API key not found in environment variables")
        if not api_key.startswith('sk-'):
            raise APIKeyError("Invalid OpenAI API key format")
        return api_key
