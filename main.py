from diagramming_workflow import DiagrammingWorkflow, DiagrammingState
from console_interface import ConsoleInterface
from qna_agent.agent.questionnaire_agent import QuestionnaireAgent

def main():
    workflow = DiagrammingWorkflow()
    interface = ConsoleInterface()
    questionnaire_agent = QuestionnaireAgent()

    initial_state = DiagrammingState()
    
    interface.display_welcome_message()
    
    # Run questionnaire
    state = workflow.run_questionnaire(initial_state, {"agent": questionnaire_agent})
    
    if state.diagram_type is None:
        interface.display_unsupported_diagram_message(state.error_message)
        return

    # Generate Mermaid diagram
    final_state = workflow.generate_mermaid(state, {})
    
    # Display results
    interface.display_results(final_state.brief, final_state.mermaid_code)
    interface.display_completion_message()

if __name__ == "__main__":
    main()