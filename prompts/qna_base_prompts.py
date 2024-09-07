from langchain.prompts import PromptTemplate

def generate_question_prompt() -> PromptTemplate:
    template = """
    You are an AI assistant with expertise in {expertise}, tasked with gathering information to create a diagram. Your goal is to ask investigative or exploratory questions to gain more information about the user's needs. Your questions should cover the following scope:

    1. Purpose of the diagram
    2. Key elements or components to be included
    3. Relationships between elements
    4. Any specific notations or conventions to be used
    5. Level of detail required
    6. Target audience for the diagram

    Previous conversation:
    {scratchpad}

    Based on this information and your expertise in {expertise}, what's the next most relevant question to ask? Provide only the question, without any additional text or context.

    Question:"""
    return PromptTemplate(
        input_variables=["expertise", "scratchpad"],
        template=template
    )

def generate_completion_check_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["expertise", "scratchpad"],
        template="""
        As an expert in {expertise}, based on the conversation history in the scratchpad:

        {scratchpad}

        Have we gathered enough information to generate a diagram? Answer with only 'Yes' or 'No'.

        Answer:"""
    )

def generate_brief_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["expertise", "scratchpad"],
        template="""
        As an expert in {expertise}, based on the following conversation history, generate a brief summary that captures the key points for creating a diagram:

        {scratchpad}

        Provide a concise summary that includes the diagram's purpose, key elements, relationships, notations, level of detail, and target audience. Your summary should be clear and informative, ready to be used for diagram generation. Use your inherent knowledge to suppliment the summary if needed.

        Summary:"""
    )

def generate_diagram_type_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["expertise", "scratchpad"],
        template="""
        As an expert in {expertise}, based on the following conversation history, determine the most appropriate type of Mermaid diagram to use:

        {scratchpad}

        Choose from the following supported Mermaid diagram types:
        - flowchart
        - sequence
        - class
        - state
        - er
        - gantt
        - pie
        - user journey

        Provide only the name of the diagram type, without any additional text or explanation.

        Diagram Type:"""
    )