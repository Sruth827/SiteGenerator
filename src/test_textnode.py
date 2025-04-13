import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_nq(self):
        node3 = TextNode("This is a text node", TextType.NORMAL)
        node4 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node3, node4)

    def test_url(self):
        node5 = TextNode("This is a text node", TextType.LINK, "www.aol.com")
        node6 = TextNode("This is a text node", TextType.LINK, "www.aol.com")
        self.assertEqual(node5, node6)

    def test_url_none(self): 
        node7 = TextNode("This is a text node", TextType.IMAGE)
        node8 = TextNode("This is a text node", TextType.IMAGE, "www.github.com")
        self.assertNotEqual(node7, node8)

if __name__ == "__main__":
    unittest.main()
