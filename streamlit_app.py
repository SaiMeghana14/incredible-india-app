import streamlit as st
import snowflake.connector
import pandas as pd

# Title and Description
st.set_page_config(page_title="Incredible India – Cultural Explorer", layout="wide")
st.title("🇮🇳 Incredible India – Cultural Explorer")
st.markdown("Explore the rich cultural diversity of India – from festivals and food to monuments and traditions.")

# Connect to Snowflake
@st.cache_resource
def get_snowflake_connection():
    conn = snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"]
    )
    return conn

# Fetch data from Snowflake
def fetch_data():
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM explorer")
    df = cursor.fetch_pandas_all()
    cursor.close()
    return df

# Display cultural data
df = fetch_data()
categories = df["category"].unique()
selected_category = st.selectbox("Choose a Category", options=categories)

filtered_df = df[df["category"] == selected_category]

for _, row in filtered_df.iterrows():
    with st.container():
        st.subheader(f"{row['name']} ({row['state']})")
        st.image(row['image_url'], use_column_width=True)
        st.write(row['description'])
        st.markdown("---")