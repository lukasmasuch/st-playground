import streamlit as st

if st.button("Trigger Exception"):
    raise Exception("This is an exception")
