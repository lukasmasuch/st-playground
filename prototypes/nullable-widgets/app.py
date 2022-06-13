import streamlit as st

st.header("Nullable State Demo")

st.subheader("Normal Date")
st.code(
    """
my_date = st.date_input("Normal Date")
st.write(my_date)
"""
)

my_date = st.date_input("Normal Date")
st.write("Value:", my_date)


st.subheader("Normal Date & Clearable")
st.code(
    """
my_date = st.date_input("Normal Date & Clearable", clearable=True)
st.write(my_date)
"""
)

my_date = st.date_input("Normal Date & Clearable", clearable=True)
st.write("Value:", my_date)


st.subheader("None Date & Clearable")
st.code(
    """
my_date = st.date_input("None Date & Clearable", None, clearable=True)
st.write(my_date)
"""
)

my_date = st.date_input("None Date & Clearable", None, clearable=True)
st.write("Value:", my_date)


st.subheader("None Date & Not Clearable")
st.code(
    """
my_date = st.date_input("None Date & Not Clearable", None, clearable=False)
st.write(my_date)
"""
)

my_date = st.date_input("None Date & Not Clearable", value=None, clearable=False)
st.write("Value:", my_date)
