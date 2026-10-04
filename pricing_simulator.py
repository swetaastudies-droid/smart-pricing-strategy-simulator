import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# BIZPILOT AI - SMART PRICING SIMULATOR
# ============================================================

# ------------------------------------------------------------
# 1. Load segmented customer data
# ------------------------------------------------------------

df = pd.read_csv("BizPilot_AI_Segmented_Customers.csv")

print("\n==========================================")
print("BIZPILOT AI PRICING SIMULATOR")
print("==========================================")

print("\nCustomer dataset loaded successfully!")
print("Total customers:", len(df))


# ------------------------------------------------------------
# 2. Basic startup assumptions
# ------------------------------------------------------------

# Number of customers considered in the simulation
initial_customers = len(df)

# Monthly fixed operating costs
fixed_cost = 150000

# Variable cost per retained customer
variable_cost_per_customer = 120

# Monthly marketing spend
marketing_cost = 50000


# ------------------------------------------------------------
# 3. Pricing scenarios
# ------------------------------------------------------------

price_points = [499, 699, 899, 1199, 1499]

results = []


# ------------------------------------------------------------
# 4. Simulate each price point
# ------------------------------------------------------------

for price in price_points:

    # Average churn probability from customer dataset
    average_churn = df["Churn_Probability"].mean()

    # Customers retained after churn
    retained_customers = initial_customers * (1 - average_churn)

    # Revenue
    revenue = price * retained_customers

    # Variable cost
    variable_cost = variable_cost_per_customer * retained_customers

    # Total costs
    total_cost = variable_cost + fixed_cost + marketing_cost

    # Contribution
    contribution = revenue - variable_cost

    # Contribution margin percentage
    contribution_margin = (
        contribution / revenue
    ) * 100

    # Estimated operating profit
    profit = revenue - total_cost

    # Profit margin
    profit_margin = (
        profit / revenue
    ) * 100

    # Break-even customers
    contribution_per_customer = (
        price - variable_cost_per_customer
    )

    break_even_customers = (
        (fixed_cost + marketing_cost)
        / contribution_per_customer
    )

    results.append({
        "Price": price,
        "Expected_Customers": round(retained_customers),
        "Churn_Rate_%": round(average_churn * 100, 2),
        "Revenue": round(revenue, 2),
        "Variable_Cost": round(variable_cost, 2),
        "Fixed_Cost": fixed_cost,
        "Marketing_Cost": marketing_cost,
        "Contribution": round(contribution, 2),
        "Contribution_Margin_%": round(contribution_margin, 2),
        "Profit": round(profit, 2),
        "Profit_Margin_%": round(profit_margin, 2),
        "Break_Even_Customers": round(
            break_even_customers
        )
    })


# ------------------------------------------------------------
# 5. Create results table
# ------------------------------------------------------------

results_df = pd.DataFrame(results)

print("\n==========================================")
print("PRICING SCENARIO RESULTS")
print("==========================================")

print(results_df.to_string(index=False))


# ------------------------------------------------------------
# 6. Save results
# ------------------------------------------------------------

results_df.to_csv(
    "BizPilot_AI_Pricing_Simulation.csv",
    index=False
)

print("\nPricing simulation saved as:")
print("BizPilot_AI_Pricing_Simulation.csv")


# ------------------------------------------------------------
# 7. Identify highest-profit scenario
# ------------------------------------------------------------

best_scenario = results_df.loc[
    results_df["Profit"].idxmax()
]

print("\n==========================================")
print("HIGHEST PROFIT SCENARIO")
print("==========================================")

print(
    "Price: ₹",
    best_scenario["Price"]
)

print(
    "Expected Customers:",
    best_scenario["Expected_Customers"]
)

print(
    "Revenue: ₹",
    best_scenario["Revenue"]
)

print(
    "Estimated Profit: ₹",
    best_scenario["Profit"]
)

print(
    "Contribution Margin:",
    best_scenario["Contribution_Margin_%"],
    "%"
)


# ------------------------------------------------------------
# 8. Price vs Revenue Chart
# ------------------------------------------------------------

plt.figure(figsize=(9, 5))

plt.plot(
    results_df["Price"],
    results_df["Revenue"],
    marker="o"
)

plt.title("BizPilot AI - Price vs Revenue")
plt.xlabel("Monthly Price (₹)")
plt.ylabel("Revenue (₹)")
plt.grid(True)

plt.tight_layout()

plt.savefig(
    "BizPilot_AI_Price_vs_Revenue.png",
    dpi=300
)

plt.show()


# ------------------------------------------------------------
# 9. Price vs Profit Chart
# ------------------------------------------------------------

plt.figure(figsize=(9, 5))

plt.plot(
    results_df["Price"],
    results_df["Profit"],
    marker="o"
)

plt.axhline(
    y=0,
    linestyle="--"
)

plt.title("BizPilot AI - Price vs Profit")
plt.xlabel("Monthly Price (₹)")
plt.ylabel("Estimated Profit (₹)")
plt.grid(True)

plt.tight_layout()

plt.savefig(
    "BizPilot_AI_Price_vs_Profit.png",
    dpi=300
)

plt.show()


print("\n==========================================")
print("SIMULATION COMPLETED SUCCESSFULLY!")
print("==========================================")