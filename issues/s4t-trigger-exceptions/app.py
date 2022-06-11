import streamlit as st

if st.button("Trigger exception"):
    test = {}
    test["foo"]
    print("foo")