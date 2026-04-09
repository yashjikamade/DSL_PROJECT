"""
train_model.py
────────────────────────────────────────────────────────────────
Trains a Linear Regression model on the generated dataset and
saves it as model.pkl so the Streamlit app can load it without
re-training on every restart (optional — the app also trains
inline via @st.cache_resource).

Run:  python train_model.py
Output: model.pkl, model_metrics.json
"""

import json
import pickle

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split

# ── Load ──────────────────────────────────────────────────────
print("Loading dataset…")
df = pd.read_csv("monthly_spending_dataset_2020_2025.csv")
print(f"  Rows: {len(df):,}  |  Columns: {list(df.columns)}")

FEATURES = [
    "Income (₹)",
    "Savings (₹)",
    "Rent (₹)",
    "Groceries (₹)",
    "Transportation (₹)",
    "Utilities (₹)",
    "Dining Out (₹)",
    "Entertainment (₹)",
]
TARGET = "Total Expenditure (₹)"

X = df[FEATURES]
y = df[TARGET]

# ── Split ─────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ── Train ─────────────────────────────────────────────────────
model = LinearRegression()
model.fit(X_train, y_train)

# ── Evaluate ──────────────────────────────────────────────────
y_pred = model.predict(X_test)

mae   = mean_absolute_error(y_test, y_pred)
rmse  = np.sqrt(mean_squared_error(y_test, y_pred))
r2    = r2_score(y_test, y_pred)

cv_scores = cross_val_score(model, X, y, cv=5, scoring="r2")

print("\n── Model Performance ─────────────────────────────────")
print(f"  MAE  : ₹{mae:,.0f}")
print(f"  RMSE : ₹{rmse:,.0f}")
print(f"  R²   : {r2:.4f}")
print(f"  CV R²: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

print("\n── Feature Coefficients ──────────────────────────────")
for feat, coef in zip(FEATURES, model.coef_):
    print(f"  {feat:<30s}: {coef:+.4f}")
print(f"  {'Intercept':<30s}: {model.intercept_:+.2f}")

# ── Save ──────────────────────────────────────────────────────
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

metrics = {
    "mae":    round(mae, 2),
    "rmse":   round(rmse, 2),
    "r2":     round(r2, 4),
    "cv_r2_mean": round(float(cv_scores.mean()), 4),
    "cv_r2_std":  round(float(cv_scores.std()), 4),
    "features": FEATURES,
    "target":   TARGET,
    "train_rows": len(X_train),
    "test_rows":  len(X_test),
}
with open("model_metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

print("\n✅  model.pkl and model_metrics.json saved.")
