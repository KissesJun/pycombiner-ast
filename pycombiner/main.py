"""
Main entry point for the Python file combiner
"""

import sys
import os
from pathlib import Path
from combiner.file_handler import find_python_files, read_file
from combiner.ast_parser import analyze_file, build_dependency_graph
from combiner.merger import merge_files

def main_procedure(source_dir: Path, entry_file: Path, output_file: Path):
    """Main procedure for merging Python files
    
    Args:
        source_dir: Source directory containing Python files
        entry_file: Entry point file (e.g., main.py)
        output_file: Output file path for merged result
    """
    print(f"\n[DEBUG] Source directory: {source_dir}")
    print(f"[DEBUG] Entry file: {entry_file}")
    
    # Find Python files
    python_files = find_python_files(source_dir)
    if not python_files:
        print(f"Error: No Python files found in '{source_dir}'")
        sys.exit(1)
    
    print(f"\n[DEBUG] Found {len(python_files)} Python files:")
    for file in python_files:
        print(f"  - {file}")
    
    # Analyze imports
    print("\n[DEBUG] Analyzing imports:")
    print("----------------------------------------")
    imports_by_file = {}
    for file_path in python_files:
        abs_path = source_dir / file_path if not file_path.is_absolute() else file_path
        content = read_file(abs_path)
        if not content:
            continue
        imports, _ = analyze_file(content, str(abs_path))
        imports_by_file[str(abs_path)] = imports
        print(f"\n[DEBUG] File: {file_path}")
        for imp in imports:
            print(f"  - {imp}")

    # Build dependency graph
    print("\n[DEBUG] Building dependency graph:")
    print("----------------------------------------")
    dependency_graph = build_dependency_graph(imports_by_file, str(source_dir))
    print("\n[DEBUG] Dependency graph:")
    for module, deps in dependency_graph.items():
        print(f"  {module} -> {deps}")

    # Merge files
    print("\n[DEBUG] Starting file merge:")
    print("----------------------------------------")
    print("python_files:", python_files)
    print("entry_file:", entry_file)
    merge_files(python_files, dependency_graph, source_dir, output_file, entry_file)
    print(f"\n[DEBUG] Merge complete. Output written to {output_file}")


def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print("Usage: python main.py <source_dir_or_file> <output_file>")
        sys.exit(1)
        
    source_path = Path(sys.argv[1]).resolve()
    output_file = Path(sys.argv[2]).resolve()
    
    # Check if source path exists
    if not source_path.exists():
        print(f"Error: '{source_path}' does not exist")
        sys.exit(1)
    
    # If source path is a file, use its directory as source_dir
    if source_path.is_file():
        source_dir = source_path.parent
        entry_file = source_path
    else:
        source_dir = source_path
        entry_file = source_dir / 'main.py'
        if not entry_file.exists():
            print(f"Error: No main.py found in '{source_dir}'")
            sys.exit(1)
            
    main_procedure(source_dir, entry_file, output_file)

if __name__ == "__main__":
    # main()
    source_dir = Path('pycombiner/tests/examples/deep_demo')
    entry_file = source_dir / 'main.py'
    output_file = Path('demo-result.py')
    main_procedure(source_dir, entry_file, output_file)