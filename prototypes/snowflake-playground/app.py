import streamlit as st
from snowflake.snowpark import Session


@st.experimental_singleton
def create_session():
    return Session.builder.configs(st.secrets.snowflake).create()


session = create_session()
st.success("Connected to Snowflake! ❄️")


@st.experimental_memo
def load_data():
    # Get a table.
    table = session.table("SNOWFLAKE_SAMPLE_DATA.TPCDS_SF100TCL.CATALOG_PAGE")

    # Do some computation on it.
    table = table.limit(10)

    # Collect the results. This will run the query and download the data.
    table = table.to_pandas()
    return table


"Here's some example data from `SNOWFLAKE_SAMPLE_DATA.TPCDS_SF100TCL.CATALOG_PAGE`:"
df = load_data()
st.dataframe(df)
