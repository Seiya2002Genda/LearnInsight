class MakeLearningReport:
    def generate_report(self, user_info, learning_records):
        total_subjects = len(learning_records)
        total_study_time = sum(float(record["study_time"]) for record in learning_records) if learning_records else 0
        average_score = sum(float(record["score"]) for record in learning_records) / total_subjects if total_subjects else 0

        return {
            "user": user_info,
            "total_records": total_subjects,
            "total_study_time": round(total_study_time, 2),
            "average_score": round(average_score, 2),
            "records": learning_records
        }