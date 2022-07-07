import streamlit as st
import time

import itertools

st.set_page_config(page_title="Partial Reruns - Prototype", page_icon="⛓")


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


icon("⛓")

st.caption("""
This prototype demonstrates an early implementation of component groups. 
Component groups enable partial reruns so that any element interaction within a component group will 
only rerun a small section of the code instead of the entire script. This allows building interactive forms, 
couple widgets to a single chart, or on-the-fly fetching capabilities for dataframes and charts (live dashboards). 
In general, it could help make large apps much faster."
"""
)

st.caption("In this example, the main script is quite slow, but interactions within the component group are very fast since it does not trigger a complete rerun."
)

with st.expander("Show code..."):
    st.code(
    """
import streamlit as st

st.button("Button in main script")

@st.group
def interactive_form():
    # Changes to the selectbox only "reruns" the group function and its widgets
    option = st.selectbox("How would you like to be contacted?", ("Email", "Phone"))
    contact_info = st.text_input(f"Enter {option}")

    if st.button("Submit"):
        # -> results in changed return value which triggers rerun of the app
        return contact_info


with st.expander("Component group with partial rerun", expanded=True):
    interactive_form()

st.text_input(f"Input in main script")
"""
    )

with st.spinner("Doing some work..."):
    time.sleep(3)


if "reruns" not in st.session_state:
    st.session_state.reruns = 0

st.session_state.reruns += 1

st.button("Button in main script")

@st.group
def interactive_form():
    st.caption("Interacting with any of the elements in this group will only rerun the code of this group.")
    # Changes to the selectbox only "reruns" the group function and its widgets
    option = st.selectbox("How would you like to be contacted?", ("Email", "Phone"))
    contact_info = st.text_input(f"Enter {option}")

    if st.button("Submit"):
        # -> results in changed return value which triggers rerun of the app
        return contact_info


with st.expander("Component group with partial rerun", expanded=True):
    interactive_form()

other_input = st.text_input(f"Input in main script")
st.write(f"Reruns of main script: {st.session_state.reruns}")

