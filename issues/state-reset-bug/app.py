import streamlit as st

print("WARNING")
if "clicks" not in st.session_state:
    st.session_state["clicks"] = 0

st.write("Step 1: Write anything into the text input")
st.text_input("Write anything")

st.write(
    "Step 2: Click the button fast until the site reloads (your text input should be removed at that point)"
)
if st.button("Click me fast"):
    st.session_state.clicks += 1

import numpy as np
import pandas as pd

if "dataset" not in st.session_state:
    st.session_state["dataset"] = df = pd.DataFrame(
        np.random.randint(0, 100, size=(50000, 5)),
        columns=["Col A", "Col B", "Col C", "Col D", "Col E"],
    )

st.dataframe(st.session_state["dataset"])