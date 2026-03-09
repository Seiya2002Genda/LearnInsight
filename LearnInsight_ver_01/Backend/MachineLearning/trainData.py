import numpy as np
from sklearn.linear_model import LinearRegression


class TrainData:
    def __init__(self):
        self.model = None

    def train(self, X, y):
        X_array = np.array(X).reshape(-1, 1) if np.array(X).ndim == 1 else np.array(X)
        y_array = np.array(y)
        self.model = LinearRegression()
        self.model.fit(X_array, y_array)
        return self.model

    def get_model(self):
        return self.model