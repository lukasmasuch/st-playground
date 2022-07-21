import itertools

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Streamlit Theme for Charts", page_icon="🗃")


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


icon("🗃")

st.title("Tab Container Prototype")

def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")

@st.experimental_memo
def get_data():
    return pd.DataFrame(np.random.randn(20, 5), columns=["a", "b", "c", "d", "e"])

if "tabs" not in st.session_state:
    st.session_state["tabs"] = ["Filter Data", "Raw Data", "📈 Chart"]

if "tabs_sidebar" not in st.session_state:
    st.session_state["tabs_sidebar"] = False

with st.expander("Show code"):
    st.code("""
import streamlit as st
import pandas as pd
import numpy as np

@st.experimental_memo
def get_data():
    return pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

tab1, tab2, tab3 = st.tabs(["Filter Data", "Raw Data", "📈 Chart"])

with tab1:
    col = st.selectbox("Select column", options=["a", "b", "c"])
    filter = st.slider("Filter range", -2.5, 2.5, (-2.0, 2.0), step=0.01)
    filter_query = f"{filter[0]} < {col} < {filter[1]}"

with tab2:
    st.dataframe(get_data().query(filter_query))

with tab3:
    st.line_chart(get_data().query(filter_query))
    """)

tabs = st.tabs(st.session_state["tabs"])

with tabs[0]:
    col = st.selectbox("Select column", options=["a", "b", "c"])
    filter = st.slider("Filter range", -2.5, 2.5, (-2.0, 2.0), step=0.01)
    filter_query = f"{filter[0]} < {col} < {filter[1]}"

with tabs[1]:
    st.dataframe(get_data().query(filter_query), height=300)

with tabs[2]:
    st.line_chart(get_data().query(filter_query))

if  st.session_state["tabs_sidebar"]:
    tab1, tab2 = st.sidebar.tabs(["Tab 1", "Tab 2"])
    data = np.random.randn(10, 1)

    tab1.write("this is tab 1")

    tab2.write("this is tab 2")

space(num_lines=2)

colored_header("Tabs Configruations")

new_tab = st.text_input("Tab label", "New Tab")
if st.button("Add tab"):
    st.session_state["tabs"].append(new_tab)
    st.experimental_rerun()

if st.button("Add tabs container to sidebar"):
    st.session_state["tabs_sidebar"] = True
    st.experimental_rerun()
