import streamlit as st

# import pandas as pd
# import numpy as np

# chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])


for i in range(20):
    st.markdown("dummy text")


tab1, tab2 = st.tabs(["tab1", "tab2"])

with tab1:
    # st.line_chart(chart_data)
    st.video("https://www.youtube.com/watch?v=R2nr1uZ8ffc")

with tab2:
    # st.line_chart(chart_data)
    st.video("https://www.youtube.com/watch?v=R2nr1uZ8ffc")

st.markdown("test")

if st.checkbox("Add more content"):
    st.video("https://www.youtube.com/watch?v=R2nr1uZ8ffc")
