import re

from node import TextNode, TextType


class DelimiterException(Exception):
    pass


def check_delimiter(delimiter, node):
    if delimiter not in node.text:
        raise DelimiterException(f"Missing delimiter {delimiter} in node: {node}")


TYPES_TO_SPLIT = {TextType.CODE, TextType.BOLD, TextType.ITALIC}


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not should_split(text_type, node):
            new_nodes.append(node)
            continue

        try:
            check_delimiter(delimiter, node)
            texts = node.text.split(delimiter)
            for i in range(0, len(texts)):
                # ending the with delimiter will result in an empty string at the end -> ignore that
                if texts[i] == "":
                    continue

                type = TextType.TEXT if i % 2 == 0 else text_type
                new_nodes.append(TextNode(texts[i], type))
        except DelimiterException:
            new_nodes.append(node)

    return new_nodes


def should_split(text_type, node):
    return node.text_type == TextType.TEXT and text_type in TYPES_TO_SPLIT


def split_nodes_regex(old_nodes, extract_matches, regex, text_type):
    new_nodes = []
    for node in old_nodes:
        # no text node
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        tuples = extract_matches(node.text)
        # no matches found
        if len(tuples) == 0:
            new_nodes.append(node)
            continue

        texts = re.split(regex, node.text)

        # Remove the regex matches (pattern: text, regex, regex, text, regex regex, text ...)
        texts = [text for i, text in enumerate(texts) if i % 3 == 0]

        # len(tuples) is always len(texts) - 1
        for i in range(0, len(texts)):
            text = texts[i]
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))

            if i < len(tuples):
                alt_text, url = tuples[i]
                new_nodes.append(TextNode(alt_text, text_type, url))

    return new_nodes


def split_nodes_image(old_nodes):
    return split_nodes_regex(
        old_nodes, extract_markdown_images, IMAGE_REGEX, TextType.IMAGE
    )


def split_nodes_link(old_nodes):
    return split_nodes_regex(
        old_nodes, extract_markdown_links, LINK_REGEX, TextType.LINK
    )


IMAGE_REGEX = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"


def extract_markdown_images(text):
    return re.findall(IMAGE_REGEX, text)


LINK_REGEX = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"


def extract_markdown_links(text):
    return re.findall(LINK_REGEX, text)


def text_to_textnodes(text):
    nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
