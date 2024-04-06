import pandas as pd
import streamlit as st

df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})


st.dataframe(df)
