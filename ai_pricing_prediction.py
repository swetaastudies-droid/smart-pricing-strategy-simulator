import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# ============================================================
# BIZPILOT AI - AI/ML PRICING PREDICTION
# ============================================================

print("\n==========================================")
print("BIZPILOT AI - AI/ML PRICING PREDICTION")
print("==========================================")

# ------------------------------------------------------------
# STEP 1: Load segmented customer data
# ------------------------------------------------------------

df = pd.read_csv("BizPilot_AI_Segmented_Customers.csv")

print("\nCustomer data loaded successfully!")
print("Total customers:", len(df))


# ------------------------------------------------------------
# STEP 2: Create the target variable
# ------------------------------------------------------------

# Adjust willingness-to-pay based on churn probability.
#
# This is a simplified simulated value used for the ML model.
# It is NOT actual customer revenue.

df["Adjusted_Value"] = (
    df["Willingness_to_Pay"]
    * (1 - df["Churn_Probability"])
)


# ------------------------------------------------------------
# STEP 3: Define ML inputs and target
# ------------------------------------------------------------

X = df[
    [
        "Willingness_to_Pay",
        "Churn_Probability"
    ]
]

y = df["Adjusted_Value"]


# ------------------------------------------------------------
# STEP 4: Train Linear Regression model
# ------------------------------------------------------------

model = LinearRegression()

model.fit(X, y)


# ------------------------------------------------------------
# STEP 5: Check model performance
# ------------------------------------------------------------

predictions = model.predict(X)

r2 = r2_score(y, predictions)

print("\n==========================================")
print("LINEAR REGRESSION MODEL")
print("==========================================")

print("Intercept:", round(model.intercept_, 2))

print(
    "Willingness-to-Pay coefficient:",
    round(model.coef_[0], 4)
)

print(
    "Churn coefficient:",
    round(model.coef_[1], 4)
)

print(
    "R² Score:",
    round(r2, 4)
)


# ------------------------------------------------------------
# STEP 6: Predict adjusted value for every customer
# ------------------------------------------------------------

df["Predicted_Adjusted_Value"] = model.predict(X)

df["Predicted_Adjusted_Value"] = (
    df["Predicted_Adjusted_Value"].round(2)
)


# ------------------------------------------------------------
# STEP 7: Create candidate prices
# ------------------------------------------------------------

candidate_prices = np.array([
    499,
    699,
    899,
    1199,
    1499
])


# ------------------------------------------------------------
# STEP 8: Predict price recommendation for each segment
# ------------------------------------------------------------

segment_results = []

segments = [
    "Price-Sensitive Customers",
    "Value-Oriented Customers",
    "Premium Customers"
]

for segment in segments:

    segment_data = df[
        df["Customer_Segment"] == segment
    ]

    # Average customer characteristics
    avg_wtp = segment_data[
        "Willingness_to_Pay"
    ].mean()

    avg_churn = segment_data[
        "Churn_Probability"
    ].mean()

    # ML prediction for representative customer
    predicted_value = model.predict(
        [[avg_wtp, avg_churn]]
    )[0]

    # Keep predicted value within realistic pricing range
    predicted_value = max(
        candidate_prices.min(),
        min(
            predicted_value,
            candidate_prices.max()
        )
    )

    # Find nearest test price
    recommended_price = candidate_prices[
        np.abs(
            candidate_prices - predicted_value
        ).argmin()
    ]

    segment_results.append({
        "Customer_Segment": segment,
        "Customers": len(segment_data),
        "Average_Willingness_to_Pay":
            round(avg_wtp, 2),
        "Average_Churn_Probability":
            round(avg_churn, 3),
        "ML_Predicted_Value":
            round(predicted_value, 2),
        "Recommended_Price_to_Test":
            recommended_price
    })


# ------------------------------------------------------------
# STEP 9: Create segment recommendation table
# ------------------------------------------------------------

segment_results_df = pd.DataFrame(
    segment_results
)

print("\n==========================================")
print("AI/ML PRICING RECOMMENDATIONS")
print("==========================================")

print(
    segment_results_df.to_string(
        index=False
    )
)


# ------------------------------------------------------------
# STEP 10: Save customer predictions
# ------------------------------------------------------------

df.to_csv(
    "BizPilot_AI_ML_Customer_Predictions.csv",
    index=False
)


# ------------------------------------------------------------
# STEP 11: Save segment recommendations
# ------------------------------------------------------------

segment_results_df.to_csv(
    "BizPilot_AI_ML_Pricing_Recommendations.csv",
    index=False
)


# ------------------------------------------------------------
# STEP 12: Display final recommendation
# ------------------------------------------------------------

print("\n==========================================")
print("RECOMMENDED PRICES TO TEST")
print("==========================================")

for _, row in segment_results_df.iterrows():

    print(
        f"{row['Customer_Segment']}: "
        f"₹{row['Recommended_Price_to_Test']}"
    )


# ------------------------------------------------------------
# STEP 13: Explain the result
# ------------------------------------------------------------

print("\n==========================================")
print("IMPORTANT INTERPRETATION")
print("==========================================")

print(
    "The ML model provides a simulated pricing "
    "hypothesis based on willingness-to-pay "
    "and churn probability."
)

print(
    "The recommended prices should be tested "
    "with real customers before making a final "
    "pricing decision."
)

print("\nFiles created successfully:")
print("1. BizPilot_AI_ML_Customer_Predictions.csv")
print("2. BizPilot_AI_ML_Pricing_Recommendations.csv")