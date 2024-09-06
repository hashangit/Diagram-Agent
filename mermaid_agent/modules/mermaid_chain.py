class MermaidChain:
    def __init__(self, llm_handler):
        self.llm_handler = llm_handler

    def run(self, prompt):
        try:
            response = self.llm_handler.generate_response(prompt)
            return self._extract_mermaid_code(response)
        except Exception as e:
            raise Exception(f"Error running Mermaid chain: {str(e)}")

    def _extract_mermaid_code(self, response):
        lines = response.split('\n')
        mermaid_code = []
        in_code_block = False

        for line in lines:
            if line.strip() == '```mermaid':
                in_code_block = True
            elif line.strip() == '```' and in_code_block:
                in_code_block = False
            elif in_code_block:
                mermaid_code.append(line.strip())

        if mermaid_code:
            return '\n'.join(mermaid_code)
        else:
            # If no code blocks are found, return the entire response
            return response.strip()