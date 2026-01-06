import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(
    page_title="被動收入模擬器",
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
st.sidebar.header("⚙️ 參數設定")

# Inputs
total_principal = st.sidebar.number_input(
    "目前總本金 (TWD)",
    min_value=0,
    value=1000000,
    step=10000,
    format="%d"
)

avg_yield = st.sidebar.number_input(
    "平均年化殖利率 (%)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.1,
    format="%.2f"
)

target_monthly_income = st.sidebar.number_input(
    "目標月被動收入 (TWD)",
    min_value=0,
    value=50000,
    step=1000,
    format="%d"
)

st.sidebar.markdown("---")
st.sidebar.subheader("🚀 特殊資產設定")

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
st.title("💸 被動收入戰情室")
st.markdown(f"**目標:** 達成每月 **${target_monthly_income:,.0f}** 被動收入")

# Metrics Row
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="📊 目前月被動收入", value=f"${current_monthly_income:,.0f}")

with col2:
    st.metric(label="🎯 距離目標差距", value=f"${gap:,.0f}", delta=f"-{gap:,.0f}" if gap > 0 else "目標達成！", delta_color="inverse")

with col3:
    st.metric(label="💰 有效總資產", value=f"${effective_capital + (1500000 if enable_medical_reservoir else 0):,.0f}") 
    # Note: Adding 150w to display for total wealth view

st.markdown("---")

# Progress Bar
st.subheader("🚀 進度追蹤")
st.write(f"目前達成率: **{progress*100:.1f}%**")

# Color Logic for text
bar_color_emoji = "🔴 繼續加油！"
if progress >= 1.0:
    bar_color_emoji = "🟢 太棒了！目標達成！"
elif progress >= 0.5:
    bar_color_emoji = "🟡 好的開始！已經過半了！"

st.progress(progress_clamped)
st.caption(f"狀態: {bar_color_emoji}")

# Chart
st.markdown("---")
st.subheader("📈 視覺化比較")

chart_data = pd.DataFrame({
    '類別': ['目前收入', '目標收入'],
    '金額': [current_monthly_income, target_monthly_income]
})

# Simple Bar Chart
st.bar_chart(chart_data.set_index('類別'))

# Footer / Debug info
with st.expander("ℹ️ 模擬詳情"):
    st.write("計算細節:")
    st.write(f"- 殖利率收入: ${yield_income_monthly:,.0f} (來自 ${effective_capital:,.0f} @ {avg_yield}%)")
    st.write(f"- 醫療險/固定配息: ${medical_income_monthly:,.0f}")
    if simulate_compensation:
        st.info("✅ 已模擬投入 300w 賠償金。")
    if enable_medical_reservoir:
        st.info("✅ 已啟用 150w 醫療險大水庫 (固定月收 $10k)。")
