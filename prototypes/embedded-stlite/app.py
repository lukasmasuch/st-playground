import streamlit as st
from streamlit.components.v1 import html

DEFAULT_SNIPPET = """
import streamlit as st

name = st.text_input('Your name')
st.write("Hello,", name or "world")
"""

st_snippet = st.text_area("Write your app:", value=DEFAULT_SNIPPET, height=300)

html(
    f"""
        <!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1, shrink-to-fit=no"
    />
    <title>stlite app</title>
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.14.0/build/stlite.css"
    />
  </head>
  <body>
    <div id="root"></div>
    <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.14.0/build/stlite.js"></script>
    <script>
      if (window.location.search !== "?embed=true") {{
        window.location.search = "?embed=true";
      }}
      stlite.mount(
        `
import streamlit as st

st.markdown('<style>[data-baseweb~="modal"]{{visibility: hidden;}}</style>', unsafe_allow_html=True,)

{st_snippet}
`,
        document.getElementById("root")
      );
    </script>
  </body>
</html>
        """,
    height=600,
    scrolling=True,
)
