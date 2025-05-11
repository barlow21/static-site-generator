import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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
