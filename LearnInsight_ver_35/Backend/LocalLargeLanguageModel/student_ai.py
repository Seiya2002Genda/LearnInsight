from .tokenizer import Tokenizer
from .knowledge_base import KnowledgeBase


class StudentAI:

    def __init__(self):

        self.tokenizer = Tokenizer()

        self.kb = KnowledgeBase()

    def answer(self, message, context):

        tokens = self.tokenizer.tokenize(message)

        knowledge = self.kb.search(tokens)

        if knowledge:
            return f"Study Advice:\n\n{knowledge}"

        return """
                Study Advice:
                
                1. Define the learning goal clearly.
                2. Study actively using examples.
                3. Review mistakes carefully.
                """