from sklearn.linear_model import LinearRegression


class MakeLearningModel:
    def __init__(self):
        self.model = LinearRegression()

    def create_model(self):
        return self.model