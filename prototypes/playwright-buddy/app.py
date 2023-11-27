import os
from dataclasses import dataclass, field
from typing import List, Optional

import prompts
import streamlit as st
from code_editor import code_editor
from openai import OpenAI


def page_setup() -> None:
    st.secrets.load_if_toml_exists()

    st.set_page_config(
        page_title="Playwright Buddy",
        page_icon="🎭",
        initial_sidebar_state="collapsed" if "openai_key" not in st.session_state else "expanded",
    )

    PASSCODE = os.environ.get("PASSCODE")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    if OPENAI_API_KEY:
        st.session_state["openai_key"] = OPENAI_API_KEY

    if PASSCODE and "authenticate" not in st.session_state:
        if st.text_input("What is the passcode?", type="password") == PASSCODE:
            st.session_state["authenticate"] = True
            st.experimental_rerun()
        else:
            st.stop()

    with st.sidebar:
        st.session_state["openai_model"] = st.selectbox(
            "OpenAI Chat Model",
            options=["gpt-4-1106-preview", "gpt-4", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"],
            help="Make sure that the provided API key is activated for the selected model.",
        )
        if not OPENAI_API_KEY:
            st.session_state["openai_key"] = st.text_input(
                "OpenAI API Key",
                type="password",
                help="You can find your API keys [here](https://platform.openai.com/account/api-keys).",
            )
        st.session_state["show_system_messages"] = st.checkbox("Show System Messages", value=False)

page_setup()
st.title("🎭 Playwright Buddy")

@dataclass
class ConversionRequest:
    instruction: Optional[str] = None
    generated_code: Optional[str] = None


@dataclass
class ConversionState:
    cypress_test_code: Optional[str] = None
    streamlit_e2e_code: Optional[str] = None
    history: List[ConversionRequest] = field(default_factory=list)


if "state" not in st.session_state:
    st.session_state["state"] = ConversionState()
conversion_state: ConversionState = st.session_state["state"]

openai_client = OpenAI(
    api_key=st.session_state["openai_key"]
)

editor_actions = (
    {
        "name": "Submit",
        "feather": "Play",
        "primary": True,
        "hasText": True,
        "alwaysOn": True,
        "commands": ["save-state", ["response", "saved"]],
        "response": "saved",
        "style": {"bottom": "0.44rem", "right": "0.4rem"},
    },
)

with st.chat_message("assistant", avatar="🎭"):
    st.write(
        "Hello 👋 I'm an expert in converting Streamlit's Cypress e2e tests into Playwright tests. "
    )

    st.write("To get started, please paste in the **Streamlit e2e script (Python)** below:")
    e2e_code_placeholder = st.empty()
    if not conversion_state.streamlit_e2e_code:
        with e2e_code_placeholder.container():
            response_dict = code_editor(
                "",
                lang="python",
                height=[5, 20],
                buttons=editor_actions,
                key="streamlit_e2e_code",
            )
            if "text" in response_dict and response_dict["text"]:
                conversion_state.streamlit_e2e_code = response_dict["text"]

    if conversion_state.streamlit_e2e_code:
        e2e_code_placeholder.code(conversion_state.streamlit_e2e_code, language="python")
    
    st.write("As well as the corresponding **Cypress e2e spec (Javascript)**:")
    cypress_code_placeholder = st.empty()
    if not conversion_state.cypress_test_code:
        with cypress_code_placeholder.container():
            response_dict = code_editor(
                "",
                lang="javascript",
                height=[5, 20],
                buttons=editor_actions,
                key="cypress_code",
            )

            if "text" in response_dict and response_dict["text"]:
                conversion_state.cypress_test_code = response_dict["text"]
    
    if conversion_state.cypress_test_code:
        cypress_code_placeholder.code(conversion_state.cypress_test_code, language="javascript")

if not conversion_state.cypress_test_code or not conversion_state.streamlit_e2e_code:
    st.stop()

for chart_request in conversion_state.history:
    if chart_request.instruction:
        st.chat_message("user").write(chart_request.instruction)
    with st.chat_message("assistant"):
        st.write("Here is the generated Playwright code:")
        st.code(chart_request.generated_code, language="python")
    
if not conversion_state.history:
    new_request = ConversionRequest()
    with st.chat_message("assistant", avatar="🎭"):
        with st.spinner("♻️ Converting Cypress test..."):
            new_request.generated_code = prompts.get_converted_code(conversion_state.cypress_test_code, conversion_state.streamlit_e2e_code, openai_key=st.session_state["openai_key"], openai_model=st.session_state.openai_model, show_system_messages=st.session_state.show_system_messages)
        
        if new_request.generated_code:
            st.write("Here is the generated Playwright code:")
            st.code(new_request.generated_code, language="python")
            conversion_state.history.append(new_request)


latest_request = conversion_state.history[-1]
if latest_request.generated_code:
    prompt = st.chat_input("What would you like to modify?", key="user_input")

    if prompt:
        st.chat_message("user").write(prompt)
        new_request = ConversionRequest()
        new_request.instruction = prompt
        with st.chat_message("assistant", avatar="🎭"):
            with st.spinner("♻️ Modifying Playwright code..."):
                new_request.generated_code = prompts.get_modified_code(conversion_state.streamlit_e2e_code, latest_request.generated_code, instruction=prompt, openai_key=st.session_state["openai_key"], openai_model=st.session_state.openai_model, show_system_messages=st.session_state.show_system_messages)
            if new_request.generated_code:
                st.write("Here is the generated Playwright code:")
                st.code(new_request.generated_code, language="python")
                conversion_state.history.append(new_request)
