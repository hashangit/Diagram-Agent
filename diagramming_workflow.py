from typing import List, Dict, Any
from pydantic import BaseModel
from qna_agent.agent.questionnaire_agent import QuestionnaireAgent
from mermaid_agent.modules.mermaid_agent import MermaidAgent
from console_interface import ConsoleInterface

class DiagrammingState(BaseModel):
    brief: str = ""
    diagram_type: str = ""
    mermaid_code: str = ""
    error_message: str = ""

class DiagrammingWorkflow:
    def __init__(self):
        self.mermaid_agent = MermaidAgent()
        self.console = ConsoleInterface()

    def run_questionnaire(self, state: DiagrammingState, inputs: Dict[str, Any]) -> DiagrammingState:
        questionnaire_agent = inputs.get("agent", QuestionnaireAgent())
        questionnaire = questionnaire_agent.run_questionnaire()
        
        try:
            while True:
                question = next(questionnaire)
                print("DEBUG: Question:", question)  # Debug print
                
                if isinstance(question, tuple):  # This is the final result
                    questions, answers, brief, diagram_type = question
                    state.brief = brief
                    state.diagram_type = diagram_type
                    print("DEBUG: Final result received")  # Debug print
                    break
                elif isinstance(question, str):
                    if question.startswith("I apologize"):  # Unsupported diagram type
                        state.error_message = question
                        state.diagram_type = None
                        print("DEBUG: Unsupported diagram type")  # Debug print
                        break
                    else:  # This is a question
                        self.console.display_question(question)
                        user_input = self.console.get_user_input("Your answer: ")
                        print("DEBUG: User input:", user_input)  # Debug print
                        questionnaire.send(user_input)
        except StopIteration:
            print("DEBUG: StopIteration caught")  # Debug print
            # Use whatever information is available in the scratchpad
            state.brief = questionnaire_agent.generate_brief()
            state.diagram_type = questionnaire_agent.generate_diagram_type()
        
        # Validate state after questionnaire
        if not state.brief or not state.diagram_type:
            state.error_message = "Unable to determine diagram type or generate brief. Please provide more information."
            state.diagram_type = None
        elif not questionnaire_agent.is_diagram_supported(state.diagram_type):
            state.error_message = f"The {state.diagram_type} diagram is not supported. Please try with a supported Mermaid diagram type."
            state.diagram_type = None
        
        return state

    def generate_mermaid(self, state: DiagrammingState, inputs: Dict[str, Any]) -> DiagrammingState:
        if state.diagram_type is None:
            return state
        state.mermaid_code = self.mermaid_agent.generate_diagram(state.brief, state.diagram_type)
        return state

if __name__ == "__main__":
    initial_state = DiagrammingState()
    workflow = DiagrammingWorkflow()
    console = ConsoleInterface()

    console.display_welcome_message()
    state = workflow.run_questionnaire(initial_state, {})
    if state.diagram_type is not None:
        final_state = workflow.generate_mermaid(state, {})
        console.display_results(final_state.brief, final_state.mermaid_code)
    else:
        console.display_unsupported_diagram_message(state.error_message)
    console.display_completion_message()