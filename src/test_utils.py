import unittest
import tempfile
from utils import extract_title

class TestMarkdownParser(unittest.TestCase):
    def test_title_extract(self):
        md = """# Lord of The Rings
###Return of the Kings"""   
        #create a temp file for the markdown
        with tempfile.NamedTemporaryFile('w+', delete=True) as temp:
            temp.write(md)
            temp.seek(0) 
            title = extract_title(temp.name)
        self.assertEqual(title, "Lord of The Rings")

