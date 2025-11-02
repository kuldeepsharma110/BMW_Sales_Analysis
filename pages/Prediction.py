# pages/page_2.py
import streamlit as st
import pandas as pd
import numpy as np


from bmw_car_sales_eda_app import asia_df

st.title("PREDICTION OF SALES FOR ASIA")
st.subheader("ASIA Dataset of Sales")
st.dataframe(asia_df)