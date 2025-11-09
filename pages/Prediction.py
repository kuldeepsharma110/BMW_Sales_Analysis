# pages/page_2.py
import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import joblib

from bmw_car_sales_eda_app import df
#from bmw_car_sales_volume_analysis import model_loaded

st.title("PREDICTION OF SALES")
# st.subheader("ASIA Dataset of Sales")
# st.dataframe(asia_df)

model=st.selectbox("Enter car model",df["Model"].unique())
yr=st.selectbox("Enter manufacturing Year",df["Year"].unique())
color=st.selectbox("Enter car color",df["Color"].unique())
trans_type=st.selectbox("Enter car transmission type",df["Transmission"].unique())
region=st.selectbox("Enter the region",df["Region"].unique())
eng_size=st.number_input("Enter the engine size")
fuel_type=st.selectbox("Enter car fuel type",df["Fuel_Type"].unique())

if st.button("Predict Sales"):
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
        Engine_Size_L FLOAT,
        Region varchar(30)
    );
    """
    cursor.execute(create_table_query)
    conn.commit()

        # ✅ Create region coloum if not exists
    create_region_query = """
    ALTER TABLE asia_sales_records
    ADD COLUMN IF NOT EXISTS Region VARCHAR(30);
    """
    cursor.execute(create_region_query)
    conn.commit()





    insert_query = """
    INSERT INTO asia_sales_records (Model, Year, Color, Fuel_Type, Transmission, Engine_Size_L,Region)
    VALUES (%s, %s, %s, %s, %s, %s,%s)
    """

    data_tuple = (model, yr, color, fuel_type, trans_type, eng_size,region)
    cursor.execute(insert_query, data_tuple)

    conn.commit()
    cursor.close()
    conn.close()

    st.write("✅ Record successfully inserted database!")

    # Load the model
    model_loaded = joblib.load("model.pkl")

    sales_prediction=model_loaded.predict(pd.DataFrame({"Model":[model], "Year":[yr], 
                                                        "Color":[color], "Fuel_Type":[fuel_type], 
                                                        "Transmission":[trans_type],
                                                          "Engine_Size_L":[eng_size],"Region":[region]}))
    
    st.success(f"The Prediction for sales is {sales_prediction}")

