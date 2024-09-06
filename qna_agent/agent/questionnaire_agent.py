from typing import List, Dict, Any, Tuple
import yaml
from langchain.schema import AIMessage
from langchain.prompts import PromptTemplate

from config import QUESTIONNAIRE_EXPERTISE
from prompts.qna_base_prompts import generate_question_prompt, generate_brief_prompt, generate_diagram_type_prompt
from common.llm_handler import LLMHandler, get_llm

class QuestionnaireAgent:
    def __init__(self, expertise: str = QUESTIONNAIRE_EXPERTISE):
        self.llm = get_llm()
        self.llm_handler = LLMHandler()
        self.expertise = expertise
        self.scratchpad = []
        self.supported_diagrams = ["flowchart", "sequence", "class", "state", "er", "gantt", "pie", "user journey"]
        self.points = 0
        self.max_questions = 6

    def add_to_scratchpad(self, role: str, content: str):
        self.scratchpad.append({"role": role, "content": content})

    def generate_initial_question(self) -> str:
        template = """
        Generate a friendly and conversational question asking the user what type of diagram they need. 
        Encourage them to provide details about their requirements. Keep it concise and clear. only output the question, no overhead chatter.
        
        Question:
        """
        prompt = PromptTemplate(template=template, input_variables=[])
        chain = self.llm_handler.create_llm_chain(prompt)
        response = chain.invoke({})
        return response.content if isinstance(response, AIMessage) else str(response).strip()

    def generate_question(self) -> str:
        prompt = generate_question_prompt()
        chain = self.llm_handler.create_llm_chain(prompt)
        response = chain.invoke({"expertise": self.expertise, "scratchpad": yaml.dump(self.scratchpad)})
        return response.content if isinstance(response, AIMessage) else str(response).strip()

    def is_diagram_supported(self, diagram_type: str) -> bool:
        return diagram_type.lower() in self.supported_diagrams

    def generate_brief(self) -> str:
        brief_prompt = generate_brief_prompt()
        chain = self.llm_handler.create_llm_chain(brief_prompt)
        response = chain.invoke({"expertise": self.expertise, "scratchpad": yaml.dump(self.scratchpad)})
        return response.content if isinstance(response, AIMessage) else str(response).strip()

    def generate_diagram_type(self) -> str:
        diagram_type_prompt = generate_diagram_type_prompt()
        chain = self.llm_handler.create_llm_chain(diagram_type_prompt)
        response = chain.invoke({"expertise": self.expertise, "scratchpad": yaml.dump(self.scratchpad)})
        return (response.content if isinstance(response, AIMessage) else str(response)).strip().lower()

    def evaluate_answer(self, answer: str) -> Tuple[int, str, str]:
        template = """
        Evaluate the following answer on a scale of 0 to 20 based on its relevance and detail for creating a {expertise} diagram:
        
        Answer: {answer}
        
        Consider the specific requirements and best practices for {expertise} diagrams when evaluating.
        
        Provide your response in the following format:
        Score: [0-20]
        Next Question: [Your suggested next question]
        Diagram Type: [Suggested diagram type based on the answer]
        
        Response:
        """
        prompt = PromptTemplate(template=template, input_variables=["expertise", "answer"])
        chain = self.llm_handler.create_llm_chain(prompt)
        response = chain.invoke({"expertise": self.expertise, "answer": answer})
        response_content = response.content if isinstance(response, AIMessage) else str(response)
        
        lines = response_content.strip().split('\n')
        score = 10  # Default value
        next_question = ""
        diagram_type = ""
        
        for line in lines:
            if line.startswith("Score:"):
                try:
                    score = int(line.split(":")[1].strip())
                except ValueError:
                    score = 10  # Default value if parsing fails
            elif line.startswith("Next Question:"):
                next_question = line.split(":", 1)[1].strip()
            elif line.startswith("Diagram Type:"):
                diagram_type = line.split(":", 1)[1].strip()
        
        return score, next_question, diagram_type

    def run_questionnaire(self):
        # Generate and ask the initial question
        initial_question = self.generate_initial_question()
        self.add_to_scratchpad("assistant", initial_question)
        
        questions = [initial_question]
        answers = []
        
        question_count = 0
        try:
            while self.points < 100 and question_count < self.max_questions:
                if question_count > 0:
                    questions.append(next_question)
                
                user_input = yield questions[question_count]
                
                if user_input is not None:
                    self.add_to_scratchpad("human", user_input)
                    answers.append(user_input)
                    
                    # Use LLM to evaluate the answer, get the score, next question, and initial diagram type
                    score, next_question, diagram_type = self.evaluate_answer(user_input)
                    self.points += score
                    self.add_to_scratchpad("system", f"Diagram Type: {diagram_type}")
                    self.add_to_scratchpad("system", f"Score: {score}")
                
                question_count += 1
        except StopIteration:
            # Questionnaire ended unexpectedly, use available information
            pass

        # Generate the final diagram type based on the entire conversation
        diagram_type = self.generate_diagram_type()
        
        # Check if the diagram type is supported
        if not self.is_diagram_supported(diagram_type):
            yield f"I apologize, but the {diagram_type} diagram is not supported by the diagramming agent at this time. Please try with a supported Mermaid diagram type (flowchart, sequence, class, state, er, gantt, pie, user journey) or wait for future updates."
            return

        # Generate the brief based on the entire conversation
        brief = self.generate_brief()
        
        return questions, answers, brief, diagram_type