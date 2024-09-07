from langchain.llms import BaseLLM
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseMemory
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.callbacks.manager import CallbackManager
from langchain.schema.runnable import RunnableSequence
from typing import Optional
from config import (
    LLM_PROVIDER, OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS,
    ANTHROPIC_API_KEY, ANTHROPIC_MODEL, ANTHROPIC_TEMPERATURE, ANTHROPIC_MAX_TOKENS
)

class LLMHandler:
    def __init__(self):
        self.provider = LLM_PROVIDER
        
        if self.provider == "openai":
            self.model = OPENAI_MODEL
            self.temperature = OPENAI_TEMPERATURE
            self.max_tokens = OPENAI_MAX_TOKENS
            self.llm = ChatOpenAI(
                model_name=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                openai_api_key=OPENAI_API_KEY,
                streaming=False
            )
        elif self.provider == "anthropic":
            self.model = ANTHROPIC_MODEL
            self.temperature = ANTHROPIC_TEMPERATURE
            self.max_tokens = ANTHROPIC_MAX_TOKENS
            self.llm = ChatAnthropic(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                anthropic_api_key=ANTHROPIC_API_KEY,
                streaming=False
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def create_llm_chain(self, prompt: PromptTemplate, memory: Optional[BaseMemory] = None) -> RunnableSequence:
        if memory:
            return RunnableSequence(
                memory.load_memory_variables | prompt | self.llm | memory.save_context
            )
        else:
            return prompt | self.llm

    def generate_response(self, prompt: str, system_prompt: str = "") -> str:
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            response = self.llm.generate([messages])
            return response.generations[0][0].text.strip()
        except Exception as e:
            raise Exception(f"Error generating LLM response: {str(e)}")

    def conditional_render(self, template: str, context: dict) -> str:
        rendered_template = template
        for key, value in context.items():
            rendered_template = rendered_template.replace(f"{{{key}}}", str(value))
        return rendered_template

def get_llm() -> BaseLLM:
    return LLMHandler().llm
