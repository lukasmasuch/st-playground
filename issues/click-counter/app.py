import streamlit as st

import time

if st.checkbox("Enable faster reruns"):
    st._config.set_option("runner.fastReruns", True)
else:
    st._config.set_option("runner.fastReruns", False)

if "counter" not in st.session_state:
    st.session_state["counter"] = 0

button_clicked = st.button("Click me")

st.write("You clicked the button:")
with st.spinner("Doing some computation"):
    time.sleep(2)
if button_clicked:
    st.session_state["counter"] += 1
st.write(str(st.session_state["counter"]) + " times")
