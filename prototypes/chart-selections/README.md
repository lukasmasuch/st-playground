# Selections on Charts - Prototype

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/lukasmasuch/st-playground/main/prototypes/chart-selections/app.py)
[![Open Development Branch](https://img.shields.io/badge/-feature%20branch-blue?style=flat&logo=git&logoColor=white)](https://github.com/LukasMasuch/streamlit/tree/feature/vega-lite-selections)
[![Compare Development Changes](https://img.shields.io/badge/-compare%20changes-blue?style=flat&logo=github&logoColor=white)](https://github.com/streamlit/streamlit/compare/develop...LukasMasuch:feature/vega-lite-selections)

This prototype evaluates adding selection events to `vega_lite` and `altair` charts. This allows reacting to user selections (single/multiple points or areas) on various chart types. The selections need to be added based on the `selection` capabilities of `altair`/`vega_lite` ([documentation](https://altair-viz.github.io/user_guide/interactions.html?highlight=cars)).

## Run locally

_**Requirement**: An installation of [pipenv](https://github.com/pypa/pipenv) is required to run this app locally._

```bash
pipenv install && pipenv run app
```
