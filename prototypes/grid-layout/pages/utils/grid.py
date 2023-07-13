from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal, Optional, Sequence, Union

import streamlit as st
from streamlit.errors import StreamlitAPIException

if TYPE_CHECKING:
    from streamlit.delta_generator import DeltaGenerator

SpecType = Union[int, Sequence[Union[int, float]]]


def stylable_container(
    class_name: str, css_styles: str | List[str]
) -> "DeltaGenerator":
    if isinstance(css_styles, str):
        css_styles = [css_styles]

    style_text = f"""
<style>
"""

    for style in css_styles:
        style_text += f"""

div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.{class_name}) {style}

"""

    style_text += f"""
    </style>
"""

    container = st.container()
    container.markdown(style_text, unsafe_allow_html=True)
    container.markdown(f'<span class="{class_name}"></span>', unsafe_allow_html=True)
    return container


class GridDeltaGenerator:
    def __init__(
        self,
        parent_dg: "DeltaGenerator",
        spec: List[SpecType],
        *,
        gap: Optional[str] = "small",
        repeat: bool = True,
    ):
        self._parent_dg = parent_dg
        self._container_queue: List["DeltaGenerator"] = []
        self._number_of_rows = 0
        self._spec = spec
        self._gap = gap
        self._repeat = repeat

    def _get_next_cell_container(self) -> "DeltaGenerator":
        if not self._container_queue:
            if not self._repeat and self._number_of_rows > 0:
                raise StreamlitAPIException("The row is already filled up.")

            # Create a new row using st.columns:
            self._number_of_rows += 1
            spec = self._spec[self._number_of_rows % len(self._spec) - 1]
            self._container_queue.extend(self._parent_dg.columns(spec, gap=self._gap))

        return self._container_queue.pop(0)

    def __getattr__(self, name):
        return getattr(self._get_next_cell_container(), name)

    # TODO: context manager support doesn't work yet
    # def __enter__(self):
    #     return self._get_next_cell_container().__enter__()

    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     return self._get_next_cell_container().__exit__(exc_type, exc_val, exc_tb)


def grid(
    *spec: SpecType,
    gap: Optional[str] = "small",
    align_items: Literal["top", "center", "bottom"] = "top",
) -> GridDeltaGenerator:
    container = stylable_container(
        class_name=f"grid_{align_items}",
        css_styles=[
            """
div[data-testid="column"] > div {
   height: 100%;
}
""",
            f"""
div[data-testid="column"] > div > div[data-testid="stVerticalBlock"] > div.element-container {{
    {"margin-top: auto;" if align_items in ["center", "bottom"] else ""}
    {"margin-bottom: auto;" if align_items == "center" else ""}
}}
""",
        ],
    )

    return GridDeltaGenerator(
        parent_dg=container, spec=list(spec), gap=gap, repeat=True
    )


def row(
    spec: SpecType,
    gap: Optional[str] = "small",
    align_items: Literal["top", "center", "bottom"] = "top",
) -> GridDeltaGenerator:
    container = stylable_container(
        class_name=f"row_{align_items}",
        css_styles=[
            """
div[data-testid="column"] > div {
   height: 100%;
}
""",
            f"""
div[data-testid="column"] > div > div[data-testid="stVerticalBlock"] > div.element-container {{
    {"margin-top: auto;" if align_items in ["center", "bottom"] else ""}
    {"margin-bottom: auto;" if align_items == "center" else ""}
}}
""",
        ],
    )

    return GridDeltaGenerator(parent_dg=container, spec=[spec], gap=gap, repeat=False)
