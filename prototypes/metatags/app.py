import streamlit as st

st.set_page_config(
    page_title="Meta Tags Prototype",
    page_icon="🔖",
    page_description="This prototype demonstrates a new capability to add meta tags (title, description, image) to the app.",
)

st.title("🔖 Meta Tags Prototype")

st.markdown(
    "This prototype demonstrates a new capability to add meta tags (title, description, image) to Streamlit apps. "
    + "The meta tags are used to create social sharing previews and are used by search engines to improve the search results. "
    + "Every page can have different page meta tags by using the `st.set_page_config` function. "
)

st.markdown(
    "You can try out how this apps social preview looks like [here](https://socialsharepreview.com/). "
    + "**Note**: This currently only works with the [internal app URL](.) on Streamlit Cloud. Please attach `/~/+/` to the URL to see the preview. "
)
