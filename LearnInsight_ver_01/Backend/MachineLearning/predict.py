import numpy as np


class Predict:
    def predict(self, model, data):
        data_array = np.array(data).reshape(-1, 1) if np.array(data).ndim == 1 else np.array(data)
        return model.predict(data_array).tolist()