import logging
from typing import Optional
from .mermaid_chain import MermaidChain
from common.llm_handler import LLMHandler
from prompts.mermaid_agent_prompt import get_agent_prompt
from mermaid_agent.utils import load_example

logger = logging.getLogger(__name__)

class MermaidAgent:
    """
    MermaidAgent class responsible for generating, resolving, and iterating Mermaid diagrams.
    """

    def __init__(self):
        """
        Initialize MermaidAgent with necessary handlers and chains.
        """
        self.llm_handler = LLMHandler()
        self.chain = MermaidChain(self.llm_handler)  # Pass the entire LLMHandler instance

    def generate_diagram(self, brief: str, diagram_type: str) -> str:
        """
        Generate a Mermaid diagram based on the given brief and diagram type.

        Args:
            brief (str): A detailed description of the desired diagram.
            diagram_type (str): The type of Mermaid diagram to generate (e.g., 'flowchart', 'sequence', 'class').

        Returns:
            str: The generated Mermaid code.

        Raises:
            ValueError: If the input parameters are invalid.
            Exception: For any other errors during diagram generation.
        """
        try:
            if not brief or not diagram_type:
                raise ValueError("Both brief and diagram_type must be provided.")

            prompt = self._create_generation_prompt(brief, diagram_type)
            mermaid_code = self.chain.run(prompt)
            logger.debug(f"Generated Mermaid code:\n{mermaid_code}")
            return mermaid_code
        except ValueError as ve:
            logger.error(f"Invalid input: {str(ve)}")
            raise
        except Exception as e:
            logger.error(f"Error generating diagram: {str(e)}")
            raise

    def _create_generation_prompt(self, brief: str, diagram_type: str) -> str:
        """
        Create a prompt for generating a Mermaid diagram.

        Args:
            brief (str): A detailed description of the desired diagram.
            diagram_type (str): The type of Mermaid diagram to generate.

        Returns:
            str: The rendered generation prompt.
        """
        generation_prompt = get_agent_prompt("generation")
        context = {
            "brief": brief,
            "diagram_type": diagram_type,
        }
        return self.llm_handler.conditional_render(generation_prompt, context)

    # Other methods remain unchanged