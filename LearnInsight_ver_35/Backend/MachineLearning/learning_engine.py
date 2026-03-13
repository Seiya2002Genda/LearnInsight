from LearnInsight_ver_35.Backend.MachineLearning.trainData import TrainData
from LearnInsight_ver_35.Backend.MachineLearning.MakeLearningModel import MakeLearningModel
from LearnInsight_ver_35.Backend.MachineLearning.predict import Predictor
from LearnInsight_ver_35.Backend.MachineLearning.evaluate import EvaluateModel
from LearnInsight_ver_35.Backend.MachineLearning.UseLearningModel import UseLearningModel


class LearningEngine:

    def __init__(self):
        self.train_data = TrainData()
        self.model_builder = MakeLearningModel()
        self.predictor = Predictor()
        self.evaluator = EvaluateModel()
        self.model_user = UseLearningModel()

        self.model = None
        self.metrics = None
        self.is_trained = False

    def train(self):
        x_data, y_data = self.train_data.load_data()

        if len(x_data) == 0 or len(y_data) == 0:
            self.model = None
            self.metrics = None
            self.is_trained = False
            return False

        self.model = self.model_builder.create_model(x_data, y_data)
        self.metrics = self.evaluator.evaluate(self.model, x_data, y_data)
        self.is_trained = True
        return True

    def ensure_model(self):
        if not self.is_trained or self.model is None:
            self.train()

    def predict_score(self, study_time):
        self.ensure_model()

        if self.model is None:
            return 0.0

        return self.predictor.predict_score(self.model, study_time)

    def recommend_learning_plan(self, study_time):
        predicted_score = self.predict_score(study_time)
        recommendation = self.model_user.recommend(predicted_score, study_time)

        return {
            "study_time": float(study_time),
            "predicted_score": predicted_score,
            "recommendation": recommendation
        }

    def get_model_metrics(self):
        self.ensure_model()

        if self.metrics is None:
            return {
                "mse": 0.0,
                "mae": 0.0,
                "r2": 0.0
            }

        return self.metrics