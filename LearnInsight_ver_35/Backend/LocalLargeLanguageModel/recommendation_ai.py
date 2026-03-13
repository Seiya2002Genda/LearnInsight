class RecommendationAI:

    def recommend(self, context):

        score = context.get("average_score", 0)

        if score < 60:
            return "Recommendation: Increase study time and review fundamentals."

        if score < 80:
            return "Recommendation: Practice more exercises."

        return "Recommendation: Continue advanced learning."