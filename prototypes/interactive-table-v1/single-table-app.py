from datetime import date
from typing import List
import pandas as pd
import itertools
import streamlit as st

st.set_page_config(page_title="Single Data Table - Demo", page_icon=":abacus:")


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


@st.experimental_memo
def get_profile_dataset(number_of_items: int = 250) -> pd.DataFrame:
    new_data = []

    def calculate_age(born):
        today = date.today()
        return (
            today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        )

    import random
    from faker import Faker

    fake = Faker()
    Faker.seed(0)
    for i in range(min(number_of_items, 1000)):
        profile = fake.profile()
        new_data.append(
            {
                "name": profile["name"],
                "avatar": f"https://picsum.photos/200/200?lock={i}",
                "birthdate": profile["birthdate"],
                "age": calculate_age(profile["birthdate"]),
                "website": profile["website"][0],
                "address": profile["address"],
            }
        )

    if len(new_data) < number_of_items:
        # Pick random items from the generated data
        new_data = [random.choice(new_data) for _ in range(number_of_items)]

    return pd.DataFrame(new_data)


icon("🧮")

st.title("Interactive Data Table Demo")

write_dg = st.empty()
write_dg.write("Nothing selected.")


def rows_selection_callback(rows):
    write_dg.write(
        f"Selected {len(rows)} rows: " + ", ".join(str(row.row) for row in rows)
    )


def columns_selection_callback(columns):
    write_dg.write(
        f"Selected {len(columns)} columns: "
        + ", ".join(str(column.column) for column in columns)
    )


def my_cell_selection_callback(cell):
    if cell:
        write_dg.write(
            f"Selected 1 cell {cell.row} (row) / {cell.column} (column) with value: {cell.value}"
        )


edited_df = st.data_editor(
    get_profile_dataset(2500),
    columns={
        "avatar": {"type": "image"},
        "website": {"type": "url"},
    },
    on_selection_change=[
        rows_selection_callback,
        columns_selection_callback,
        my_cell_selection_callback,
    ],
    key="singple_table_example",
)

st.subheader("Edited Dataframe")

st.dataframe(edited_df, key="edited_df")