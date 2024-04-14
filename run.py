from epub_extractor import extract
from consolidate_epub import consolidate

def main():
    character_limit = 9999999999
    # Extract files from .epub files
    extract()

    # Consolidate .xhtml files into text files
    consolidate('books',character_limit)

if __name__ == '__main__':
    main()
