from datetime import date
from typing import List
import pandas as pd
import itertools
import streamlit as st

st.set_page_config(
    page_title="Interactive Data Tables - Playground", page_icon=":abacus:"
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


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
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


@st.experimental_memo
def get_profile_dataset(number_of_items: int = 250) -> pd.DataFrame:
    new_data = []

    def calculate_age(born):
        today = date.today()
        return (
            today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        )

    from faker import Faker

    fake = Faker()
    Faker.seed(0)
    for i in range(number_of_items):
        profile = fake.profile()
        new_data.append(
            {
                "name": profile["name"],
                "avatar": f"https://picsum.photos/400/400?lock={i}",
                "birthdate": profile["birthdate"],
                "age": calculate_age(profile["birthdate"]),
                "website": profile["website"][0],
                "address": profile["address"],
            }
        )
    return pd.DataFrame(new_data)


@st.experimental_memo
def get_random_dataset(number_of_items: int = 500) -> pd.DataFrame:
    import numpy as np
    from faker import Faker
    import random

    fake = Faker()
    Faker.seed(0)

    fake_sentences = [fake.sentence(nb_words=10) for _ in range(1000)]

    dataset = {}
    dataset["numbers"] = np.random.randint(0, 1000000, size=number_of_items)
    dataset["booleans"] = np.random.randint(0, 2, size=number_of_items)
    dataset["strings"] = [random.choice(fake_sentences) for _ in range(number_of_items)]
    dataset["numbers2"] = np.random.randint(0, 1000000, size=number_of_items)
    dataset["numbers3"] = np.random.randint(0, 1000000, size=number_of_items)
    dataset["numbers4"] = np.random.randint(0, 1000000, size=number_of_items)

    df = pd.DataFrame.from_dict(dataset)
    df["booleans"] = df["booleans"].astype(bool)
    return df


@st.experimental_memo
def get_titanic_dataset() -> pd.DataFrame:
    titanic_df = pd.read_csv(
        "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    )
    titanic_df["Survived"] = titanic_df["Survived"].astype(bool)
    titanic_df["Age"] = titanic_df["Age"].fillna(0).astype(int)
    titanic_df = titanic_df.drop(columns=["PassengerId"])
    return titanic_df


icon("🧮")

st.title("Interactive Data Tables")


with st.expander("Content Overview"):
    st.markdown(
        """
- [⚙️ Installation](#installation)
- [🧮 Interactive Data Table: `st.dataframe`](#interactive-data-table-st-dataframe)
    - [✨ New look & feel](#new-look-feel)
    - [☝🏽 On click event via callback](#on-click-event-via-callback)
    - [☝🏽 On click event via state](#on-click-event-via-state)
    - [☑️ On select event via callback](#on-select-event-via-callback)
    - [☑️ On select event via state](#on-select-event-via-state)
    - [🔎 Built-in search](#built-in-search)
    - [📤 Copy to clipboard](#copy-to-clipboard)
- [⚡️ Editable Data Table: `st.data_editor`](#editable-data-table-st-data-editor)
    - [✏️ Edit cells & add rows](#edit-cells-add-rows)
    - [📝 Edit a list of strings](#edit-a-list-of-strings)
    - [📝 Edit a list of dictionaries](#edit-a-list-of-dictionaries)
    - [🎚 Customize column width & title](#customize-column-width-title)
    - [🖼️ Render images & urls](#render-images-urls)
    - [➡️ Row selection event](#row-selection-event)
    - [⬇️ Column selection event](#column-selection-event)
    - [🔲 Cell selection event](#cell-selection-event)
    - [↕️ Multi row/column selection event](#multi-row-column-selection-event)
    - [📋 Compatible with st.form](#compatible-with-st-form)
    - [📥 Paste from clipboard](#paste-from-clipboard)
- [↔️ Comparison with current version](#comparison-with-current-version)
- [🚧 Known limitiations & issues](#known-limitiations-issues)
"""
    )

st.info(
    "This playground contains a large number of tables which slows down the overall performance. You can find another demo with a single table [here](https://share.streamlit.io/lukasmasuch/st-dataframe-playground/main/single-table-app.py)."
)

space(2)

st.header("⚙️ Installation")

st.markdown(
    "To install the Streamlit version that includes these prototypes on your machine, execute:"
)

st.code(
    """
pip install -U https://core-previews.s3-us-west-2.amazonaws.com/hackathon-q1-2022-preview/streamlit-1.5.0-py2.py3-none-any.whl
""",
    language="bash",
)

st.markdown(
    "If you want to deploy an app with this streamlit version to Streamlit Cloud, add the following line to the `requirements.txt` file in the root of your repo:"
)

st.code(
    """
https://core-previews.s3-us-west-2.amazonaws.com/hackathon-q1-2022-preview/streamlit-1.5.0-py2.py3-none-any.whl
""",
    language="plain",
)

space(4)

st.header("🧮 Interactive Data Table: `st.dataframe`")

st.markdown(
    "This new data table component is a rebuild of the existing read-only `st.dataframe` component and provides a couple of improvements and new features such as click events. "
    "Our goal is to reach feature parity to the existing `st.dataframe` implementation. Some features are still not finalized in this prototype such as column sorting or support for pandas styler."
)

with st.expander("Method documentation"):
    st.markdown(
        """
```python
st.dataframe(
    data: Optional[Union[pandas.DataFrame, Iterable, dict]] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    key: Optional[Union[str, int]] = None,
    on_click: Optional[Union[Callback, bool]] = None,
    on_select: Optional[Union[Callback, bool]] = None,
    args: Optional[Tuple[Any, ...]] = None,
    kwargs: Optional[Dict[str, Any]] = None,
) → DeltaGenerator
```

Display a dataframe as an interactive table.

**Args:**

- <b>`data`</b>:  The data to display.
- <b>`width`</b>: Desired width of the UI element expressed in pixels. If `None`, a default width based on the page width is used.
- <b>`height`</b>: Desired height of the UI element expressed in pixels. If `None`, a default height is used.
- <b>`key`</b>: An optional string or integer to use as the unique key for the widget. If this is omitted, a key will be generated for the widget 
        based on its content. Multiple widgets of the same type may not share the same key.
- <b>`on_click`</b>: An optional callback invoked when the user clicks on a cell. The click event can also be activated by passing `True` as the value.
    Thereby, the value is only accesible from the state. The state is cleared after rerun. 
    The click event (stored in the sessions state) is a `NamedTuple` containing the following fields: `row`, `column`, and `value`.
- <b>`on_select`</b>: An optional callback invoked when the user selects a cell. The cell selection can also be activated by passing `True` as the value.
    Thereby, the value is only accesible from the state. The selection is persisted in the session state.
    The selection event (stored in the sessions state) is a `NamedTuple` containing the following fields: `row`, `column`, and `value`.
- <b>`args`</b>: An optional tuple of args to pass to the callback.
- <b>`kwargs`</b>: An optional dict of kwargs to pass to the callback.
""",
        unsafe_allow_html=True,
    )

colored_header(
    "✨ New look & feel",
    description="The new data table component is rebuild from ground-up and comes with a new UI/UX. It allows to resize columns and the table heigth, displays the data type, has improved data renderers & performance, and a lot more...",
)

st.caption(
    "_**Note:** You can double click on any cell to see the full content. You can also try to resize columns & the table height (works only on Chrome and Firefox) or try to use differnt Streamlit themes._"
)

with st.expander("Code Snippet"):
    st.code(
        """
st.dataframe(my_dataframe, key="my_dataframe")
""",
        language="python",
    )

st.dataframe(get_titanic_dataset()[550:], key="my_dataframe")

colored_header(
    "☝🏽 On click event via callback",
    description="Provide a callback function to `on_click` to interact with the data. This will store events as `NamedTuple` in the `st.session_state` for the given key. The click is only fired once - similar to `st.button`, use `on_select` for a stateful interaction. You can supply `args` and `kwargs` the same way as its done with [existing event callbacks](https://docs.streamlit.io/library/api-reference/session-state#use-callbacks-to-update-session-state).",
)

with st.expander("Code Snippet"):
    st.code(
        """
def my_click_callback():
    click_event = st.session_state.on_click_callback
    if click_event:
        st.write(
            f"Clicked on {click_event.row} (row) / {click_event.column} (column) with value: {click_event.value}"
        )

st.dataframe(my_dataframe, on_click=my_click_callback, key="on_click_callback")
""",
        language="python",
    )


def my_click_callback():
    click_event = st.session_state.on_click_callback
    if click_event:
        st.write(
            f"Clicked on {click_event.row} (row) / {click_event.column} (column) with value: {click_event.value}"
        )


st.dataframe(get_titanic_dataset(), on_click=my_click_callback, key="on_click_callback")

colored_header(
    "☝🏽 On click event via state",
    description="Activate `on_click` events by setting it to `True`. This will store events as `NamedTuple` in the `st.session_state` for the given key. The click is only fired once - similar to `st.button`, use `on_select` for a stateful interaction.",
)

with st.expander("Code Snippet"):
    st.code(
        """
st.dataframe(my_dataframe, on_click=True, key="on_click_state")

click_event = st.session_state.on_click_state
if click_event:
    st.write(
        f"Clicked on {click_event.row} (row) / {click_event.column} (column) with value: {click_event.value}"
    )
""",
        language="python",
    )


st.dataframe(get_titanic_dataset()[500:], on_click=True, key="on_click_state")
click_event = st.session_state.on_click_state
if click_event:
    st.write(
        f"Clicked on {click_event.row} (row) / {click_event.column} (column) with value: {click_event.value}"
    )

colored_header(
    "☑️ On select event via callback",
    description="Provide a callback function to `on_select` to react to cell selections. This will store events as `NamedTuple` in the `st.session_state` for the given key. In comparison with `on_click`, the selection event in the session state is persisted (stateful interaction). "
    "You can supply `args` and `kwargs` the same way as its done with [existing event callbacks](https://docs.streamlit.io/library/api-reference/session-state#use-callbacks-to-update-session-state).",
)

with st.expander("Code Snippet"):
    st.code(
        """
def my_select_callback():
    select_event = st.session_state.on_select_callback
    if select_event:
        st.write(
            f"Selected {select_event.row} (row) / {select_event.column} (column) with value: {select_event.value}"
        )


st.dataframe(
    my_dataframe, on_select=my_select_callback, key="on_select_callback"
)
""",
        language="python",
    )


def my_select_callback():
    select_event = st.session_state.on_select_callback
    if select_event:
        st.write(
            f"Selected {select_event.row} (row) / {select_event.column} (column) with value: {select_event.value}"
        )


st.dataframe(
    get_titanic_dataset()[499:], on_select=my_select_callback, key="on_select_callback"
)

colored_header(
    "☑️ On select event via state",
    description="Activate `on_select` events by setting it to `True`. This will store events as `NamedTuple` in the `st.session_state` for the given key. In comparison with `on_click`, the selection event in the session state is persisted (stateful interaction).",
)

with st.expander("Code Snippet"):
    st.code(
        """
st.dataframe(my_dataframe, on_select=True, key="on_select_state")

select_event = st.session_state.on_select_state
if select_event:
    st.write(
        f"Selected {select_event.row} (row) / {select_event.column} (column) with value: {select_event.value}"
    )
""",
        language="python",
    )

st.dataframe(get_titanic_dataset()[498:], on_select=True, key="on_select_state")

select_event = st.session_state.on_select_state
if select_event:
    st.write(
        f"Selected {select_event.row} (row) / {select_event.column} (column) with value: {select_event.value}"
    )


colored_header(
    "🔎 Built-in search",
    description="Search for any data within the table by pressing `Ctrl`/`⌘` + `f`. Make sure you are focused on the table when pressing the hotkey.",
)

st.caption(
    "_**Note:** There is currently an issue with the built-in search. The search hotkey also triggers the search overlay for other tables on the same page._"
)

with st.expander("Code Snippet"):
    st.code(
        """
st.dataframe(my_dataframe, key="search_example")
""",
        language="python",
    )

st.dataframe(
    get_profile_dataset(),
    columns={
        "avatar": {"type": "image"},
        "website": {"type": "url"},
    },
    key="built_in_search",
)

colored_header(
    "📤 Copy to clipboard",
    description="Copy data from this data table and paste it into applications such as Excel or Google Sheets.",
)

st.warning("This feature does not seem to work with apps deployed in Streamlit Cloud.")

with st.expander("Code Snippet"):
    st.code(
        """
st.dataframe(
    ["button", "selectbox", "dataframe", "slider"],
    key="copy_demo",
)
""",
        language="python",
    )
st.dataframe(
    ["button", "selectbox", "dataframe", "slider"],
    columns={0: {"title": "Streamlit Widgets"}},
    key="copy_demo",
)


space(4)

st.header("⚡️ Editable Data Table: `st.data_editor`")

st.markdown(
    "The editable data table - `st.data_editor` - is an experimental input widget that allows to edit table structures. The main purpose of the current prototype is to evaluate various features and test technical limitations. "
    " It is not decided yet in what form or when an editable data table migth be released."
)

with st.expander("Method documentation"):
    st.markdown(
        """
```python
st.data_editor(
    data: Optional[Union[pandas.DataFrame, list]] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    key: Optional[Union[str, int]] = None,
    on_selection_change: Optional[Union[Callable, List[Callable]]] = None,
    columns: Optional[Dict[Union[int, str], dict]] = None,
    editable: bool = True,
    args: Optional[Tuple[Any, ...]] = None,
    kwargs: Optional[Dict[str, Any]] = None,
) → Union[pandas.DataFrame, list]
```

Display an editable table input widget.

**Arguments:**

- <b>`data`</b>:  The data to display.
- <b>`width`</b>: Desired width of the UI element expressed in pixels. If `None`, a default width based on the page width is used.
- <b>`height`</b>: Desired height of the UI element expressed in pixels. If `None`, a default height is used.
- <b>`key`</b>: An optional string or integer to use as the unique key for the widget. If this is omitted, a key will be generated for the widget 
        based on its content. Multiple widgets of the same type may not share the same key.
- <b>`on_selection_change`</b>: An optional callback or list of callbacks to invoke when the user selects rows, columns or cells.
    The callback is required to have any of the following parameters: `cell`, `row`, `column`, `rows`, `columns`. 
    When you provide a callback for columns, rows, or cells, the respective selection capabilities is activated.
    The value of the selection is passed to the respective callback parameter. 
    If a selection is cleared, `None` or empty list is passed to the paramter
- <b>`columns`</b>: Allows to configure how table columns are displayed.
    It is a mapping of column names or indexes to a dict that contains configuration options. Use `*` for configurations to all columns.
    The following configuration options are supported: `title` (change column title), `width` (set column width), `editable` (set column as editable), `type` (set column data type).
- <b>`editable`</b>: Determines if the table is editable or read-only.
- <b>`args`</b>: An optional tuple of args to pass to the callback.
- <b>`kwargs`</b>: An optional dict of kwargs to pass to the callback.

**Returns:**

- `Union[pandas.DataFrame, list]`: The edited data structure.
""",
        unsafe_allow_html=True,
    )

colored_header(
    "✏️ Edit cells & add rows",
    description="The `st.data_editor` can be used as an input widget since it allows to edit cells and add rows. It returns and edited version of the inital data.",
)

st.caption(
    "_**Note:** Some data types - e.g. datetime - do not support editing in this version._"
)

with st.expander("Code Snippet"):
    st.code(
        """
edited_df = st.data_editor(my_dataframe)

st.write(edited_df)
""",
        language="python",
    )

edited_df = st.data_editor(get_titanic_dataset(), key="editable_demo")

st.write(edited_df)


colored_header(
    "📝 Edit a list of strings",
    description="Besides dataframes, the `st.data_editor` also supports editing other data structures such as a list of strings.",
)

st.caption(
    "_**Note:** It is not possible with this version to start with an empty list as the inital value._"
)

with st.expander("Code Snippet"):
    st.code(
        """
edited_list = st.data_editor(
    ["button", "selectbox", "dataframe", "slider"],
    columns={0: {"title": "Streamlit Widgets"}}
)

st.write("Edited list:", edited_list)
""",
        language="python",
    )

edited_list = st.data_editor(
    ["button", "selectbox", "dataframe", "slider"],
    columns={0: {"title": "Streamlit Widgets"}},
)
st.write("Edited list:", edited_list)

colored_header(
    "📝 Edit a list of dictionaries",
    description="The `st.data_editor` can also be used to edit a list of dictionaries.",
)

st.caption(
    "_**Note:** It is not possible with this version to start with an empty list as the inital value._"
)

with st.expander("Code Snippet"):
    st.code(
        """
edited_list = st.data_editor(
    [
        {
            "repo": "streamlit/streamlit",
            "stars": 176000,
            "awesome": True,
        }
    ]
)

st.write("Edited list:", edited_list)
""",
        language="python",
    )

edited_list = st.data_editor(
    [
        {
            "repo": "streamlit/streamlit",
            "stars": 176000,
            "awesome": True,
        }
    ],
)

st.write("Edited list:", edited_list)

colored_header(
    "🎚 Customize column width & title",
    description="The `columns` configuration allows to customize the `width` and/or `title` of a column. A column can be specified via its name or index. To apply modifications for all columns, use the `*`.",
)

with st.expander("Code Snippet"):
    st.code(
        """
st.data_editor(
    get_titanic_dataset(),
    columns={
        "*": {"width": 100},
        0: {"width": 95},
        "Name": {"width": 200},
        "Pclass": {"title": "Class", "width": 70},
        "SibSp": {"title": "Siblings/Spouse Onboard", "width": 70},
        "Parch": {"title": "Parents/Children Onboard", "width": 70},
    },
)
""",
        language="python",
    )

st.data_editor(
    get_titanic_dataset(),
    columns={
        "*": {"width": 100},
        0: {"width": 95},
        "Name": {"width": 200},
        "Pclass": {"title": "Class", "width": 70},
        "SibSp": {"title": "Siblings/Spouse Onboard", "width": 70},
        "Parch": {"title": "Parents/Children Onboard", "width": 70},
    },
)

colored_header(
    "🖼️ Render images & urls",
    description="The `columns` configuration allows to render values as images or URLs via the `type` property. A column can be specified via its name or index.",
)

with st.expander("Code Snippet"):
    st.code(
        """
st.data_editor(
    [
        {
            "name": "Streamlit",
            "website": "https://streamlit.io",
            "logo": "data:image/svg+xml,%3Csvg fill='none' xmlns='http://www.w3.org/2000/svg' alt='Streamlit Logo. Click to go back to the home page.' viewBox='0 0 301 165' class='max-h-5 w-auto'%3E%3Cpath d='M150.731 101.547l-52.592-27.8-91.292-48.25c-.084-.083-.25-.083-.334-.083-3.333-1.584-6.75 1.75-5.5 5.083L47.53 149.139l.008.025c.05.117.092.233.142.35 1.909 4.425 6.075 7.158 10.609 8.233.383.084.657.159 1.117.251.459.102 1.1.241 1.65.283.09.008.174.008.266.016h.067c.066.009.133.009.2.017h.091c.059.008.125.008.184.008h.108c.067.009.133.009.2.009a817.728 817.728 0 00177.259 0c.708 0 1.4-.034 2.066-.1l.634-.075c.025-.009.058-.009.083-.017.142-.017.283-.042.425-.067.208-.025.417-.066.625-.108.417-.092.606-.158 1.172-.353.565-.194 1.504-.534 2.091-.817.588-.283.995-.555 1.487-.863a26.566 26.566 0 001.774-1.216c.253-.194.426-.318.609-.493l-.1-.058-99.566-52.617z' fill='%23FF4B4B'%3E%3C/path%3E%3Cpath d='M294.766 25.498h-.083l-91.326 48.25 50.767 75.609 46.4-118.859v-.167c1.167-3.5-2.416-6.666-5.758-4.833' fill='%237D353B'%3E%3C/path%3E%3Cpath d='M155.598 2.556c-2.334-3.409-7.417-3.409-9.667 0L98.139 73.748l52.592 27.8 99.667 52.674c.626-.613 1.128-1.21 1.658-1.841a20.98 20.98 0 002.067-3.025l-50.767-75.608-47.758-71.192z' fill='%23BD4043'%3E%3C/path%3E%3C/svg%3E",
        },        
        {
            "name": "Python",
            "website": "https://www.python.org",
            "logo": "https://upload.wikimedia.org/wikipedia/commons/f/f8/Python_logo_and_wordmark.svg",
        },
    ],
    columns={
        "logo": {"type": "image"},
        "website": {"type": "url"},
    },
)
""",
        language="python",
    )

st.data_editor(
    [
        {
            "name": "Streamlit",
            "website": "https://streamlit.io",
            "logo": "data:image/svg+xml,%3Csvg fill='none' xmlns='http://www.w3.org/2000/svg' alt='Streamlit Logo. Click to go back to the home page.' viewBox='0 0 301 165' class='max-h-5 w-auto'%3E%3Cpath d='M150.731 101.547l-52.592-27.8-91.292-48.25c-.084-.083-.25-.083-.334-.083-3.333-1.584-6.75 1.75-5.5 5.083L47.53 149.139l.008.025c.05.117.092.233.142.35 1.909 4.425 6.075 7.158 10.609 8.233.383.084.657.159 1.117.251.459.102 1.1.241 1.65.283.09.008.174.008.266.016h.067c.066.009.133.009.2.017h.091c.059.008.125.008.184.008h.108c.067.009.133.009.2.009a817.728 817.728 0 00177.259 0c.708 0 1.4-.034 2.066-.1l.634-.075c.025-.009.058-.009.083-.017.142-.017.283-.042.425-.067.208-.025.417-.066.625-.108.417-.092.606-.158 1.172-.353.565-.194 1.504-.534 2.091-.817.588-.283.995-.555 1.487-.863a26.566 26.566 0 001.774-1.216c.253-.194.426-.318.609-.493l-.1-.058-99.566-52.617z' fill='%23FF4B4B'%3E%3C/path%3E%3Cpath d='M294.766 25.498h-.083l-91.326 48.25 50.767 75.609 46.4-118.859v-.167c1.167-3.5-2.416-6.666-5.758-4.833' fill='%237D353B'%3E%3C/path%3E%3Cpath d='M155.598 2.556c-2.334-3.409-7.417-3.409-9.667 0L98.139 73.748l52.592 27.8 99.667 52.674c.626-.613 1.128-1.21 1.658-1.841a20.98 20.98 0 002.067-3.025l-50.767-75.608-47.758-71.192z' fill='%23BD4043'%3E%3C/path%3E%3C/svg%3E",
        },
        {
            "name": "Python",
            "website": "https://www.python.org",
            "logo": "https://upload.wikimedia.org/wikipedia/commons/f/f8/Python_logo_and_wordmark.svg",
        },
    ],
    columns={
        "logo": {"type": "image"},
        "website": {"type": "url"},
    },
)

colored_header(
    "➡️ Row selection event",
    description="The `st.data_editor` allows to react to row selections. Pass a callback with the parameter `row` to `on_selection_change` to activate row selection.",
)

st.caption(
    "_**Note:** There is an issue with the frontend component that prevents to enforce the selection of a only a single row._"
)

with st.expander("Code Snippet"):
    st.code(
        """
def my_row_selection_callback(row):
    if row:
        st.write(f"Selected row {row.row} with value:")
        st.json(row.value.to_dict())

st.data_editor(my_dataframe, on_selection_change=my_row_selection_callback)
""",
        language="python",
    )


def my_row_selection_callback(row):
    if row:
        st.write(f"Selected row {row.row} with value:")
        st.json(row.value.to_dict())


st.data_editor(
    get_titanic_dataset(),
    on_selection_change=my_row_selection_callback,
    editable=False,
    key="row_selection",
)

colored_header(
    "⬇️ Column selection event",
    description="The `st.data_editor` allows to react to column selections. Pass a callback with the parameter `column` to `on_selection_change` to activate column selection.",
)

st.caption(
    "_**Note:** There is an issue with the frontend component that prevents to enforce the selection of a only a single column._"
)

with st.expander("Code Snippet"):
    st.code(
        """
def my_column_selection_callback(column):
    if column:
        st.write(f"Selected column {column.column} with name {column.name}")

st.data_editor(
    my_dataframe,
    on_selection_change=my_column_selection_callback,
    key="column_selection",
)
""",
        language="python",
    )


def my_column_selection_callback(column):
    if column:
        st.write(f"Selected column {column.column} with name {column.name}")


st.data_editor(
    get_titanic_dataset(),
    on_selection_change=my_column_selection_callback,
    editable=False,
    key="column_selection",
)

colored_header(
    "🔲 Cell selection event",
    description="The `st.data_editor` allows to react to cell selections. Pass a callback with the parameter `cell` to `on_selection_change` to activate cell selection.",
)

with st.expander("Code Snippet"):
    st.code(
        """
def my_cell_selection_callback(cell):
    if cell:
        st.write(
            f"Selected {cell.row} (row) / {cell.column} (column) with value: {cell.value}"
        )

st.data_editor(
    my_dataframe,
    on_selection_change=my_cell_selection_callback,
)
""",
        language="python",
    )


def my_cell_selection_callback(cell):
    if cell:
        st.write(
            f"Selected {cell.row} (row) / {cell.column} (column) with value: {cell.value}"
        )


st.data_editor(
    get_titanic_dataset(),
    on_selection_change=my_cell_selection_callback,
    editable=False,
    key="cell_selection",
)

colored_header(
    "↕️ Multi row/column selection event",
    description="The `st.data_editor` also supports multi row/column selection events. Pass a callback with a parameter called `rows` / `columns` to activate multi selection. "
    "To select multiple rows/columns, hold the `Shift` or `Ctrl`/`⌘` while clicking on the row/column. This example also shows that you can combine multiple callbacks.",
)


st.caption(
    "_**Note:** The multi selection is only possible with columns and rows. Selection of multiple cells is not supported._"
)

with st.expander("Code Snippet"):
    st.code(
        """
def rows_selection_callback(rows):
    st.write(f"Selected {len(rows)} rows: " + ", ".join(str(row.row) for row in rows))

def columns_selection_callback(columns):
    st.write(
        f"Selected {len(columns)} columns: "
        + ", ".join(str(column.column) for column in columns)
    )

st.data_editor(
    my_dataframe,
    on_selection_change=[rows_selection_callback, columns_selection_callback],
)
""",
        language="python",
    )


def rows_selection_callback(rows):
    st.write(f"Selected {len(rows)} rows: " + ", ".join(str(row.row) for row in rows))


def columns_selection_callback(columns):
    st.write(
        f"Selected {len(columns)} columns: "
        + ", ".join(str(column.column) for column in columns)
    )


st.data_editor(
    get_titanic_dataset(),
    on_selection_change=[rows_selection_callback, columns_selection_callback],
    editable=False,
    key="multi_selection",
)

colored_header(
    "📋 Compatible with st.form",
    description="The `st.data_editor` can be used inside a `st.form`. This is useful if you want to allow frequent edits to the data without impacting the user experience.",
)

with st.expander("Code Snippet"):
    st.code(
        """
with st.form("my_form"):
    edited_df = st.data_editor(my_dataframe)
    submitted = st.form_submit_button("Submit")

if submitted:
    st.write("Edited dataframe:", edited_df)
""",
        language="python",
    )

with st.form("my_form"):
    edited_df = st.data_editor(get_profile_dataset())
    submitted = st.form_submit_button("Submit")

if submitted:
    st.write("Edited dataframe:", edited_df)

colored_header(
    "📥 Paste from clipboard",
    description="Copy data from [this Googel Sheets document](https://docs.google.com/spreadsheets/d/1x6wQgOaGfb97ocFcFKb5c41F_TXnwbcdWWAV9jY--eQ/edit?usp=sharing) to clipboard and paste it into the data editor. This supports the copy format of Google Sheets and Excel.",
)

st.caption(
    "_**Note:** In this version, pasting data does not automatically add rows. It only overwrites the data of existing rows._"
)

st.warning("This feature does not seem to work with apps deployed in Streamlit Cloud.")

with st.expander("Code Snippet"):
    st.code(
        """
edited_df = st.data_editor(my_dataframe)
st.write("Edited dataframe:", edited_df)
""",
        language="python",
    )
edited_df = st.data_editor(get_profile_dataset(), key="paste_demo")
st.write("Edited dataframe:", edited_df)


colored_header(
    "↔️ Comparison with current version",
    description="Both components can handle large amount of data. The new component has an improved scrolling UX and switches to a performance-optimized scrolling behavior if the table has more than 100k rows.",
)

number_of_rows = st.slider(
    "Number of rows", min_value=10, max_value=1000000, value=100000
)
if st.button("Compare components"):
    dataset_for_comparison = get_random_dataset(number_of_rows)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("New `st.dataframe` component:")
        st.dataframe(dataset_for_comparison, key="component_comparison", height=300)

    with col2:
        st.markdown("Current `st.dataframe` component:")
        st.dataframe(dataset_for_comparison, height=300)

colored_header(
    "🚧 Known limitiations & issues",
    description="Collection of known limitations and issues with the interactive `st.dataframe` and `st.data_editor` components.",
)

st.dataframe(
    [
        {
            "description": "The hotkey for the built-in search also opens the search box for other tables on the same page.",
            "feature": ["built-in search"],
            "component": ["st.dataframe", "st.data_editor"],
        },
        {
            "description": "Column-based sorting is currently not implemented.",
            "feature": ["sorting"],
            "component": ["st.dataframe", "st.data_editor"],
        },
        {
            "description": "Column-based filtering is currently not implemented.",
            "feature": ["filtering"],
            "component": ["st.dataframe", "st.data_editor"],
        },
        {
            "description": "Fullscreen mode is buggy with interactive events and editing.",
            "feature": ["fullscreen"],
            "component": ["st.dataframe", "st.data_editor"],
        },
        {
            "description": "It's currently not possible to enforce single selection for rows and columns.",
            "feature": ["selection-events"],
            "component": ["st.data_editor"],
        },
        {
            "description": "Clearing selection is only supported via hotkey (`Escape`). Therefore, the selection cannot be cleared on mobile.",
            "feature": ["selection-events"],
            "component": ["st.data_editor", "st.dataframe"],
        },
        {
            "description": "Click events also select the cells on the frontend. There is no way currently to only support click events without the selction frame.",
            "feature": ["selection-events"],
            "component": ["st.dataframe"],
        },
        {
            "description": "Adding rows via `st.add_rows` is buggy in combination with interactive events and editing.",
            "feature": ["add-rows"],
            "component": ["st.dataframe", "st.data_editor", "st.add_rows"],
        },
        {
            "description": "Date, time, or datetime cells cannot be edited.",
            "feature": ["cell-editing"],
            "component": ["st.data_editor"],
        },
        {
            "description": "Image cells cannot be edited.",
            "feature": ["cell-editing"],
            "component": ["st.data_editor"],
        },
        {
            "description": "Custom pandas index is currently not supported/tested.",
            "feature": ["index"],
            "component": ["st.dataframe", "st.data_editor"],
        },
        {
            "description": "The resize icon does not appear in Safari.",
            "feature": ["height-resize"],
            "component": ["st.dataframe", "st.data_editor"],
        },
        {
            "description": "Native support for row deletion is not implemented.",
            "feature": ["row-deletion"],
            "component": ["st.data_editor"],
        },
        {
            "description": "Paste from clipboard does not automatically create additional rows.",
            "feature": ["paste-clipboard"],
            "component": ["st.data_editor"],
        },
        {
            "description": "The hover effect of the new row cell does not work sometimes.",
            "feature": ["row-addition"],
            "component": ["st.data_editor"],
        },
        {
            "description": "The key of `st.dataframe` is currently not correctly applied. This might cause a duplicated widget ID.",
            "feature": [],
            "component": ["st.dataframe"],
        },
        {
            "description": "Some cell editors (e.g. number, ID) do not work properly with different themes.",
            "feature": ["theming"],
            "component": ["st.dataframe"],
        },
    ],
    key="known_limitations",
)