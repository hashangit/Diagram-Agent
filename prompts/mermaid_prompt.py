MERMAID_PROMPT_TEMPLATE = """
You are a Mermaid diagram expert. Your task is to generate a Mermaid diagram based on the given information.

Diagram Type: {diagram_type}

Description: {description}

Example:
```mermaid
{example}
```

Please create a Mermaid diagram that matches the requested type and follows the given description. Use the provided example as a reference for structure and syntax, but create a unique diagram that fits the description.

Rules:
1. Start the diagram with the appropriate Mermaid syntax for the diagram type.
2. Use clear and concise labels for nodes and connections.
3. Ensure the diagram is logically structured and easy to read.
4. Include all relevant information from the description.
5. Do not copy the example directly; create a new diagram based on the description.

Provide only the Mermaid code for the diagram, without any additional explanations or markdown formatting.
"""

def get_mermaid_prompt(diagram_type, description, example):
    return MERMAID_PROMPT_TEMPLATE.format(
        diagram_type=diagram_type,
        description=description,
        example=example
    )