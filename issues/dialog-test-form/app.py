import numpy as np
import pandas as pd
import streamlit as st

if st.toggle("Show data"):
    num_rows = st.number_input("Num rows", 0, 500000, 100000, 1000)
    # create a random dataframe
    df = pd.DataFrame(
        np.random.randn(num_rows, 20), columns=("col %d" % i for i in range(20))
    )
    st.dataframe(df)

with st.form("my_form"):
    st.write("Hello again!")
    form_input = st.text_input("Enter something!")
    st.form_submit_button("Submit")

st.write(form_input)
