import unittest
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from src.ipynb2md.notebook_converter import NotebookConverter


class TestNotebookConverter(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.test_notebook_path = Path(self.temp_dir.name) / "test_notebook.ipynb"
        self.test_image_dir = Path(self.temp_dir.name) / "test_images"
        self.test_image_dir.mkdir(exist_ok=True)

        notebook_content = {
            "cells": [
                {
                    "cell_type": "code",
                    "source": ["print('Hello, World!')"],
                    "metadata": {},
                    "outputs": [],
                },
                {
                    "cell_type": "markdown",
                    "source": ["# Heading\n", "Some text"],
                    "metadata": {},
                    "outputs": [],
                },
            ],
            "metadata": {"kernelspec": {"name": "python3", "language": "python"}},
        }
        with open(self.test_notebook_path, "w") as f:
            json.dump(notebook_content, f)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_read_notebook(self):
        converter = NotebookConverter(str(self.test_notebook_path))
        self.assertTrue(converter.read_notebook())
        self.assertEqual(len(converter.cells), 2)

    def test_detect_notebook_language(self):
        converter = NotebookConverter(str(self.test_notebook_path))
        converter.read_notebook()
        self.assertEqual(converter.detect_notebook_language(), "python")

    def test_convert(self):
        converter = NotebookConverter(str(self.test_notebook_path))
        converter.read_notebook()
        markdown_content = converter.convert()
        self.assertIn("```python", markdown_content)
        self.assertIn("print('Hello, World!')", markdown_content)
        self.assertIn("# Heading", markdown_content)
        self.assertIn("Some text", markdown_content)

    def test_save(self):
        converter = NotebookConverter(str(self.test_notebook_path))
        converter.read_notebook()
        output_path = Path(self.temp_dir.name) / "output.md"
        success, saved_path = converter.save(str(output_path))
        self.assertTrue(success)
        self.assertTrue(output_path.exists())
        with open(output_path, "r") as f:
            content = f.read()
            self.assertIn("```python", content)
            self.assertIn("print('Hello, World!')", content)
            self.assertIn("# Heading", content)
            self.assertIn("Some text", content)


if __name__ == "__main__":
    unittest.main()
