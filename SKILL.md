# PDF-to-Markdown RAG Toolkit Skill

## Project Overview

This is a Python toolkit for converting PDF documents to Markdown format, specifically optimized for RAG (Retrieval Augmented Generation) and LLM applications. The project provides two main utilities:

1. **PDF to Markdown Conversion** - Extract text, tables, and images from PDFs in reading order
2. **Markdown Chunking** - Split large markdown files into smaller chunks based on heading boundaries

## Project Context

- **Purpose**: Enable efficient PDF document processing for vector databases and RAG pipelines
- **Target Use Case**: Converting technical documentation, manuals, and large documents for LLM consumption
- **Python Version**: 3.13+
- **Key Dependencies**: PyMuPDF, PyMuPDF4LLM
- **Package Manager**: uv (modern Python package manager)

## File Structure

```
.
├── pymupdf_rag.py          # Main PDF→MD converter (AGPL licensed, from Artifex)
├── split_md.py             # MD chunking utility (custom, simple)
├── main.py                 # Placeholder entry point
├── pyproject.toml          # Project metadata
├── uv.lock                 # Dependency lock file
├── .python-version         # Python 3.13
└── .gitignore              # Excludes connect* files, .venv, Python artifacts
```

## Key Workflows

### 1. PDF Conversion Workflow
```bash
# Basic conversion
python pymupdf_rag.py document.pdf

# With page selection
python pymupdf_rag.py document.pdf -pages 1-50,75-N

# Output: document.md
```

### 2. Markdown Chunking Workflow
```bash
# Split by headings
python split_md.py document.md

# Output: document-0000000.md, document-0000001.md, etc.
```

### 3. Complete RAG Pipeline
```bash
# Step 1: Convert PDF
python pymupdf_rag.py large-manual.pdf -pages 1-N

# Step 2: Split for RAG
python split_md.py large-manual.md

# Result: Numbered markdown chunks ready for vector embedding
```

## Important Code Conventions

### pymupdf_rag.py
- **License**: GNU AGPL v3.0 (Artifex Software)
- **DO NOT MODIFY** without understanding AGPL implications
- Uses PyMuPDF4LLM helper modules for text extraction
- Handles multi-column layouts, tables, images
- Reading order detection algorithm (Western reading order)
- Progress bar for long documents

### split_md.py
- **Simple utility** - only uses standard libraries
- Splits at ANY heading level (`#`, `##`, `###`, etc.)
- Zero-padded 7-digit numbering for proper sorting
- UTF-8 encoding throughout
- Safe to modify and extend

## Common Development Tasks

### Adding Features to split_md.py
When enhancing the chunking utility:
- Keep it dependency-free (only stdlib)
- Maintain UTF-8 encoding
- Consider adding CLI arguments for:
  - Heading level selection (e.g., split only on `##`)
  - Custom output directory
  - Chunk size limits
  - Overlap options for RAG

### Testing PDF Conversions
- Test PDFs are ignored via `.gitignore` (connect* pattern)
- Always verify table formatting after conversion
- Check for proper reading order in multi-column layouts
- Validate UTF-8 encoding in output

### Dependency Management
```bash
# Add new dependency
uv add package-name

# Update dependencies
uv lock

# Sync environment
uv sync
```

## RAG-Specific Considerations

### Chunk Size Guidelines
- Each heading section becomes one chunk
- Ideal for semantic search and retrieval
- Consider overlap strategies for context preservation
- Monitor chunk sizes for embedding model limits

### Output Format
- GitHub-flavored Markdown
- Preserves structure (headings, lists, code blocks)
- Tables in pipe format: `| col1 | col2 |`
- Images can be base64 embedded or referenced

### Vector Database Integration
After chunking, typical workflow:
1. Load each numbered .md file
2. Generate embeddings (OpenAI, Cohere, etc.)
3. Store in vector DB (Pinecone, Weaviate, ChromaDB)
4. Index with metadata (filename, chunk number, headings)

## Troubleshooting

### "Module not found" errors
```bash
uv sync  # Reinstall dependencies
```

### Memory issues with large PDFs
- Use `-pages` parameter to process in batches
- Process 50-100 pages at a time

### Garbled text output
- May indicate scanned PDF (needs OCR)
- Check PDF encoding/fonts

### Table formatting issues
- Complex nested tables may need manual cleanup
- Consider post-processing with regex if patterns emerge

## Code Modification Guidelines

### When modifying pymupdf_rag.py
- ⚠️ **Caution**: AGPL licensed - modifications must be open source
- Maintain compatibility with PyMuPDF4LLM helpers
- Preserve reading order algorithm
- Keep progress bar for UX
- Test with multi-column PDFs

### When modifying split_md.py
- ✅ Safe to modify freely
- Keep simple and fast
- Avoid adding heavy dependencies
- Maintain backward compatibility with existing chunks
- Test with edge cases (empty headings, nested structures)

### When working with main.py
- Currently unused placeholder
- Consider making it a CLI orchestrator for both tools
- Could add argument parsing with `argparse` or `click`
- Potential for unified pipeline command

## Integration Patterns

### With LangChain
```python
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter

# Use split chunks directly
loader = UnstructuredMarkdownLoader("document-0000001.md")
docs = loader.load()
```

### With LlamaIndex
```python
from llama_index import SimpleDirectoryReader

# Load all chunks
documents = SimpleDirectoryReader(
    input_files=["document-0000000.md", "document-0000001.md"]
).load_data()
```

### Custom RAG Pipeline
```python
import glob

# Process all chunks
for chunk_file in sorted(glob.glob("document-*.md")):
    with open(chunk_file, 'r') as f:
        content = f.read()
        # Generate embedding
        # Store in vector DB
```

## Testing Recommendations

### Manual Testing
1. Test with various PDF types:
   - Single column documents
   - Multi-column layouts
   - Tables (simple and complex)
   - Images and diagrams
   - Mixed content

2. Verify chunking:
   - Count output files
   - Check chunk boundaries
   - Verify heading preservation
   - Test with very large files

### Automated Testing
Consider adding:
- Unit tests for split_md.py functions
- Integration tests for full pipeline
- Regression tests with sample PDFs
- Output validation (markdown linting)

## Future Enhancement Ideas

### For pymupdf_rag.py
- Batch processing multiple PDFs
- JSON output option with metadata
- Custom table formatting
- OCR integration for scanned PDFs

### For split_md.py
- Configurable heading levels
- Chunk size limits (token/character based)
- Overlap option for context
- Metadata output (JSON with chunk info)
- Merge small chunks below threshold

### New Features
- Web interface for conversions
- API endpoint for document processing
- Batch processing CLI
- Quality metrics (tables detected, images found)
- Unified main.py orchestrator

## Best Practices

1. **Always test conversions** - PDF parsing is complex and document-dependent
2. **Check licenses** - pymupdf_rag.py is AGPL
3. **Version control chunks** - Useful for tracking document changes
4. **Monitor chunk sizes** - Important for embedding models
5. **Preserve metadata** - File paths, page numbers, headings are valuable for RAG
6. **Use consistent naming** - Zero-padded numbers ensure proper sorting

## Quick Reference

| Task | Command |
|------|---------|
| Convert PDF | `python pymupdf_rag.py file.pdf` |
| Convert pages | `python pymupdf_rag.py file.pdf -pages 1-10` |
| Split markdown | `python split_md.py file.md` |
| Install deps | `uv sync` |
| Add dependency | `uv add package-name` |

## Related Resources

- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [PyMuPDF4LLM GitHub](https://github.com/pymupdf/PyMuPDF4LLM)
- [uv Documentation](https://github.com/astral-sh/uv)
- [Markdown Spec](https://spec.commonmark.org/)

## Notes

- The `.gitignore` excludes `connect*` files (likely test/sample PDFs)
- Virtual environment is `.venv` (excluded from git)
- Python 3.13 specified in `.python-version`
- Project uses modern Python tooling (uv, not pip/virtualenv)
