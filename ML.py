from sklearn.ensemble import RandomForestRegressor
import numpy as np

class MLModel:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.is_trained = False

    def train(self, X, y):
        self.model.fit(X, y)
        self.is_trained = True

    def predict(self, Pa, ECM, RCS, ENV):
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        X = np.array([[Pa, ECM, RCS, ENV]])
        return self.model.predict(X)[0]

# 使用示例
# ml_model = MLModel()
# 训练数据
# X_train = [[0.7, 50, 5, 7], [0.8, 30, 10, 8], ...]  # 更多训练数据
# y_train = [0.6, 0.8, ...]  # 对应的ρ值
# ml_model.train(X_train, y_train)
# 预测
# rho = ml_model.predict(Pa=0.75, ECM=60, RCS=5, ENV=7)