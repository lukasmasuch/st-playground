# import numpy as np
# import pandas as pd

import gc
import resource
import time

import objgraph
import psutil
import streamlit as st
from guppy import hpy

# import resource

# st.write(resource.getrlimit(resource.RLIMIT_AS))
# resource.setrlimit(resource.RLIMIT_AS, (500 * int(1e6), 1000 * int(1e6)))


# np.random.seed(0)
# if st.checkbox("Show dataframe", value=False):
#     df = pd.DataFrame(
#         np.random.randn(1000, 20), columns=("col %d" % i for i in range(20))
#     )

#     # This should use truncation for all
#     st.dataframe(df)


# @st.cache_data
# def cache():
#     return pd.DataFrame(
#         np.random.randn(200000, 20), columns=("col %d" % i for i in range(20))
#     )


# cache()

# st.session_state["df"] = "foo"

# st.write(process.memory_info())
# st.write(resource.getrusage(resource.RUSAGE_SELF))
# st.write(objgraph.get_leaking_objects())
# st.write(objgraph.count("builtin_function_or_method", objgraph.get_leaking_objects()))
# st.write(objgraph.get_new_ids())


gc.collect()

st.text(hpy().heap())

process = psutil.Process()
st.write("RSS memory (bytes):", process.memory_info().rss)
st.write("Max RSS memory (bytes):", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

gc.collect()
st.dataframe(objgraph.most_common_types(100))

if st.button("Show stats"):
    gc.collect()
    st.dataframe(objgraph.growth())

if st.toggle("Auto-rerun", value=False):
    time.sleep(0.5)
    st.rerun()