from typing import Tuple, Any, Optional, List, Union
import itertools

import pandas as pd
import streamlit as st
from vega_datasets import data

st.set_page_config(page_title="Streamlit Chart Creator", page_icon="📊")


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


HEADER_COLOR_CYCLE = itertools.cycle(
    [
        "#00c0f2",  # light-blue-70",
        "#ffbd45",  # "orange-70",
        "#00d4b1",  # "blue-green-70",
        "#1c83e1",  # "blue-70",
        "#803df5",  # "violet-70",
        "#ff4b4b",  # "red-70",
        "#21c354",  # "green-70",
        "#faca2b",  # "yellow-80",
    ]
)


def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")


def colored_header(label, description=None, color=None):
    """Shows a header with a colored underline and an optional description."""
    space(num_lines=2)
    if color is None:
        color = next(HEADER_COLOR_CYCLE)
    st.subheader(label)
    st.write(
        f'<hr style="background-color: {color}; margin-top: 0; margin-bottom: 0; height: 3px; border: none; border-radius: 3px;">',
        unsafe_allow_html=True,
    )
    if description:
        st.caption(description)


icon("📊")


@st.experimental_memo
def get_dataset(dataset_name: str) -> Tuple[Any, pd.DataFrame]:
    dataset_name = dataset_name.replace("-", "_")
    dataset = getattr(data, dataset_name)
    print(type(dataset))
    return dataset, dataset()


@st.experimental_memo
def get_profiling_report(dataset_name: str):
    _, dataset_df = get_dataset(dataset_name)
    return dataset_df.profile_report()


st.title("Streamlit Chart Creator")

colored_header("🗄 Select Data")

IGNORLIST = [
    "earthquakes",
    "ffox",
    "gimp",
    "graticule",
    "world-110m",
    "us-10m",
    "movies",
    "miserables",
    "londonTubeLines",
    "londonBoroughs",
    "annual-precip",
    "7zip",
]
datasets = data.list_datasets()

datasets = [
    dataset_name
    for dataset_name in data.list_datasets()
    if dataset_name not in IGNORLIST
]

upload_own = "Upload your own dataset"
stocks_wide = "stocks - wide-format"
dataset_options = [upload_own, stocks_wide]
dataset_options.extend(datasets)
selected_dataset_name = st.selectbox(
    "Select a dataset",
    options=dataset_options,
    index=dataset_options.index(str(stocks_wide)),
)

selected_dataset_df = pd.DataFrame()
selected_dataset_code = ""

if selected_dataset_name == upload_own:
    selected_dataset_code = 'return pd.read_csv("PATH_TO_YOUR_CSV", sep=None)'
    uploaded_file = st.file_uploader("Load a CSV file", type="csv")
    if uploaded_file:
        selected_dataset_df = pd.read_csv(uploaded_file, sep=None)
elif selected_dataset_name == stocks_wide:
    selected_dataset_code = 'dataset_df = data.stocks()\n    return dataset_df.pivot(index="date", columns="symbol", values="price")'
    selected_dataset, selected_dataset_df = get_dataset("stocks")

    if selected_dataset.description:
        st.caption(selected_dataset.description)

    selected_dataset_df = selected_dataset_df.pivot(
        index="date", columns="symbol", values="price"
    )
else:
    selected_dataset_code = f"return data.{selected_dataset_name}()"
    selected_dataset, selected_dataset_df = get_dataset(selected_dataset_name)

    if selected_dataset.description:
        st.caption(selected_dataset.description)

col1, col2 = st.columns(2)

with col1:
    st.metric("Number of Rows", value=len(selected_dataset_df))

with col2:
    st.metric("Number of Columns", value=len(selected_dataset_df.columns))

st.dataframe(selected_dataset_df.head(min(len(selected_dataset_df), 1000)))

colored_header("🧮 Transform Data")

data_type_transformations = ""
with st.expander("Change Data Types"):
    st.caption(
        """
"""
    )

    pandas_dtype_options = [
        "object",
        "str",
        "int64",
        "float64",
        "bool",
        "datetime64[year]",
        "datetime64",
        "datetime64[ns]",
        "timedelta[ns]",
        "category",
    ]

    for df_col in selected_dataset_df.columns:
        dtype = selected_dataset_df[df_col].dtype
        extended_options = pandas_dtype_options + [dtype]
        selected_type = st.selectbox(
            f"{df_col}",
            options=extended_options,
            index=pandas_dtype_options.index(str(dtype)),
        )

        if str(selected_dataset_df[df_col].dtype) != selected_type:
            if selected_type == "datetime64[year]":
                selected_dataset_df[df_col] = pd.to_datetime(
                    selected_dataset_df[df_col], format="%Y"
                )
                data_type_transformations += f'\ndataset_df["{df_col}"] = pd.to_datetime(dataset_df["{df_col}"], format="%Y")\n'
            elif selected_type == "datetime64":
                selected_dataset_df[df_col] = pd.to_datetime(
                    selected_dataset_df[df_col], infer_datetime_format=True
                )
                data_type_transformations += f'\ndataset_df["{df_col}"] = pd.to_datetime(dataset_df["{df_col}"])\n'
            else:
                selected_dataset_df[df_col] = selected_dataset_df[df_col].astype(
                    selected_type
                )
                data_type_transformations += f'\ndataset_df["{df_col}"] = dataset_df["{df_col}"].astype("{selected_type}")\n'


melt_df_code = ""

with st.expander("Melt Dataset - convert to long-format"):
    st.caption(
        """
Unpivot a DataFrame from wide to long format, optionally leaving identifiers set.

This function is useful to massage a DataFrame into a format where one or more columns are identifier
variables, while all other columns, considered measured variables, are “unpivoted”
    to the row axis, leaving just two non-identifier columns, variable and value.
"""
    )
    index_name = selected_dataset_df.index.name or "index"
    column_options = [index_name]
    column_options.extend(selected_dataset_df.columns)

    id_vars = st.multiselect(
        "Columns to use as identifier variables", options=column_options
    )
    value_vars = st.multiselect("Columns to unpivot", options=column_options)
    var_name = st.text_input("Name to use for the variable column", value="variable")
    value_name = st.text_input("Name to use for the value column", value="value")

    if id_vars:
        reset_index_code = "dataset_df"
        if index_name in id_vars or index_name in value_vars:
            reset_index_code += ".reset_index()"
            selected_dataset_df = selected_dataset_df.reset_index()
        selected_dataset_df = selected_dataset_df.melt(
            id_vars=id_vars,
            value_vars=value_vars if value_vars else None,
            var_name=var_name,
            value_name=value_name,
        )

        melt_df_code = f"""
dataset_df = {reset_index_code}.melt(
    id_vars={id_vars},
    value_vars={value_vars if value_vars else None},
    var_name="{var_name}",
    value_name="{value_name}",
)
"""

        st.dataframe(selected_dataset_df)


pivot_df_code = ""
with st.expander("Pivot Dataset - convert to wide-format"):
    st.caption(
        """
Return reshaped DataFrame organized by given index / column values.

Reshape data (produce a “pivot” table) based on column values. Uses unique values
from specified index / columns to form axes of the resulting DataFrame. This function
does not support data aggregation, multiple values will result in a MultiIndex in the columns.
"""
    )
    column_options = selected_dataset_df.columns
    index_options = [""]
    index_options.extend(column_options)
    index_column = st.selectbox(
        "Index",
        options=index_options,
        help="Column to use to make new frames index. If None, uses existing index.",
    )
    columns = st.multiselect(
        "Columns",
        options=column_options,
        help="Column to use to make new frames columns.",
    )
    values: Union[List[str], str, None] = st.multiselect(
        "Values",
        options=column_options,
        help="Column(s) to use for populating new frames values. If not specified, all remaining columns will be used and the result will have hierarchically indexed columns.",
    )

    if columns:
        column_code = f"\n    columns={columns},"
        if len(columns) == 1:
            columns = columns[0]
            column_code = f'\n    columns="{columns}",'

        values_code = ""
        if not values:
            values = None
        elif len(values) == 1:
            values = values[0]
            values_code = f'\n    values="{values}",'
        else:
            values_code = f"\n    values={values},"

        index_column_code = ""
        if not index_column:
            index_column = None
        else:
            index_column_code = f'\n    index="{index_column}",'
        selected_dataset_df = selected_dataset_df.pivot(
            index=index_column,
            columns=columns,
            values=values if values else None,
        )

        pivot_df_code = f"""
dataset_df = dataset_df.pivot({index_column_code}{column_code}{values_code}
    values={values if values else None}
)
"""
        st.dataframe(selected_dataset_df)

with st.expander("Dataset Profile"):
    st.markdown("Data types:")
    st.dataframe(selected_dataset_df.dtypes.astype(str))
    st.markdown("---")

    profiling_placeholder = st.empty()

    if profiling_placeholder.button("🔬 Run Profiling"):
        profiling_placeholder.empty()
        from streamlit_pandas_profiling import st_profile_report

        st_profile_report(get_profiling_report(selected_dataset_name))

st.dataframe(selected_dataset_df.head(min(len(selected_dataset_df), 1000)))

colored_header("📈 Create Chart")

col1, col2, col3 = st.columns(3)

with col1:
    options = [""]
    options.extend(selected_dataset_df.columns)
    selected_x = st.selectbox("Select column for x", options=options)
    if not selected_x:
        selected_x = None
with col2:
    selected_y: Optional[str] = st.multiselect(
        "Select columns for y", options=selected_dataset_df.columns
    )
    if not selected_y:
        selected_y = None
    elif len(selected_y) == 1:
        selected_y = selected_y[0]

with col3:
    selected_chart = st.selectbox(
        "Select chart type", options=["line_chart", "area_chart", "bar_chart"]
    )

try:
    chart_command = getattr(st, selected_chart)
    chart_command(
        selected_dataset_df, x=selected_x, y=selected_y, use_container_width=True
    )
except st.StreamlitAPIException as e:
    st.error(e)

colored_header("🪄 Generated Code")

x_parameter = f"\n    x='{selected_x}'," if selected_x else ""
y_parameter = ""
if selected_y and isinstance(selected_y, str):
    y_parameter = f"\n    y='{selected_y}',"
elif selected_y:
    y_parameter = f"\n    y={selected_y},"

st.code(
    f"""
import streamlit as st
import pandas as pd
from vega_datasets import data

@st.experimental_memo
def get_dataset() -> pd.DataFrame:
    {selected_dataset_code}

dataset_df = get_dataset()
{data_type_transformations}{melt_df_code}{pivot_df_code}
st.{selected_chart}(
    dataset_df,{x_parameter}{y_parameter}
    use_container_width=True
)
"""
)
