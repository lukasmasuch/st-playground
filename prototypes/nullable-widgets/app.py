import streamlit as st

st.header("Nullable State Demo")
st.code(
    """
my_date = st.date_input("foo", None, clearable=True)
st.write(my_date)
"""
)

my_date = st.date_input("Nullable Date Chooser", None, clearable=True)
st.write("Value:", my_date)
