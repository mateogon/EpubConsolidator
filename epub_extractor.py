'''
## `EpubExtractor` Class
    The `EpubExtractor` class is designed to extract content from `.epub` files. The class has several methods to accomplish this:

### `__init__(self, epub_path: str)`
    The class constructor takes a string argument, `epub_path`, which is the path to the `.epub` file to be processed. It initializes the class with this path and creates an output folder for the extracted contents.

### `create_output_folder(self) -> Path`
    This method creates an output folder for the extracted contents based on the name of the `.epub` file. The folder is created inside a parent directory named "books". If the parent directory does not exist, it is created. 

### `find_opf_file(self, myzip: zipfile.ZipFile) -> Optional[str]`
    This method takes a `zipfile.ZipFile` object as argument, representing the `.epub` file to be processed. It searches for the `.opf` file inside the `.epub` file, which contains metadata and the manifest for the `.epub` file. The method extracts the order of `.xhtml` files listed in the `.opf` file and saves this order to a `.txt` file by calling the `save_order_to_file` method. If the `.opf` file is found, the method returns its name; otherwise, it returns `None`.

### `extract_xhtml_files(self) -> None`
    This method extracts all `.xhtml` files from the `.epub` file and saves them to the output directory created by `create_output_folder`. Each `.xhtml` file is saved under its own name.

### `save_order_to_file(self, xhtml_files_order: list) -> None`
    This method takes a list of `.xhtml` file names and saves them to a `.txt` file in the order they appear in the `.opf` file. The `.txt` file is saved to the output directory.

## `extract()` Function
    It finds all .epub files in the current directory and creates an instance of the EpubExtractor class for each .epub file. It then calls the find_opf_file and extract_xhtml_files methods to extract the contents of each .epub file.
 '''
 

import logging
from pathlib import Path
import zipfile
from xml.etree import ElementTree
import os
from collections import defaultdict
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO)

class EpubExtractor:
    def __init__(self, epub_path: str):
        self.epub_path = Path(epub_path)
        self.output_folder = self.create_output_folder()

    def create_output_folder(self) -> Path:
        """Creates an output folder based on the epub file name."""
        books_folder = Path("books")
        books_folder.mkdir(exist_ok=True)

        epub_folder = books_folder / self.epub_path.stem
        epub_folder.mkdir(exist_ok=True)

        return epub_folder

    def find_opf_file(self, myzip: zipfile.ZipFile) -> Optional[str]:
        """Finds the .opf file in the entire .epub file and extracts the order of files."""
        for file in myzip.namelist():
            if file.endswith('.opf'):
                with myzip.open(file) as opf_file:
                    tree = ElementTree.parse(opf_file)

                manifest_items = tree.findall('.//{http://www.idpf.org/2007/opf}item')

                # Extend search to include .html files
                files_order = [item.attrib['href'] for item in manifest_items if 'html' in item.attrib['href']]
                self.save_order_to_file(files_order)

                return file
        return None

    def extract_xhtml_files(self) -> None:
        """Extracts all .xhtml and .html files from the epub file."""
        with zipfile.ZipFile(self.epub_path, 'r') as myzip:
            for file in myzip.namelist():
                # Extend extraction to include .html files
                if file.endswith('.xhtml') or file.endswith('.html'):
                    with myzip.open(file) as content_file:
                        content = content_file.read()

                    output_file_path = self.output_folder / Path(file).name
                    with open(output_file_path, 'wb') as new_file:
                        new_file.write(content)
                    logging.info(f"Extracted file: {output_file_path}")


    def save_order_to_file(self, files_order: list) -> None:
        """Saves the order of XHTML and HTML files to a text file."""
        order_file_path = self.output_folder / "files_order.txt"
        with open(order_file_path, 'w') as order_file:
            for file in files_order:
                file_name = os.path.basename(file)
                order_file.write(file_name + "\n")
        logging.info(f"Files order saved to {order_file_path}")


def extract():
    epub_files = Path('.').glob('*.epub')
    for epub_path in epub_files:
        extractor = EpubExtractor(epub_path)
        with zipfile.ZipFile(epub_path, 'r') as myzip:
            extractor.find_opf_file(myzip)
        extractor.extract_xhtml_files()
