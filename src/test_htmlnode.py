import unittest
from htmlnode import HTMLNode, ParentNode, LeafNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_props_valid(self):
        node = HTMLNode(None, None, None, {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        result = node.props_to_html()
        expected = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(result, expected)

    def test_props_empty(self):
        node = HTMLNode(None, None, None, {})
        result = node.props_to_html()
        expected = ""  
        self.assertEqual(result, expected)

    def test_props_single(self):
        node = HTMLNode(None, None, None, {
            "href": "https://www.google.com",
        })
        result = node.props_to_html()
        expected = 'href="https://www.google.com"'
        self.assertEqual(result, expected)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

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

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("span", "child 1")
        child2 = LeafNode("p", "child 2")
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(parent_node.to_html(), "<div><span>child 1</span><p>child 2</p></div>")

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_with_mixed_children(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        leaf_node = LeafNode("p", "leaf node")
        parent_node = ParentNode("div", [child_node, leaf_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><p>leaf node</p></div>",
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_Link(self):
        node = TextNode("This is a text node", TextType.LINK, "www.github.com/sruth827")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "www.github.com/sruth827")

    def test_text_Code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")



if __name__ == "__main__":
    unittest.main()
