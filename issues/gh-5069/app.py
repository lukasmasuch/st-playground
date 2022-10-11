import streamlit as st
import os
import pandas as pd
import numpy as np

script_path = os.path.dirname(os.path.realpath(__file__))

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])


for i in range(20):
    st.markdown("dummy text")

video_file = open(os.path.join(script_path, "myvideo.mp4"), "rb")
video_bytes = video_file.read()

# st.video(video_bytes)

tab1, tab2, tab3 = st.tabs(["tab1", "tab2", "tab3"])

with tab1:
    st.video(video_bytes)
    # st.line_chart(chart_data)
    # st.video("https://www.youtube.com/watch?v=R2nr1uZ8ffc")
    # st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.video(video_bytes)
    with col2:
        st.video(video_bytes)
    # st.line_chart(chart_data)
    # st.video("https://www.youtube.com/watch?v=R2nr1uZ8ffc")
    # st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab3:
    st.video("https://www.youtube.com/watch?v=R2nr1uZ8ffc")

st.markdown("test")

with st.sidebar.container():
    st.video(video_bytes)

st.sidebar.number_input("Number", value=1, min_value=0, max_value=10)
# if st.checkbox("Add more content"):
#     st.video("https://www.youtube.com/watch?v=R2nr1uZ8ffc")


# col1, col2 = st.columns(2)

# with col1:
#     tab1, tab2 = st.tabs(["tab1", "tab2"])

#     with tab1:
#         # st.line_chart(chart_data)
#         st.video("https://www.youtube.com/watch?v=R2nr1uZ8ffc")
#         # st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

#     with tab2:
#         # st.line_chart(chart_data)
#         st.video("https://www.youtube.com/watch?v=R2nr1uZ8ffc")
#         # st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

# with col2:
#     tab1, tab2 = st.tabs(["tab1", "tab2"])

#     with tab1:
#         # st.line_chart(chart_data)
#         st.video("https://www.youtube.com/watch?v=R2nr1uZ8ffc")
#         # st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

#     with tab2:
#         # st.line_chart(chart_data)
#         st.video("https://www.youtube.com/watch?v=R2nr1uZ8ffc")
#         # st.image("https://static.streamlit.io/examples/cat.jpg", width=200)


# with st.container():
#     st.video("https://www.youtube.com/watch?v=R2nr1uZ8ffc")
