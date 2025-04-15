import unittest
from splitblock import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownParser(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph
        
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_heading(self):
        md = "#### test test test"
        tested = block_to_block_type(md)
        self.assertEqual(tested, BlockType.HEADING)

    def test_block_to_block_code(self):
        md = "``` test test test```"
        tested = block_to_block_type(md)
        self.assertEqual(tested, BlockType.CODE)

    def test_block_to_block_quote(self):
        md = ">'sdsdsdsd'"
        tested = block_to_block_type(md)
        self.assertEqual(tested, BlockType.QUOTE)
 
    def test_block_to_block_code_unordered(self):
        md = "- sadknadkn,as dad , a d,"
        tested = block_to_block_type(md)
        self.assertEqual(tested, BlockType.UNORDERED_LIST)

    def test_block_to_block_ordered(self):
        md = "1.     2.      3.     4.     5.    "
        tested = block_to_block_type(md)
        self.assertEqual(tested, BlockType.ORDERED_LIST)

    def test_block_to_block_paragraph(self):
        md = "dnamsdn902323nas8dasd "
        tested = block_to_block_type(md)
        self.assertEqual(tested, BlockType.PARAGRAPH)



if __name__ == "__main__":
    unittest.main()


