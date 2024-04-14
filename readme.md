# EpubConsolidator

EpubConsolidator is a versatile Python tool designed to simplify the process of converting `.epub` files into clean, consolidated text suitable for querying any large language model (LLM). It efficiently processes `.epub` files, removing unnecessary HTML and metadata, and segments the text into manageable parts to overcome character limits typically imposed by LLMs.

## Overview

The tool is ideal for users looking to extract pure textual content from books, making it easier to leverage LLMs for insights, research, or any form of textual analysis. EpubConsolidator ensures that users receive only the essential content, free from formatting distractions, allowing for more effective interaction with various LLM technologies.

## Components

EpubConsolidator consists of two main components:

1. **EpubExtractor:** Extracts `.xhtml` and `.html` files based on the order defined in the `.opf` file contained within the `.epub`, ensuring the textual content retains its original narrative sequence.

2. **EpubConsolidator:** Cleans the extracted files by removing HTML tags and unnecessary sections like indexes or footnotes. The process respects the character limitations of LLMs by segmenting the text into parts.

## Usage

To use EpubConsolidator, simply place your `.epub` files in the same directory as the tool and execute the provided script. This automatically handles the extraction and consolidation of the text into clean segments ready for LLM processing.

## How to Run

1. Clone or download the repository.
2. Ensure your `.epub` files are in the epub folder.
3. Execute the script to start the extraction and consolidation process:

```bash
python run.py
```

4. Find the output in the 'books' directory, organized into subdirectories named after the original .epub files, with consolidated text files labeled as book*segment*\*.txt.
