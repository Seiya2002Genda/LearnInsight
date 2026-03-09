import numpy as np


class UseLearningModel:
    def use_model(self, model, input_data):
        input_array = np.array(input_data).reshape(-1, 1) if np.array(input_data).ndim == 1 else np.array(input_data)
        result = model.predict(input_array)
        return result.tolist()