from LearnInsight_ver_35.Backend.MachineLearning.learning_engine import LearningEngine


class LearningModel:

    def __init__(self):
        self.engine = LearningEngine()

    def train_model(self):
        return self.engine.train()

    def predict_score(self, study_time):
        return self.engine.predict_score(study_time)

    def recommend_learning_plan(self, study_time):
        return self.engine.recommend_learning_plan(study_time)

    def evaluate_model(self):
        return self.engine.get_model_metrics()