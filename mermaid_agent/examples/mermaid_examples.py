import os
from typing import Optional, Dict, List
from modules.mermaid_agent import MermaidAgent
from modules.classes import (
    OneShotMermaidParams,
    ResolutionMermaidParams,
    IterateMermaidParams,
    BulkMermaidParams,
)

def read_example_file(file_name: str) -> str:
    """Read the content of an example file."""
    with open(os.path.join("examples", file_name), "r") as file:
        return file.read()

# Example diagrams mapped to their file names
EXAMPLE_FILES: Dict[str, str] = {
    "class": "class_example.py",
    "er": "er_example.py",
    "flowchart": "flowchart_example.py",
    "gantt": "gantt_example.py",
    "pie": "pie_example.py",
    "sequence": "sequence_example.py",
}

def get_example_diagram(diagram_type: str) -> str:
    """
    Get the example diagram for the specified type.
    
    Args:
        diagram_type (str): The type of the diagram.
    
    Returns:
        str: The example diagram for the specified type, or an empty string if not found.
    """
    file_name = EXAMPLE_FILES.get(diagram_type.lower())
    if file_name:
        return read_example_file(file_name)
    return ""

def one_shot_mermaid_agent(params: OneShotMermaidParams) -> str:
    agent = MermaidAgent()
    example_diagram = get_example_diagram(params.diagram_type)
    enhanced_prompt = f"Here's an example of a {params.diagram_type} diagram:\n\n{example_diagram}\n\nNow, create a new {params.diagram_type} diagram based on the following prompt:\n{params.prompt}"
    return agent.generate_diagram(enhanced_prompt, params.diagram_type)

def resolution_mermaid_agent(params: ResolutionMermaidParams) -> str:
    agent = MermaidAgent()
    example_diagram = get_example_diagram(params.diagram_type)
    enhanced_prompt = f"Here's an example of a correct {params.diagram_type} diagram:\n\n{example_diagram}\n\nNow, fix the following damaged diagram:\n{params.damaged_mermaid_chart}\n\nError message: {params.error}\n\nOriginal prompt: {params.base_prompt}"
    return agent.resolve_diagram(params.error, params.damaged_mermaid_chart, enhanced_prompt, params.diagram_type)

def bulk_mermaid_agent(params: BulkMermaidParams) -> List[str]:
    responses = []
    agent = MermaidAgent()
    example_diagram = get_example_diagram(params.diagram_type)
    enhanced_prompt = f"Here's an example of a {params.diagram_type} diagram:\n\n{example_diagram}\n\nNow, create {params.count} new {params.diagram_type} diagrams based on the following prompt:\n{params.prompt}"
    
    for _ in range(params.count):
        response = agent.generate_diagram(enhanced_prompt, params.diagram_type)
        responses.append(response)
    return responses

def iterate_mermaid_agent(params: IterateMermaidParams) -> str:
    agent = MermaidAgent()
    example_diagram = get_example_diagram(params.diagram_type)
    enhanced_prompt = f"Here's an example of a {params.diagram_type} diagram:\n\n{example_diagram}\n\nNow, modify the following diagram based on the change request:\n{params.current_mermaid_chart}\n\nChange request: {params.change_prompt}\n\nOriginal prompt: {params.base_prompt}"
    return agent.iterate_diagram(params.change_prompt, enhanced_prompt, params.diagram_type, params.current_mermaid_chart)