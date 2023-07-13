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
    vertical_align: Literal["top", "center", "bottom"] = "top",
) -> GridDeltaGenerator:
    """Insert a multi-element, grid container.

    Inserts a container into your app that can be used to hold
    multiple elements. The elements are arranged in a grid layout
    as defined by the provided spec.

    To add elements to the returned container, you can use "with" notation
    (preferred) or just call methods directly on the returned object. See
    examples below.

    Parameters
    ----------
    *spec : int or iterable of numbers
        One or many row specs which control the number and width of cells in each row.
        Each spec can be one of:

        * An integer that specifies the number of cells. All cells have equal
          width in this case.
        * An iterable of numbers (int or float) that specify the relative width of
          each cell. E.g. ``[0.7, 0.3]`` creates two cells where the first
          one takes up 70% of the available with and the second one takes up 30%.
          Or ``[1, 2, 3]`` creates three cells where the second one is two times
          the width of the first one, and the third one is three times that width.

        It will iterate over the provided specs in a round-robin order. Whenever a row
        is filled up, it will move on to the next spec or the first spec if there are no
        more specs.

    gap : "small", "medium", or "large"
        The size of the gap between the cells. Defaults to "small". This
        argument can only be supplied by keyword.

    vertical_align : "top", "center", or "bottom"
        The vertical alignment of the cells in the row. Defaults to "top".

    Returns
    -------
    grid container
        The grid container that can be used to add elements to the grid.

    """
    container = stylable_container(
        class_name=f"grid_{vertical_align}",
        css_styles=[
            """
div[data-testid="column"] > div {
   height: 100%;
}
""",
            f"""
div[data-testid="column"] > div > div[data-testid="stVerticalBlock"] > div.element-container {{
    {"margin-top: auto;" if vertical_align in ["center", "bottom"] else ""}
    {"margin-bottom: auto;" if vertical_align == "center" else ""}
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
    vertical_align: Literal["top", "center", "bottom"] = "top",
) -> GridDeltaGenerator:
    """Insert a multi-element, horizontal container.

    Inserts a container into your app that can be used to hold
    as many elements as defined in the provided spec.

    To add elements to the returned container, you can use "with" notation
    (preferred) or just call methods directly on the returned object. See
    examples below.

    Parameters
    ----------
    spec : int or iterable of numbers
        Controls the number and width of cells to insert in the row. Can be one of:

        * An integer that specifies the number of cells. All cells have equal
          width in this case.
        * An iterable of numbers (int or float) that specify the relative width of
          each cell. E.g. ``[0.7, 0.3]`` creates two cells where the first
          one takes up 70% of the available with and the second one takes up 30%.
          Or ``[1, 2, 3]`` creates three cells where the second one is two times
          the width of the first one, and the third one is three times that width.

    gap : "small", "medium", or "large"
        The size of the gap between the cells. Defaults to "small". This
        argument can only be supplied by keyword.

    vertical_align : "top", "center", or "bottom"
        The vertical alignment of the cells in the row. Defaults to "top".

    Returns
    -------
    row container
        The row container that can be used to add elements to the row.

    """
    container = stylable_container(
        class_name=f"row_{vertical_align}",
        css_styles=[
            """
div[data-testid="column"] > div {
   height: 100%;
}
""",
            f"""
div[data-testid="column"] > div > div[data-testid="stVerticalBlock"] > div.element-container {{
    {"margin-top: auto;" if vertical_align in ["center", "bottom"] else ""}
    {"margin-bottom: auto;" if vertical_align == "center" else ""}
}}
""",
        ],
    )

    return GridDeltaGenerator(parent_dg=container, spec=[spec], gap=gap, repeat=False)
