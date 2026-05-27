# ============================================================
# ml_module.py
# Collision Risk Prediction
# Features: distance (cm) + relative_speed (cm/s)
# relative_speed = consecutive distance readings ka difference / time
# ============================================================
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

class MLModule:
    def __init__(self, model_path='collision_model1.pkl'):
        self.model_path = model_path
        self.model      = None
        self.is_trained = False

        if os.path.exists(self.model_path):
            os.remove(self.model_path)
            print("Old model1 removed, training new model...")

        self.train_model()

    def train_model(self):
        """
        Train on distance + relative_speed.
        relative_speed = cm/s mein object kitni tezi se paas aa raha hai
        Positive = object paas aa raha hai (dangerous)
        Negative = object door ja raha hai (safe)
        """
        print("Training Collision Model (Distance + Relative Speed)...")

        np.random.seed(42)
        n = 3000

        distance       = np.random.uniform(2, 300, n)
        relative_speed = np.random.uniform(-50, 150, n)

        collision = np.zeros(n, dtype=int)

        for i in range(n):
            d  = distance[i]
            rs = relative_speed[i]

            if d < 15:
                collision[i] = 1                      # bahut paas — hamesha danger
            elif d < 30 and rs > 10:
                collision[i] = 1                      # paas + tezi se aa raha
            elif d < 50 and rs > 30:
                collision[i] = 1                      # medium dist + fast
            elif d < 80 and rs > 60:
                collision[i] = 1                      # thoda door + very fast
            elif d < 30 and rs < 0:
                collision[i] = 0                      # paas par door ja raha — safe
            else:
                collision[i] = 0

        df = pd.DataFrame({
            'distance':       distance,
            'relative_speed': relative_speed,
            'collision':      collision
        })

        X = df[['distance', 'relative_speed']]
        y = df['collision']

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=8,
            random_state=42
        )
        self.model.fit(X_train, y_train)

        acc = accuracy_score(y_test, self.model.predict(X_test))
        print(f"Model trained! Accuracy: {acc * 100:.2f}%")
        print(classification_report(y_test, self.model.predict(X_test),
                                    target_names=['Safe', 'Collision']))

        joblib.dump(self.model, self.model_path)
        self.is_trained = True

    def predict_collision(self, speed=0, distance=999, relative_speed=0.0):
        """
        Parameters:
            distance       : cm mein current distance
            relative_speed : cm/s (positive=paas aa raha, negative=door ja raha)
            speed          : backward compatibility ke liye rakha hai

        Returns: (collision_bool, probability_float)
        """
        if not self.is_trained or self.model is None:
            return False, 0.0

        try:
            X_new = pd.DataFrame([{
                'distance':       distance,
                'relative_speed': relative_speed
            }])
            prediction  = self.model.predict(X_new)[0]
            probability = self.model.predict_proba(X_new)[0][1]
            return bool(prediction), round(float(probability), 2)

        except Exception as e:
            print(f"Prediction error: {e}")
            return False, 0.0


# ── Singleton ─────────────────────────────────────────────────
_ml_instance = None

def get_ml_module():
    global _ml_instance
    if _ml_instance is None:
        _ml_instance = MLModule()
    return _ml_instance


if __name__ == "__main__":
    ml = get_ml_module()

    print(f"\n{'Distance':>10}  {'Rel.Speed':>12}  {'Collision':>10}  {'Prob':>8}  Meaning")
    print("-" * 70)

    tests = [
        (8,   50,  "Bahut paas + tezi se aa raha"),
        (25,  40,  "Paas + aa raha"),
        (25, -20,  "Paas par door ja raha — safe"),
        (60,  80,  "Medium + bahut tezi"),
        (60,  10,  "Medium + slow"),
        (100,  5,  "Door + slow"),
        (200,  0,  "Bahut door + static"),
    ]

    for dist, rs, meaning in tests:
        col, prob = ml.predict_collision(distance=dist, relative_speed=rs)
        c = "🚨 YES" if col else "  no"
        print(f"{dist:>8}cm  {rs:>+10.0f}cm/s  {c:>10}  {prob*100:>7.0f}%  {meaning}")