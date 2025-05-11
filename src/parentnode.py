from functools import reduce
from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag must not be null for parent node")

        if self.children is None:
            raise ValueError("Children must not be null for parent node")

        children_html = reduce(
            lambda x, child: f"{x}{child.to_html()}", self.children, ""
        )
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
