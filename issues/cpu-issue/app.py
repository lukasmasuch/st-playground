import gc
import random
import resource
import time

import numpy as np
import objgraph
import pandas as pd
import psutil
import streamlit as st

np.random.seed(0)

st.write(st.__version__)
st.write("hello")


@st.cache_data
def cache_something(num):
    time.sleep(2)
    return num


if "counter" not in st.session_state:
    st.session_state.counter = 0

cpu_percent = psutil.cpu_percent(interval=1)
st.write("CPU percantage", cpu_percent)


@st.cache_data(max_entries=3)
def get_data_1(counter: int):
    return pd.DataFrame(
        np.random.randn(50000 + counter, 20), columns=("col %d" % i for i in range(20))
    )


@st.cache_resource(max_entries=3)
def get_data_2(counter):
    return pd.DataFrame(
        np.random.randn(50000 + counter, 20), columns=("col %d" % i for i in range(20))
    )


if st.button("Release memory"):
    import gc

    gc.collect()
    import pyarrow

    pool = pyarrow.default_memory_pool()
    pool.release_unused()

if st.button("Configure jemelloc decay"):
    import pyarrow as pa

    pa.jemalloc_set_decay_ms(0)

if st.button("Show heap"):
    import psutil
    from guppy import hpy

    gc.collect()
    heap = hpy().heap()
    st.text(heap)
    process = psutil.Process()
    st.write("RSS memory (bytes):", process.memory_info().rss)
    st.write(
        "Max RSS memory (bytes):", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    )
    # st.write("heap.bytype")
    # st.text(heap.bytype)
    # st.write("heap.byclodo")
    # st.text(heap.byclodo)

if st.button("Show most common types"):
    gc.collect()
    st.dataframe(objgraph.most_common_types(100))

if st.button("Show growth"):
    gc.collect()
    st.dataframe(objgraph.growth())

obj_type = st.text_input("Object type", value=None)
if st.button("Explore type"):
    st.write(
        "Leaking obj from type",
        objgraph.count(obj_type, objgraph.get_leaking_objects()),
    )
    st.write("Backref chain")
    st.write(
        objgraph.find_backref_chain(
            random.choice(objgraph.by_type(obj_type)), objgraph.is_proper_module
        )
    )


object_rank = st.number_input("The n-largest object", min_value=0, value=0)
if st.button("Show n-largest object path"):
    from guppy import hpy

    heap = hpy().heap()
    obj = heap.byid[object_rank]
    st.write(f"Object {object_rank}: ", "Path:", obj.sp, "Info:", obj.stat)

if st.button("Show config"):
    from streamlit.config import get_option

    st.write(get_option("global.storeCachedForwardMessagesInMemory"))

if st.toggle("Auto-rerun", value=False):
    my_bar = st.progress(0, text="Progress...")

    for percent_complete in range(100):
        time.sleep(0.02)
        my_bar.progress(percent_complete + 1, text="Progress...")
    my_bar.empty()
    st.dataframe(get_data_1(st.session_state.counter))
    st.dataframe(get_data_2(st.session_state.counter))
    st.write("Counter:", st.session_state.counter)
    cache_something(random.randint(0, 10000))
    time.sleep(2)
    st.session_state.counter += 1
    st.rerun()
