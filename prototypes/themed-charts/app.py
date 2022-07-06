import itertools

import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
from vega_datasets import data

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


if st.checkbox("Use Streamlit Theme", value=True):
    SELECTED_THEME = "streamlit"
else:
    SELECTED_THEME = None

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


colored_header("st.altair_chart - Scatterplot")
with st.expander("Show code"):
    st.code(
        """
import streamlit as st
import altair as alt
from vega_datasets import data

chart = (
    alt.Chart(data.cars())
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

chart = (
    alt.Chart(data.cars())
    .mark_circle()
    .encode(
        x="Horsepower",
        y="Miles_per_Gallon",
        color="Origin",
    ).properties(
    title="Top Directors by Average Worldwide Gross",
    )
    .interactive()
)

st._arrow_altair_chart(chart, theme=SELECTED_THEME, use_container_width=True)

colored_header("st.altair_chart - Histogram")

with st.expander("Show code"):
    st.code(
        """
import streamlit as st
import altair as alt
from vega_datasets import data

chart = alt.Chart(data.movies.url).mark_bar().encode(
    alt.X("IMDB_Rating:Q", bin=True),
    y='count()',
)

st._arrow_altair_chart(chart, theme="streamlit", use_container_width=True)
"""
    )

chart = alt.Chart(data.movies.url).mark_bar().encode(
    alt.X("IMDB_Rating:Q", bin=True),
    y='count()',
)

st._arrow_altair_chart(chart, theme=SELECTED_THEME, use_container_width=True)


colored_header("st.altair_chart - Bar Chart")

with st.expander("Show code"):
    st.code(
        """
import streamlit as st
import altair as alt
from vega_datasets import data

chart = alt.Chart( data.barley()).mark_bar().encode(
    x='sum(yield):Q',
    y=alt.Y('site:N', sort='-x')
)

st._arrow_altair_chart(chart, theme="streamlit", use_container_width=True)
"""
    )

chart = alt.Chart( data.barley()).mark_bar().encode(
    x='sum(yield):Q',
    y=alt.Y('site:N', sort='-x')
)

st._arrow_altair_chart(chart, theme=SELECTED_THEME, use_container_width=True)

colored_header("st.altair_chart - Stacked Bar Chart")

with st.expander("Show code"):
    st.code(
        """
import streamlit as st
import altair as alt
from vega_datasets import data

chart = alt.Chart(data.barley()).mark_bar().encode(
    x='sum(yield)',
    y='variety',
    color='site',
    order=alt.Order(
      # Sort the segments of the bars by this field
      'site',
      sort='ascending'
    )
)

st._arrow_altair_chart(chart, theme="streamlit", use_container_width=True)
"""
    )

chart = alt.Chart(data.barley()).mark_bar().encode(
    x='sum(yield)',
    y='variety',
    color='site',
    order=alt.Order(
      # Sort the segments of the bars by this field
      'site',
      sort='ascending'
    )
).interactive()

st._arrow_altair_chart(chart, theme=SELECTED_THEME, use_container_width=True)


colored_header("st.altair_chart - Binned Scatterplot")

with st.expander("Show code"):
    st.code(
        """
import streamlit as st
import altair as alt
from vega_datasets import data

chart = alt.Chart(data.movies.url).mark_circle().encode(
    alt.X('IMDB_Rating:Q', bin=True),
    alt.Y('Rotten_Tomatoes_Rating:Q', bin=True),
    size='count()'
).properties(height=400).interactive()

st._arrow_altair_chart(chart, theme="streamlit", use_container_width=True)
"""
    )

chart = alt.Chart(data.movies.url).mark_circle().encode(
    alt.X('IMDB_Rating:Q', bin=True),
    alt.Y('Rotten_Tomatoes_Rating:Q', bin=True),
    size='count()'
).properties(height=400).interactive()
st._arrow_altair_chart(chart, theme=SELECTED_THEME, use_container_width=True)

colored_header("st.altair_chart - Binned Heatmap")

with st.expander("Show code"):
    st.code(
        """
import streamlit as st
import altair as alt
from vega_datasets import data

chart = alt.Chart(data.movies.url, height=400).mark_rect().encode(
    alt.X('IMDB_Rating:Q', bin=alt.Bin(maxbins=60)),
    alt.Y('Rotten_Tomatoes_Rating:Q', bin=alt.Bin(maxbins=40)),
    alt.Color('count():Q')
).interactive()

st._arrow_altair_chart(chart, theme="streamlit", use_container_width=True)
"""
    )

chart = alt.Chart(data.movies.url, height=400).mark_rect().encode(
    alt.X('IMDB_Rating:Q', bin=alt.Bin(maxbins=60)),
    alt.Y('Rotten_Tomatoes_Rating:Q', bin=alt.Bin(maxbins=40)),
    alt.Color('count():Q')
).interactive()

st._arrow_altair_chart(chart, theme=SELECTED_THEME, use_container_width=True)

colored_header("st.altair_chart - Geoshape Plot")

with st.expander("Show code"):
    st.code(
        """
import streamlit as st
import altair as alt
from vega_datasets import data

chart = alt.Chart(alt.topo_feature(data.us_10m.url, 'counties')).mark_geoshape().encode(
    color='rate:Q'
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(data.unemployment.url, 'id', ['rate'])
).project(
    type='albersUsa'
).properties(
    height=600,
    title="Unemployment rate per county"
)

st._arrow_altair_chart(chart, theme="streamlit", use_container_width=True)
"""
    )

chart = alt.Chart(alt.topo_feature(data.us_10m.url, 'counties')).mark_geoshape().encode(
    color='rate:Q'
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(data.unemployment.url, 'id', ['rate'])
).project(
    type='albersUsa'
).properties(
    height=600,
    title="Unemployment rate per county"
)

st._arrow_altair_chart(chart, theme=SELECTED_THEME, use_container_width=True)

colored_header("st.altair_chart - Layered Histogram")

with st.expander("Show code"):
    st.code(
        """
import streamlit as st
import altair as alt
import numpy as np
import pandas as pd

np.random.seed(42)

# Generating Data
source = pd.DataFrame({
    'Trial A': np.random.normal(0, 0.8, 1000),
    'Trial B': np.random.normal(-2, 1, 1000),
    'Trial C': np.random.normal(3, 2, 1000)
})

chart = alt.Chart(source).transform_fold(
    ['Trial A', 'Trial B', 'Trial C'],
    as_=['Experiment', 'Measurement']
).mark_bar(
    opacity=0.3,
    binSpacing=0
).encode(
    alt.X('Measurement:Q', bin=alt.Bin(maxbins=100)),
    alt.Y('count()', stack=None),
    alt.Color('Experiment:N')
).interactive()

st._arrow_altair_chart(chart, theme="streamlit", use_container_width=True)
"""
    )


np.random.seed(42)

# Generating Data
source = pd.DataFrame({
    'Trial A': np.random.normal(0, 0.8, 1000),
    'Trial B': np.random.normal(-2, 1, 1000),
    'Trial C': np.random.normal(3, 2, 1000)
})

chart = alt.Chart(source).transform_fold(
    ['Trial A', 'Trial B', 'Trial C'],
    as_=['Experiment', 'Measurement']
).mark_bar(
    opacity=0.3,
    binSpacing=0
).encode(
    alt.X('Measurement:Q', bin=alt.Bin(maxbins=100)),
    alt.Y('count()', stack=None),
    alt.Color('Experiment:N')
).interactive()

st._arrow_altair_chart(chart, theme=SELECTED_THEME, use_container_width=True)

colored_header("st.altair_chart - Pie Chart")

with st.expander("Show code"):
    st.code(
        """
import streamlit as st
import altair as alt

chart = alt.Chart(pd.DataFrame({"category": [1, 2, 3, 4, 5, 6], "value": [4, 6, 10, 3, 7, 8]})).mark_arc().encode(
    theta=alt.Theta(field="value", type="quantitative"),
    color=alt.Color(field="category", type="nominal"),
)

st._arrow_altair_chart(chart, theme="streamlit")
"""
    )

chart = alt.Chart(pd.DataFrame({"category": [1, 2, 3, 4, 5, 6], "value": [4, 6, 10, 3, 7, 8]})).mark_arc().encode(
    theta=alt.Theta(field="value", type="quantitative"),
    color=alt.Color(field="category", type="nominal"),
)

st._arrow_altair_chart(chart, theme=SELECTED_THEME)

colored_header("st.altair_chart - Grouped Bar Chart")

with st.expander("Show code"):
    st.code(
        """
import streamlit as st
import altair as alt
from vega_datasets import data

chart = alt.Chart(data.barley()).mark_bar().encode(
    x='year:O',
    y='sum(yield):Q',
    color='year:N',
    column='site:N'
).interactive()

st._arrow_altair_chart(chart, theme="streamlit")
"""
    )

chart = alt.Chart(data.barley()).mark_bar().encode(
    x='year:O',
    y='sum(yield):Q',
    color='year:N',
    column='site:N'
).interactive()

st._arrow_altair_chart(chart, theme=SELECTED_THEME)

colored_header("st.altair_chart - Strip Plot")

with st.expander("Show code"):
    st.code(
        """
import streamlit as st
import altair as alt
from vega_datasets import data

chart = alt.Chart(data.cars()).mark_tick().encode(
    x='Horsepower:Q',
    y='Cylinders:O'
).interactive()

st._arrow_altair_chart(chart, theme="streamlit", use_container_width=True)
"""
    )

chart = alt.Chart(data.cars()).mark_tick().encode(
    x='Horsepower:Q',
    y='Cylinders:O'
).interactive()

st._arrow_altair_chart(chart, theme=SELECTED_THEME, use_container_width=True)

colored_header("st.altair_chart - Line Chart")

with st.expander("Show code"):
    st.code(
        """
import streamlit as st
import altair as alt
from vega_datasets import data

chart = alt.Chart(data.population()).mark_line().encode(
    x='year:O',
    y=alt.Y(
        'sum(people)',
        scale=alt.Scale(type="log")  # Here the scale is applied
    )
)

st._arrow_altair_chart(chart, theme="streamlit", use_container_width=True)
"""
    )

chart = alt.Chart(data.population()).mark_line().encode(
    x='year:O',
    y=alt.Y(
        'sum(people)',
        scale=alt.Scale(type="log")  # Here the scale is applied
    )
)

st._arrow_altair_chart(chart, theme=SELECTED_THEME, use_container_width=True)

colored_header("st.altair_chart - Multi-series Line Chart")

with st.expander("Show code"):
    st.code(
        """
import streamlit as st
import altair as alt
from vega_datasets import data

chart = alt.Chart(data.stocks()).mark_line().encode(
    x='date',
    y='price',
    color='symbol',
    strokeDash='symbol',
).interactive()

st._arrow_altair_chart(chart, theme="streamlit", use_container_width=True)
"""
    )

chart = alt.Chart(data.stocks()).mark_line().encode(
    x='date',
    y='price',
    color='symbol',
    strokeDash='symbol',
).interactive()

st._arrow_altair_chart(chart, theme=SELECTED_THEME, use_container_width=True)

colored_header("st.altair_chart - Layered Line Chart")
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

st._arrow_altair_chart(band + line, theme=SELECTED_THEME, use_container_width=True)

colored_header("st.altair_chart - Combined Chart")
with st.expander("Show code"):
    st.code(
        """
import streamlit as st
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

source = data.cars()

brush = alt.selection(type="interval")

points = (
    alt.Chart(source, width=550)
    .mark_point()
    .encode(
        x="Horsepower:Q",
        y="Miles_per_Gallon:Q",
        color=alt.condition(brush, "Origin:N", alt.value("lightgray")),
    )
    .add_selection(brush)
)

bars = (
    alt.Chart(source, width=550)
    .mark_bar()
    .encode(y="Origin:N", color="Origin:N", x="count(Origin):Q")
    .transform_filter(brush)
)
# autosize=alt.AutoSizeParams(contains="padding" ,type="pad", resize=True))
st._arrow_altair_chart(alt.vconcat(points, bars), theme=SELECTED_THEME, use_container_width=True)

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
        "mark": {"type": "circle"},
        "encoding": {
            "x": {"field": "a", "type": "quantitative"},
            "y": {"field": "b", "type": "quantitative"},
            "size": {"field": "c", "type": "quantitative"},
        },
    },
    theme=SELECTED_THEME,
    use_container_width=True,
)
