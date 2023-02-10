import streamlit as st
from streamlit.components.v1 import iframe

col1, col2 = st.columns(2)

with col1:
    iframe("https://example-time-series-annotation.streamlit.app/~/+/?embedded=true")

with col2:
    iframe("https://example-time-series-annotation.streamlit.app/?embedded=true")
