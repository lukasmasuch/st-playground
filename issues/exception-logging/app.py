import streamlit as st
import os

st.json(dict(os.environ))
if st.button("Trigger Exception"):
    raise Exception("This is an exception")
