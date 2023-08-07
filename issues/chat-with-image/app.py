import os

import streamlit as st

script_path = os.path.dirname(os.path.realpath(__file__))

with st.chat_message("user", avatar=os.path.join(script_path, "myimage.png")):
    st.write("Hello")

st.image(os.path.join(script_path, "myimage.png"))

