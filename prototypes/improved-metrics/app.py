import streamlit as st
import numpy as np
import pandas as pd
import plotly

st.set_page_config(layout="centered")
st.write("foo")

st.json(st.experimental_get_query_params())

col1, col2, col3 = st.columns(3)
with col1:
    st.write("foo")

with col2:
    st.text_input("this is a test", value="foobar", max_chars=100)

st.selectbox("this is another test", options=[1, 2, 3, 4, 5], index=1)

col3.number_input("This is a number input", min_value=10, max_value=100, value=50)

st.sidebar.multiselect("This is a multiselect", options=["foo", "bar", "baz"])

np.random.seed(42)
df = pd.DataFrame(np.random.randn(10, 4), columns=["A", "B", "C", "D"])

st.write(df)

if st.button("trigger error"):
    st.session_state["not existant"]


if st.button("rerun"):
    st.experimental_rerun()

if st.button("stop"):
    st.stop()

with st.echo():
    st.write("This code will be printed")

if st.button("wait..."):
    with st.spinner("waiting..."):
        import time

        time.sleep(5)

st.text(123)

st.experimental_show(df)
thing = "something"
st.experimental_show(df)

st.help(st.audio)
st.help(st.text)

import inspect

st.text(str(inspect.signature(st.audio)))
st.text(str(inspect.signature(st.text)))

from st_aggrid import AgGrid
import pandas as pd

df = pd.read_csv(
    "https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv"
)
AgGrid(df)


@st.experimental_memo
def square(x):
    return x**2


@st.experimental_singleton
def get_database_session(url):
    # Create a database session object that points to the URL.
    return url


@st.cache(persist=True)
def fetch_and_clean_data(url):
    # Fetch data from URL here, and then clean it up.
    return url


@st.experimental_memo
def get_df():
    df = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    return df


import datetime

d = st.date_input("When's your birthday", datetime.date(2019, 7, 6))
st.write("Your birthday is:", d)

import streamlit as st
import plotly.figure_factory as ff
import numpy as np

# Add histogram data
x1 = np.random.randn(200) - 2
x2 = np.random.randn(200)
x3 = np.random.randn(200) + 2

# Group data together
hist_data = [x1, x2, x3]

group_labels = ["Group 1", "Group 2", "Group 3"]

# Create distplot with custom bin_size
fig = ff.create_distplot(hist_data, group_labels, bin_size=[0.1, 0.25, 0.5])

# Plot!
st.plotly_chart(fig, use_container_width=True)

import matplotlib.pyplot as plt
import numpy as np

arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

st.pyplot(fig)

import streamlit as st
from bokeh.plotting import figure

x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]

p = figure(title="simple line example", x_axis_label="x", y_axis_label="y")

p.line(x, y, legend_label="Trend", line_width=2)

st.bokeh_chart(p, use_container_width=True)

import pandas as pd
import numpy as np
import altair as alt

df = pd.DataFrame(np.random.randn(200, 3), columns=["a", "b", "c"])

c = (
    alt.Chart(df)
    .mark_circle()
    .encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"])
)

st.altair_chart(c, use_container_width=True)

get_database_session("foo")
get_database_session("bar")
get_database_session("blob")

square(1)
square(2)

fetch_and_clean_data("foo")
fetch_and_clean_data("bar")

get_df()

if st.button("Clear All"):
    # Clears all singleton caches:
    st.experimental_singleton.clear()
    st.experimental_memo.clear()


chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

# Use magic
chart_data

st._arrow_dataframe(chart_data, width=100, height=100)

st.line_chart(data=chart_data)

st.write(
    "<style>table { max-width: 500px; table-layout: fixed; width: 500px;}</style>",
    unsafe_allow_html=True,
)

st.write(chart_data.to_html(escape=False, index=False), unsafe_allow_html=True)
