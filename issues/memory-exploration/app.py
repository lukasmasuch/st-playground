# import numpy as np
# import pandas as pd

import gc
import random
import resource
import time

import numpy as np
import objgraph
import pandas as pd
import psutil
import streamlit as st
from guppy import hpy

np.random.seed(0)
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

if "counter" not in st.session_state:  
    st.session_state.counter = 0

@st.cache_data(max_entries=3)
def get_data_1(counter: int):
    return pd.DataFrame(
        np.random.randn(50000+counter, 20), columns=("col %d" % i for i in range(20))
    )

@st.cache_resource(max_entries=3)
def get_data_2(counter):
    return pd.DataFrame(
        np.random.randn(50000+counter, 20), columns=("col %d" % i for i in range(20))
    )

if st.toggle("Auto-rerun", value=False):
    my_bar = st.progress(0, text="Progress...")

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text="Progress...")
    my_bar.empty()
    st.dataframe(get_data_1(st.session_state.counter))
    st.dataframe(get_data_2(st.session_state.counter))
    time.sleep(0.5)
    st.session_state.counter += 1
    st.rerun()

if st.button("Show memory stats"):
    gc.collect()
    heap = hpy().heap()
    st.text(heap)
    process = psutil.Process()
    st.write("RSS memory (bytes):", process.memory_info().rss)
    st.write("Max RSS memory (bytes):", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    gc.collect()
    st.dataframe(objgraph.most_common_types(100))
    st.write("heap.bytype")
    st.text(heap.bytype)
    st.write("heap.byclodo")
    st.text(heap.byclodo)

if st.button("Show growth"):
    gc.collect()
    st.dataframe(objgraph.growth())

obj_type = st.text_input("Object type", value=None)
if st.button("Explore type"):
    st.write("Leaking obj from type", objgraph.count(obj_type, objgraph.get_leaking_objects()))
    st.write("Backref chain")
    st.write(objgraph.find_backref_chain(
        random.choice(objgraph.by_type(obj_type)), 
        objgraph.is_proper_module))
   

object_rank = st.number_input("The n-largest object", min_value=0, value=0)
if st.button("Show n-largest object path"):
    heap = hpy().heap()
    obj = heap.byid[object_rank]
    st.write(f"Object {object_rank}: ", "Path:", obj.sp, "Info:", obj.stat)

st.write("Counter:", st.session_state.counter)