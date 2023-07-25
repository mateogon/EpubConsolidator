from epub_extractor import extract
from consolidate_epub import consolidate

def main():
    # Extract .xhtml files from .epub files
    extract()

    # Consolidate .xhtml files into text files
    consolidate('books')

if __name__ == '__main__':
    main()
