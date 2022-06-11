import streamlit as st

st.header("With label")
st.code("""
st.text_input("With label")
""")

st.text_input("With label", key="with-label")

st.header("Empty label")
st.code("""
st.text_input("")
""")

st.text_input("", key="empty-label")

st.header("`None` label")
st.code("""
st.text_input(None)
""")

st.text_input(None, key="no-label")

st.header("`None` label & help")
st.code("""
st.text_input(None, help="None label with a help tooltip.")
""")

st.text_input(
    None, help="None label with a help tooltip.", key="no-label-with-help"
)
