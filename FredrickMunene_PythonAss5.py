"""
Program: FredrickMunene_PythonAss5.py
Author: Fredrick Munene
Course: BUIS 305 / INSS 405
Assignment 5 – Streamlit Sales Analytics Dashboard
Date: 11/25/2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("Sales Analytics Dashboard — Juices vs Smoothies")
st.caption("BUIS 305 / INSS 405 — Assignment 5")

st.write("Upload the juice sales dataset to begin.")

# File uploader
uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

# Correct load_data function (ONLY ONE!)
def load_data(file):
    """Load CSV or Excel file into DataFrame safely."""
    try:
        return pd.read_excel(file, engine="openpyxl")
    except:
        file.seek(0)
        return pd.read_csv(file)

# Load dataset
df = None
if uploaded_file is not None:
    df = load_data(uploaded_file)

# Stop program if no file uploaded
if df is None:
    st.stop()

st.success("File uploaded successfully.")
# Dataset preview
with st.expander("Preview Dataset"):
    st.write("First 5 Rows")
    st.dataframe(df.head())
    st.write("Last 5 Rows")
    st.dataframe(df.tail())

# Function to detect the sales column
def get_sales_column(df):
    for col in df.columns:
        if "sales" in col.lower() or "$" in col.lower():
            return col
    return None

sales_col = get_sales_column(df)

# Create tabs for each question
tab1, tab2, tab3 = st.tabs(["Category Sales", "Sales Over Time", "Satisfaction Ratings"])

# Question 1: Category Sales Comparison
with tab1:
    st.header("Question 1: Sales Comparison — Juices vs Smoothies")

    if "Category" not in df.columns:
        st.error("Missing required column: Category")
    elif sales_col is None:
        st.error("No sales column found. Expected something like 'Sales' or '$ Sales'.")
    else:
        category_sales = df.groupby("Category")[sales_col].sum()

        fig, ax = plt.subplots()
        ax.bar(category_sales.index, category_sales.values)
        ax.set_title("Total Sales by Category")
        ax.set_xlabel("Category")
        ax.set_ylabel("Total Sales ($)")
        st.pyplot(fig)

        top_category = category_sales.idxmax()
        st.write(f"Interpretation: {top_category} generated the highest total sales.")

# Question 2: Sales Trend Over Time
with tab2:
    st.header("Question 2: Sales Over Time")

    if "Date Ordered" not in df.columns:
        st.error("Missing required column: Date Ordered")
    else:
        df["Date Ordered"] = pd.to_datetime(df["Date Ordered"], errors="coerce")
        daily_sales = df.groupby("Date Ordered")[sales_col].sum().sort_index()

        fig2, ax2 = plt.subplots()
        ax2.plot(daily_sales.index, daily_sales.values)
        ax2.set_title("Daily Sales Trend")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Total Sales ($)")
        plt.xticks(rotation=45)
        st.pyplot(fig2)

        peak_date = daily_sales.idxmax()
        st.write(f"Interpretation: Highest sales occurred on {peak_date.strftime('%Y-%m-%d')}.")

# Question 3: Customer Satisfaction Rating Distribution
with tab3:
    st.header("Question 3: Customer Satisfaction Ratings")

    if "Service Satisfaction Rating" not in df.columns:
        st.error("Missing required column: Service Satisfaction Rating")
    else:
        ratings = pd.to_numeric(df["Service Satisfaction Rating"], errors="coerce").dropna()
        rating_counts = ratings.value_counts().sort_index()

        fig3, ax3 = plt.subplots()
        ax3.bar(rating_counts.index.astype(str), rating_counts.values)
        ax3.set_title("Satisfaction Rating Distribution")
        ax3.set_xlabel("Rating")
        ax3.set_ylabel("Number of Customers")
        st.pyplot(fig3)

        most_common_rating = rating_counts.idxmax()
        st.write(f"Interpretation: The most common satisfaction rating is {most_common_rating}.")

st.write("---")
st.caption("Created for Assignment 5 — Streamlit + Pandas + Matplotlib")
