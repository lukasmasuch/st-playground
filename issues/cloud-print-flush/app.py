import streamlit as st

if st.button("Set PYTHONUNBUFFERED env"):
    import os
    os.environ["PYTHONUNBUFFERED"] = "1"

print("test 1")
if st.button("Test Print"):
    print("triggered print")
print("test 2")

if st.button("Flush Print"):
    print("flush print", flush=True)
