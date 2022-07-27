import streamlit as st

tab1, tab2, tab3 = st.tabs(["tab1", "tab2", "tab3"])
with tab1:
    with st.form("test"):
        st.number_input("test")
        st.form_submit_button("submit")
    if st.button("Test"):
        st.write("Click")
