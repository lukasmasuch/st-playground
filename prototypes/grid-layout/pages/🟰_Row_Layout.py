import numpy as np
import pandas as pd
import streamlit as st
from pages.utils.grid import row

random_df = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])


st.title("🟰 Row Layout Prototype")

with st.expander("Show Docstring"):
    st.help(row)

with st.expander("Show Code"):
    st.code(
        """
row1 = st.row(2, vertical_align="center")
row1.dataframe(random_df, use_container_width=True)
row1.line_chart(random_df, use_container_width=True)

row2 = st.row([2, 4, 1], vertical_align="bottom")

row2.selectbox("Select Country", ["Germany", "Italy", "Japan", "USA"])
row2.text_input("Your name")
row2.button("Send", use_container_width=True)
"""
    )

row1 = row(2, vertical_align="center")
row1.dataframe(random_df, use_container_width=True)
row1.line_chart(random_df, use_container_width=True)

row2 = row([2, 4, 1], vertical_align="bottom")

row2.selectbox("Select Country", ["Germany", "Italy", "Japan", "USA"])
row2.text_input("Your name")
row2.button("Send", use_container_width=True)
