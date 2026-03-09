from LearnInsight_ver_01.Backend.Information.InputLearningInformation import InputLearningInformation


class LearningSummaryService:

    def get_summary(self, user_id):

        records = InputLearningInformation().get_learning_data_by_user(user_id)

        if not records:
            return {
                "total_study_time": 0,
                "average_score": 0,
                "record_count": 0,
                "records": []
            }

        total_time = sum(r["study_time"] for r in records)
        avg_score = sum(r["score"] for r in records) / len(records)

        return {
            "total_study_time": total_time,
            "average_score": round(avg_score,2),
            "record_count": len(records),
            "records": records
        }