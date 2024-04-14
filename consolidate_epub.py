import os
import re
from pathlib import Path

class EpubConsolidator:
    def __init__(self, base_path, character_limit = 350000):
        self.base_path = Path(base_path)
        self.order_file = self.base_path / "files_order.txt" # Updated file name
        self.order = self.read_order_file()
        self.character_limit = character_limit
    def read_order_file(self):
        with open(self.order_file, 'r', encoding='utf-8') as file:
            order = file.readlines()
        return [x.strip() for x in order]

    def remove_html_tags_and_empty_lines(self, text):
        # Remove all spaces and tabs first
        text = re.sub(r"\s+", " ", text)  # This collapses all whitespace into single spaces for cleaner processing
        
        # Insert a newline before the start and after the end of <p> and <h1> tags
        text = re.sub(r"<div[^>]*>", "", text)
        text = re.sub(r"</div>", "\n", text)
        text = re.sub(r"<p[^>]*>", "", text)
        text = re.sub(r"</p>", "\n", text)
        text = re.sub(r"<h1[^>]*>", "", text)
        text = re.sub(r"</h1>", "\n", text)
        text = re.sub(r"<a[^>]*>", "", text)
        text = re.sub(r"</a>", "\n", text)
        text = re.sub(r"<span[^>]*>", "", text)
        text = re.sub(r"<link[^>]*/>", "", text)
        text = re.sub(r"</span>", "\n", text)
        # Remove DOCTYPE declarations
        text = re.sub(r"<!DOCTYPE[^>]*>", "", text)
        text = re.sub(r"&nbsp;"," ",text)
        # Remove CSS style blocks
        text = re.sub(r"<style.*?>.*?</style>", "", text, flags=re.DOTALL)

        # Remove HTML comments
        text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)

        # Remove all other HTML tags
        text = re.sub(r"<.*?>", "", text)

        # Remove consecutive spaces and tabs
        #text = re.sub(r"\s+", " ", text)

        # Split text into lines and remove empty lines
        lines = text.split('\n')
        non_empty_lines = [line for line in lines if line.strip() != '']
        
        return '\n'.join(non_empty_lines)
        #return text



    def consolidate_files(self):
        combined_files = ""
        copyright_keywords = [
            "copyright", "all rights reserved",
            "ISBN", "Library of Congress"
        ]
        for file_name in self.order:
            full_file_path = self.base_path / file_name
            if full_file_path.is_file():
                with open(full_file_path, 'r', encoding='utf-8', errors='replace') as file:
                    file_content = file.read()

                    html_content = re.findall("<.*?>", file_content)
                    html_content_length = sum(len(tag) for tag in html_content)
                    total_content_length = len(file_content)

                    if html_content_length / total_content_length > 0.9:
                        print(f"File {file_name} is mainly HTML, skipping.")
                        continue

                    cleaned_content = self.remove_html_tags_and_empty_lines(file_content)
                    lines = cleaned_content.split('\n')
                    non_empty_lines = [line for line in lines if line.strip() != '']

                    # Keyword check for copyright pages
                    if any(keyword in cleaned_content.lower() for keyword in copyright_keywords):
                        print(f"File {file_name} detected as a copyright page, skipping.")
                        continue

                    # Analyze the content to determine if it's likely an index or footnote
                    if len(non_empty_lines) < 5 or (sum(len(line) for line in non_empty_lines) / len(non_empty_lines)) < 40:
                        print(f"File {file_name} seems to be an index or footnote, skipping.")
                        continue

                    # Add a new line and the file name as an indicator for a new chapter
                    combined_files += f"\n\nChapter: {file_name}\n\n{cleaned_content}\n"
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
            if char_count + line_length >= self.character_limit:
                file_number += 1
                output_file = output_file_base.with_name(f"{output_file_base.stem}_{file_number}.txt")
                char_count = 0
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(line + '\n')
                char_count += line_length

        print(f"Files consolidated and saved to {output_file_base.stem}_*.txt files successfully.")

def consolidate(books_folder,character_limit):
    books_folder = Path(books_folder)
    for book_folder in books_folder.iterdir():
        if book_folder.is_dir():
            print(f"----Consolidating files in {book_folder}----")
            consolidator = EpubConsolidator(book_folder,character_limit)
            combined_files = consolidator.consolidate_files()
            consolidator.save_consolidated_files(combined_files)
