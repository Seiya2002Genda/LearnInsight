import os
import matplotlib.pyplot as plt


class MakeLearningDataGraph:
    def create_graph(self, learning_records, output_path="FrontEnd/static/images/learning_graph.png"):
        if not learning_records:
            return None

        dates = [str(record["learning_date"]) for record in learning_records]
        scores = [float(record["score"]) for record in learning_records]

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        plt.figure(figsize=(10, 5))
        plt.plot(dates, scores, marker="o")
        plt.title("Learning Progress")
        plt.xlabel("Date")
        plt.ylabel("Score")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

        return output_path