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

@st.experimental_memo
def get_data():
    return pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

tab1, tab2, tab3 = st.tabs(["Filter Data", "Raw Data", "📈 Chart"])

with tab1:
    st.selectbox("Select column", options=["a", "b", "c"])
    st.slider("Filter range", 0, 100, 1)

with tab2:
    st.dataframe(get_data(), height=300)

with tab3:
    st.line_chart(get_data())
