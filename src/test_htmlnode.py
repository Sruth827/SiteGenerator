import unittest
from htmlnode import HTMLNode
from leafnode import LeafNode

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

if __name__ == "__main__":
    unittest.main()
