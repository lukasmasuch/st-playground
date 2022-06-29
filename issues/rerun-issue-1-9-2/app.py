import streamlit as st
import time

time.sleep(1)


value = st.number_input("test", value=100)

items = list(range(11, value))
st.multiselect("Quickly remove stuff in here", items, items)

# This seems to be important. This simulates network delays and busy servers.
time.sleep(1)
