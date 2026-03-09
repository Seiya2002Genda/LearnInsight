import numpy as np
from sklearn.metrics import mean_squared_error, r2_score


class Evaluate:
    def evaluate_model(self, y_true, y_pred):
        y_true_array = np.array(y_true)
        y_pred_array = np.array(y_pred)
        mse = mean_squared_error(y_true_array, y_pred_array)
        rmse = float(np.sqrt(mse))
        r2 = r2_score(y_true_array, y_pred_array)
        return {
            "mse": float(mse),
            "rmse": rmse,
            "r2": float(r2)
        }