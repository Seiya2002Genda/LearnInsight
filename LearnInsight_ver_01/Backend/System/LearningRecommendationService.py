from LearnInsight_ver_01.Backend.System.RecommendLearningPlan import RecommendLearningPlan
from LearnInsight_ver_01.Backend.System.LearningSummaryService import LearningSummaryService


class LearningRecommendationService:

    def recommend(self,user_id):

        summary = LearningSummaryService().get_summary(user_id)

        avg = summary["average_score"]
        study = summary["total_study_time"]

        return RecommendLearningPlan().recommend(avg,study)