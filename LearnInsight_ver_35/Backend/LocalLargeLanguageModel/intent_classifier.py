from .tokenizer import Tokenizer


class IntentClassifier:

    def __init__(self):

        self.tokenizer = Tokenizer()

    def classify(self, text):

        tokens = self.tokenizer.tokenize(text)

        if "assignment" in tokens:
            return "teacher"

        if "recommend" in tokens:
            return "recommendation"

        if "school" in tokens or "performance" in tokens:
            return "admin"

        return "student"