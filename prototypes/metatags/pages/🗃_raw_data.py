import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Explore raw data",
    page_icon="🗃",
    page_description="This page allows you to explore the raw data.",
)


st.title("🗃 Explore raw data")

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

st.dataframe(chart_data)
