import itertools

import pandas as pd
import streamlit as st
import altair as alt
from vega_datasets import data

st.set_page_config(page_title="Selections on Charts - Prototype", page_icon="📈")


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


icon("📈")

st.title("Selections on Charts - Prototype")

st.markdown("This prototype evaluates adding selection events to `vega_lite` and `altair` charts."
    " This allows reacting to user selections on various chart types."
)

colored_header(
    "Area selection (via session state)",
    description="Select an area on the chart via drag & drop. Double click on the selection box to clear it.",
)

with st.expander("Show code"):
    st.code(
        """
import streamlit as st
import altair as alt
from vega_datasets import data

brush = alt.selection_interval(name="interval")  # selection of type "interval"

chart = (
    alt.Chart(data.cars.url)
    .mark_point()
    .encode(x="Miles_per_Gallon:Q", y="Horsepower:Q", color="Origin:N")
    .add_selection(brush)
)

st._arrow_altair_chart(chart, on_selection="selected_cars")

# Do something with: st.session_state.selected_cars
...
"""
    )


@st.experimental_memo
def get_car_df():
    return pd.read_json(data.cars.url)


brush = alt.selection_interval(name="interval")

chart = (
    alt.Chart(data.cars.url)
    .mark_point()
    .encode(x="Miles_per_Gallon:Q", y="Horsepower:Q", color="Origin:N")
    .add_selection(brush)
)

st._arrow_altair_chart(chart, on_selection="selected_cars", use_container_width=True)


try:
    car_df = get_car_df()
    miles_selection = st.session_state.selected_cars["interval"]["Miles_per_Gallon"]
    horsepower_selection = st.session_state.selected_cars["interval"]["Horsepower"]
    car_df = car_df[
        car_df["Miles_per_Gallon"].between(
            left=miles_selection[0], right=miles_selection[1]
        )
        & car_df["Horsepower"].between(
            left=horsepower_selection[0], right=horsepower_selection[1]
        )
    ]
    st.dataframe(car_df)
except Exception:
    st.write("No selection")

colored_header(
    "Single selection (via callback)",
    description="Select single item on the chart by clicking on it.",
)

with st.expander("Show code"):
    st.code(
        """
import streamlit as st
import altair as alt
from vega_datasets import data

def car_selected(selections):
    # Do something with selections
    ...

single_selection = alt.selection_single(name="single")

chart = (
    alt.Chart(data.cars.url)
    .mark_point()
    .encode(x="Miles_per_Gallon:Q", y="Horsepower:Q", color="Origin:N")
    .add_selection(single_selection)
)

st._arrow_altair_chart(chart, on_selection=car_selected)
"""
    )


def car_selected(selections):
    try:
        car_df = get_car_df()
        selected_item = selections["single"]["_vgsid_"][0]
        st.markdown("**Selected car:** " + str(car_df.loc[selected_item - 1]["Name"]))
    except Exception:
        st.write("Please select a car on the chart.")


single_selection = alt.selection_single(name="single")

chart = (
    alt.Chart(data.cars.url)
    .mark_point(
        tooltip=True,
    )
    .encode(
        x="Miles_per_Gallon:Q",
        y="Horsepower:Q",
        color=alt.condition(single_selection, "Origin:N", alt.value("lightgray")),
    )
    .add_selection(single_selection)
)

st._arrow_altair_chart(chart, on_selection=car_selected, use_container_width=True)

colored_header(
    "Multi selection (via session state)",
    description="Select one or multiple items on the chart via (shift+) click.",
)

with st.expander("Show code"):
    st.code(
        """
import streamlit as st
import altair as alt
from vega_datasets import data

multi_selection = alt.selection_multi(name="multi", encodings=["x"])

chart = (
    alt.Chart(data.cars.url)
    .mark_bar()
    .encode(
        x="Origin:N",
        y="count()",
        color=alt.condition(multi_selection, "Origin:N", alt.value("lightgray")),
    )
    .add_selection(multi_selection)
)

st._arrow_altair_chart(chart, on_selection="selected_countries")

# Do something with: st.session_state.selected_countries
...
"""
    )

multi_selection = alt.selection_multi(name="multi", encodings=["x"])

chart = (
    alt.Chart(data.cars.url)
    .mark_bar()
    .encode(
        x="Origin:N",
        y="count()",
        color=alt.condition(multi_selection, "Origin:N", alt.value("lightgray")),
    )
    .add_selection(multi_selection)
)

st._arrow_altair_chart(
    chart, on_selection="selected_countries", use_container_width=True
)

try:
    car_df = get_car_df()
    selected_countries = st.session_state.selected_countries["multi"]["Origin"]
    car_df = car_df[car_df["Origin"].isin(selected_countries)]
    st.dataframe(car_df)
except Exception:
    st.write("No selection")
