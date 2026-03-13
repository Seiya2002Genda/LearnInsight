import re

class Tokenizer:

    def tokenize(self, text):

        text = text.lower()

        text = re.sub(r"[^a-z0-9\s]", " ", text)

        tokens = text.split()

        return tokens