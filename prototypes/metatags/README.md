# Metatags Prototype

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/lukasmasuch/st-playground/main/prototypes/metatags/app.py)
[![Open Development Branch](https://img.shields.io/badge/-feature%20branch-blue?style=flat&logo=git&logoColor=white)](https://github.com/LukasMasuch/streamlit/tree/feature/metatags)
[![Compare Development Changes](https://img.shields.io/badge/-compare%20changes-blue?style=flat&logo=github&logoColor=white)](https://github.com/streamlit/streamlit/compare/develop...LukasMasuch:feature/metatags)

This prototype demonstrates a new capability to add meta tags (title, description, image) to Streamlit apps. The meta tags are used to create social sharing previews and are used by search engines to improve the search results. Every page can have different page meta tags by using the `st.set_page_config` function.

## Run locally

_**Requirement**: An installation of [pipenv](https://github.com/pypa/pipenv) is required to run this app locally._

```bash
pipenv install && pipenv run app
```
