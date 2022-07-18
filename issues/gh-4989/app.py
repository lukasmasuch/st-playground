import streamlit as st


st.session_state["apply_workaround"] = st.checkbox("Apply workaround")

st.write(st.session_state)