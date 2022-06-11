from datetime import date
import random

import pandas as pd
import streamlit as st
import numpy as np


st.set_page_config(
    page_title="Interactive Tables - Column Config & Types", page_icon=":abacus:"
)


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


icon("🧮")

st.title("Tables - Column Config & Types")


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
                "age": calculate_age(profile["birthdate"]),
                "active": random.choice([True, False]),
                "birthdate": profile["birthdate"],
                "homepage": profile["website"][0],
                "activity": np.random.randint(2, 50, size=25),
                "websites": profile["website"],
                # "address": profile["address"],
                "daily_activity": np.random.rand(25),
                "status": random.random(),
            }
        )
    return pd.DataFrame(new_data)


profile_dataset = get_profile_dataset()

st._arrow_dataframe(
    profile_dataset,
    columns={
        0: st.column_config(title="user"),
        "avatar": st.column_config(type="image"),
        "homepage": st.column_config(type="url"),
        "birthdate": st.column_config(hidden=True),
        "activity": st.column_config(type="line-chart", width=250),
        "daily_activity": st.column_config(type="bar-chart"),
        "status": st.column_config(type="progress-chart"),
    },
)

with st.expander("Show Code"):
    st.code(
        """
st.dataframe(
    get_profile_dataset(),
    columns={
        0: st.column_config(title="user"),
        "avatar": st.column_config(type="image"),
        "homepage": st.column_config(type="url"),
        "birthdate": st.column_config(hidden=True),
        "activity": st.column_config(type="line-chart", width=250),
        "daily_activity": st.column_config(type="bar-chart"),
        "status": st.column_config(type="progress-chart"),
    },
)
    """
    )

st.markdown("---")
st.header("Configuration playground")
col1, col2, col3 = st.columns(3)

# Start with empty string
column_options = [""]
column_options.extend(profile_dataset.columns.to_list())
# Add number indices (number columns + 1 for index)
column_options.extend(range(0, len(column_options)))

selected_col = col1.selectbox("Select column", options=column_options)

if selected_col != "":
    selected_option = col2.selectbox(
        "Select config option", options=["", "title", "type", "hidden", "width"]
    )

    if selected_option:
        columns_configration = {}

        if selected_option == "title":
            title = col3.text_input("Configure column title", value="Custom Title")
            columns_configration[selected_col] = st.column_config(title=title)

        elif selected_option == "type":
            type = col3.selectbox(
                "Configure column type",
                options=[
                    "text",
                    "number",
                    "boolean",
                    "list",
                    "url",
                    "image",
                    "bar-chart",
                    "line-chart",
                    "progress-chart",
                ],
            )
            columns_configration[selected_col] = st.column_config(type=type)

        elif selected_option == "hidden":
            hidden = (
                col3.selectbox("Hide the column", options=["show", "hide"]) == "hide"
            )
            columns_configration[selected_col] = st.column_config(hidden=hidden)

        elif selected_option == "width":
            width = col3.number_input(
                "Configure the column width", value=150, min_value=0, max_value=500
            )
            columns_configration[selected_col] = st.column_config(width=width)

        st._arrow_dataframe(
            profile_dataset,
            columns=columns_configration,
        )