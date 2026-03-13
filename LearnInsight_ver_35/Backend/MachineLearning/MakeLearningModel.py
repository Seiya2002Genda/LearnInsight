from sklearn.linear_model import LinearRegression


class MakeLearningModel:

    def __init__(self):
        self.model = LinearRegression()

    def create_model(self, x_data, y_data):
        self.model.fit(x_data, y_data)
        return self.model