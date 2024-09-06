import re
from config import MERMAID_THEME, MERMAID_DIRECTION, ENABLE_COLORS, ENABLE_ICONS

class MermaidHandler:
    def __init__(self):
        self.theme = MERMAID_THEME
        self.direction = MERMAID_DIRECTION

    def process_mermaid_code(self, mermaid_code):
        processed_code = f"%%{self.theme}\n%%{self.direction}\n{mermaid_code}"
        
        processed_code = self._apply_custom_styling(processed_code)
        processed_code = self._validate_mermaid_syntax(processed_code)
        
        return processed_code

    def _apply_custom_styling(self, mermaid_code):
        if ENABLE_COLORS:
            # Add color-related styling
            pass
        if ENABLE_ICONS:
            # Add icon-related styling
            pass
        return mermaid_code

    def _validate_mermaid_syntax(self, mermaid_code):
        if not re.search(r'^\s*\w+', mermaid_code, re.MULTILINE):
            raise ValueError("Invalid Mermaid syntax: Missing diagram type declaration")
        return mermaid_code