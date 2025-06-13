"""
Python file combiner package
"""

# 定义包版本
__version__ = "0.1.0"

# 导入核心函数，方便外部直接访问
from .file_handler import find_python_files, read_file
from .ast_parser import analyze_file, build_dependency_graph
from .merger import merge_files, topological_sort_files

__all__ = [
    "find_python_files",
    "read_file",
    "analyze_file",
    "build_dependency_graph",
    "merge_files",
    "topological_sort_files",
    '__version__',
]
