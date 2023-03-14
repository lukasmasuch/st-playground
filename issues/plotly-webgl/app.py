import pandas as pd
import plotly.express as px
import streamlit as st

df = pd.DataFrame({"y": list(range(2000)), "dt": pd.date_range("2020-01-01", periods=2000)})

n = st.slider("Select a number", 1, 100, 10)

st.write(f"Plotting {n} timeseries")

use_svg = st.checkbox("Force render_mode=svg (default is webgl for datasets > 1000 points)")

for i in range(n):
    st.write(i)
    fig = px.line(df, x="dt", y="y", render_mode="svg" if use_svg else "auto")
    st.plotly_chart(fig)
