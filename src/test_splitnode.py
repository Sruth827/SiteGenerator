import unittest
from textnode import TextNode, TextType
from splitnode import split_node_delimiter, extract_markdown_images, extract_markdown_links



class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_split(self):
        node = TextNode("This is `code` text", TextType.TEXT)
        new_nodes = split_node_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_multiple_delimiters(self):
        node = TextNode("This `has` multiple `code` blocks", TextType.TEXT)
        new_nodes = split_node_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[1].text, "has")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[3].text, "code")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)

    def test_italic_split(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_node_delimiter([node], "_", TextType.ITALIC)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)

    def test_bold_split(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_node_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

    def test_no_split(self):
        node = TextNode("No delimiters here", TextType.TEXT)
        new_nodes = split_node_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "No delimiters here")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_unmatched_delimiter(self):
        node = TextNode("Unmatched `delimiter", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_node_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(str(context.exception), "Invalid Markdown: no matching '`'")

    def test_mixed_node_types(self):
        node1 = TextNode("This is `code` text", TextType.TEXT)
        node2 = TextNode("This is bold text", TextType.BOLD)
        new_nodes = split_node_delimiter([node1, node2], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[3].text, "This is bold text")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with [github](https://github.com/sruth827)"
        )
        self.assertListEqual([("github", "https://github.com/sruth827")], matches)

    def test_extract_markdown_NoImage(self):
        matches = extract_markdown_images("This is a text with an ![]()")
        self.assertNotEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    
    def text_extract_markdown_NoLinks(self):
        matches = extract_markdown_links("This is text with []()")
        self.assertNotEqual([("github", "https://github.com/sruth827")], matches)

if __name__ == "__main__":
    unittest.main()
