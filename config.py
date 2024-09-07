import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# LLM Configuration
LLM_PROVIDER = "anthropic" # "openai" # "anthropic"  # Changed default to 'anthropic'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# OpenAI Configuration
OPENAI_MODEL = "gpt-4o"
OPENAI_TEMPERATURE = 0.3
OPENAI_MAX_TOKENS = 1000

# Anthropic Configuration
ANTHROPIC_MODEL = "claude-3-5-sonnet-20240620"  # Updated to the latest model
ANTHROPIC_TEMPERATURE = 0
ANTHROPIC_MAX_TOKENS = 1000

# Mermaid Configuration
MERMAID_THEME = "default"
MERMAID_DIRECTION = "TB"  # Top to Bottom

# File paths
EXAMPLES_DIR = "examples"
OUTPUTS_DIR = "outputs"

# Customization options
ENABLE_COLORS = True
ENABLE_ICONS = True

# Performance tuning
CACHE_RESULTS = True
CACHE_EXPIRY = 3600  # in seconds

# Questionnaire Agent Configuration
QUESTIONNAIRE_EXPERTISE = "diagramming"  # Default expertise for the questionnaire agent