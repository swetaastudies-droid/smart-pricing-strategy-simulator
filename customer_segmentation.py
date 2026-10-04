import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ---------------------------------------------------
# STEP 1: Load the customer dataset
# ---------------------------------------------------

df = pd.read_csv("BizPilot_AI_Customer_Data.csv")

print("\nCustomer data loaded successfully!")
print("Number of customers:", len(df))

# ---------------------------------------------------
# STEP 2: Select variables for segmentation
# ---------------------------------------------------

X = df[[
    "Willingness_to_Pay",
    "Churn_Probability"
]]

# ---------------------------------------------------
# STEP 3: Standardize the variables
# ---------------------------------------------------

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ---------------------------------------------------
# STEP 4: Create 3 customer clusters
# ---------------------------------------------------

kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

df["Cluster"] = kmeans.fit_predict(X_scaled)

# ---------------------------------------------------
# STEP 5: Create meaningful segment names
# ---------------------------------------------------

cluster_summary = df.groupby("Cluster").agg(
    Average_Willingness_to_Pay=("Willingness_to_Pay", "mean"),
    Average_Churn_Probability=("Churn_Probability", "mean"),
    Customer_Count=("Customer_ID", "count")
).reset_index()

# Identify clusters based on willingness-to-pay
sorted_clusters = cluster_summary.sort_values(
    "Average_Willingness_to_Pay"
)["Cluster"].tolist()

segment_names = {
    sorted_clusters[0]: "Price-Sensitive Customers",
    sorted_clusters[1]: "Value-Oriented Customers",
    sorted_clusters[2]: "Premium Customers"
}

df["Customer_Segment"] = df["Cluster"].map(segment_names)

# ---------------------------------------------------
# STEP 6: Display segment summary
# ---------------------------------------------------

final_summary = df.groupby("Customer_Segment").agg(
    Customers=("Customer_ID", "count"),
    Average_Willingness_to_Pay=("Willingness_to_Pay", "mean"),
    Average_Churn_Probability=("Churn_Probability", "mean")
).reset_index()

final_summary["Average_Willingness_to_Pay"] = (
    final_summary["Average_Willingness_to_Pay"].round(2)
)

final_summary["Average_Churn_Probability"] = (
    final_summary["Average_Churn_Probability"].round(3)
)

print("\n==========================================")
print("CUSTOMER SEGMENTATION SUMMARY")
print("==========================================")

print(final_summary.to_string(index=False))

# ---------------------------------------------------
# STEP 7: Save segmented dataset
# ---------------------------------------------------

df.to_csv(
    "BizPilot_AI_Segmented_Customers.csv",
    index=False
)

# Save summary separately
final_summary.to_csv(
    "BizPilot_AI_Segment_Summary.csv",
    index=False
)

print("\n==========================================")
print("Files created successfully!")
print("==========================================")
print("1. BizPilot_AI_Segmented_Customers.csv")
print("2. BizPilot_AI_Segment_Summary.csv")

# ---------------------------------------------------
# STEP 8: Create visualization
# ---------------------------------------------------

plt.figure(figsize=(10, 6))

for segment in df["Customer_Segment"].unique():

    segment_data = df[
        df["Customer_Segment"] == segment
    ]

    plt.scatter(
        segment_data["Willingness_to_Pay"],
        segment_data["Churn_Probability"],
        label=segment,
        alpha=0.6
    )

plt.xlabel("Willingness to Pay (₹)")
plt.ylabel("Churn Probability")
plt.title("BizPilot AI - Customer Segmentation")
plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig(
    "BizPilot_AI_Customer_Segmentation.png",
    dpi=300
)

plt.show()

print("\nSegmentation chart saved as:")
print("BizPilot_AI_Customer_Segmentation.png")