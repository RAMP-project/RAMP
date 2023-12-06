from nbconvert import RSTExporter
from nbconvert.writers import FilesWriter
import nbformat
import os

path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
    )
)


def convert_notebook_to_rst(input_file, output_dir, file_name):
    # Load the notebook
    with open(input_file, "r", encoding="utf-8") as f:
        notebook_content = nbformat.read(f, as_version=4)

    # Create an RST exporter
    rst_exporter = RSTExporter()

    # Generate RST content
    rst_content, resources = rst_exporter.from_notebook_node(notebook_content)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    output_file = os.path.join(output_dir, f"{file_name}.rst")

    # Write RST content to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rst_content)

    print(f"Conversion successful. RST file saved to: {output_file}")

    # Copy images to the output folder
    image_dir = output_dir
    for image_filename, image_data in resources["outputs"].items():
        image_path = os.path.join(output_dir, image_filename)
        with open(image_path, "wb") as img_file:
            img_file.write(image_data)


def get_all_ipynb_files(examples_path="notebooks"):
    all_files = os.listdir(examples_path)
    return [
        (os.path.join(path, examples_path, file), file.split(".ipynb")[0])
        for file in all_files
        if file.endswith("ipynb")
    ]


if __name__ == "__main__":
    files = get_all_ipynb_files()

    for file, folder in files:
        convert_notebook_to_rst(
            file, os.path.join(path, "source", "examples", folder), folder
        )
