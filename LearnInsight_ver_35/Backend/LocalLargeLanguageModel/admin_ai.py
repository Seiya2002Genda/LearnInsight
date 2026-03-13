class AdminAI:

    def school_performance(self, records):

        if not records:
            return "No performance data available."

        avg_score = sum(r.get("score", 0) for r in records) / len(records)

        return f"School Average Score: {round(avg_score,2)}"