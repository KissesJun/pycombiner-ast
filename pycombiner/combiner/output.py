"""
Output formatting module for PyCombiner
"""
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple
import time

class MergeReport:
    def __init__(self, entry_file: Path, source_dir: Path, output_file: Path):
        self.entry_file = entry_file
        self.source_dir = source_dir
        self.output_file = output_file
        self.start_time = time.time()
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
            'classes': 0
        }

    def add_file_info(self, file_path: Path, lines: int, imports: Set[str], unhandled_imports: Set[str]):
        """Add information about a processed file"""
        self.files_info.append({
            'path': file_path,
            'lines': lines,
            'imports': imports,
            'unhandled_imports': unhandled_imports
        })
        self.stats['total_lines'] += lines

    def set_dependency_graph(self, graph: Dict[str, Set[str]]):
        """Set the dependency graph"""
        self.dependency_graph = graph

    def set_merge_order(self, order: List[Path]):
        """Set the merge order of files"""
        self.merge_order = order

    def update_stats(self, stats: Dict[str, int]):
        """Update statistics"""
        self.stats.update(stats)

    def _get_file_order(self, file_path: Path) -> int:
        """Get the order number of a file in the merge order"""
        try:
            return self.merge_order.index(file_path) + 1
        except ValueError:
            return 0

    def _format_import_summary(self) -> List[str]:
        """Format the import handling summary section"""
        lines = []
        lines.append("📦 Import Handling Summary")
        lines.append("─" * 100)
        lines.append(f"{'':<40} {'Lines':<10} | {'Unhandled':<10} | {'Handled':<10}")
        lines.append("─" * 100)

        # Build directory tree for files
        tree = {}
        for info in self.files_info:
            path = info['path']
            parts = path.parts
            current = tree
            for i, part in enumerate(parts):
                if i == len(parts) - 1:  # File
                    current[part] = info
                else:  # Directory
                    if part not in current:
                        current[part] = {}
                    current = current[part]

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
                        result.append(
                            f"{prefix}{'└── ' if is_last_item else '├── '}{order_str}{name}{entry_mark:<15} "
                            f"→ {info['lines']:<6} {len(info['unhandled_imports']):<10} {len(info['imports']):<10}"
                        )
            return result

        lines.extend(format_tree(tree))
        lines.append("─" * 100)
        
        # Add totals
        total_lines = sum(info['lines'] for info in self.files_info)
        total_unhandled = sum(len(info['unhandled_imports']) for info in self.files_info)
        total_handled = sum(len(info['imports']) for info in self.files_info)
        lines.append(f"{'*[]indicates Importing Order':<40} Total {total_lines:<6} | {total_unhandled:<6} | {total_handled:<6}")
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
        for file, imports in self.imports_by_file.items():
            file_path = Path(file)
            parts = file_path.parts
            current = handled_imports
            for i, part in enumerate(parts):
                if i == len(parts) - 1:  # File
                    current[part] = imports
                else:  # Directory
                    if part not in current:
                        current[part] = {}
                    current = current[part]

        def format_handled_imports(tree: Dict, prefix: str = "") -> List[str]:
            result = []
            items = sorted(tree.items())
            for i, (name, value) in enumerate(items):
                is_last = i == len(items) - 1
                if isinstance(value, dict):  # Directory
                    result.append(f"{prefix}{'└── ' if is_last else '├── '}{name}/")
                    new_prefix = prefix + ("    " if is_last else "│   ")
                    result.extend(format_handled_imports(value, new_prefix))
                else:  # File
                    order = self._get_file_order(Path(name))
                    order_str = f"[{order}]" if order > 0 else ""
                    result.append(f"{prefix}{'└── ' if is_last else '├── '}{name}{order_str}:")
                    for imp in value:
                        result.append(f"{prefix}{'    ' if is_last else '│   '}    - {imp}")
            return result

        lines.extend(format_handled_imports(handled_imports))

        # Format unhandled imports
        lines.append("")
        lines.append("└── ⚠️ Unhandled Imports")
        unhandled_imports = {}
        for info in self.files_info:
            if info['unhandled_imports']:
                path = info['path']
                parts = path.parts
                current = unhandled_imports
                for i, part in enumerate(parts):
                    if i == len(parts) - 1:  # File
                        current[part] = info['unhandled_imports']
                    else:  # Directory
                        if part not in current:
                            current[part] = {}
                        current = current[part]

        def format_unhandled_imports(tree: Dict, prefix: str = "") -> List[str]:
            result = []
            items = sorted(tree.items())
            for i, (name, value) in enumerate(items):
                is_last = i == len(items) - 1
                if isinstance(value, dict):  # Directory
                    result.append(f"{prefix}{'└── ' if is_last else '├── '}{name}/")
                    new_prefix = prefix + ("    " if is_last else "│   ")
                    result.extend(format_unhandled_imports(value, new_prefix))
                else:  # File
                    result.append(f"{prefix}{'└── ' if is_last else '├── '}{name}:")
                    imports_str = ", ".join(sorted(value))
                    result.append(f"{prefix}{'    ' if is_last else '│   '}    → {imports_str}")
            return result

        lines.extend(format_unhandled_imports(unhandled_imports))
        lines.append("─" * 100)
        lines.append("")
        return lines

    def format_report(self) -> str:
        """Format the report as a string."""
        report = []
        report.append("══════════════════════════ 🔍 PyCombiner Merge Report ══════════════════════════")
        report.append("")
        report.append(f"Generated On     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Entry File       : {self.entry_file}")
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
        report.append(f" • Lines written to merged output…… {self.stats['functions'] + self.stats['classes']} → {self.output_file}")
        report.append(f" • Redundant imports removed………… {self.stats['redundant_imports']}")
        report.append(f" • Total time elapsed………………… {self.stats['total_time']:.2f} s")
        report.append("")
        
        report.append(f"✅ Merge complete! Output saved to: {self.output_file}")
        report.append(f"   You can now run:  python {self.output_file}")
        report.append("")
        return "\n".join(report)

def print_merge_report(report: MergeReport):
    """Print the merge report to console"""
    print(report.format_report()) 