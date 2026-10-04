import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ============================================================
# BIZPILOT AI - SMART PRICING STRATEGY SIMULATOR
# ============================================================

st.set_page_config(
    page_title="BizPilot AI Pricing Simulator",
    page_icon="💰",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_customer_data():

    try:
        df = pd.read_csv(
            "BizPilot_AI_Segmented_Customers.csv"
        )
        return df

    except FileNotFoundError:
        return None


@st.cache_data
def load_ml_recommendations():

    try:
        df = pd.read_csv(
            "BizPilot_AI_ML_Pricing_Recommendations.csv"
        )
        return df

    except FileNotFoundError:
        return None


customer_df = load_customer_data()
ml_df = load_ml_recommendations()


# ============================================================
# HEADER
# ============================================================

st.title("💰 BizPilot AI")
st.subheader("Smart Pricing Strategy Simulator")

st.write(
    """
    An interactive pricing simulator that helps startups
    understand how pricing assumptions can affect customer
    retention, revenue, contribution margin, profitability
    and break-even.
    """
)

st.info(
    "All customer and financial figures used in this simulator "
    "are simulation assumptions unless separately validated "
    "with real-world data."
)


# ============================================================
# SIDEBAR INPUTS
# ============================================================

st.sidebar.header("⚙️ Pricing Inputs")

# Customer segment

segments = [
    "All Customers",
    "Price-Sensitive Customers",
    "Value-Oriented Customers",
    "Premium Customers"
]

selected_segment = st.sidebar.selectbox(
    "Customer Segment",
    segments
)


# Default values

default_price = 699
default_customers = 1000
default_churn = 10.0
default_variable_cost = 120
default_fixed_cost = 150000
default_marketing = 50000
default_discount = 0.0


# Price

price = st.sidebar.slider(
    "Monthly Price (₹)",
    min_value=299,
    max_value=1999,
    value=default_price,
    step=50
)


# Customers

customers = st.sidebar.slider(
    "Expected Customers",
    min_value=100,
    max_value=3000,
    value=default_customers,
    step=50
)


# Churn

churn_rate = st.sidebar.slider(
    "Monthly Churn Rate (%)",
    min_value=0.0,
    max_value=30.0,
    value=default_churn,
    step=0.5
)


# Variable cost

variable_cost_per_customer = st.number_input(
    "Variable Cost / Customer (₹)",
    min_value=0.0,
    max_value=1000.0,
    value=float(default_variable_cost),
    step=10.0
)


# Fixed cost

fixed_cost = st.number_input(
    "Monthly Fixed Cost (₹)",
    min_value=0.0,
    max_value=1000000.0,
    value=float(default_fixed_cost),
    step=10000.0
)


# Marketing

marketing_cost = st.number_input(
    "Monthly Marketing Cost (₹)",
    min_value=0.0,
    max_value=1000000.0,
    value=float(default_marketing),
    step=5000.0
)


# Discount

discount = st.slider(
    "Discount (%)",
    min_value=0.0,
    max_value=30.0,
    value=default_discount,
    step=1.0
)


# ============================================================
# CUSTOMER SEGMENT LOGIC
# ============================================================

if customer_df is not None:

    if selected_segment == "All Customers":

        segment_data = customer_df

    else:

        segment_data = customer_df[
            customer_df["Customer_Segment"]
            == selected_segment
        ]

    if len(segment_data) > 0:

        data_churn = (
            segment_data["Churn_Probability"].mean()
            * 100
        )

        avg_wtp = (
            segment_data["Willingness_to_Pay"].mean()
        )

    else:

        data_churn = churn_rate
        avg_wtp = price

else:

    data_churn = churn_rate
    avg_wtp = price


# Use manually selected churn rate
# This allows the founder to perform what-if analysis.

effective_price = price * (
    1 - discount / 100
)

retained_customers = customers * (
    1 - churn_rate / 100
)


# ============================================================
# FINANCIAL CALCULATIONS
# ============================================================

revenue = (
    effective_price
    * retained_customers
)

variable_cost = (
    variable_cost_per_customer
    * retained_customers
)

contribution = (
    revenue - variable_cost
)

contribution_margin = (
    contribution / revenue * 100
    if revenue > 0
    else 0
)

total_cost = (
    variable_cost
    + fixed_cost
    + marketing_cost
)

profit = (
    revenue - total_cost
)

profit_margin = (
    profit / revenue * 100
    if revenue > 0
    else 0
)

contribution_per_customer = (
    effective_price
    - variable_cost_per_customer
)

if contribution_per_customer > 0:

    break_even_customers = (
        fixed_cost + marketing_cost
    ) / contribution_per_customer

else:

    break_even_customers = np.inf


# ============================================================
# KPI CARDS
# ============================================================

st.markdown("## 📊 Current Pricing Scenario")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Effective Price",
    f"₹{effective_price:,.0f}"
)

col2.metric(
    "Retained Customers",
    f"{retained_customers:,.0f}"
)

col3.metric(
    "Revenue",
    f"₹{revenue:,.0f}"
)

col4.metric(
    "Estimated Profit",
    f"₹{profit:,.0f}"
)


col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "Contribution",
    f"₹{contribution:,.0f}"
)

col6.metric(
    "Contribution Margin",
    f"{contribution_margin:.1f}%"
)

col7.metric(
    "Break-Even Customers",
    (
        f"{break_even_customers:,.0f}"
        if np.isfinite(break_even_customers)
        else "N/A"
    )
)

col8.metric(
    "Profit Margin",
    f"{profit_margin:.1f}%"
)


# ============================================================
# AI / ML RECOMMENDATION
# ============================================================

st.markdown("## 🤖 AI/ML Pricing Recommendation")

if ml_df is not None:

    if selected_segment != "All Customers":

        recommendation = ml_df[
            ml_df["Customer_Segment"]
            == selected_segment
        ]

        if len(recommendation) > 0:

            recommended_price = int(
                recommendation.iloc[0][
                    "Recommended_Price_to_Test"
                ]
            )

            predicted_value = float(
                recommendation.iloc[0][
                    "ML_Predicted_Value"
                ]
            )

            st.success(
                f"Recommended price to test for "
                f"**{selected_segment}: ₹{recommended_price:,}**"
            )

            st.write(
                f"ML predicted adjusted customer value: "
                f"**₹{predicted_value:,.2f}**"
            )

    else:

        st.info(
            "Select a specific customer segment to view "
            "the segment-level ML pricing recommendation."
        )

else:

    st.warning(
        "ML recommendation file was not found. "
        "Run ai_pricing_prediction.py first."
    )


# ============================================================
# PRICE SCENARIO SIMULATION
# ============================================================

st.markdown("## 📈 Price Scenario Analysis")

scenario_prices = [
    499,
    699,
    899,
    1199,
    1499
]

scenario_results = []

for scenario_price in scenario_prices:

    # Simple demand assumption for simulation
    if scenario_price <= 499:
        demand_factor = 1.15

    elif scenario_price <= 699:
        demand_factor = 1.00

    elif scenario_price <= 899:
        demand_factor = 0.85

    elif scenario_price <= 1199:
        demand_factor = 0.70

    else:
        demand_factor = 0.55

    scenario_customers = (
        customers * demand_factor
    )

    scenario_retained = (
        scenario_customers
        * (1 - churn_rate / 100)
    )

    scenario_revenue = (
        scenario_price
        * scenario_retained
    )

    scenario_variable_cost = (
        variable_cost_per_customer
        * scenario_retained
    )

    scenario_profit = (
        scenario_revenue
        - scenario_variable_cost
        - fixed_cost
        - marketing_cost
    )

    scenario_results.append({
        "Price": scenario_price,
        "Expected Customers":
            round(scenario_customers),
        "Retained Customers":
            round(scenario_retained),
        "Revenue":
            round(scenario_revenue),
        "Profit":
            round(scenario_profit)
    })


scenario_df = pd.DataFrame(
    scenario_results
)


# ============================================================
# DISPLAY SCENARIO TABLE
# ============================================================

st.dataframe(
    scenario_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# REVENUE CHART
# ============================================================

st.markdown("### Price vs Revenue")

fig_revenue = go.Figure()

fig_revenue.add_trace(
    go.Scatter(
        x=scenario_df["Price"],
        y=scenario_df["Revenue"],
        mode="lines+markers",
        name="Revenue"
    )
)

fig_revenue.update_layout(
    xaxis_title="Monthly Price (₹)",
    yaxis_title="Revenue (₹)",
    template="plotly_white"
)

st.plotly_chart(
    fig_revenue,
    use_container_width=True
)


# ============================================================
# PROFIT CHART
# ============================================================

st.markdown("### Price vs Profit")

fig_profit = go.Figure()

fig_profit.add_trace(
    go.Scatter(
        x=scenario_df["Price"],
        y=scenario_df["Profit"],
        mode="lines+markers",
        name="Profit"
    )
)

fig_profit.add_hline(
    y=0,
    line_dash="dash"
)

fig_profit.update_layout(
    xaxis_title="Monthly Price (₹)",
    yaxis_title="Estimated Profit (₹)",
    template="plotly_white"
)

st.plotly_chart(
    fig_profit,
    use_container_width=True
)


# ============================================================
# SEGMENT INFORMATION
# ============================================================

st.markdown("## 👥 Customer Segment Information")

if customer_df is not None:

    segment_summary = (
        customer_df
        .groupby("Customer_Segment")
        .agg(
            Customers=(
                "Customer_ID",
                "count"
            ),
            Average_WTP=(
                "Willingness_to_Pay",
                "mean"
            ),
            Average_Churn=(
                "Churn_Probability",
                "mean"
            )
        )
        .reset_index()
    )

    segment_summary[
        "Average_WTP"
    ] = segment_summary[
        "Average_WTP"
    ].round(2)

    segment_summary[
        "Average_Churn"
    ] = (
        segment_summary[
            "Average_Churn"
        ] * 100
    ).round(2)

    st.dataframe(
        segment_summary,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# BUSINESS INTERPRETATION
# ============================================================

st.markdown("## 💡 Business Interpretation")

if profit > 0:

    st.success(
        f"The current scenario generates an estimated "
        f"operating profit of ₹{profit:,.0f}."
    )

else:

    st.error(
        f"The current scenario generates an estimated "
        f"operating loss of ₹{abs(profit):,.0f}."
    )

if np.isfinite(break_even_customers):

    st.write(
        f"The startup needs approximately "
        f"**{break_even_customers:,.0f} retained customers** "
        f"to cover fixed and marketing costs under the "
        f"current assumptions."
    )

st.caption(
    "This dashboard is a management simulation. "
    "Pricing recommendations should be validated with "
    "real customer behaviour, actual costs and pricing experiments."
)