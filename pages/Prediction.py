# pages/page_2.py
import streamlit as st
import pandas as pd
import numpy as np
import psycopg2


from bmw_car_sales_eda_app import asia_df

st.title("PREDICTION OF SALES FOR ASIA")
st.subheader("ASIA Dataset of Sales")
st.dataframe(asia_df)

model=st.text_input("Enter car model")
yr=st.number_input("Enter manufacturing Year")
color=st.text_input("Enter car color")
trans_type=st.text_input("Enter car transmission type")
#region=st.selectbox("Enter the region",asia_df["Region"].unique())
eng_size=st.number_input("Enter the engine size")
fuel_type=st.text_input("Enter car fuel type")

if st.button("💾 Save Record to Database"):
    # PostgreSQL connection setup
    conn = psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        database=st.secrets["postgres"]["dbname"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"],
        port=st.secrets["postgres"]["port"]
    )

    cursor = conn.cursor()

    # ✅ Create table if not exists
    create_table_query = """
    CREATE TABLE IF NOT EXISTS asia_sales_records (
        id SERIAL PRIMARY KEY,
        Model VARCHAR(50),
        Year INT,
        Color VARCHAR(30),
        Fuel_Type VARCHAR(30),
        Transmission VARCHAR(30),
        Engine_Size_L FLOAT
    );
    """
    cursor.execute(create_table_query)
    conn.commit()


    insert_query = """
    INSERT INTO asia_sales_records (Model, Year, Color, Fuel_Type, Transmission, Engine_Size_L)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    data_tuple = (model, yr, color, fuel_type, trans_type, eng_size)
    cursor.execute(insert_query, data_tuple)

    conn.commit()
    cursor.close()
    conn.close()

    st.success("✅ Record successfully inserted into PostgreSQL database!")