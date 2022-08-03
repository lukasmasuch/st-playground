import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Visualize the data",
    page_icon="📈",
    page_description="This page allows you to visualize the data in charts.",
)


st.title("📈 Visualize the data")

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

st.line_chart(chart_data)
