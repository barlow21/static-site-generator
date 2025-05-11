import unittest

from leafnode import LeafNode
from parentnode import ParentNode


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


if __name__ == "__main__":
    unittest.main()
