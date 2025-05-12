import unittest

from node import (
    HTMLNode,
    LeafNode,
    ParentNode,
    TextNode,
    TextType,
    text_node_to_html_node,
)


class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("p", "Hello, world!")
        node2 = HTMLNode("p", "Hello, world!")
        self.assertEqual(node1.tag, node2.tag)
        self.assertEqual(node1.value, node2.value)
        self.assertEqual(node1.children, node2.children)
        self.assertEqual(node1.props, node2.props)

        node3 = HTMLNode("div", None, [node1], {"class": "container"})
        node4 = HTMLNode("div", None, [node2], {"class": "container"})
        self.assertEqual(node3.tag, node4.tag)
        self.assertEqual(node3.value, node4.value)
        self.assertEqual(len(node3.children), len(node4.children))
        self.assertEqual(node3.props, node4.props)

    def test_props_to_html(self):
        node = HTMLNode(
            "p", "Hello, world!", None, {"class": "text", "id": "paragraph"}
        )
        self.assertEqual(node.props_to_html(), ' class="text" id="paragraph"')

        node_no_props = HTMLNode("p", "Hello, world!")
        self.assertEqual(node_no_props.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode("p", "Hello", None, {"class": "text"})
        expected = "HTMLNode(p, Hello, None, {'class': 'text'})"
        self.assertEqual(repr(node), expected)


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "parent", "id": "main"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="parent" id="main"><span>child</span></div>',
        )

    def test_to_html_no_tag(self):
        child_node = LeafNode("p", "text")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaisesRegex(ValueError, "Tag must not be null for parent node"):
            parent_node.to_html()

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaisesRegex(
            ValueError, "Children must not be null for parent node"
        ):
            parent_node.to_html()

    def test_to_html_multiple_children(self):
        child1 = LeafNode("p", "first")
        child2 = LeafNode("p", "second")
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(parent_node.to_html(), "<div><p>first</p><p>second</p></div>")


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("p", "Hello, world!")
        node.props = {"class": "text", "id": "paragraph"}
        self.assertEqual(
            node.to_html(), '<p class="text" id="paragraph">Hello, world!</p>'
        )

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node_bold = TextNode("This is a text node", TextType.BOLD)
        node_bold2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node_bold, node_bold2)

        node_italic = TextNode("This is a italic node", TextType.ITALIC)
        node_italic2 = TextNode("This is a italic node", TextType.ITALIC)
        self.assertEqual(node_italic, node_italic2)

        node_code = TextNode("This is a code node", TextType.CODE)
        node_code2 = TextNode("This is a code node", TextType.CODE)
        self.assertEqual(node_code, node_code2)

        node_link = TextNode("This is a link node", TextType.LINK, "https://boot.dev")
        node_link2 = TextNode("This is a link node", TextType.LINK, "https://boot.dev")
        self.assertEqual(node_link, node_link2)

        node_image = TextNode("This is a image node", TextType.IMAGE, "https://img.url")
        node_image2 = TextNode(
            "This is a image node", TextType.IMAGE, "https://img.url"
        )
        self.assertEqual(node_image, node_image2)

        self.assertNotEqual(node_bold, node_image)
        self.assertNotEqual(
            node_link,
            TextNode("This is a link node", TextType.LINK, "https://other.dev"),
        )
        self.assertNotEqual(
            node_image,
            TextNode("This is a image node", TextType.IMAGE, "https://other.dev"),
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props["href"], "https://boot.dev")

    def test_image(self):
        node = TextNode("image alt text", TextType.IMAGE, "https://image.url")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props["src"], "https://image.url")
        self.assertEqual(html_node.props["alt"], "image alt text")


if __name__ == "__main__":
    unittest.main()
