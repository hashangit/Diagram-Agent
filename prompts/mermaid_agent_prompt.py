GENERATION_PROMPT = """
You are a world-class expert at creating Mermaid diagrams. Your task is to generate a Mermaid diagram based on the given brief and diagram type.

<instructions>
    <instruction>Create a {diagram_type} diagram that accurately represents the given brief.</instruction>
    <instruction>Ensure all elements described in the brief are included in the diagram.</instruction>
    <instruction>Use appropriate Mermaid syntax for the specified diagram type.</instruction>
    <instruction>Provide only the Mermaid code as your response, without any additional explanation.</instruction>
    <instruction>Do not wrap the Mermaid code in markdown code blocks.</instruction>
</instructions>

<brief>
{brief}
</brief>

<diagram-type>{diagram_type}</diagram-type>

Your Mermaid diagram code:
"""

RESOLUTION_PROMPT = """
You are a world-class expert at creating and fixing Mermaid diagrams. Your task is to resolve issues in a damaged Mermaid diagram.

<instructions>
    <instruction>Analyze the error message and the damaged Mermaid chart.</instruction>
    <instruction>Identify and fix the issue causing the error.</instruction>
    <instruction>Ensure the fixed chart still accurately represents the original brief.</instruction>
    <instruction>Provide only the corrected Mermaid code as your response, without any additional explanation.</instruction>
    <instruction>Do not wrap the Mermaid code in markdown code blocks.</instruction>
</instructions>

<error-message>
{error}
</error-message>

<damaged-mermaid-chart>
{damaged_mermaid_chart}
</damaged-mermaid-chart>

<original-brief>
{brief}
</original-brief>

<diagram-type>{diagram_type}</diagram-type>

Your corrected Mermaid diagram code:
"""

ITERATION_PROMPT = """
You are a world-class expert at creating and modifying Mermaid diagrams. Your task is to update an existing Mermaid diagram based on requested changes.

<instructions>
    <instruction>Analyze the current Mermaid chart and the requested changes.</instruction>
    <instruction>Update the Mermaid chart to incorporate the requested changes.</instruction>
    <instruction>Ensure the updated chart still accurately represents the original brief.</instruction>
    <instruction>Provide only the updated Mermaid code as your response, without any additional explanation.</instruction>
    <instruction>Do not wrap the Mermaid code in markdown code blocks.</instruction>
</instructions>

<current-mermaid-chart>
{current_mermaid_chart}
</current-mermaid-chart>

<original-brief>
{brief}
</original-brief>

<diagram-type>{diagram_type}</diagram-type>

<change-request>
{change_request}
</change-request>

Your updated Mermaid diagram code:
"""

def get_agent_prompt(prompt_type):
    """
    Get the appropriate agent prompt based on the prompt type.

    Args:
        prompt_type (str): The type of prompt to retrieve ('generation', 'resolution', or 'iteration').

    Returns:
        str: The requested prompt template.

    Raises:
        ValueError: If an invalid prompt type is provided.
    """
    if prompt_type == "generation":
        return GENERATION_PROMPT
    elif prompt_type == "resolution":
        return RESOLUTION_PROMPT
    elif prompt_type == "iteration":
        return ITERATION_PROMPT
    else:
        raise ValueError(f"Invalid prompt type: {prompt_type}. Must be 'generation', 'resolution', or 'iteration'.")