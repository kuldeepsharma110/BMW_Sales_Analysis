# -*- coding: utf-8 -*-
"""
BMW Car Sales Volume Analysis — Streamlit App
"""

# ================== IMPORTS ==================
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import kagglehub
import warnings
warnings.filterwarnings("ignore")

def set_bg_from_local(image_file):
    import base64
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    css = f"""
    <style>
    /* ========== Background image ========== */
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

     [data-testid="stHeader"] {{
         background: rgba(0,0,0,0);
     }}

     [data-testid="stSidebar"] > div:first-child {{
         background: rgba(255, 255, 255, 0.85);
         color: black;
     }}

     /* ========== Main text color ========== */
     h1, h2, h3, h4, h5, h6, p, .stMarkdown, .stText, .stSubheader, .stTitle {{
         color: white !important;
     }}

     /* ========== TABLES / DATAFRAMES ========== */
     [data-testid="stDataFrame"] div {{
         background: rgba(255,255,255,0.2) !important;
         color: white !important;
         border-radius: 10px !important;
         border: 1px solid rgba(255,255,255,0.2) !important;
         font-size: 14px !important;
     }}

     [data-testid="stDataFrame"] th {{
         background-color: rgba(0, 0, 0, 0.8) !important;
         color: #ffffff !important;
         font-weight: bold !important;
     }}

     [data-testid="stDataFrame"] tr:hover td {{
         background-color: rgba(255,255,255,0.1) !important;
     }}

     /* ========== df.info() output (st.text) background fix ========== */
     [data-testid="stMarkdownContainer"] pre, 
     [data-testid="stCodeBlock"], 
     .stText pre {{
         background-color: white !important;
         color: black !important;
         border-radius: 8px;
         padding: 10px;
         font-family: monospace;
     }}
     </style>
     """
    st.markdown(css, unsafe_allow_html=True)



# ================== PAGE CONFIG ==================
st.set_page_config(page_title="BMW Car Sales EDA", layout="wide")
st.sidebar.success("Choose the service")


# 🌆 Add background image
#set_bg_from_local("images/bmw.jpg")
from PIL import Image
# Load an image from a file
image = Image.open('images/bmw.jpg')
# Display the image with a caption
st.image(image, caption='BMW', use_container_width=True)

st.title("🚗 BMW Worldwide Car Sales (2010–2024) — EDA Dashboard")
st.markdown("---")

# ================== DATA LOADING ==================
@st.cache_data
def load_data():
    dir_path = kagglehub.dataset_download("ahmadrazakashif/bmw-worldwide-sales-records-20102024")
    file = [f for f in os.listdir(dir_path) if f.endswith(".csv")][0]
    file_path = os.path.join(dir_path, file)
    df = pd.read_csv(file_path)
    return df

df = load_data()
st.write("Data Loaded Successfully!")

# ================== DATA OVERVIEW ==================
st.subheader("📊 Dataset Overview")
st.write("**Shape:**", df.shape)
st.dataframe(df.head())

import io

with st.expander("Show Summary Information"):
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    st.text(info_str)
    st.write(df.describe())


# ================== DATA VALIDATION ==================
st.subheader("🔍 Data Validation Checks")
st.write("**Duplicate Rows:**", df.duplicated().sum())

cat_column = [col for col in df.columns if df[col].dtype == 'object']
num_column = [col for col in df.columns if df[col].dtype != 'object']

st.write(f"Categorical Columns: {cat_column}")
st.write(f"Numerical Columns: {num_column}")

# ================== DISTRIBUTION CHECKS ==================
st.subheader("📈 Univariate Analysis")

tab1, tab2 = st.tabs(["Categorical", "Numerical"])

with tab1:
    col = st.selectbox("Select categorical column", cat_column)
    fig, ax = plt.subplots(figsize=(8,4))
    sns.countplot(x=df[col], ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

with tab2:
    num = st.selectbox("Select numerical column", num_column)
    fig, ax = plt.subplots(figsize=(8,4))
    sns.kdeplot(x=df[num], ax=ax)
    st.pyplot(fig)

# ================== REMOVE UNUSED COLUMN ==================
if "Mileage_KM" in df.columns:
    df = df.drop(columns=["Mileage_KM"])

# ================== BIVARIATE ANALYSIS ==================
st.subheader("📊 Model vs Sales Volume")

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(data=df, x="Model", y="Sales_Volume", estimator=sum, ci=None, ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# ================== YEARLY SALES TREND ==================
st.subheader("📆 Yearly Sales Trend")

fig, ax = plt.subplots(figsize=(10,5))
sns.lineplot(data=df, x="Year", y="Sales_Volume", estimator=sum, ci=None, ax=ax)
st.pyplot(fig)

# ================== REGION ANALYSIS ==================
st.subheader("🌍 Region-wise Sales Distribution")
df_region = df.groupby("Region").agg({"Sales_Volume": "sum"}).reset_index()

fig, ax = plt.subplots(figsize=(6,6))
ax.pie(df_region["Sales_Volume"], labels=df_region["Region"], autopct="%.2f")
st.pyplot(fig)

# ================== FILTER ASIA DATA ==================
st.subheader("📍 Focus Region: Asia")

asia_df = df[df["Region"] == "Asia"]
st.write("**Shape:**", asia_df.shape)
st.dataframe(asia_df.head())

# ================== i3 MODEL ANALYSIS ==================
st.subheader("🚘 BMW i3 Model Analysis (Asia)")
asia_i3_df = asia_df[asia_df["Model"] == "i3"]

fig, ax = plt.subplots(figsize=(10,5))
sns.lineplot(data=asia_i3_df, x="Year", y="Sales_Volume", ci=None, ax=ax)
st.pyplot(fig)

# ================== COLOR, TRANSMISSION, FUEL ==================
st.markdown("### Color-wise Trend")
fig, ax = plt.subplots(figsize=(10,5))
sns.lineplot(data=asia_i3_df, x="Year", y="Sales_Volume", hue="Color", ax=ax, ci=None)
st.pyplot(fig)

st.markdown("### Transmission-wise Trend")
fig, ax = plt.subplots(figsize=(10,5))
sns.lineplot(data=asia_i3_df, x="Year", y="Sales_Volume", hue="Transmission", ax=ax,ci=None)
st.pyplot(fig)

st.markdown("### Fuel Type-wise Trend")
fig, ax = plt.subplots(figsize=(10,5))
sns.lineplot(data=asia_i3_df, x="Year", y="Sales_Volume", hue="Fuel_Type", ax=ax,ci=None)
st.pyplot(fig)

# ================== ENGINE SIZE CATEGORY ==================
st.subheader("⚙️ Engine Size Categorization")

conditions = [
    asia_i3_df["Engine_Size_L"] < 1.5,
    (asia_i3_df["Engine_Size_L"] >= 1.5) & (asia_i3_df["Engine_Size_L"] <= 3),
    asia_i3_df["Engine_Size_L"] > 3
]
choices = ["small engine", "mid size engine", "big engine"]
asia_i3_df["engine_category"] = np.select(conditions, choices, default="unknown")

fig, ax = plt.subplots(figsize=(10,5))
sns.lineplot(data=asia_i3_df[asia_i3_df["Fuel_Type"] == "Hybrid"],
             x="Year", y="Sales_Volume", hue="engine_category", ax=ax,ci=None)
st.pyplot(fig)

# ================== CONCLUSION ==================
st.subheader("📋 Key Findings")
st.markdown("""
1. Sales Volume is approximately same across all regions.  
2. In Asia, **BMW i3** model has lowest sales.  
3. **Black** and **Grey** colors have highest sales in some years (2010, 2015, 2021).  
4. Manual transmission shows consistent sales, automatic shows fluctuations.  
5. **Petrol** variant sales are declining.  
6. **Hybrid (mid-size engine)** demand has risen after 2021.  
""")

st.success("""
💡 **Recommendation:**  
To boost sales of the BMW i3 model, BMW should focus on producing **Black or Grey cars**  
with **Manual transmission** and **Mid-size engines**, while avoiding **Petrol variants**.
""")



