import mysql.connector
import pandas as pd
import streamlit as st

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Drishvig997@",
            database="sports",   # change if your schema name is different
            port=3306
        )
        return conn
    except Exception as e:
        st.error("❌ Database connection failed")
        st.error(e)
        st.stop()

def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df
