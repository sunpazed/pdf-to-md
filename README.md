# PDF to Markdown Converter

A Python toolkit for converting PDF documents to Markdown format optimized for RAG (Retrieval Augmented Generation) and LLM applications. This project provides tools to extract text from PDFs in reading order, preserve tables, and optionally split large markdown files into manageable chunks.

## Features

### PDF to Markdown Conversion ([pymupdf_rag.py](pymupdf_rag.py))
- **Smart Text Extraction**: Extracts text in Western reading order
- **Table Detection**: Automatically detects and converts tables to Markdown format
- **Multi-Column Support**: Handles multi-column layouts intelligently
- **Image Handling**: Can extract and embed images (optional base64 encoding)
- **Page Selection**: Convert specific pages or page ranges
- **Progress Tracking**: Visual progress bar during conversion
- **GitHub-Compatible**: Produces GitHub-flavored Markdown

### Markdown Splitting ([split_md.py](split_md.py))
- **Heading-Based Chunking**: Splits markdown files at heading boundaries
- **Sequential Naming**: Outputs numbered files for easy ordering
- **Preserves Structure**: Each chunk maintains its heading and content
- **Simple & Fast**: Uses only standard Python libraries

## Requirements

- Python 3.13+
- PyMuPDF v1.25.5 or later
- PyMuPDF4LLM (for enhanced LLM-optimized extraction)

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management:

```bash
# Clone the repository
git clone <repository-url>
cd pdf-to-md

# Install dependencies with uv
uv sync

# Or install manually with pip
pip install pymupdf pymupdf4llm
```

## Usage

### Converting PDF to Markdown

Basic conversion:
```bash
python pymupdf_rag.py input.pdf
```

This creates `input.md` in the same directory.

#### Convert specific pages:
```bash
# Convert pages 2-15, 40, and 43 to the last page
python pymupdf_rag.py input.pdf -pages 2-15,40,43-N

# Convert first 10 pages
python pymupdf_rag.py document.pdf -pages 1-10

# Convert single page
python pymupdf_rag.py document.pdf -pages 5
```

The `-pages` parameter accepts:
- Single pages: `5`
- Page ranges: `10-20`
- Multiple selections: `1-5,10,15-20`
- Last page indicator: `N` (e.g., `50-N` for page 50 to end)

### Splitting Markdown into Chunks

After converting a PDF to Markdown, you can split it into smaller files based on headings:

```bash
python split_md.py document.md
```

This creates files named:
- `document-0000000.md`
- `document-0000001.md`
- `document-0000002.md`
- ...

Each file contains content from one heading section.

## Project Structure

```
pdf-to-md/
├── pymupdf_rag.py          # Main PDF to Markdown converter
├── split_md.py             # Markdown splitting utility
├── main.py                 # Entry point (placeholder)
├── pyproject.toml          # Project metadata
├── uv.lock                 # Dependency lock file
├── .gitignore              # Git ignore rules
├── .python-version         # Python version specification
└── README.md               # This file
```

## Example Workflow

Here's a complete workflow from PDF to chunked markdown:

```bash
# 1. Convert PDF to Markdown
python pymupdf_rag.py large-document.pdf

# This creates: large-document.md

# 2. Split into chunks for RAG processing
python split_md.py large-document.md

# This creates:
# large-document-0000000.md
# large-document-0000001.md
# large-document-0000002.md
# ... (one file per heading section)
```

The chunked files can then be:
- Indexed in a vector database
- Processed individually by LLMs
- Used for semantic search
- Fed into RAG pipelines

## Use Cases

- **RAG Applications**: Convert documentation for vector database indexing
- **LLM Training**: Prepare PDF content in LLM-friendly format
- **Knowledge Base**: Convert technical manuals and guides to searchable markdown
- **Document Processing**: Batch convert PDF archives to markdown
- **Content Migration**: Move PDF-based content to markdown-based systems

## Technical Details

### pymupdf_rag.py
- Uses PyMuPDF for robust PDF parsing
- Implements custom reading order detection
- Handles complex layouts (multi-column, nested elements)
- Preserves formatting (bold, italic, lists, code blocks)
- Converts tables to pipe-separated markdown format
- Optional image extraction with base64 encoding
- Progress bar for long documents

### split_md.py
- Splits at any heading level (`#`, `##`, `###`, etc.)
- Preserves heading in each chunk
- Uses zero-padded numbering (7 digits) for proper sorting
- Handles UTF-8 encoding properly
- Lightweight with no external dependencies

## License

### pymupdf_rag.py
Copyright (C) 2024-2025 Artifex Software, Inc.

Licensed under the GNU Affero General Public License v3.0 or later.
Alternative commercial licensing available from Artifex Software.

For commercial licensing:
- Website: https://www.artifex.com/
- Contact: Artifex Software, Inc., 39 Mesa Street, Suite 108A, San Francisco, CA 94129, USA

### split_md.py
Custom utility script - free to use and modify.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Troubleshooting

**Issue**: "Module not found" errors
```bash
# Make sure dependencies are installed
uv sync
# or
pip install pymupdf pymupdf4llm
```

**Issue**: Conversion produces garbled text
- Some PDFs use non-standard encodings or are scanned images
- Try using OCR preprocessing for scanned documents

**Issue**: Tables not formatting correctly
- Complex tables may require manual adjustment
- Nested tables are converted to nested markdown

**Issue**: Memory issues with large PDFs
- Use the `-pages` parameter to process in batches
- Split the PDF before processing

## Acknowledgments

- Built with [PyMuPDF](https://pymupdf.readthedocs.io/)
- Uses [PyMuPDF4LLM](https://github.com/pymupdf/PyMuPDF4LLM) for optimized extraction
