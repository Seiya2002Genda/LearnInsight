class Predictor:

    def __init__(self):
        pass

    def predict_score(self, model, study_time):
        prediction = model.predict([[float(study_time)]])
        return float(prediction[0])

    def predict_many(self, model, study_times):
        input_data = [[float(t)] for t in study_times]
        predictions = model.predict(input_data)
        return [float(value) for value in predictions]