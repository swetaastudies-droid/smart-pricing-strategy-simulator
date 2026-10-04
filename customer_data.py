import pandas as pd
import numpy as np

# Reproducible results
np.random.seed(42)

# Generate 1,000 customers
df = pd.DataFrame({
    "Customer_ID": range(1, 1001),
    "Willingness_to_Pay": np.random.randint(499, 2000, 1000),
    "Churn_Probability": np.round(
        np.random.uniform(0.02, 0.25, 1000), 3
    )
})

# Convert churn probability into percentage
df["Churn_Rate_%"] = (
    df["Churn_Probability"] * 100
).round(1)

# Display first 10 records
print("\nFirst 10 Customers:")
print(df.head(10))

# Display summary
print("\nDataset Summary:")
print(df.describe())

# Save as CSV
df.to_csv("BizPilot_AI_Customer_Data.csv", index=False)

print("\nDataset created successfully!")
print("File saved as: BizPilot_AI_Customer_Data.csv")