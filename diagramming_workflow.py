from qna_agent.agent.questionnaire_agent import QuestionnaireAgent
from mermaid_agent.modules.mermaid_agent import MermaidAgent
from console_interface import ConsoleInterface
from dataclasses import dataclass

@dataclass
class DiagrammingState:
    brief: str = ""
    diagram_type: str = ""
    mermaid_code: str = ""
    error_message: str = ""

class DiagrammingWorkflow:
    def __init__(self):
        self.console = ConsoleInterface()

    def run_questionnaire(self, state: DiagrammingState, context: dict) -> DiagrammingState:
        agent = context.get("agent", QuestionnaireAgent())
        questionnaire = agent.run_questionnaire()

        try:
            while True:
                question = next(questionnaire)
                if isinstance(question, tuple):
                    questions, answers, brief, diagram_type = question
                    state.brief = brief
                    state.diagram_type = diagram_type
                    break
                elif isinstance(question, str):
                    if question.startswith("I apologize"):
                        state.diagram_type = None
                        state.error_message = question
                        break
                    self.console.display_message(question)  # Restored print statement for questions
                    user_input = self.console.get_user_input("Your answer: ")
                    questionnaire.send(user_input)
        except StopIteration:
            pass

        return state

    def generate_mermaid(self, state: DiagrammingState, context: dict) -> DiagrammingState:
        mermaid_agent = MermaidAgent()
        state.mermaid_code = mermaid_agent.generate_diagram(state.brief, state.diagram_type)
        return state

    def _print_header(self, text):
        print("=" * 50)
        print(text.center(50))
        print("=" * 50)