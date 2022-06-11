import streamlit as st

if "run_counter" not in st.session_state:
    st.session_state["run_counter"] = 1
else:
    st.session_state["run_counter"] += 1

st.write("Run counter: ", st.session_state["run_counter"])