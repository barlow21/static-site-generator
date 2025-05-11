import unittest

from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        from htmlnode import HTMLNode

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


if __name__ == "__main__":
    unittest.main()
