from src.ipynb2md.notebook_converter import NotebookConverter
from src.ipynb2md.utils import setup_argparser


def main() -> int:
    """
    Function of the main program.

    Returns:
        int: Exit code (0: successful, 1: error)
    """
    parser = setup_argparser()
    args = parser.parse_args()

    # Create the converter
    converter = NotebookConverter(args.input_file)

    # Read the Notebook
    if not converter.read_notebook():
        return 1

    # Convert and save
    success, output_path = converter.save(args.output)

    if success:
        print(f"Conversion successful: {output_path}")
        # Provide information for extracted images
        images_path = converter.image_dir
        if images_path.exists() and any(images_path.iterdir()):
            print(f"Extracted images: {images_path}")
        return 0
    else:
        return 1
