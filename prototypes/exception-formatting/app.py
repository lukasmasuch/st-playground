# -*- coding: utf-8 -*-

import streamlit as st
import time
from module import raise_execption, do_stuff
import os
import sys
from pydantic import BaseModel, Field, parse_obj_as
import streamlit_pydantic as sp
from typing import Literal, Optional
import numpy as np

st.header("Exception Formatting Playground")


def raise_key_error():
    key = "foo"
    raise_execption(key)


def numpy_error():
    # np.seterr(divide='raise')
    # np.divide(2, 0)

    array1 = np.array([1, 2])
    array2 = np.array([1, None])
    array1 / array2  # should be np.array([0, 1, 2])


exception_options: dict = {
    "key error": raise_key_error,
    "numpy error": numpy_error,
    "import error": do_stuff,
}
selected_option = st.selectbox(
    "Select Exception", options=list(exception_options.keys())
)
exception_func = exception_options[str(selected_option)]

if st.button("Trigger Default Formatting"):
    try:
        exception_func()
    except:
        import traceback
        print("#############################")
        print("\n\nShow exception with default formatting:\n\n")
        print("#############################\n\n\n\n")
        print(traceback.format_exc())


class RichTracebackConfig(BaseModel):
    color_system: Literal["standard", "256", "truecolor", "auto"] = Field(
        "256",
        description="The color system supported by your terminal, either `standard`, `256` or `truecolor`. Leave as `auto` to autodetect.",
    )
    force_terminal: bool = Field(
        True,
        description="Enable/disable terminal control codes, or None to auto-detect terminal.",
    )
    force_jupyter: bool = Field(
        False,
        description="Enable/disable Jupyter rendering, or None to auto-detect Jupyter.",
    )
    force_interactive: bool = Field(
        False,
        description="Enable/disable interactive mode, or None to auto detect.",
    )
    soft_wrap: bool = Field(
        False,
        description="Set soft wrap default on print method.",
    )
    width: int = Field(
        88,
        description="The width of the terminal. Leave as default to auto-detect width.",
    )
    # height: int = Field(
    #     100,
    #     description="The height of the terminal. Leave as default to auto-detect height.",
    # )
    no_color: bool = Field(
        False,
        description="Enabled no color mode, or None to auto detect.",
    )
    tab_size: int = Field(
        8,
        description="Number of spaces used to replace a tab character.",
    )
    markup: bool = Field(
        True,
        description="Boolean to enable :ref:`console_markup`.",
    )
    emoji: bool = Field(
        True,
        description="Enable emoji code.",
    )
    highlight: bool = Field(
        True,
        description="Enable automatic highlighting.",
    )
    log_time: bool = Field(
        True,
        description="Boolean to enable logging of time by :meth:`log` methods.",
    )
    log_path: bool = Field(
        True,
        description="Boolean to enable the logging of the caller by :meth:`log`.",
    )
    extra_lines: int = Field(3, description="Additional lines of code to render.", ge=0)
    theme: Optional[str] = Field(
        None,
        description="Override pygments theme used in traceback.",
    )
    word_wrap: bool = Field(
        True,
        description="Enable word wrapping of long lines.",
    )
    show_locals: bool = Field(
        False,
        description="Enable display of local variables.",
    )
    max_frames: int = Field(
        100,
        description="Maximum number of frames to show in a traceback, 0 for no maximum.",
        ge=0,
    )
    box_style: Literal[
        "ASCII",
        "ASCII2",
        "ASCII_DOUBLE_HEAD",
        "SQUARE",
        "SQUARE_DOUBLE_HEAD",
        "MINIMAL",
        "MINIMAL_HEAVY_HEAD",
        "MINIMAL_DOUBLE_HEAD",
        "SIMPLE",
        "SIMPLE_HEAD",
        "SIMPLE_HEAVY",
        "HORIZONTALS",
        "ROUNDED",
        "HEAVY",
        "HEAVY_EDGE",
        "HEAVY_HEAD",
        "DOUBLE",
        "DOUBLE_EDGE",
        "CUSTOM_HORIZONTALS"
    ] = Field(
        "CUSTOM_HORIZONTALS",
        description="The box style that defines the look of the border.",
    )
    # suppress: str = Field(description="Optional sequence of modules or paths to exclude from traceback.")

rich_traceback_config: RichTracebackConfig = RichTracebackConfig()

with st.expander("Configure Rich", expanded=False):
    config_data = sp.pydantic_input(key="rich_errors_config", model=RichTracebackConfig)
    rich_traceback_config = parse_obj_as(RichTracebackConfig, config_data)


if st.button("Trigger Rich Traceback"):
    from rich import panel, box, traceback

    BOX_STYLE_MAPPING = {
        "ASCII": box.ASCII,
        "ASCII2": box.ASCII2,
        "ASCII_DOUBLE_HEAD": box.ASCII_DOUBLE_HEAD,
        "SQUARE": box.SQUARE,
        "SQUARE_DOUBLE_HEAD": box.SQUARE_DOUBLE_HEAD,
        "MINIMAL": box.MINIMAL,
        "MINIMAL_HEAVY_HEAD": box.MINIMAL_HEAVY_HEAD,
        "MINIMAL_DOUBLE_HEAD": box.MINIMAL_DOUBLE_HEAD,
        "SIMPLE": box.SIMPLE,
        "SIMPLE_HEAD": box.SIMPLE_HEAD,
        "SIMPLE_HEAVY": box.SIMPLE_HEAVY,
        "HORIZONTALS": box.HORIZONTALS,
        "ROUNDED": box.ROUNDED,
        "HEAVY": box.HEAVY,
        "HEAVY_EDGE": box.HEAVY_EDGE,
        "HEAVY_HEAD": box.HEAVY_HEAD,
        "DOUBLE": box.DOUBLE,
        "DOUBLE_EDGE": box.DOUBLE_EDGE,
        "CUSTOM_HORIZONTALS": box.Box(
"""\
────
    
────
    
────
────
    
────
""")
    }

    class ConfigurablePanel(panel.Panel):
        def __init__(
            self, renderable: "RenderableType", box: box.Box = BOX_STYLE_MAPPING[rich_traceback_config.box_style], **kwargs
        ):
            super(ConfigurablePanel, self).__init__(renderable, box, **kwargs)

    traceback.Panel = ConfigurablePanel

    from rich.console import Console


    # https://github.com/willmcgugan/rich/blob/master/rich/console.py#L120
    console = Console(
        color_system=rich_traceback_config.color_system,
        force_terminal=rich_traceback_config.force_terminal,
        force_jupyter=rich_traceback_config.force_jupyter,
        force_interactive=rich_traceback_config.force_interactive,
        soft_wrap=rich_traceback_config.soft_wrap,
        width=rich_traceback_config.width,
        # height=rich_traceback_config.height,
        no_color=rich_traceback_config.no_color,
        tab_size=rich_traceback_config.tab_size,
        markup=rich_traceback_config.markup,
        emoji=rich_traceback_config.emoji,
        highlight=rich_traceback_config.highlight,
        log_time=rich_traceback_config.log_time,
        log_path=rich_traceback_config.log_path,
    )
    try:
        exception_func()
    except Exception:
        print("#############################")
        print("\n\nShow exception with Rich formatting:\n\n")
        print("#############################\n\n\n\n")
        # https://github.com/willmcgugan/rich/blob/3db6396a0c6838fd8fa642ccab3a095838d88329/rich/console.py#L1759
        console.print_exception(
            width=rich_traceback_config.width,
            show_locals=rich_traceback_config.show_locals,
            max_frames=rich_traceback_config.max_frames,
            word_wrap=rich_traceback_config.word_wrap,
            theme=rich_traceback_config.theme,
            extra_lines=rich_traceback_config.extra_lines,
        )
        # from rich.traceback import Traceback
        # traceback = Traceback() # Contains a snapshot of the last exception
        # console = Console(width=100, no_color=False, color_system="256")
        # with console.capture() as capture:
        #    console.print(traceback)
        # traceback_str = capture.get()
        # st.text(traceback_str) 
        # .replace("│", "").replace("╭", "").replace("─", "").replace("╮", "").replace("╰","").replace("╯","")

class PrettyErrorsConfig(BaseModel):
    mono_color: bool = Field(
        True,
        description="Sets some config options in a way that is useful for monochrome output.",
    )
    display_locals: bool = Field(
        True,
        description="When enabled, local variables appearing in the top stack frame code will be displayed with their values.",
    )
    line_number_first: bool = Field(
        False,
        description="When enabled the line number will be displayed first, rather than the filename.",
    )
    lines_before: int = Field(
        2,
        description="How many lines of code to display for the top frame, before the line the exception occurred on.",
        ge=0,
    )
    lines_after: int = Field(
        2,
        description="How many lines of code to display for the top frame, after the line the exception occurred on.",
        ge=0,
    )
    line_length: int = Field(
        88,
        description="Output will be wrapped at this point. If set to 0 (which is the default) it will automatically match your console width.",
        ge=0,
    )
    display_timestamp: bool = Field(
        False,
        description="When enabled a timestamp is written in the traceback header.",
    )
    filename_display: Literal[
        "FILENAME_COMPACT", "FILENAME_EXTENDED", "FILENAME_FULL"
    ] = Field(
        "FILENAME_EXTENDED",
        description="How the filename is displayed.",
    )
    infix: str = Field(
        "---------------------------",
        description="Text string which is displayed between each frame of the stack.",
    )
    prefix: str = Field(
        "",
        description="Text string which is displayed at the top of the report, just below the header.",
    )
    postfix: str = Field(
        "",
        description="Text string which is displayed at the bottom of the exception report.",
    )
    inner_exception_separator: bool = Field(
        False,
        description="Default is False. When set to True a header will be written before the inner_exception_message.",
    )
    display_arrow: bool = Field(
        True,
        description="When enabled an arrow will be displayed for syntax errors, pointing at the offending token.",
    )
    truncate_locals: bool = Field(
        True,
        description="When enabled the values of displayed local variables will be truncated to fit the line length.",
    )
    display_trace_locals: bool = Field(
        True,
        description="When enabled, local variables appearing in other stack frame code will be displayed with their values.",
    )
    truncate_code: bool = Field(
        True,
        description="When enabled each line of code will be truncated to fit the line length.",
    )
    trace_lines_after: int = Field(
        0,
        description="How many lines of code to display for each other frame in the stack trace, after the line the exception occurred on.",
        ge=0,
    )
    trace_lines_before: int = Field(
        0,
        description="How many lines of code to display for each other frame in the stack trace, before the line the exception occurred on.",
        ge=0,
    )
    top_first: bool = Field(
        False,
        description="When enabled the stack trace will be reversed, displaying the top of the stack first.",
    )
    stack_depth: int = Field(
        0,
        description="The maximum number of entries from the stack trace to display. When 0 will display the entire stack, which is the default.",
        ge=0,
    )
    exception_above: bool = Field(
        True,
        description="When enabled the exception is displayed above the stack trace.",
    )
    exception_below: bool = Field(
        False,
        description="When enabled the exception is displayed below the stack trace.",
    )
    separator_character: str = Field(
        "-",
        description="Character used to create the header line. Hyphen is used by default. If set to None or '' then header will be disabled.",
    )
    full_line_newline: bool = Field(
        True,
        description="Insert a hard newline even if the line is full. If line_length is the same as your console width and this is enabled then you will see double newlines when the line is exactly full, so usually you would only set this if they are different.",
    )
    always_display_bottom: bool = Field(
        True,
        description="When enabled (which is the default) the bottom frame of the stack trace will always be displayed.",
    )
    display_link: bool = Field(
        False,
        description="When enabled a link is written below the error location, which VSCode will allow you to click on.",
    )
    arrow_tail_character: str = Field(
        "-",
        description="Characters used to draw the arrow tail which points at syntax errors.",
    )
    arrow_head_character: str = Field(
        "^",
        description="Characters used to draw the arrow head which points at syntax errors.",
    )
    reset_stdout: bool = Field(
        True,
        description="When enabled the reset escape sequence will be written to stdout as well as stderr; turn this on if your console is being left with the wrong color.",
    )


pretty_errors_config: PrettyErrorsConfig = PrettyErrorsConfig()

with st.expander("Configure PrettyErrors", expanded=False):
    config_data = sp.pydantic_input(key="pretty_error_config", model=PrettyErrorsConfig)
    pretty_errors_config = parse_obj_as(PrettyErrorsConfig, config_data)

st.warning("Triggering PrettyError will reconfigure (and break) the terminal coloring of rich. Only an app reboot will fix this.")
if st.button("Trigger PrettyError"):
    import pretty_errors
    pretty_errors.config = pretty_errors.PrettyErrorsConfig()
    if pretty_errors_config.mono_color:
        pretty_errors.mono()

    # https://github.com/onelivesleft/PrettyErrors/blob/master/pretty_errors/__init__.py#L53
    pretty_errors.configure(
        display_locals=pretty_errors_config.display_locals,
        line_number_first=pretty_errors_config.line_number_first,
        lines_before=pretty_errors_config.lines_before,
        lines_after=pretty_errors_config.lines_after,
        line_length=pretty_errors_config.line_length,
        display_timestamp=pretty_errors_config.display_timestamp,
        full_line_newline=pretty_errors_config.full_line_newline,
        exception_above=pretty_errors_config.exception_above,
        exception_below=pretty_errors_config.exception_below,
        separator_character=pretty_errors_config.separator_character,
        filename_display=pretty_errors.FILENAME_EXTENDED
        if pretty_errors_config.filename_display == "FILENAME_EXTENDED"
        else pretty_errors.FILENAME_FULL
        if pretty_errors_config.filename_display == "FILENAME_FULL"
        else pretty_errors.FILENAME_COMPACT,
        stack_depth=pretty_errors_config.stack_depth,
        display_arrow=pretty_errors_config.display_arrow,
        top_first=pretty_errors_config.top_first,
        always_display_bottom=pretty_errors_config.always_display_bottom,
        display_link=pretty_errors_config.display_link,
        trace_lines_after=pretty_errors_config.trace_lines_after,
        trace_lines_before=pretty_errors_config.trace_lines_before,
        truncate_code=pretty_errors_config.truncate_code,
        display_trace_locals=pretty_errors_config.display_trace_locals,
        truncate_locals=pretty_errors_config.truncate_locals,
        infix=pretty_errors_config.infix,
        prefix=pretty_errors_config.prefix,
        postfix=pretty_errors_config.postfix,
        inner_exception_separator=pretty_errors_config.inner_exception_separator,
        arrow_tail_character=pretty_errors_config.arrow_tail_character,
        arrow_head_character=pretty_errors_config.arrow_head_character,
    )

    err_out = pretty_errors.StdErr()

    def output_error(s):
        err_out.write(s + "\n")
    
    try:
        exception_func()
    except:
        import traceback
        print("#############################")
        print("\n\nShow exception with PrettyErrors formatting:\n\n")
        print("#############################\n\n\n\n")
        output_error(traceback.format_exc())


class BetterExceptionsConfig(BaseModel):
    should_encode: bool = Field(True, description="")
    supports_color: bool = Field(
        False, description="Configure if coloring should be used."
    )
    max_length: int = Field(88, description="The maximum length per line.")
    pipe_char: str = Field(
        u"\u2502", description="Character used for the line of the arrow."
    )
    cap_char: str = Field(u"\u2514", description="Character used for the arrow head.")


better_exceptions_config: BetterExceptionsConfig = BetterExceptionsConfig()

with st.expander("Configure Better Exceptions", expanded=False):
    from better_exceptions import ExceptionFormatter
    config_data = sp.pydantic_input(
        key="better_exceptions_config", model=BetterExceptionsConfig
    )
    better_exceptions_config = parse_obj_as(BetterExceptionsConfig, config_data)

if st.button("Trigger Better Exceptions"):
    try:
        exception_func()
    except:
        print("#############################")
        print("\n\nShow exception with BetterExceptions formatting:\n\n")
        print("#############################\n\n\n\n")
        # https://github.com/Qix-/better-exceptions/blob/4e150ba3428013e55c274b06829b0360704d6750/better_exceptions/__init__.py#L45
        formatter = ExceptionFormatter(
            colored=better_exceptions_config.supports_color,
            max_length=better_exceptions_config.max_length,
            pipe_char=better_exceptions_config.pipe_char,
            cap_char=better_exceptions_config.cap_char,
        )
        print("".join(formatter.format_exception(*sys.exc_info())))