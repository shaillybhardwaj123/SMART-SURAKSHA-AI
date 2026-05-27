# ============================================================
# ml_module.py
# Collision Risk Prediction — Speed + Distance only
# ============================================================
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

class MLModule:
    def __init__(self, model_path='collision_model.pkl'):
        self.model_path = model_path
        self.model = LogisticRegression()
        self.is_trained = False

        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.is_trained = True
            print("✅ Collision model loaded.")
        else:
            self.train_model()

    def train_model(self):
        """Generate synthetic data and train on speed + distance."""
        print("🔄 Training Collision Model on Speed + Distance...")

        np.random.seed(42)
        n = 1000

        speed    = np.random.uniform(0, 120, n)      # km/h
        distance = np.random.uniform(5, 200, n)      # cm

        # Collision logic:
        # High speed + low distance = collision likely
        collision = ((speed > 60) & (distance < 50)).astype(int)
        collision = np.where(
            (speed > 80) & (distance < 30), 1, collision
        )

        df = pd.DataFrame({
            'speed': speed,
            'distance': distance,
            'collision': collision
        })

        X = df[['speed', 'distance']]
        y = df['collision']

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        self.model.fit(X_train, y_train)
        acc = accuracy_score(y_test, self.model.predict(X_test))
        print(f"✅ Collision Model trained! Accuracy: {acc * 100:.2f}%")

        joblib.dump(self.model, self.model_path)
        self.is_trained = True

    def predict_collision(self, speed, distance):
        """
        Returns: (collision_bool, probability_float)
        """
        if not self.is_trained:
            return False, 0.0

        try:
            X_new = pd.DataFrame([{
                'speed': speed,
                'distance': distance
            }])
            prediction   = self.model.predict(X_new)[0]
            probability  = self.model.predict_proba(X_new)[0][1]
            return bool(prediction), round(float(probability), 2)
        except Exception as e:
            print(f"❌ Collision prediction error: {e}")
            return False, 0.0


# ---- Singleton so model loads only once ----
_ml_instance = None

def get_ml_module():
    global _ml_instance
    if _ml_instance is None:
        _ml_instance = MLModule()
    return _ml_instance


if __name__ == "__main__":
    ml = get_ml_module()
    collision, prob = ml.predict_collision(speed=90, distance=25)
    print(f"Collision: {collision}, Probability: {prob}")