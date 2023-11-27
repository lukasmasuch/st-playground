import re
from typing import List

import streamlit as st
import tiktoken
from openai import OpenAI


def extract_first_code_block(markdown_text: str) -> str:
    if (
        "```" not in markdown_text
        and "def" in markdown_text
    ):
        # Assume that everything is code
        return markdown_text

    pattern = r"(?<=```).+?(?=```)"

    # Use re.DOTALL flag to make '.' match any character, including newlines
    first_code_block = re.search(pattern, markdown_text, flags=re.DOTALL)

    code = first_code_block.group(0) if first_code_block else ""
    code = code.strip().lstrip("python").strip()
    return code


def num_tokens_from_messages(
    messages: List[dict], model: str = "gpt-3.5-turbo-0301"
) -> int:
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            num_tokens += (
                4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            )
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )

def get_examples():
    return """

## Example 1:

Streamlit script that is used for e2e testing:

```python
import numpy as np
import pandas as pd

import streamlit as st
from tests.streamlit import snowpark_mocks

# Explicitly seed the RNG for deterministic results
np.random.seed(0)

data = np.random.randn(100, 100)

df = pd.DataFrame(data)
st._arrow_dataframe(df)
st._arrow_dataframe(df, 250, 150)
st._arrow_dataframe(df, width=250)
st._arrow_dataframe(df, height=150)
st._arrow_dataframe(df, 5000, 5000)
st._arrow_dataframe(df, use_container_width=True)

small_df = pd.DataFrame(np.random.randn(100, 3))
st._arrow_dataframe(small_df, width=500)
st._arrow_dataframe(small_df, use_container_width=True)
st._arrow_dataframe(small_df, width=200, use_container_width=True)
st._arrow_dataframe(small_df, width=200, use_container_width=False)

one_col_df = pd.DataFrame(np.random.randn(100, 1))
st._arrow_dataframe(one_col_df, use_container_width=True)

st._arrow_dataframe(snowpark_mocks.DataFrame(), use_container_width=True)
```

Cypress test that needs to be converted:

```javascript
describe("DataFrame with different sizes", () => {
  const expected = [
    { width: "704px", height: "400px" },
    { width: "250px", height: "150px" },
    { width: "250px", height: "400px" },
    { width: "704px", height: "150px" },
    { width: "704px", height: "5000px" },
    { width: "704px", height: "400px" },
    { width: "500px", height: "400px" },
    { width: "704px", height: "400px" },
    { width: "704px", height: "400px" },
    { width: "200px", height: "400px" },
    { width: "704px", height: "400px" },
    { width: "704px", height: "400px" },
  ];

  before(() => {
    cy.loadApp("http://localhost:3000/");
  });

  it("should show as expected", () => {
    cy.get(".stDataFrame")
      .should("have.length", 12)
      .each(($element, index) => {
        return cy
          .wrap($element)
          .should("have.css", "width", expected[index].width)
          .should("have.css", "height", expected[index].height);
      });
  });
});
```

Converted Playwright e2e test (pytest):

```python
from playwright.sync_api import Page, expect


def test_data_frame_with_different_sizes(app: Page):
    \"\"\"Test that st.dataframe should show different sizes as expected.\"\"\"
    expected = [
        {"width": "704px", "height": "400px"},
        {"width": "250px", "height": "150px"},
        {"width": "250px", "height": "400px"},
        {"width": "704px", "height": "150px"},
        {"width": "704px", "height": "5000px"},
        {"width": "704px", "height": "400px"},
        {"width": "500px", "height": "400px"},
        {"width": "704px", "height": "400px"},
        {"width": "704px", "height": "400px"},
        {"width": "200px", "height": "400px"},
        {"width": "704px", "height": "400px"},
        {"width": "704px", "height": "400px"},
    ]

    dataframe_elements = app.get_by_test_id("stDataFrame")
    expect(dataframe_elements).to_have_count(12)

    for i, element in enumerate(dataframe_elements.all()):
        expect(element).to_have_css("width", expected[i]["width"])
        expect(element).to_have_css("height", expected[i]["height"])
```

## Example 2:

Streamlit script that is used for e2e testing:

```python
import random

import numpy as np
import pandas as pd

import streamlit as st
from tests.streamlit.data_mocks import (
    BASE_TYPES_DF,
    DATETIME_TYPES_DF,
    INTERVAL_TYPES_DF,
    LIST_TYPES_DF,
    NUMBER_TYPES_DF,
    PERIOD_TYPES_DF,
    SPECIAL_TYPES_DF,
    UNSUPPORTED_TYPES_DF,
)

np.random.seed(0)
random.seed(0)

st.set_page_config(layout="wide")

st.subheader("Base types")
st._arrow_dataframe(BASE_TYPES_DF, use_container_width=True)

st.subheader("Number types")
st._arrow_dataframe(NUMBER_TYPES_DF, use_container_width=True)

st.subheader("Date, time and datetime types")
st._arrow_dataframe(DATETIME_TYPES_DF, use_container_width=True)

st.subheader("List types")
st._arrow_dataframe(LIST_TYPES_DF, use_container_width=True)

st.subheader("Interval dtypes in pd.DataFrame")
st._arrow_dataframe(INTERVAL_TYPES_DF, use_container_width=True)

st.subheader("Special types")
st._arrow_dataframe(SPECIAL_TYPES_DF, use_container_width=True)

st.subheader("Period dtypes in pd.DataFrame")
st._arrow_dataframe(PERIOD_TYPES_DF, use_container_width=True)

st.subheader("Unsupported types")
st._arrow_dataframe(UNSUPPORTED_TYPES_DF, use_container_width=True)

st.subheader("Long colum header")
st._arrow_dataframe(
    pd.DataFrame(
        np.random.randn(100, 4),
        columns=[
            "this is a very long header name",
            "A",
            "C",
            "this is another long name",
        ],
    )
)
```

Cypress test that needs to be converted:

```javascript
describe("st.dataframe supports a variety of column types", () => {
  before(() => {
    cy.loadApp("http://localhost:3000/");
    cy.prepForElementSnapshots();
    // Make the toolbar disappear to not interfere with snapshots (in wide mode)
    cy.get("[data-testid='stToolbar']").invoke("css", "opacity", 0);
  });

  it("renders element correctly", () => {
    cy.get(".stDataFrame").should("have.length", 9);

    /** Since glide-data-grid uses HTML canvas for rendering the table we
    cannot run any tests based on the HTML DOM. Therefore, we only use snapshot
    matching to test that our table examples render correctly. In addition, glide-data-grid
    itself also has more advanced canvas based tests for some of the interactive features. */

    cy.get(".stDataFrame").each((el, idx) => {
      return cy.wrap(el).matchThemedSnapshots("dataframe-column-types-" + idx);
    });
  });
});
```

Converted Playwright e2e test (pytest):

```python
from playwright.sync_api import Page, expect

from e2e_playwright.conftest import ImageCompareFunction


def test_dataframe_column_types_rendering(
    themed_app: Page, assert_snapshot: ImageCompareFunction
):
    \"\"\"Test that st.dataframe renders various column types correctly via screenshot matching\"\"\"
    elements = themed_app.get_by_test_id("stDataFrame")
    expect(elements).to_have_count(8)

    assert_snapshot(elements.nth(0), name="st_dataframe-base_types")
    assert_snapshot(elements.nth(1), name="st_dataframe-numerical_types")
    assert_snapshot(elements.nth(2), name="st_dataframe-datetime_types")
    assert_snapshot(elements.nth(3), name="st_dataframe-list_types")
    assert_snapshot(elements.nth(4), name="st_dataframe-interval_types")
    assert_snapshot(elements.nth(5), name="st_dataframe-special_types")
    assert_snapshot(elements.nth(6), name="st_dataframe-period_types")
    assert_snapshot(elements.nth(7), name="st_dataframe-unsupported_types")

```

"""


def get_expect_api_reference():
    return """
Assertion	Description
expect(locator).to_be_checked()	Checkbox is checked
expect(locator).to_be_disabled()	Element is disabled
expect(locator).to_be_editable()	Element is editable
expect(locator).to_be_empty()	Container is empty
expect(locator).to_be_enabled()	Element is enabled
expect(locator).to_be_focused()	Element is focused
expect(locator).to_be_hidden()	Element is not visible
expect(locator).to_be_visible()	Element is visible
expect(locator).to_contain_text()	Element contains text
expect(locator).to_have_attribute()	Element has a DOM attribute
expect(locator).to_have_class()	Element has a class property
expect(locator).to_have_count()	List has exact number of children
expect(locator).to_have_css()	Element has CSS property
expect(locator).to_have_id()	Element has an ID
expect(locator).to_have_js_property()	Element has a JavaScript property
expect(locator).to_have_text()	Element matches text
expect(locator).to_have_value()	Input has a value
expect(locator).to_have_values()	Select has options selected
expect(page).to_have_title()	Page has a title
expect(page).to_have_url()	Page has a URL
expect(api_response).to_be_ok()	Response has an OK status
"""

def get_modified_code( 
        streamlit_e2e_script: str,
        pytest_playwright_code: str,    
        instruction: str,
        openai_key: str,
        openai_model: str = "gpt-3.5-turbo",
        show_system_messages: bool = False
) -> str:
    user_prompt = f"""
I just converted a Cypress e2e test to a Playwright e2e Python test (Pytest) for the 
Streamlit internal e2e tests. I would like to get your help on modifying the implemented
Playwright test code based on an instruction I will give below.

Here is the underlying Streamlit script that is used in the e2e testing:

```python
{streamlit_e2e_script}
```

And here is the current implementation of the Playwright pytest code:

```python
{pytest_playwright_code}
```

Please modify the Playwright pytest code code based on the following instruction:

```
{instruction}
```

We currently provide the following fixtures:

- app (Page): Fixture that opens the Streamlit app and provides a playwright page object.
        This fixtures already uses goto() to open the app, please don't use goto() again!
- themed_app (Page): Fixture that opens the Streamlit app with the dark & light theme 
        and provides a playwright page object.
        This fixtures already uses goto() to open the app, please don't use goto() again!
- assert_snapshot (function): Takes a snapshot of a selected element and compares it 
        to a previously stored snapshot.

Please use the expect from Playwright to make non-screenshot assertions wherever possible.
If you use expect for testing, you can use the following assertions:

{get_expect_api_reference()}

Please put the full modified code in a markdown code block (```) and ONLY respond with the Playwright Pytest code:
    """

    messages = [
        {
            "role": "system",
            "content": "You are a helpful expert that helps to with writing e2e tests for Streamlit repo using Playwright in Python/Pytest." +
            " The user will give you some existing implementation and you will modify it based on an instruction.",
        },
        {"role": "user", "content": user_prompt},
    ]

    print("Prompt tokens", num_tokens_from_messages(messages))
    openai_client = OpenAI(
        api_key=openai_key
    )
    completion = openai_client.chat.completions.create(model=openai_model, messages=messages)
    response = completion.choices[0].message.content.strip()

    if show_system_messages:
        with st.expander("System messages"):
            for message in messages:
                st.markdown(message["content"])
            st.divider()
            st.markdown("**GPT Response:**")
            st.markdown(response)
            st.divider()
            st.markdown(f"**User tokens:** {num_tokens_from_messages(messages)}")

    code_block = extract_first_code_block(response)
    if not code_block and response:
        st.info(response, icon="🤖")
    return code_block



@st.cache_data(show_spinner=False)
def get_converted_code(
    cypress_e2e_spec: str,
    streamlit_e2e_script: str,
    openai_key: str,
    openai_model: str = "gpt-3.5-turbo",
    show_system_messages: bool = False,
) -> str:
    user_prompt = f"""
Your job is to convert a Cypress e2e test to a Playwright e2e Python test (Pytest). 
First, here are some examples of Cypress tests and their corresponding Playwright tests:

{get_examples()}

Here is the Streamlit script that is used for e2e testing:

```python
{streamlit_e2e_script}
```

And here is the corresponding Cypress test that you need to convert for me:

```javascript
{cypress_e2e_spec}
```

Please convert to provided code snippet into a valid Playwright pytest e2e test. 
Therefore, you can use the following fixtures:

- app (Page): Fixture that opens the Streamlit app and provides a playwright page object.
        This fixtures already uses goto() to open the app, please don't use goto() again!
- themed_app (Page): Fixture that opens the Streamlit app with the dark & light theme 
        and provides a playwright page object.
        This fixtures already uses goto() to open the app, please don't use goto() again!
- assert_snapshot (function): Takes a snapshot of a selected element and compares it 
        to a previously stored snapshot.

Please create one pytest test function for every `it` in the Cypress test. 
And use the expect from Playwright to make non-screenshot assertions wherever possible. 
If you use expect for testing, you can use the following assertions:

{get_expect_api_reference()}

Please put the full code in a markdown code block (```) and ONLY respond with the converted Playwright Pytest code:
    """

    messages = [
        {
            "role": "system",
            "content": "You are a helpful expert that helps to convert the Cypress e2e tests (Javascript) of the Streamlit repo to Playwright e2e tests (Python / Pytest).",
        },
        {"role": "user", "content": user_prompt},
    ]

    print("Prompt tokens", num_tokens_from_messages(messages))
    
    openai_client = OpenAI(
        api_key=openai_key
    )
    completion = openai_client.chat.completions.create(model=openai_model, messages=messages)
    response = completion.choices[0].message.content.strip()

    if show_system_messages:
        with st.expander("System messages"):
            for message in messages:
                st.markdown(message["content"])
            st.divider()
            st.markdown("**GPT Response:**")
            st.markdown(response)
            st.divider()
            st.markdown(f"**User tokens:** {num_tokens_from_messages(messages)}")

    code_block = extract_first_code_block(response)
    if not code_block and response:
        st.info(response, icon="🤖")
    return code_block
