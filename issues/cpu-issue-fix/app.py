import random
import time

import streamlit as st


@st.cache_data
def cache_something(num):
    time.sleep(2)
    return 42


if st.button("Run"):
    for _ in range(1000):
        time.sleep(1)
        cache_something(random.randint(0, 1000))
