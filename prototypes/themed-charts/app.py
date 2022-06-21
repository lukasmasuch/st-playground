import itertools

import pandas as pd
import numpy as np
import streamlit as st


st.set_page_config(page_title="Streamlit Theme for Charts", page_icon="📊")


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


HEADER_COLOR_CYCLE = itertools.cycle(
    [
        "#00c0f2",  # light-blue-70",
        "#ffbd45",  # "orange-70",
        "#00d4b1",  # "blue-green-70",
        "#1c83e1",  # "blue-70",
        "#803df5",  # "violet-70",
        "#ff4b4b",  # "red-70",
        "#21c354",  # "green-70",
        "#faca2b",  # "yellow-80",
    ]
)


def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")


def colored_header(label, description=None, color=None):
    """Shows a header with a colored underline and an optional description."""
    space(num_lines=2)
    if color is None:
        color = next(HEADER_COLOR_CYCLE)
    st.subheader(label)
    st.write(
        f'<hr style="background-color: {color}; margin-top: 0; margin-bottom: 0; height: 3px; border: none; border-radius: 3px;">',
        unsafe_allow_html=True,
    )
    if description:
        st.caption(description)


icon("📊")

st.title("Charts with Streamlit Theme")

colored_header("st.line_chart")

with st.expander("Show code"):
    st.code(
        """
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
st.line_chart(chart_data)
"""
    )

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
st.line_chart(chart_data)

colored_header("st.area_chart")
with st.expander("Show code"):
    st.code(
        """
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
st.area_chart(chart_data)
"""
    )

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
st.area_chart(chart_data)

colored_header("st.bar_chart")
with st.expander("Show code"):
    st.code(
        """
chart_data = pd.DataFrame(np.random.randn(50, 3), columns=["a", "b", "c"])
st.bar_chart(chart_data)
"""
    )

chart_data = pd.DataFrame(np.random.randn(50, 3), columns=["a", "b", "c"])
st.bar_chart(chart_data)

colored_header("st.altair_chart - Example 1")
with st.expander("Show code"):
    st.code(
        """
import altair as alt
from vega_datasets import data

source = data.cars()

line = alt.Chart(source).mark_line().encode(x="Year", y="mean(Miles_per_Gallon)")

band = (
    alt.Chart(source)
    .mark_errorband(extent="ci")
    .encode(
        x="Year",
        y=alt.Y("Miles_per_Gallon", title="Miles/Gallon"),
    )
)

st._arrow_altair_chart(band + line, theme="streamlit", use_container_width=True)
"""
    )

import altair as alt
from vega_datasets import data

source = data.cars()

line = alt.Chart(source).mark_line().encode(x="Year", y="mean(Miles_per_Gallon)")

band = (
    alt.Chart(source)
    .mark_errorband(extent="ci")
    .encode(
        x="Year",
        y=alt.Y("Miles_per_Gallon", title="Miles/Gallon"),
    )
)

st._arrow_altair_chart(band + line, theme="streamlit", use_container_width=True)

colored_header("st.altair_chart - Example 2")
with st.expander("Show code"):
    st.code(
        """
import altair as alt
from vega_datasets import data

source = data.cars()

chart = (
    alt.Chart(source)
    .mark_circle()
    .encode(
        x="Horsepower",
        y="Miles_per_Gallon",
        color="Origin",
    )
    .interactive()
)

st._arrow_altair_chart(chart, theme="streamlit", use_container_width=True)
"""
    )


import altair as alt
from vega_datasets import data

source = data.cars()

chart = (
    alt.Chart(source)
    .mark_circle()
    .encode(
        x="Horsepower",
        y="Miles_per_Gallon",
        color="Origin",
    )
    .interactive()
)

st._arrow_altair_chart(chart, theme="streamlit", use_container_width=True)

colored_header("st.altair_chart - Example 3")
with st.expander("Show code"):
    st.code(
        """
import altair as alt
from vega_datasets import data

source = data.cars()

brush = alt.selection(type="interval")

points = (
    alt.Chart(source, width=500)
    .mark_point()
    .encode(
        x="Horsepower:Q",
        y="Miles_per_Gallon:Q",
        color=alt.condition(brush, "Origin:N", alt.value("lightgray")),
    )
    .add_selection(brush)
)

bars = (
    alt.Chart(source, width=500)
    .mark_bar()
    .encode(y="Origin:N", color="Origin:N", x="count(Origin):Q")
    .transform_filter(brush)
)

st._arrow_altair_chart(points & bars, theme="streamlit", use_container_width=True)
"""
    )

import altair as alt
from vega_datasets import data

source = data.cars()

brush = alt.selection(type="interval")

points = (
    alt.Chart(source, width=500)
    .mark_point()
    .encode(
        x="Horsepower:Q",
        y="Miles_per_Gallon:Q",
        color=alt.condition(brush, "Origin:N", alt.value("lightgray")),
    )
    .add_selection(brush)
)

bars = (
    alt.Chart(source, width=500)
    .mark_bar()
    .encode(y="Origin:N", color="Origin:N", x="count(Origin):Q")
    .transform_filter(brush)
)

st._arrow_altair_chart(points & bars, theme="streamlit", use_container_width=True)

colored_header("st.vega_lite_chart")
with st.expander("Show code"):
    st.code(
        """
df = pd.DataFrame(np.random.randn(200, 3), columns=["a", "b", "c"])

st._arrow_vega_lite_chart(
    df,
    {
        "mark": {"type": "circle", "tooltip": True},
        "encoding": {
            "x": {"field": "a", "type": "quantitative"},
            "y": {"field": "b", "type": "quantitative"},
            "size": {"field": "c", "type": "quantitative"},
        },
    },
    theme="streamlit",
    use_container_width=True,
)
"""
    )

df = pd.DataFrame(np.random.randn(200, 3), columns=["a", "b", "c"])

st._arrow_vega_lite_chart(
    df,
    {
        "mark": {"type": "circle", "tooltip": True},
        "encoding": {
            "x": {"field": "a", "type": "quantitative"},
            "y": {"field": "b", "type": "quantitative"},
            "size": {"field": "c", "type": "quantitative"},
        },
    },
    theme="streamlit",
    use_container_width=True,
)
