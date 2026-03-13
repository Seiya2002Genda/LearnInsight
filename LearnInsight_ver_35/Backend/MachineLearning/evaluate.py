from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


class EvaluateModel:

    def __init__(self):
        pass

    def evaluate(self, model, x_data, y_data):
        predictions = model.predict(x_data)

        mse = mean_squared_error(y_data, predictions)
        mae = mean_absolute_error(y_data, predictions)
        r2 = r2_score(y_data, predictions)

        return {
            "mse": float(mse),
            "mae": float(mae),
            "r2": float(r2)
        }