import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(
    page_title="Passive Income Simulator",
    page_icon="💰",
    layout="wide"
)

# Custom CSS for aesthetics (optional but good for "Modern" feel)
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --------------------
# 1. Sidebar - Configuration
# --------------------
st.sidebar.header("⚙️ Configuration (參數設定)")

# Inputs
total_principal = st.sidebar.number_input(
    "目前總本金 (Total Principal)",
    min_value=0,
    value=1000000,
    step=10000,
    format="%d"
)

avg_yield = st.sidebar.number_input(
    "平均年化殖利率 (Average Yield %)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.1,
    format="%.2f"
)

target_monthly_income = st.sidebar.number_input(
    "目標月被動收入 (Target Monthly Income)",
    min_value=0,
    value=50000,
    step=1000,
    format="%d"
)

st.sidebar.markdown("---")
st.sidebar.subheader("🚀 Special Assets (特殊資產)")

# Special Asset Logic
enable_medical_reservoir = st.sidebar.checkbox("啟用 150w 醫療險大水庫 🏥")
simulate_compensation = st.sidebar.checkbox("模擬投入 300w 賠償金 ⚖️")

# --------------------
# 2. Logic Implementation
# --------------------

# Base Capital Calculation
effective_capital = total_principal
if simulate_compensation:
    effective_capital += 3000000

# Monthly Income Calculation
# Part A: From Capital Yield
yield_income_monthly = (effective_capital * (avg_yield / 100)) / 12

# Part B: Fixed Income (Medical Reservoir)
medical_income_monthly = 0
if enable_medical_reservoir:
    # Logic: "Enable 150w Medical Insurance Reservoir" -> Fixed 10k income (as per req, maybe this 150w is separate from principal or just yields 10k?)
    # Requirement: "untick: fixed add 150w principal... set estimated monthly dividend (e.g. 10,000)"
    # A bit ambiguous if 150w is added to principal AND yields 10k separate, or 150w just gives 10k.
    # Requirement says: "untick... fixed add 150w principal, and set its estimated monthly dividend (e.g., 10,000)."
    # Interpreting as: 150w is a separate bucket that provides fixed 10k/month.
    # If it was added to "effective_capital", it would use "avg_yield". Since it has a specific 10k return, I'll treat it as fixed income.
    medical_income_monthly = 10000

# Total Passive Income
current_monthly_income = yield_income_monthly + medical_income_monthly
gap = target_monthly_income - current_monthly_income

# Progress Calculation
progress = current_monthly_income / target_monthly_income if target_monthly_income > 0 else 0
progress_clamped = min(max(progress, 0.0), 1.0) # Clamp between 0 and 1 for progress bar

# --------------------
# 3. Main Dashboard
# --------------------
st.title("💸 Passive Income Command Center")
st.markdown(f"**Goal:** Reach **${target_monthly_income:,.0f}** / month")

# Metrics Row
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="📊 Current Monthly Income", value=f"${current_monthly_income:,.0f}")

with col2:
    st.metric(label="🎯 Target Gap", value=f"${gap:,.0f}", delta=f"-{gap:,.0f}" if gap > 0 else "Goal Reached!", delta_color="inverse")

with col3:
    st.metric(label="💰 Effective Capital", value=f"${effective_capital + (1500000 if enable_medical_reservoir else 0):,.0f}") 
    # Note: Adding 150w to display for total wealth view, even if yield is calculated differently.

st.markdown("---")

# Progress Bar
st.subheader("🚀 Progress Tracker")
st.write(f"Current Achievement: **{progress*100:.1f}%**")

# Color Logic for text (Progress bar color in Streamlit is standard, but we can hack it or just use standard)
# Native st.progress doesn't support color change dynamically based on value easily without custom HTML, 
# but we requested "Native Streamlit Components". 
# So we stick to standard st.progress but maybe add an emoji indicator.

bar_color = "red"
if progress >= 1.0:
    bar_color_emoji = "🟢 Perfect!"
elif progress >= 0.5:
    bar_color_emoji = "🟡 Good Start!"
else:
    bar_color_emoji = "🔴 Keep Going!"

st.progress(progress_clamped)
st.caption(f"Status: {bar_color_emoji}")

# Chart
st.markdown("---")
st.subheader("📈 Visual Comparison")

chart_data = pd.DataFrame({
    'Category': ['Current Income', 'Target Income'],
    'Amount': [current_monthly_income, target_monthly_income]
})

# Simple Bar Chart
st.bar_chart(chart_data.set_index('Category'))

# Footer / Debug info
with st.expander("ℹ️ Simulation Details"):
    st.write("Calculation Breakdown:")
    st.write(f"- Yield Income: ${yield_income_monthly:,.2f} (from ${effective_capital:,.0f} @ {avg_yield}%)")
    st.write(f"- Fixed/Medical Income: ${medical_income_monthly:,.2f}")
    if simulate_compensation:
        st.info("✅ Simulating 300w compensation injection.")
    if enable_medical_reservoir:
        st.info("✅ 150w Medical Reservoir active (Fixed $10k/mo).")

