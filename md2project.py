#!/usr/bin/env python3
"""
Markdown to Project Structure Utility

Extracts file paths and code blocks from markdown documentation
and creates the corresponding folder structure and files.
"""

import re
import os
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple


def extract_files_from_markdown(markdown_content: str) -> Dict[str, str]:
    """Extract file paths and their content from markdown files."""
    files_dict = {}

    # Pattern 1: Bold filename followed by code block
    pattern1 = r'\*\*([^\*]+\.(ts|tsx|js|jsx|json|css|html|md|py|go|sh|yaml|yml|toml|txt|env|gitignore))\*\*\s*(?:\[.*?\])?\s*```(?:\w+)?\s*\n(.*?)```'

    # Pattern 2: Filename as header followed by code block
    pattern2 = r'###?\s+([^\n]+\.(ts|tsx|js|jsx|json|css|html|md|py|go|sh|yaml|yml|toml|txt|env|gitignore))\s*\n```(?:\w+)?\s*\n(.*?)```'

    # Pattern 3: Filename with backticks followed by code block
    pattern3 = r'`([^\`]+\.(ts|tsx|js|jsx|json|css|html|md|py|go|sh|yaml|yml|toml|txt|env|gitignore))`\s*```(?:\w+)?\s*\n(.*?)```'

    for pattern in [pattern1, pattern2, pattern3]:
        matches = re.findall(pattern, markdown_content, re.DOTALL | re.MULTILINE)
        for match in matches:
            file_path = match[0].strip()
            content = match[2].strip() if len(match) > 2 else match[1].strip()

            # Skip if it's a command block
            if any(cmd in content[:100] for cmd in ['npm install', 'npm create', 'cd ', '#!/bin/bash']):
                lines = content.split('\n')
                if len(lines) > 5 and not all(line.startswith(('#', 'npm', 'cd', 'mkdir')) for line in lines[:5]):
                    files_dict[file_path] = content
            else:
                files_dict[file_path] = content

    return files_dict


def create_project_structure(files_dict: Dict[str, str], base_dir: str = '.', verbose: bool = True) -> Tuple[int, int]:
    """Create all directories and files from the files dictionary."""
    base_path = Path(base_dir)
    base_path.mkdir(parents=True, exist_ok=True)

    dirs_created = set()
    files_created = []

    for file_path, content in sorted(files_dict.items()):
        full_path = base_path / file_path

        parent_dir = full_path.parent
        if parent_dir != base_path and str(parent_dir) not in dirs_created:
            parent_dir.mkdir(parents=True, exist_ok=True)
            dirs_created.add(str(parent_dir))
            if verbose:
                print(f'📁 Created directory: {parent_dir.relative_to(base_path)}')

        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            files_created.append(file_path)
            if verbose:
                print(f'📄 Created file: {file_path}')
        except Exception as e:
            print(f'❌ Error creating {file_path}: {e}')

    return len(dirs_created), len(files_created)


def analyze_markdown(markdown_files: List[str]) -> Dict[str, str]:
    """Read and combine multiple markdown files, then extract all file contents."""
    combined_content = ""

    for md_file in markdown_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                combined_content += "\n\n" + content
                print(f"✓ Read {md_file} ({len(content)} characters)")
        except Exception as e:
            print(f"❌ Error reading {md_file}: {e}")

    files_dict = extract_files_from_markdown(combined_content)
    return files_dict


def main():
    """Main function to run the utility."""
    examples = """
Examples:
  python md2project.py docs.md
  python md2project.py part1.md part2.md part3.md
  python md2project.py docs.md -o my-project
  python md2project.py docs.md --dry-run
"""

    parser = argparse.ArgumentParser(
        description='Extract files and folders from markdown documentation.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=examples
    )

    parser.add_argument('markdown_files', nargs='+', help='Markdown file(s) to process')
    parser.add_argument('-o', '--output', default='.', help='Output directory (default: current directory)')
    parser.add_argument('--dry-run', action='store_true', help='Analyze only, do not create files')
    parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode (minimal output)')

    args = parser.parse_args()

    verbose = not args.quiet

    if verbose:
        print("=" * 70)
        print("📦 Markdown to Project Structure Utility")
        print("=" * 70)
        print()

    files_dict = analyze_markdown(args.markdown_files)

    if not files_dict:
        print("❌ No files found in markdown. Check the format.")
        return 1

    print()
    print(f"📊 Analysis complete: Found {len(files_dict)} files")
    print()

    if verbose:
        print("📋 Files to be created:")
        for file_path in sorted(files_dict.keys()):
            print(f"   {file_path}")
        print()

    if args.dry_run:
        print("🔍 Dry run mode - no files created")
        return 0

    print(f"🚀 Creating project in: {args.output}")
    print()

    dirs_count, files_count = create_project_structure(
        files_dict, 
        base_dir=args.output, 
        verbose=verbose
    )

    print()
    print("=" * 70)
    print(f"✅ Project created successfully!")
    print(f"   Directories: {dirs_count}")
    print(f"   Files: {files_count}")
    print(f"   Location: {os.path.abspath(args.output)}")
    print("=" * 70)

    return 0


if __name__ == '__main__':
    sys.exit(main())
