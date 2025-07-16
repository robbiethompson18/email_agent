import os
import sys
from openai import OpenAI
from dotenv import load_dotenv


class OpenAIAgent:
    """Base class for agents that use OpenAI API."""
    
    def __init__(self, api_key=None):
        """Initialize the OpenAI client.
        
        Args:
            api_key (str, optional): OpenAI API key. If not provided, will try to get from env var.
        """
        # Try to load from .env file
        load_dotenv()
        
        # Get API key with priority: 1) passed param, 2) env var, 3) .env file
        openai_api_key = api_key or os.environ.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        
        if not openai_api_key:
            print("Error: OPENAI_API_KEY not found. Please provide it as a parameter or set it as an environment variable.")
            print("You can set it in your shell with: export OPENAI_API_KEY='your-key-here'")
            print("Or create a .env file in the project directory with: OPENAI_API_KEY='your-key-here'")
            sys.exit(1)
            
        # Initialize OpenAI client
        self.client = OpenAI(api_key=openai_api_key)