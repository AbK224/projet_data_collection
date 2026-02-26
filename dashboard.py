import streamlit as st
import pandas as pd


def show_dashboard(df: pd.DataFrame):
    st.subheader("Dashboard des données animales")
    st.write(f"Nombre total d'animaux: {df.shape[0]}")
    st.write(f"les 10 animaux les plus chers:")
    st.write(df.nlargest(10, "prix"))