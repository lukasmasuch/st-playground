import streamlit as st

elements_num = st.number_input("Number input", value=10)

for i in range(elements_num):
    st.button(f"Button {i}")
