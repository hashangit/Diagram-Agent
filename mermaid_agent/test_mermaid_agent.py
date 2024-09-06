import unittest
from unittest.mock import patch, MagicMock
from modules.mermaid_agent import MermaidAgent
from redundant.llm_handler import LLMHandler
from modules.mermaid_chain import MermaidChain
from modules.mermaid_handler import MermaidHandler

class TestMermaidAgent(unittest.TestCase):

    def setUp(self):
        self.agent = MermaidAgent()

    @patch('modules.mermaid_agent.load_example')
    @patch('modules.mermaid_agent.get_agent_prompt')
    def test_generate_diagram(self, mock_get_agent_prompt, mock_load_example):
        # Mock the dependencies
        mock_load_example.return_value = "Example Mermaid code"
        mock_get_agent_prompt.return_value = "Mocked prompt"
        self.agent.chain.run = MagicMock(return_value="Generated Mermaid code")
        self.agent.mermaid_handler.process_mermaid_code = MagicMock(return_value="Processed Mermaid code")

        # Call the method
        result = self.agent.generate_diagram("flowchart", "Test flowchart")

        # Assert the result
        self.assertEqual(result, "Processed Mermaid code")

        # Assert that the mocks were called with the correct arguments
        mock_load_example.assert_called_once_with("flowchart")
        mock_get_agent_prompt.assert_called_once_with("flowchart", "Test flowchart", "Example Mermaid code")
        self.agent.chain.run.assert_called_once_with("Mocked prompt")
        self.agent.mermaid_handler.process_mermaid_code.assert_called_once_with("Generated Mermaid code")

class TestLLMHandler(unittest.TestCase):

    @patch('modules.llm_handler.config')
    @patch('modules.llm_handler.openai.ChatCompletion.create')
    def test_generate_response_openai(self, mock_create, mock_config):
        # Configure the mocks
        mock_config.LLM_PROVIDER = "openai"
        mock_config.OPENAI_API_KEY = "test_api_key"
        mock_config.OPENAI_MODEL = "gpt-3.5-turbo"
        mock_config.OPENAI_TEMPERATURE = 0.7
        mock_config.OPENAI_MAX_TOKENS = 150
        
        mock_create.return_value.choices[0].message.content = "Mocked OpenAI response"

        # Create LLMHandler instance
        llm_handler = LLMHandler()

        # Call the method
        result = llm_handler.generate_response("Test prompt")

        # Assert the result
        self.assertEqual(result, "Mocked OpenAI response")

class TestMermaidChain(unittest.TestCase):

    def setUp(self):
        self.llm_handler = MagicMock()
        self.chain = MermaidChain(self.llm_handler)

    def test_extract_mermaid_code(self):
        response = """
        Here's the Mermaid code:
        ```mermaid
        graph TD;
            A-->B;
            B-->C;
            C-->D;
        ```
        """
        expected_code = "graph TD;\nA-->B;\nB-->C;\nC-->D;"
        result = self.chain._extract_mermaid_code(response)
        self.assertEqual(result, expected_code)

class TestMermaidHandler(unittest.TestCase):

    def setUp(self):
        self.handler = MermaidHandler()

    def test_validate_mermaid_syntax(self):
        valid_code = "graph TD;\n    A-->B;"
        invalid_code = "   \n  \n  "  # Only whitespace and newlines

        self.assertEqual(self.handler._validate_mermaid_syntax(valid_code), valid_code)
        with self.assertRaises(ValueError):
            self.handler._validate_mermaid_syntax(invalid_code)

if __name__ == '__main__':
    unittest.main()