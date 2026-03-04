# Python script to split a markdown file into multiple files based on headings
# the filename of the markdown files are 0000000, 0000001, 0000002, etc
# the first file is {filename}-0000000.md, the second is {filename}-0000001.md, and so on.
# We do not use the pymuppdf library here, but rather only standard libraries.

import os
import sys

def split_markdown_by_headings(input_path):
    base, _ = os.path.splitext(os.path.basename(input_path))
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    chunks = []
    current_chunk = []
    for line in lines:
        if line.startswith('#'):
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = []
        current_chunk.append(line)
    if current_chunk:
        chunks.append(current_chunk)

    for idx, chunk in enumerate(chunks):
        out_filename = f"{base}-{idx:07d}.md"
        with open(out_filename, 'w', encoding='utf-8') as out_file:
            out_file.writelines(chunk)
        print(f"Wrote {out_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python split_md.py <markdown_file>")
        sys.exit(1)
    split_markdown_by_headings(sys.argv[1])