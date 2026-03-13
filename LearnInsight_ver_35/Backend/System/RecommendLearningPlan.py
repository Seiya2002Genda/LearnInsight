class RecommendLearningPlan:

    def __init__(self, learning_model):
        self.learning_model = learning_model

    def recommend(self, average_score, study_time):

        prediction = self.learning_model.predict_score(study_time)

        if prediction < 60:
            return {
                "level": "High Priority",
                "message": "Your predicted performance is low.",
                "action": "Increase study time and review fundamentals."
            }

        if prediction < 80:
            return {
                "level": "Medium Priority",
                "message": "You are progressing but can improve.",
                "action": "Practice more exercises and review mistakes."
            }

        return {
            "level": "Good Progress",
            "message": "Your learning performance is strong.",
            "action": "Move on to advanced topics."
        }