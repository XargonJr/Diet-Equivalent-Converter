import json
import streamlit as st

@st.cache_data
def load_database():
    with open("foods.json", "r", encoding="utf-8") as f:
        return json.load(f)

FOOD_DATA = load_database()

# Helper function to extract numerical weight safely
def get_weight_value(item):
    if isinstance(item, (int, float)):
        return float(item)
    elif isinstance(item, dict):
        # Extract the value if it's stored inside a nested key
        for key in ["equivalent", "weight", "value", "g", "grammi"]:
            if key in item:
                return float(item[key])
        # Fallback to the first numeric value found in the dict
        for v in item.values():
            if isinstance(v, (int, float)):
                return float(v)
    raise ValueError(f"Could not extract numerical value from: {item}")

st.title("Diet Equivalent Converter")

# Category selection
category = st.selectbox("Select Category", list(FOOD_DATA.keys()))

# Subcategory selection
subcategories = list(FOOD_DATA[category].keys())
subcategory = st.selectbox("Select Subcategory", subcategories)

foods = FOOD_DATA[category][subcategory]

st.divider()

col1, col2 = st.columns(2)

with col1:
    prescribed_food = st.selectbox("Prescribed Food", list(foods.keys()), index=0)
    prescribed_qty = st.number_input("Prescribed Amount (g)", min_value=1.0, value=100.0)

with col2:
    default_target_idx = 1 if len(foods) > 1 else 0
    target_food = st.selectbox("Target Replacement Food", list(foods.keys()), index=default_target_idx)

# Extract numbers safely using the helper function
prescribed_equiv = get_weight_value(foods[prescribed_food])
target_equiv = get_weight_value(foods[target_food])

# Calculation
result = (prescribed_qty * target_equiv) / prescribed_equiv

st.divider()
st.success(f"**Conversion Result:** Replace **{prescribed_qty}g** of *{prescribed_food}* with **{result:.1f}g** of *{target_food}*.")