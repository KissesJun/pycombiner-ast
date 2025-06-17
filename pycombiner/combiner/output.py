"""
Output formatting module for PyCombiner
"""
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple
import time
import sys

# ANSI color codes
class Colors:
    YELLOW = '\033[93m'
    RESET = '\033[0m'

class MergeReport:
    def __init__(self, entry_file: Path, source_dir: Path, output_file: Path, debug: bool = False, show_details: bool = False):
        self.entry_file = entry_file
        self.source_dir = source_dir
        self.output_file = output_file
        self.start_time = time.time()
        self.debug = debug
        self.show_details = show_details
        self.files_info: List[Dict] = []
        self.imports_by_file: Dict[str, List[str]] = {}
        self.dependency_graph: Dict[str, Set[str]] = {}
        self.merge_order: List[Path] = []
        self.stats = {
            'total_imports': 0,
            'duplicate_imports': 0,
            'redundant_imports': 0,
            'total_lines': 0,
            'functions': 0,
            'classes': 0,
            'total_time': 0.0
        }

    def debug_print(self, message: str):
        """Print debug message if debug mode is enabled"""
        if self.debug:
            print(f"{Colors.YELLOW}[DEBUG]{Colors.RESET} {message}")

    def add_file_info(self, file_path: Path, lines: int, imports: Set[str], unhandled_imports: Set[str], import_info: Dict = None):
        """Add information about a processed file"""
        self.files_info.append({
            'path': file_path,
            'lines': lines,
            'imports': imports,
            'unhandled_imports': unhandled_imports,
            'import_statements': import_info.get('import_statements', []) if import_info else [],
            'unhandled_import_statements': import_info.get('unhandled_import_statements', []) if import_info else []
        })
        self.stats['total_lines'] += lines
        self.debug_print(f"Added file info: {file_path} ({lines} lines)")

    def set_dependency_graph(self, graph: Dict[str, Set[str]]):
        """Set the dependency graph"""
        self.dependency_graph = graph
        self.debug_print(f"Set dependency graph with {len(graph)} nodes")

    def set_merge_order(self, order: List[Path]):
        """Set the merge order of files"""
        self.merge_order = order
        self.debug_print(f"Set merge order: {[str(p) for p in order]}")

    def update_stats(self, stats: Dict[str, int]):
        """Update statistics"""
        self.stats.update(stats)
        self.debug_print("Updated statistics")

    def _get_file_order(self, file_path: Path) -> int:
        """Get the order number of a file in the merge order"""
        try:
            return self.merge_order.index(file_path) + 1
        except ValueError:
            return 0

    def _get_relative_path(self, path: Path) -> Path:
        """Get path relative to source directory"""
        try:
            return path.relative_to(self.source_dir)
        except ValueError:
            return path

    def _get_project_root(self) -> Path:
        """Get the project root directory (parent of source directory)"""
        return self.source_dir

    def _build_directory_tree(self) -> Dict:
        """Build a directory tree from files"""
        tree = {}
        project_root = self._get_project_root()
        tree[project_root.name] = {}  # Add project root directory
        
        for info in self.files_info:
            path = info['path']
            # Get the path relative to project root
            try:
                rel_path = path.relative_to(project_root)
            except ValueError:
                rel_path = path
            
            parts = rel_path.parts
            current = tree[project_root.name]  # Start from project root
            
            # Build the tree structure
            for i, part in enumerate(parts):
                if i == len(parts) - 1:  # File
                    current[part] = info
                else:  # Directory
                    if part not in current:
                        current[part] = {}
                    current = current[part]
        
        return tree

    def _format_import_summary(self) -> List[str]:
        """Format the import handling summary section"""
        lines = []
        lines.append("📦 Import Handling Summary")
        lines.append("─" * 100)
        lines.append(f"{'File':<50} {'Lines':<8} {'Unhandled':<10} {'Handled':<10}")
        lines.append("─" * 100)

        # Build directory tree for files
        tree = self._build_directory_tree()

        def format_tree(tree: Dict, prefix: str = "", is_last: bool = True) -> List[str]:
            result = []
            items = sorted(tree.items())
            for i, (name, value) in enumerate(items):
                is_last_item = i == len(items) - 1
                if isinstance(value, dict) and not any(key in value for key in ['path', 'lines', 'imports', 'unhandled_imports']):  # Directory
                    result.append(f"{prefix}{'└── ' if is_last_item else '├── '}{name}/")
                    new_prefix = prefix + ("    " if is_last_item else "│   ")
                    result.extend(format_tree(value, new_prefix, is_last_item))
                else:  # File
                    info = value
                    if isinstance(info, dict) and 'path' in info:
                        order = self._get_file_order(info['path'])
                        order_str = f"[{order}] " if order > 0 else ""
                        is_entry = info['path'] == self.entry_file
                        entry_mark = " 🚩 entry file" if is_entry else ""
                        
                        # Format the line with proper alignment
                        file_name = f"{prefix}{'└── ' if is_last_item else '├── '}{order_str}{name}{entry_mark}"
                        stats = f"{info['lines']:<8} {len(info['unhandled_imports']):<10} {len(info['imports']):<10}"
                        line = f"{file_name:<50} {stats}"
                        result.append(line)
            return result

        lines.extend(format_tree(tree))
        lines.append("─" * 100)
        
        # Add totals
        total_lines = sum(info['lines'] for info in self.files_info)
        total_unhandled = sum(len(info['unhandled_imports']) for info in self.files_info)
        total_handled = sum(len(info['imports']) for info in self.files_info)
        lines.append(f"{'*[]indicates Importing Order':<50} {total_lines:<8} {total_unhandled:<10} {total_handled:<10}")
        lines.append("")
        return lines

    def _format_import_details(self) -> List[str]:
        """Format the import handling details section"""
        lines = []
        lines.append("📦 Import Handling Details")
        lines.append("─" * 100)

        # Format handled imports
        lines.append("├── ✅ Handled Imports")
        handled_imports = {}
        project_root = self._get_project_root()
        handled_imports[project_root.name] = {}  # Add project root directory
        
        # 收集所有已处理的导入信息
        for info in self.files_info:
            if info['imports']:
                path = info['path']
                try:
                    rel_path = path.relative_to(project_root)
                except ValueError:
                    rel_path = path
                
                parts = rel_path.parts
                current = handled_imports[project_root.name]
                for i, part in enumerate(parts):
                    if i == len(parts) - 1:  # File
                        current[part] = {
                            'imports': info['imports'],
                            'order': self._get_file_order(path),
                            'import_statements': info.get('import_statements', [])  # 存储原始导入语句
                        }
                    else:  # Directory
                        if part not in current:
                            current[part] = {}
                        current = current[part]

        def format_handled_imports(tree: Dict, prefix: str = "") -> List[str]:
            result = []
            items = sorted(tree.items())
            for i, (name, value) in enumerate(items):
                is_last = i == len(items) - 1
                if isinstance(value, dict) and 'imports' not in value:  # Directory
                    result.append(f"{prefix}{'└── ' if is_last else '├── '}{name}/")
                    new_prefix = prefix + ("    " if is_last else "│   ")
                    result.extend(format_handled_imports(value, new_prefix))
                else:  # File
                    order = value.get('order', 0)
                    order_str = f"[{order}]" if order > 0 else ""
                    imports = value.get('imports', set())
                    imports_str = ", ".join(sorted(imports))
                    result.append(f"{prefix}{'└── ' if is_last else '├── '}{name}{order_str}: {imports_str}")
                    # 显示完整的导入语句
                    import_statements = value.get('import_statements', [])
                    for imp in sorted(import_statements):
                        # 计算缩进，使导入语句在中间对齐
                        indent = prefix + ("    " if is_last else "│   ")
                        result.append(f"{indent}    - {imp}")
            return result

        lines.extend(format_handled_imports(handled_imports))

        # Format unhandled imports
        lines.append("")
        lines.append("└── ⚠️ Unhandled Imports")
        unhandled_imports = {}
        unhandled_imports[project_root.name] = {}
        
        for info in self.files_info:
            if info['unhandled_imports']:
                path = info['path']
                try:
                    rel_path = path.relative_to(project_root)
                except ValueError:
                    rel_path = path
                
                parts = rel_path.parts
                current = unhandled_imports[project_root.name]
                for i, part in enumerate(parts):
                    if i == len(parts) - 1:  # File
                        current[part] = {
                            'imports': info['unhandled_imports'],
                            'import_statements': info.get('unhandled_import_statements', [])  # 存储原始导入语句
                        }
                    else:  # Directory
                        if part not in current:
                            current[part] = {}
                        current = current[part]

        def format_unhandled_imports(tree: Dict, prefix: str = "") -> List[str]:
            result = []
            items = sorted(tree.items())
            for i, (name, value) in enumerate(items):
                is_last = i == len(items) - 1
                if isinstance(value, dict) and 'imports' not in value:  # Directory
                    result.append(f"{prefix}{'└── ' if is_last else '├── '}{name}/")
                    new_prefix = prefix + ("    " if is_last else "│   ")
                    result.extend(format_unhandled_imports(value, new_prefix))
                else:  # File
                    imports = value.get('imports', set())
                    # 去掉 "import " 前缀
                    clean_imports = {imp.replace('import ', '') for imp in imports}
                    imports_str = ", ".join(sorted(clean_imports))
                    result.append(f"{prefix}{'└── ' if is_last else '├── '}{name}: {imports_str}")
                    # 显示完整的导入语句
                    import_statements = value.get('import_statements', [])
                    for imp in sorted(import_statements):
                        # 计算缩进，使导入语句在中间对齐
                        indent = prefix + ("    " if is_last else "│   ")
                        result.append(f"{indent}    - {imp}")
            return result

        lines.extend(format_unhandled_imports(unhandled_imports))
        lines.append("─" * 100)
        lines.append("")
        return lines

    def format_report(self) -> str:
        """Format the report as a string."""
        # Calculate total time
        self.stats['total_time'] = time.time() - self.start_time

        report = []
        report.append("══════════════════════════ 🔍 PyCombiner Merge Report ══════════════════════════")
        report.append("")
        report.append(f"Generated On     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Entry File       : {self._get_relative_path(self.entry_file)}")
        report.append(f"Source Directory : {self.source_dir}")
        report.append(f"Output File      : {self.output_file}")
        report.append("")

        # Add import summary
        report.extend(self._format_import_summary())

        # Add import details
        report.extend(self._format_import_details())

        # Add summary
        report.append("⚙️ Summary")
        report.append("─" * 100)
        report.append(f" • Total import statements analyzed…… {self.stats['total_imports']}")
        report.append(f" • Dependency graph built……………… {len(self.dependency_graph)} nodes / {sum(len(deps) for deps in self.dependency_graph.values())} edges")
        report.append(f" • Duplicate local imports skipped…… {self.stats['duplicate_imports']}")
        report.append(f" • Lines written to merged output…… {self.stats['functions'] + self.stats['classes']} ")
        report.append(f" • Redundant imports removed………… {self.stats['redundant_imports']}")
        report.append(f" • Total time elapsed………………… {self.stats['total_time']:.2f} s")
        report.append("")
        
        report.append(f"✅ Merge complete! Output saved:")
        report.append(f"   You can now run:  python {self.output_file}")
        report.append("")
        return "\n".join(report)

def print_merge_report(report: MergeReport):
    """Print the merge report to console"""
    print(report.format_report()) 