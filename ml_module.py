import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

class MLModule:
    def __init__(self, dataset_path='dataset.csv', model_path='accident_model.pkl'):
        self.dataset_path = dataset_path
        self.model_path = model_path
        self.model = LogisticRegression()
        self.is_trained = False

        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.is_trained = True
        else:
            self.train_model()

    def train_model(self):
        print("Training Accident Detection Model (Logistic Regression)...")
        try:
            df = pd.read_csv(self.dataset_path)
            
            X = df[['vehicle_speed', 'distance_between_cars', 'sensor_impact_force', 'ai_accident_confidence']]
            y = df['accident_occurred']

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            self.model.fit(X_train, y_train)
            
            predictions = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, predictions)
            print(f"Collision Model trained successfully! Accuracy: {accuracy * 100:.2f}%")
            
            joblib.dump(self.model, self.model_path)
            self.is_trained = True

        except Exception as e:
            print(f"Error training model: {e}")

    def predict_accident(self, speed, distance_between, impact_force, ai_conf):
        """Predicts whether an accident has occurred."""
        if not self.is_trained:
            return False, 0.0
        
        try:
            X_new = pd.DataFrame([{
                'vehicle_speed': speed,
                'distance_between_cars': distance_between,
                'sensor_impact_force': impact_force,
                'ai_accident_confidence': ai_conf
            }])
            
            prediction = self.model.predict(X_new)[0]
            probability = self.model.predict_proba(X_new)[0][1]
            return bool(prediction), float(probability)
        except Exception as e:
            print(f"Prediction error: {e}")
            return False, 0.0

if __name__ == "__main__":
    ml = MLModule()
    # Test Crash Prediction
    crash, prob = ml.predict_accident(110, 0.5, 95, 0.98)
    print(f"Test Prediction: Accident Detected={crash}, Probability={prob:.2f}")
