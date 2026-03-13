class KnowledgeBase:

    def __init__(self):

        self.study_topics = {

            "python": "Practice writing small scripts and build mini projects.",
            "math": "Solve practice problems daily and review mistakes.",
            "algorithm": "Focus on problem solving and complexity analysis.",
            "database": "Practice SQL queries and understand normalization.",
            "ai": "Study machine learning basics and experiment with datasets."
        }

    def search(self, tokens):

        for token in tokens:

            if token in self.study_topics:
                return self.study_topics[token]

        return None