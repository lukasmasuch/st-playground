import random
import time

import streamlit as st


@st.cache_data
def cache_something(num):
    time.sleep(2)
    return num


time.sleep(1)
cache_something(random.randint(0, 10000))
st.rerun()
