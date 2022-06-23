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



icon("🗃")

st.title("Tab Container Prototype")

def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")

@st.experimental_memo
def get_data():
    return pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

if "tabs" not in st.session_state:
    st.session_state["tabs"] = ["Filter Data", "Raw Data", "📈 Chart"]

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
    st.selectbox("Select column", options=["a", "b", "c"])
    st.slider("Filter range", 0, 100, 1)

with tab2:
    st.dataframe(get_data())

with tab3:
    st.line_chart(get_data())
    """)

tabs = st.tabs(st.session_state["tabs"])

with tabs[0]:
    st.selectbox("Select column", options=["a", "b", "c"])
    st.slider("Filter range", 0, 100, 1)

with tabs[1]:
    st.dataframe(get_data(), height=300)

with tabs[2]:
    st.line_chart(get_data())

st.text_input("Foo")

st.markdown("---")

new_tab = st.text_input("Tab label", "New Tab")
if st.button("Add tab"):
    st.session_state["tabs"].append(new_tab)
    st.experimental_rerun()
