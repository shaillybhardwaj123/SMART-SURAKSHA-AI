import pandas as pd
from sklearn.linear_model import LogisticRegression

# LOAD + CLEAN ONCE
df = pd.read_csv("dataset_traffic_accident_prediction1.csv")

# only needed columns
df = df[['Speed_Limit', 'Weather']].copy()
df.columns = ['speed', 'weather']

# clean
df['speed'] = pd.to_numeric(df['speed'], errors='coerce')
df['weather'] = df['weather'].astype(str).str.lower()

df = df.dropna()

# map weather
df['weather'] = df['weather'].apply(lambda x: 0 if 'clear' in x else 1)

# target (simple)
median_speed = df['speed'].median()
df['risk'] = (df['speed'] > median_speed).astype(int)

# model train (once)
X = df[['speed', 'weather']]
y = df['risk']

model = LogisticRegression()
model.fit(X, y)

def predict_risk(speed, weather):
    # safety checks
    if speed is None or weather is None:
        return "❌ Invalid input"

    weather = str(weather).strip().lower()

    # DEBUG print (terminal में दिखेगा)
    print("ML DEBUG =>", speed, weather)

    if speed > 80 and weather in ["rain", "fog"]:
        return "⚠ HIGH ACCIDENT RISK"
    elif speed > 60:
        return "⚠ MEDIUM ACCIDENT RISK"
    else:
        return "✅ LOW ACCIDENT RISK"
