import sys
import os
from pathlib import Path
from markitdown import MarkItDown

SUPPORTED = {".pdf", ".docx", ".doc", ".xlsx", ".xls"}


def convert_file(input_path: str, output_path: str = None):
    path = Path(input_path)

    if not path.exists():
        print(f"Error: File not found: {input_path}")
        return

    if path.suffix.lower() not in SUPPORTED:
        print(f"Error: Unsupported file type '{path.suffix}'. Supported: {', '.join(SUPPORTED)}")
        return

    if output_path is None:
        output_path = path.with_suffix(".md")

    md = MarkItDown()
    result = md.convert(str(path))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result.text_content)

    print(f"Converted: {input_path} -> {output_path}")


def convert_folder(folder_path: str):
    folder = Path(folder_path)

    if not folder.is_dir():
        print(f"Error: Not a directory: {folder_path}")
        return

    files = [f for f in folder.rglob("*") if f.suffix.lower() in SUPPORTED]

    if not files:
        print("No supported files found.")
        return

    for f in files:
        output = f.with_suffix(".md")
        convert_file(str(f), str(output))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python convert.py <file>              # convert a single file")
        print("  python convert.py <file> <output.md>  # convert with custom output name")
        print("  python convert.py <folder>             # convert all files in a folder")
        sys.exit(1)

    target = sys.argv[1]

    if os.path.isdir(target):
        convert_folder(target)
    else:
        out = sys.argv[2] if len(sys.argv) > 2 else None
        convert_file(target, out)
