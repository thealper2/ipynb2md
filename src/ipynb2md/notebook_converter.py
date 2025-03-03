import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set

from src.ipynb2md.notebook_cell import NotebookCell


class NotebookConverter:
    """Class that converts Jupyter Notebook file to Markdown file."""

    def __init__(self, input_file: str) -> None:
        """
        Constructor method of the NotebookConverter class.

        Args:
            input_file: Path to .ipynb file to convert
        """
        self.input_file: Path = Path(input_file)
        self.output_file: Optional[Path] = None
        self.notebook_data: Dict[str, Any] = {}
        self.cells: List[NotebookCell] = []

        # Directory for images
        self.image_dir: Path = self.input_file.parent / f"{self.input_file.stem}_images"

    def prepare_image_directory(self) -> None:
        """
        Creates an index for extracted images.
        """
        if not self.image_dir.exists():
            os.makedirs(self.image_dir, exist_ok=True)

    def read_notebook(self) -> bool:
        """
        Reads and parses the notebook file.

        Returns:
            bool: True if the read operation was successful, False otherwise
        """
        try:
            with open(self.input_file, "r", encoding="utf-8") as file:
                self.notebook_data = json.load(file)

            # Prepare index for images
            self.prepare_image_directory()

            # Separate cells
            for idx, cell_data in enumerate(self.notebook_data.get("cells", [])):
                self.cells.append(NotebookCell(cell_data, self.image_dir, idx + 1))

            return True
        except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
            print(
                f"ERROR: File {self.input_file} could not be read. {str(e)}", file=sys.stderr
            )
            return False

    def detect_notebook_language(self) -> str:
        """
        Detects the main programming language of the Notebook.

        Returns:
            str: Main programming language detected
        """
        # Language detection from kernel information
        kernel_info = self.notebook_data.get("metadata", {}).get("kernelspec", {})
        kernel_language = kernel_info.get("language", "")

        if kernel_language:
            return kernel_language

        # Count the language frequency from the code cells
        language_counts: Dict[str, int] = {}
        for cell in self.cells:
            if cell.cell_type == "code":
                language = cell.detect_language()
                language_counts[language] = language_counts.get(language, 0) + 1

        # Find the most used language
        main_language = (
            max(language_counts.items(), key=lambda x: x[1])[0]
            if language_counts
            else "python"
        )
        return main_language

    def check_for_inline_images(self) -> None:
        """
        Extracts inline base64 encoded images in Markdown cells.
        """
        for cell in self.cells:
            if cell.cell_type == "markdown":
                # Extract base64 images from Markdown content
                updated_source = cell.extract_inline_images_from_markdown()
                cell.source = [updated_source]

    def convert(self) -> str:
        """
        Converts Notebook to Markdown content.

        Returns:
            str: Created Markdown content
        """
        # Extract inline images in Markdown
        self.check_for_inline_images()

        markdown_content = ""

        # Convert and insert each cell
        for cell in self.cells:
            markdown_content += cell.to_markdown()

        # Create a list of extracted images
        extracted_images: Set[str] = set()
        for cell in self.cells:
            extracted_images.update(cell.extracted_images)

        return markdown_content

    def _extract_title(self) -> str:
        """
        It removes the hood from the notebook.

        Returns:
            str: Notebook title, if not found the file name is used
        """
        # First search for the title in the first markdown cell
        for cell in self.cells:
            if cell.cell_type == "markdown":
                source = "".join(cell.source)
                match = re.search(r"^# (.+)$", source, re.MULTILINE)
                if match:
                    return match.group(1).strip()

        # Title not found, use file name
        return self.input_file.stem

    def _ensure_relative_paths(self, content: str) -> str:
        """
        Corrects markdown content by making image paths relative.

        Args:
            content: Markdown content

        Returns:
            str: Markdown content with relative paths
        """

        # Turn absolute paths into relative paths
        def replace_path(match):
            full_path = match.group(1)
            if os.path.isabs(full_path):
                filename = os.path.basename(full_path)
                return f"](./{self.image_dir.name}/{filename})"
            return match.group(0)

        # ![...](path) fix the roads in the structure
        path_pattern = re.compile(r"\]\(([^)]+)\)")
        return path_pattern.sub(replace_path, content)

    def save(self, output_file: Optional[str] = None) -> Tuple[bool, str]:
        """
        Saves the generated Markdown content to the file.

        Args:
            output_file: Path to the output file. If not specified, a .md file with the same name as input_file is used.

        Returns:
            Tuple[bool, str]: Full path to the success status and output file
        """
        if output_file:
            self.output_file = Path(output_file)
        else:
            self.output_file = self.input_file.with_suffix(".md")

        try:
            markdown_content = self.convert()

            # Final check - relativise the paths of images
            markdown_content = self._ensure_relative_paths(markdown_content)

            with open(self.output_file, "w", encoding="utf-8") as file:
                file.write(markdown_content)

            return True, str(self.output_file)
        except (PermissionError, IOError) as e:
            error_msg = f"ERROR: Failed to write {self.output_file}. {str(e)}"
            print(error_msg, file=sys.stderr)
            return False, error_msg
