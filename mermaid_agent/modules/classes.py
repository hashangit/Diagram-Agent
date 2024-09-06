from typing import Optional, List
from PIL import Image

class OneShotMermaidParams:
    def __init__(self, prompt: str, diagram_type: str, output_file: str, input_file: Optional[str] = None):
        self.prompt = prompt
        self.diagram_type = diagram_type
        self.output_file = output_file
        self.input_file = input_file

class ResolutionMermaidParams:
    def __init__(self, error: str, damaged_mermaid_chart: str, base_prompt: str, diagram_type: str, output_file: str, input_file: Optional[str] = None):
        self.error = error
        self.damaged_mermaid_chart = damaged_mermaid_chart
        self.base_prompt = base_prompt
        self.diagram_type = diagram_type
        self.output_file = output_file
        self.input_file = input_file

class IterateMermaidParams:
    def __init__(self, change_prompt: str, base_prompt: str, current_mermaid_chart: str, diagram_type: str, current_mermaid_img: Image.Image, output_file: str, input_file: Optional[str] = None):
        self.change_prompt = change_prompt
        self.base_prompt = base_prompt
        self.current_mermaid_chart = current_mermaid_chart
        self.diagram_type = diagram_type
        self.current_mermaid_img = current_mermaid_img
        self.output_file = output_file
        self.input_file = input_file

class MermaidAgentResponse:
    def __init__(self, img: Image.Image, mermaid: str):
        self.img = img
        self.mermaid = mermaid

class BulkMermaidParams:
    def __init__(self, prompt: str, diagram_type: str, count: int, output_file: str, input_file: Optional[str] = None):
        self.prompt = prompt
        self.diagram_type = diagram_type
        self.count = count
        self.output_file = output_file
        self.input_file = input_file

class BulkMermaidAgentResponse:
    def __init__(self, responses: List[MermaidAgentResponse]):
        self.responses = responses