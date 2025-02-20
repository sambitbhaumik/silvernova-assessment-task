from src.api import execute_prompt


class LLMAsker:

  def __init__(self):
    pass

  def ask(self, question: str) -> str:
    print('Thinking...')
    response = execute_prompt(question)

    return response['response']
