import pandas as pd
import numpy as np

# ============================================================
# BIZPILOT AI - STEP 7
# TESTING & IMPROVEMENT
# ============================================================

print("\n==========================================")
print("BIZPILOT AI - TESTING & IMPROVEMENT")
print("==========================================")

# ------------------------------------------------------------
# 1. Load customer data
# ------------------------------------------------------------

df = pd.read_csv(
    "BizPilot_AI_Segmented_Customers.csv"
)

print("\nCustomer dataset loaded:", len(df))


# ------------------------------------------------------------
# 2. Core assumptions
# ------------------------------------------------------------

fixed_cost = 150000
marketing_spend = 50000
variable_cost = 120

customers = 1000

# Candidate prices
prices = [
    499,
    699,
    899,
    1199,
    1499
]


# ------------------------------------------------------------
# 3. Simulated demand assumptions
# ------------------------------------------------------------

demand_factor = {
    499: 1.15,
    699: 1.00,
    899: 0.85,
    1199: 0.70,
    1499: 0.55
}


# ------------------------------------------------------------
# 4. Calculate pricing scenarios
# ------------------------------------------------------------

results = []

for price in prices:

    expected_customers = (
        customers
        * demand_factor[price]
    )

    avg_churn = (
        df["Churn_Probability"].mean()
    )

    retained_customers = (
        expected_customers
        * (1 - avg_churn)
    )

    revenue = (
        price
        * retained_customers
    )

    variable_cost_total = (
        variable_cost
        * retained_customers
    )

    contribution = (
        revenue
        - variable_cost_total
    )

    total_cost = (
        variable_cost_total
        + fixed_cost
        + marketing_spend
    )

    profit = (
        revenue
        - total_cost
    )

    contribution_margin = (
        contribution / revenue * 100
        if revenue > 0 else 0
    )

    # --------------------------------------------------------
    # CAC
    # --------------------------------------------------------

    cac = (
        marketing_spend
        / expected_customers
    )

    # --------------------------------------------------------
    # Monthly contribution per customer
    # --------------------------------------------------------

    contribution_per_customer = (
        price - variable_cost
    )

    # --------------------------------------------------------
    # Simplified customer lifetime
    # --------------------------------------------------------

    monthly_churn = avg_churn

    if monthly_churn > 0:
        customer_lifetime = (
            1 / monthly_churn
        )
    else:
        customer_lifetime = np.inf

    # --------------------------------------------------------
    # LTV
    # --------------------------------------------------------

    ltv = (
        contribution_per_customer
        * customer_lifetime
    )

    # --------------------------------------------------------
    # LTV:CAC
    # --------------------------------------------------------

    if cac > 0:
        ltv_cac = ltv / cac
    else:
        ltv_cac = np.inf

    # --------------------------------------------------------
    # CAC Payback
    # --------------------------------------------------------

    if contribution_per_customer > 0:

        cac_payback = (
            cac
            / contribution_per_customer
        )

    else:

        cac_payback = np.inf

    results.append({

        "Price": price,

        "Expected_Customers":
            round(expected_customers),

        "Retained_Customers":
            round(retained_customers),

        "Revenue":
            round(revenue),

        "Variable_Cost":
            round(variable_cost_total),

        "Contribution":
            round(contribution),

        "Contribution_Margin_%":
            round(contribution_margin, 2),

        "Marketing_Spend":
            marketing_spend,

        "CAC":
            round(cac, 2),

        "Customer_Lifetime_Months":
            round(customer_lifetime, 2),

        "LTV":
            round(ltv, 2),

        "LTV_CAC":
            round(ltv_cac, 2),

        "CAC_Payback_Months":
            round(cac_payback, 2),

        "Estimated_Profit":
            round(profit)

    })


# ------------------------------------------------------------
# 5. Create testing table
# ------------------------------------------------------------

testing_df = pd.DataFrame(results)

print("\n==========================================")
print("PRICING TEST RESULTS")
print("==========================================")

print(
    testing_df.to_string(index=False)
)


# ------------------------------------------------------------
# 6. Find best scenario
# ------------------------------------------------------------

best_profit = testing_df.loc[
    testing_df["Estimated_Profit"].idxmax()
]

best_ltv = testing_df.loc[
    testing_df["LTV_CAC"].idxmax()
]


print("\n==========================================")
print("BEST PROFIT SCENARIO")
print("==========================================")

print(
    "Price to test: ₹",
    best_profit["Price"]
)

print(
    "Estimated profit: ₹",
    best_profit["Estimated_Profit"]
)

print(
    "LTV:CAC:",
    best_profit["LTV_CAC"]
)


print("\n==========================================")
print("BEST LTV:CAC SCENARIO")
print("==========================================")

print(
    "Price to test: ₹",
    best_ltv["Price"]
)

print(
    "LTV:",
    best_ltv["LTV"]
)

print(
    "CAC:",
    best_ltv["CAC"]
)

print(
    "LTV:CAC:",
    best_ltv["LTV_CAC"]
)


# ------------------------------------------------------------
# 7. Real-world SaaS pricing benchmarks
# ------------------------------------------------------------

competitors = pd.DataFrame({

    "Reference_Product": [
        "Freshsales Growth",
        "Zoho CRM Standard",
        "Power BI Pro",
        "Zoho Analytics"
    ],

    "Pricing_Model": [
        "Per user/month",
        "Per user/month",
        "Per user/month",
        "Subscription"
    ],

    "Reference_Price_INR": [
        np.nan,
        800,
        1165,
        1200
    ],

    "Source_Status": [
        "Official pricing; USD price",
        "Official India pricing",
        "Official India pricing",
        "Official Zoho documentation"
    ],

    "Use_in_Project": [
        "Reference benchmark",
        "Reference benchmark",
        "Reference benchmark",
        "Reference benchmark"
    ]
})


# ------------------------------------------------------------
# 8. Save competitor benchmark
# ------------------------------------------------------------

competitors.to_csv(
    "BizPilot_AI_Competitor_Benchmark.csv",
    index=False
)


# ------------------------------------------------------------
# 9. Save complete testing report
# ------------------------------------------------------------

testing_df.to_csv(
    "BizPilot_AI_Testing_Report.csv",
    index=False
)


# ------------------------------------------------------------
# 10. Testing conclusions
# ------------------------------------------------------------

print("\n==========================================")
print("TESTING CONCLUSIONS")
print("==========================================")

print("""
1. Multiple price points were tested.

2. Customer demand was varied according to
   explicit simulation assumptions.

3. Churn was incorporated into retained
   customer calculations.

4. Marketing spend was incorporated into CAC.

5. LTV was calculated using contribution margin.

6. LTV:CAC was calculated to evaluate
   customer acquisition economics.

7. Real SaaS pricing references were added
   separately from simulated BizPilot AI data.

8. The results represent pricing hypotheses,
   not actual market validation.
""")


print("\nFiles created:")
print("1. BizPilot_AI_Testing_Report.csv")
print("2. BizPilot_AI_Competitor_Benchmark.csv")

print("\nSTEP 7 TESTING COMPLETED!")