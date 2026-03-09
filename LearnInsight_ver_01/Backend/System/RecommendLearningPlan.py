class RecommendLearningPlan:
    def recommend(self, average_score, study_time):
        if average_score < 60:
            return {
                "level": "High Priority",
                "recommendation": "Increase daily study time, review weak subjects, and practice foundational concepts."
            }
        if average_score < 80:
            return {
                "level": "Moderate Priority",
                "recommendation": "Maintain consistent study habits and add targeted problem-solving practice."
            }
        if study_time < 1:
            return {
                "level": "Good Performance",
                "recommendation": "Your score is good, but increasing study time slightly may improve consistency."
            }
        return {
            "level": "Excellent",
            "recommendation": "Continue the current learning plan and focus on advanced practice."
        }