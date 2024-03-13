import gc
import random
import resource
import time

import matplotlib.pyplot as plt
import numpy as np
import objgraph
import pandas as pd
import streamlit as st
import yappi

np.random.seed(0)

st.write(st.__version__)
st.write("hello")

yappi.set_clock_type("cpu")
yappi.start()


@st.cache_data
def cache_something(num):
    time.sleep(2)
    return num


if "counter" not in st.session_state:
    st.session_state.counter = 0


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

if st.button("Print yappi"):
    print("Yappi get_func_stats", flush=True)
    yappi.get_func_stats().print_all()
    print("Yappi get_thread_stats (per thread)", flush=True)
    # retrieve thread stats by their thread id (given by yappi)
    threads = yappi.get_thread_stats()
    for thread in threads:
        print(
            "Function stats for (%s) (%d)" % (thread.name, thread.id)
        )  # it is the Thread.__class__.__name__
        yappi.get_func_stats(ctx_id=thread.id).print_all()

    print("Yappi get_thread_stats (overview)", flush=True)
    yappi.get_thread_stats().print_all()
    print("", flush=True)

if st.button("Show CPU stats"):
    import psutil

    cpu_percent = psutil.cpu_percent(interval=1)
    st.write("CPU%", cpu_percent)

    for process in [psutil.Process(pid) for pid in psutil.pids()]:
        try:
            process_name = process.name()
            process_mem = process.memory_percent()
            process_cpu = process.cpu_percent(interval=0.5)
            st.write("Name:", process_name, "CPU%:", process_cpu, "MEM%:", process_mem)
        except:
            pass

if st.toggle("Auto-rerun", value=False):
    st.write("Counter:", st.session_state.counter)
    arr = np.random.normal(1, 1, size=100)
    fig, ax = plt.subplots()
    ax.hist(arr, bins=20)

    st.pyplot(fig)

    time.sleep(10)
    st.session_state.counter += 1
    st.rerun()
