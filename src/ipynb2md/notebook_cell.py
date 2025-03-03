import base64
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional


class NotebookCell:
    """The class representing the Jupyter Notebook cell."""

    def __init__(
        self, cell_data: Dict[str, Any], image_dir: Path, cell_counter: int
    ) -> None:
        """
        Constructor method of the NotebookCell class.

        Args:
            cell_data: Raw data dictionary of the Jupyter Notebook cell
            image_dir: Directory to save extracted images
            cell_counter: Cell number (for unique identifier)
        """
        self.cell_type: str = cell_data.get("cell_type", "")
        self.source: List[str] = cell_data.get("source", [])
        self.metadata: Dict[str, Any] = cell_data.get("metadata", {})
        self.outputs: List[Dict[str, Any]] = cell_data.get("outputs", [])
        self.image_dir: Path = image_dir
        self.cell_counter: int = cell_counter
        self.image_counter: int = 0
        self.extracted_images: List[str] = []

    def detect_language(self) -> str:
        """
        Detects the programming language of the code cell.

        Returns:
            str: The detected programming language, returning the default ‘python’ if not detected.
        """
        # Get language information from metadata
        language = self.metadata.get("language", "")

        # Language extraction from kernel information
        if not language:
            kernel_spec = self.metadata.get("kernelspec", {})
            kernel_name = kernel_spec.get("name", "").lower()
            kernel_language = kernel_spec.get("language", "").lower()

            if kernel_language:
                language = kernel_language
            elif kernel_name:
                # Language extraction from kernel name
                if "python" in kernel_name:
                    language = "python"
                elif "r" == kernel_name or "ir" in kernel_name:
                    language = "r"
                elif "julia" in kernel_name:
                    language = "julia"
                elif "javascript" in kernel_name or "js" in kernel_name:
                    language = "javascript"
                elif "typescript" in kernel_name or "ts" in kernel_name:
                    language = "typescript"
                elif "java" in kernel_name:
                    language = "java"

        # If the language is not found, try to detect it from the source code
        if not language and self.cell_type == "code" and self.source:
            code = "".join(self.source).lower()

            # Simple language detection rules
            if re.search(
                r"import\s+[a-zA-Z_][a-zA-Z0-9_]*|from\s+[a-zA-Z_][a-zA-Z0-9_]*\s+import",
                code,
            ):
                language = "python"
            elif re.search(r"library\(|require\(", code):
                language = "r"
            elif re.search(
                r"console\.log|document\.get|var\s+[a-zA-Z_]|let\s+[a-zA-Z_]|const\s+[a-zA-Z_]",
                code,
            ):
                language = "javascript"
            elif re.search(
                r"public\s+(static\s+)?class|public\s+(static\s+)?void", code
            ):
                language = "java"
            elif re.search(r"System\.out\.println", code):
                language = "java"
            elif re.search(r"printf|scanf|#include", code):
                language = "c"
            elif re.search(r"cout|cin|namespace|#include\s+<iostream>", code):
                language = "cpp"
            elif re.search(r"using\s+namespace|template\s*<", code):
                language = "cpp"
            elif re.search(r"func\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(", code):
                language = "go"
            elif re.search(r"package\s+main", code):
                language = "go"
            elif re.search(
                r"SELECT|FROM|WHERE|INSERT|UPDATE|DELETE", code
            ) and re.search(r";$", code.strip()):
                language = "sql"

        # Use python by default
        return language.lower() if language else "python"

    def extract_image(self, data: str, mime_type: str) -> Optional[str]:
        """
        Extracts the Base64 encoded image and saves it to a file.

        Args:
            data: Base64 encoded image data
            mime_type: MIME type of the image (image/png, image/jpeg, vb.)

        Returns:
            Optional[str]: File path of the recorded image or None in case of error
        """
        try:
            # Determine the extension from the MIME type
            extension = mime_type.split("/")[-1]
            # PNG, JPG, JPEG, GIF, SVG destekli
            if extension == "jpeg":
                extension = "jpg"
            elif extension not in ["png", "jpg", "gif", "svg", "bmp", "webp"]:
                extension = "png"

            # Create the name of the image file - make it unique with cell number and image number
            self.image_counter += 1
            image_filename = (
                f"cell_{self.cell_counter}_image_{self.image_counter}.{extension}"
            )
            image_path = self.image_dir / image_filename

            try:
                binary_data = base64.b64decode(data)
                with open(image_path, "wb") as file:
                    file.write(binary_data)

                rel_path = str(image_path)
                self.extracted_images.append(str(image_path))
                return rel_path

            except base64.binascii.Error:
                print(
                    f"WARNING: Invalid Base64 data. Cell: {self.cell_counter}, Image: {self.image_counter}",
                    file=sys.stderr,
                )
                return None

        except Exception as e:
            print(
                f"ERROR: The image could not be extracted. Cell: {self.cell_counter}, Image: {self.image_counter}. {str(e)}",
                file=sys.stderr,
            )
            return None

    def _ensure_newline_after_content(self, content: str) -> str:
        """
        It makes sure that there is a new line at the end of the content:

        Args:
            content: Content to check

        Returns:
            str: Content with new line at the end
        """
        if not content.endswith("\n"):
            content += "\n"

        if not content.endswith("\n\n"):
            content += "\n"

        return content

    def _normalize_html_output(self, html_content: str) -> str:
        """
        Normalises HTML output for Markdown.

        Args:
            html_content: HTML content

        Returns:
            str: Normalized HTML content
        """
        # Insert new row after table
        html_content = re.sub(r"(</table>)", r"\1\n\n", html_content)

        # Insert new line after div
        html_content = re.sub(r"(</div>)", r"\1\n", html_content)

        return html_content

    def _process_markdown_source(self, source: str) -> str:
        """
        Processes Markdown source code and troubleshoots formatting issues.

        Args:
            source: Markdown source code

        Returns:
            str: Processed Markdown content
        """
        # Insert space after Markdown lists
        source = re.sub(r"(\n\s*[-*+]\s+.*\n)(?![\s\n])", r"\1\n", source)

        # Insert new line after title
        source = re.sub(r"(\n#{1,6}\s+.*\n)(?!\n)", r"\1\n", source)

        # Add whitespace before and after the code block
        source = re.sub(r"(?<!\n\n)```", "\n\n```", source)
        source = re.sub(r"```(?!\n\n)", "```\n\n", source)

        return source

    def to_markdown(self) -> str:
        """
        Converts the cell to Markdown format.

        Returns:
            str: Cell content in Markdown format
        """
        if self.cell_type == "markdown":
            # Retrieve markdown content containing HTML tags and troubleshoot formatting issues
            source = "".join(self.source)
            processed_source = self._process_markdown_source(source)
            return self._ensure_newline_after_content(processed_source)

        elif self.cell_type == "code":
            # Detect programming language
            language = self.detect_language()

            # Create programming language block for code cells
            md_content = f"\n```{language}\n"
            md_content += "".join(self.source)
            md_content += "\n```\n\n"

            if self.outputs:
                for output_idx, output in enumerate(self.outputs):
                    output_type = output.get("output_type", "")

                    if output_type == "stream":
                        md_content += "```\n"
                        md_content += "".join(output.get("text", []))
                        md_content += "\n```\n\n"

                    elif (
                        output_type == "execute_result" or output_type == "display_data"
                    ):
                        data = output.get("data", {})

                        # Output in text/plain format
                        if "text/plain" in data:
                            text_content = "".join(data["text/plain"])
                            md_content += "```\n"
                            md_content += text_content
                            md_content += "\n```\n\n"

                        # Output in text/html format
                        if "text/html" in data:
                            html_content = "".join(data["text/html"])
                            html_content = self._normalize_html_output(html_content)

                            md_content += "```html\n"
                            md_content += html_content
                            md_content += "\n```\n\n"

                        # Image output - for all image formats
                        for mime_type, content in data.items():
                            if mime_type.startswith("image/"):
                                # Get Base64 data
                                image_data = content
                                if isinstance(image_data, list):
                                    image_data = "".join(image_data)

                                # Extract and save image
                                image_path = self.extract_image(image_data, mime_type)
                                if image_path:
                                    md_content += f"![Image - Cell {self.cell_counter}, Output {output_idx + 1}]({image_path})\n\n"

                    elif output_type == "error":
                        md_content += "```\n"
                        md_content += "\n".join(output.get("traceback", []))
                        md_content += "\n```\n\n"

            return md_content

        else:
            # Warning for unknown cell types
            return f"_Unknown cell type: {self.cell_type}_\n\n"

    def extract_inline_images_from_markdown(self) -> str:
        """
        Detects and extracts inline base64 encoded images in Markdown.

        Returns:
            str: Markdown content with images removed
        """
        if self.cell_type != "markdown":
            return "".join(self.source)

        markdown_content = "".join(self.source)

        # Detect base64 encoded images in Markdown
        # ![alt text](data:image/png;base64,...)
        img_pattern = re.compile(r"!\[(.*?)\]\((data:image/([a-z]+);base64,([^)]+))\)")

        def replace_with_file(match):
            alt_text = match.group(1)
            mime_type = f"image/{match.group(3)}"
            base64_data = match.group(4)

            image_path = self.extract_image(base64_data, mime_type)
            if image_path:
                return f"![{alt_text}]({image_path})"
            else:
                # Retain original label if image is not extracted
                return match.group(0)

        # Extract all detected images and save them to files
        return img_pattern.sub(replace_with_file, markdown_content)
