# Partial Reruns via Component Groups - Prototype

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/lukasmasuch/st-playground/main/prototypes/partial-reruns/app.py)
[![Open Development Branch](https://img.shields.io/badge/-feature%20branch-blue?style=flat&logo=git&logoColor=white)](https://github.com/LukasMasuch/streamlit/tree/feature/component-groups))
[![Compare Development Changes](https://img.shields.io/badge/-compare%20changes-blue?style=flat&logo=github&logoColor=white)](https://github.com/streamlit/streamlit/compare/develop...LukasMasuch:feature/component-groups)

This prototype demonstrates an early implementation of component groups. Component groups enable partial reruns so that any element interaction within a component group will only rerun a small section of the code instead of the entire script. This allows building interactive forms, couple widgets to a single chart, or on-the-fly fetching capabilities for dataframes and charts (live dashboards). n general, it could help make large apps much faster."

## Run locally

_**Requirement**: An installation of [pipenv](https://github.com/pypa/pipenv) is required to run this app locally._

```bash
pipenv install && pipenv run app
```
