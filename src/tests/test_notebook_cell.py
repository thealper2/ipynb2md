import unittest
import base64
import os
from pathlib import Path

from src.ipynb2md.notebook_cell import NotebookCell


class TestNotebookCell(unittest.TestCase):
    def setUp(self):
        self.image_dir = Path("test_images")
        self.image_dir.mkdir(exist_ok=True)
        self.cell_counter = 1

    def tearDown(self):
        for file in self.image_dir.iterdir():
            file.unlink()

        self.image_dir.rmdir()

    def test_detect_language_python(self):
        cell_data = {
            "cell_type": "code",
            "source": ["import numpy as np\n", 'print("Hello, World!")'],
            "metadata": {},
        }
        cell = NotebookCell(cell_data, self.image_dir, self.cell_counter)
        self.assertEqual(cell.detect_language(), "python")

    def test_detect_language_r(self):
        cell_data = {
            "cell_type": "code",
            "source": ["library(ggplot2)\n", 'print("Hello, World!")'],
            "metadata": {},
        }
        cell = NotebookCell(cell_data, self.image_dir, self.cell_counter)
        self.assertEqual(cell.detect_language(), "r")

    def test_extract_image(self):
        cell_data = {"cell_type": "code", "source": [], "metadata": {}, "outputs": []}
        cell = NotebookCell(cell_data, self.image_dir, self.cell_counter)
        test_image_data = base64.b64encode(b"fake_image_data").decode("utf-8")
        image_path = cell.extract_image(test_image_data, "image/png")
        self.assertIsNotNone(image_path)
        self.assertTrue(os.path.exists(image_path))

    def test_to_markdown_code_cell(self):
        cell_data = {
            "cell_type": "code",
            "source": ['print("Hello, World!")'],
            "metadata": {},
            "outputs": [],
        }
        cell = NotebookCell(cell_data, self.image_dir, self.cell_counter)
        markdown = cell.to_markdown()
        self.assertIn("```python", markdown)
        self.assertIn('print("Hello, World!")', markdown)

    def test_to_markdown_markdown_cell(self):
        cell_data = {
            "cell_type": "markdown",
            "source": ["# Heading\n", "Some text"],
            "metadata": {},
            "outputs": [],
        }
        cell = NotebookCell(cell_data, self.image_dir, self.cell_counter)
        markdown = cell.to_markdown()
        self.assertIn("# Heading", markdown)
        self.assertIn("Some text", markdown)


if __name__ == "__main__":
    unittest.main()
