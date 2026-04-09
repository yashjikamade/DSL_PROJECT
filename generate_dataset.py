"""
generate_dataset.py
────────────────────────────────────────────────────────────────
Generates a realistic Indian household monthly spending dataset
for 2020–2025 (72 months × ~833 households ≈ 60,000 rows).

Run:  python generate_dataset.py
Output: monthly_spending_dataset_2020_2025.csv
"""

import numpy as np
import pandas as pd

np.random.seed(42)


N_HOUSEHOLDS = 833          # × 72 months ≈ 60 k rows
START_DATE   = "2020-01-01"
MONTHS       = 72           # Jan 2020 – Dec 2025

# Income tiers (₹/month)  [min, max, weight]
TIERS = [
    (15_000,  40_000, 0.30),   # Entry Level
    (40_001,  90_000, 0.35),   # Mid Level
    (90_001, 2_50_000, 0.25),  # Upper Mid
    (2_50_001, 6_00_000, 0.10),# High Earner
]


def sample_income(n):
    tiers  = np.random.choice(len(TIERS), size=n, p=[t[2] for t in TIERS])
    result = np.array([
        np.random.randint(TIERS[t][0], TIERS[t][1] + 1)
        for t in tiers
    ], dtype=float)
    return result

def clamp(arr, lo, hi):
    return np.clip(arr, lo, hi)

# ── Generate ──────────────────────────────────────────────────
dates      = pd.date_range(START_DATE, periods=MONTHS, freq="MS")
date_cycle = np.tile(dates, N_HOUSEHOLDS)[:N_HOUSEHOLDS * MONTHS]

incomes_base = sample_income(N_HOUSEHOLDS)

rows = []
for month_idx, dt in enumerate(dates):
    # Slight income growth each year (~5% annual raise)
    yoy_factor = 1 + 0.05 * (month_idx / 12)
    # Seasonal effect: higher spend in Nov-Dec (festivals), lower in Feb-Mar
    seasonal = 1.0 + 0.04 * np.sin(2 * np.pi * (dt.month - 1) / 12)

    income = incomes_base * yoy_factor * np.random.normal(1.0, 0.02, N_HOUSEHOLDS)
    income = np.round(income, -2)   # round to nearest 100

    # Expense proportions (noisy, income-correlated)
    rent_r    = np.random.normal(0.26, 0.07, N_HOUSEHOLDS)
    groc_r    = np.random.normal(0.09, 0.03, N_HOUSEHOLDS)
    trans_r   = np.random.normal(0.05, 0.02, N_HOUSEHOLDS)
    util_r    = np.random.normal(0.03, 0.01, N_HOUSEHOLDS)
    dining_r  = np.random.normal(0.06, 0.025, N_HOUSEHOLDS)
    entert_r  = np.random.normal(0.03, 0.015, N_HOUSEHOLDS)
    medical_r = np.random.normal(0.03, 0.015, N_HOUSEHOLDS)
    savings_r = np.random.normal(0.18, 0.06, N_HOUSEHOLDS)

    # Clamp proportions
    rent_r    = clamp(rent_r,    0.05, 0.55)
    groc_r    = clamp(groc_r,    0.02, 0.25)
    trans_r   = clamp(trans_r,   0.01, 0.18)
    util_r    = clamp(util_r,    0.005,0.10)
    dining_r  = clamp(dining_r,  0.00, 0.20)
    entert_r  = clamp(entert_r,  0.00, 0.15)
    medical_r = clamp(medical_r, 0.00, 0.20)
    savings_r = clamp(savings_r, 0.00, 0.50)

    rent      = np.round(income * rent_r,    -2)
    groceries = np.round(income * groc_r,    -2)
    transport = np.round(income * trans_r,   -2)
    utilities = np.round(income * util_r,    -2)
    dining    = np.round(income * dining_r,  -2)
    entertain = np.round(income * entert_r,  -2)
    medical   = np.round(income * medical_r, -2)
    savings   = np.round(income * savings_r, -2)

    # Total expenditure = everything except savings, with seasonal noise
    total = (rent + groceries + transport + utilities +
             dining + entertain + medical) * seasonal
    total = np.round(total * np.random.normal(1.0, 0.015, N_HOUSEHOLDS), -2)
    total = clamp(total, 5_000, income)   # can't spend more than you earn

    for i in range(N_HOUSEHOLDS):
        rows.append({
            "Month":                  dt.strftime("%Y-%m"),
            "Income (₹)":            int(income[i]),
            "Savings (₹)":           int(savings[i]),
            "Rent (₹)":              int(rent[i]),
            "Groceries (₹)":         int(groceries[i]),
            "Transportation (₹)":    int(transport[i]),
            "Utilities (₹)":         int(utilities[i]),
            "Dining Out (₹)":        int(dining[i]),
            "Entertainment (₹)":     int(entertain[i]),
            "Medical (₹)":           int(medical[i]),
            "Total Expenditure (₹)": int(total[i]),
        })

df = pd.DataFrame(rows)
df.to_csv("monthly_spending_dataset_2020_2025.csv", index=False)
print(f"✅  Dataset saved — {len(df):,} rows × {df.shape[1]} columns")
print(df.describe().to_string())
