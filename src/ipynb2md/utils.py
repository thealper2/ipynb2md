import argparse


def setup_argparser() -> argparse.ArgumentParser:
    """
    Sets command line arguments.

    Returns:
        argparse.ArgumentParser: Argument parser
    """
    parser = argparse.ArgumentParser(
        description="Converts Jupyter Notebook (.ipynb) files to Markdown (.md) files."
    )

    parser.add_argument("input_file", help="Path to .ipynb file to convert")

    parser.add_argument(
        "-o",
        "--output",
        help="Path to the output Markdown file (if not specified, a .md file with the same name will be created)",
    )

    return parser
