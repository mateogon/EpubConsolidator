'''
EpubConsolidator Documentation
Overview
The EpubConsolidator class is designed to consolidate .xhtml files extracted from .epub books into a combined text file. The order of consolidation is determined from an order file named xhtml_files_order.txt found in the same directory as the .xhtml files.

Class Methods
__init__(self, base_path: str)
The constructor method for the EpubConsolidator class. It takes the base path where the extracted .xhtml files are located as an argument.

read_order_file(self)
This method reads the xhtml_files_order.txt file and returns a list of .xhtml file names in the order they should be consolidated.

remove_html_tags_and_empty_lines(self, text: str)
A helper method that takes a string, removes all HTML tags and empty lines from it, and returns the cleaned text.

consolidate_files(self)
This method reads all the .xhtml files listed in the order file, removes the HTML tags and empty lines from each file's content, and concatenates the contents in order. If a file is mainly composed of HTML (more than 50% of its content), it is skipped. The method returns a string of the consolidated content.

save_consolidated_files(self, combined_files: str)
This method saves the consolidated content to one or more text files. Each output file contains no more than 380000 characters. The output files are named book_segment_1.txt, book_segment_2.txt, etc., and are stored in the same directory as the .xhtml files. If such named files already exist in the directory, they are deleted before the new files are saved.

'''

import os
import re
from pathlib import Path


class EpubConsolidator:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.order_file = self.base_path / "xhtml_files_order.txt"
        self.order = self.read_order_file()

    def read_order_file(self):
        with open(self.order_file, 'r') as file:
            order = file.readlines()
        return [x.strip() for x in order]

    def remove_html_tags_and_empty_lines(self, text):
        text = re.sub("<.*?>", "", text)
        lines = text.split('\n')
        non_empty_lines = [line for line in lines if line.strip() != '' and not line.isdigit()]
        return '\n'.join(non_empty_lines)

    def consolidate_files(self):
        combined_files = ""
        for file_name in self.order:
            full_file_path = self.base_path / file_name
            if full_file_path.is_file():
                with open(full_file_path, 'r', errors='replace') as file:  
                    file_content = file.read()
                    
                    # Calculate the proportion of HTML tags in the file content
                    html_content = re.findall("<.*?>", file_content)
                    html_content_length = sum(len(tag) for tag in html_content)
                    total_content_length = len(file_content)
                    
                    # Skip the file if more than 50% of its content are HTML tags
                    if html_content_length / total_content_length > 0.5:
                        print(f"File {file_name} is mainly HTML, skipping.")
                        continue
                    
                    file_content = self.remove_html_tags_and_empty_lines(file_content)
                    combined_files += f"{file_content}\n"
            else:
                print(f"File {file_name} not found, skipping.")
        return combined_files

    def save_consolidated_files(self, combined_files):
        output_file_base = self.base_path / 'book_segment'

        # Delete any existing "book_segment_*.txt" files
        for old_file in self.base_path.glob(f"{output_file_base.stem}_*.txt"):
            old_file.unlink()

        file_number = 1
        output_file = output_file_base.with_name(f"{output_file_base.stem}_{file_number}.txt")
        char_count = 0

        for line in combined_files.split('\n'):
            line_length = len(line)
            if char_count + line_length >= 380000:
                file_number += 1
                output_file = output_file_base.with_name(f"{output_file_base.stem}_{file_number}.txt")
                char_count = 0
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(line + '\n')
                char_count += line_length

        print(f"Files consolidated and saved to {output_file_base.stem}_*.txt files successfully.")

def consolidate(books_folder):
    books_folder = Path(books_folder)
    for book_folder in books_folder.iterdir():
        if book_folder.is_dir():
            consolidator = EpubConsolidator(book_folder)
            combined_files = consolidator.consolidate_files()
            consolidator.save_consolidated_files(combined_files)
            