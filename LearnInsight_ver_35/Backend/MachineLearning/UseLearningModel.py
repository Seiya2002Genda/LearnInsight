class UseLearningModel:

    def __init__(self):
        pass

    def recommend(self, predicted_score, study_time=None):
        predicted_score = float(predicted_score)

        if predicted_score < 60:
            return {
                "level": "high_priority",
                "message": "Focus on fundamentals and increase study consistency.",
                "action": "Review basic concepts, practice daily, and ask for support."
            }

        if predicted_score < 75:
            return {
                "level": "medium_priority",
                "message": "You understand part of the material but need stronger application.",
                "action": "Practice problem solving and review mistakes carefully."
            }

        if predicted_score < 90:
            return {
                "level": "good_progress",
                "message": "Your progress is solid. Keep improving depth and accuracy.",
                "action": "Move to harder examples and strengthen weak areas."
            }

        return {
            "level": "advanced",
            "message": "You are performing very well.",
            "action": "Challenge yourself with advanced tasks and extension work."
        }