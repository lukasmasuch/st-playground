import streamlit as st
from streamlit.components.v1 import iframe

col1, col2, col3 = st.columns(3)

with col1:
    iframe("https://example-time-series-annotation.streamlit.app/~/+/?embedded=true")
    st.markdown(
        """
<iframe loading="lazy" src="https://example-time-series-annotation.streamlit.app/~/+/?embedded=true" height="700" class="cloud_Iframe__xSBvF" allow="camera;"></iframe>
""",
        unsafe_allow_html=True,
    )


with col2:
    iframe("https://example-time-series-annotation.streamlit.app/?embedded=true")
    st.markdown(
        """
<iframe loading="lazy" src="https://example-time-series-annotation.streamlit.app/?embedded=true" height="700" class="cloud_Iframe__xSBvF" allow="camera;"></iframe>
""",
        unsafe_allow_html=True,
    )
