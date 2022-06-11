import streamlit as st
import pandas as pd
import numpy as np


@st.experimental_singleton()
def get_weather_df():
    return pd.DataFrame(
        np.random.rand(10, 2) * 5,
        index=pd.date_range(start="2021-01-01", periods=10),
        columns=["Tokyo", "Beijing"],
    )


def make_pretty(styler):
    styler.format(lambda v: "Dry" if v < 1.75 else "Rain" if v < 2.75 else "Heavy Rain")
    styler.background_gradient(axis=None, vmin=1, vmax=5, cmap="YlGnBu")
    return styler


weather_df = get_weather_df()

st.dataframe(weather_df.style.pipe(make_pretty))

selected_city = st.radio("Select City", weather_df.columns, horizontal=True)

st.line_chart(weather_df[selected_city])
