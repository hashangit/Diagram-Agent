from typing import List

def load_questions(file_path: str) -> List[str]:
    with open(file_path, 'r') as file:
        content = file.read()
        questions = [line.strip('- ').strip() for line in content.split('\n') if line.strip().startswith('- ')]
    return questions