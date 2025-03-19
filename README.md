# ipynb2md - Jupyter Notebook to Markdown Converter

**ipynb2md**, is a Python tool that converts Jupyter Notebook (.ipynb) files into Markdown (.md) format. This tool is particularly useful when you want to convert your Jupyter Notebooks into documents or blog posts.

## :clipboard: Table of Contents

1. [Features](https://github.com/thealper2/ipynb2md/tree/main?tab=readme-ov-file#%C3%B6zellikler)
2. [Installation](https://github.com/thealper2/ipynb2md/tree/main?tab=readme-ov-file#kurulum)
3. [Usage](https://github.com/thealper2/ipynb2md/tree/main?tab=readme-ov-file#kullan%C4%B1m)
4. [Contributing](https://github.com/thealper2/ipynb2md/tree/main?tab=readme-ov-file#katk%C4%B1da-bulunma)
5. [License](https://github.com/thealper2/ipynb2md/tree/main?tab=readme-ov-file#lisans)

## :dart: Features

- Converts Jupyter Notebook cells into Markdown format.
- Automatically detects code cell languages (Python, R, JavaScript, etc.).
- Extracts images from the notebook and embeds them into the Markdown file.
- Properly handles Markdown cells and HTML outputs.

## :hammer_and_wrench: Installation

Clone the project to your local machine:

```bash
git clone https://github.com/thealper2/ipynb2md.git
cd ipynb2md
```

Install the required dependencies using the `pyproject.toml` file:

```bash
pip install .
```

## :joystick: Usage

### Command Line Interface (CLI)

You can run the project from the command line using the `run.py` script:

```bash
python run.py path/to/your_notebook.ipynb
```

This command converts the specified Jupyter Notebook file into Markdown format and saves it in the same directory. You can use the `-o` or `--output` option to specify the output file name:

```bash
python run.py path/to/your_notebook.ipynb -o output_file.md
```

### Using as a Python Module

You can also use the project as a Python module:

```python
from src.ipynb2md.notebook_converter import NotebookConverter

converter = NotebookConverter("path/to/your_notebook.ipynb")
converter.read_notebook()
success, output_path = converter.save("output_file.md")

if success:
    print(f"Markdown dosyası başarıyla kaydedildi: {output_path}")
else:
    print("Dönüştürme başarısız oldu.")
```

## :handshake: Contributing

If you wish to contribute, please follow these steps:

1. Fork this repository.
2. Create a new branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push your branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## :scroll: License

This project is licensed under the MIT License. For more information, see the LICENSE file.
