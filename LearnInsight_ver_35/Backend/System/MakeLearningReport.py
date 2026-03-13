class MakeLearningReport:

    def generate_report(self, user, records):

        total_time = 0
        total_score = 0
        count = 0

        for r in records:

            study = r.get("study_time")
            score = r.get("score")

            if study:
                total_time += float(study)

            if score:
                total_score += float(score)
                count += 1

        avg_score = 0
        if count > 0:
            avg_score = round(total_score / count, 2)

        return {
            "total_study_time": total_time,
            "average_score": avg_score,
            "record_count": len(records)
        }


    def learning_summary(self, user, records):

        report = self.generate_report(user, records)

        trend = "Stable"

        if report["average_score"] > 80:
            trend = "Improving"

        if report["average_score"] < 60:
            trend = "Needs Improvement"

        return {
            "total_study_time": report["total_study_time"],
            "average_score": report["average_score"],
            "total_records": report["record_count"],
            "learning_trend": trend
        }