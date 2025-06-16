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
        self.imports_by_file: Dict[str, Set[str]] = {}
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

    def format_report(self) -> str:
        """Format the merge report"""
        width = 80
        separator = "═" * width
        
        # Header
        report = [
            f"{separator} 🔍 PyCombiner Merge Report v1.2.0 {separator}",
            f"\nGenerated On     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Entry File       : {self.entry_file.relative_to(self.source_dir)}",
            f"Source Directory : {self.source_dir}",
            f"Output File      : {self.output_file.name}\n"
        ]

        # Files Discovered
        report.append(f"📦 Files Discovered ({len(self.files_info)})")
        report.append("─" * width)
        report.append(f" #  {'File':<45} {'Lines':<8} Internal Imports")
        report.append("─" * width)
        
        for i, info in enumerate(self.files_info, 1):
            file_path = info['path'].relative_to(self.source_dir)
            report.append(f" {i:<2} {str(file_path):<45} {info['lines']:<8} {len(info['imports'])}")
            if info['unhandled_imports']:
                report.append(f"    └─ Unhandled imports: {', '.join(info['unhandled_imports'])}")
        
        report.append("─" * width)
        report.append(f" Total Lines: {self.stats['total_lines']}   |   "
                     f"Functions/Methods: {self.stats['functions']}   |   "
                     f"Classes: {self.stats['classes']}\n")

        # Imports in Entry File
        report.append("📚 Imports in Entry File (main.py)")
        report.append("─" * width)
        for imp in self.imports_by_file.get(str(self.entry_file), []):
            report.append(imp)
        report.append("")

        # Dependency Tree
        report.append("📈 Dependency Tree")
        report.append("─" * width)
        self._format_dependency_tree(report, str(self.entry_file), 0)
        report.append("")

        # Merge Order
        report.append("🧩 Merge Order (Topological Sort)")
        report.append("─" * width)
        for i, file in enumerate(self.merge_order, 1):
            is_entry = file == self.entry_file
            report.append(f" {i:<2}. {file.relative_to(self.source_dir)}"
                        f"{' ← entry file is merged last' if is_entry else ''}")
        report.append("")

        # Summary
        elapsed_time = time.time() - self.start_time
        report.append("⚙️ Summary")
        report.append("─" * width)
        report.append(f" • Total import statements analyzed…… {self.stats['total_imports']}")
        report.append(f" • Dependency graph built……………… {len(self.dependency_graph)} nodes / "
                     f"{sum(len(deps) for deps in self.dependency_graph.values())} edges")
        report.append(f" • Duplicate local imports skipped…… {self.stats['duplicate_imports']}")
        report.append(f" • Lines written to merged output…… {self.stats['total_lines']} → {self.output_file.name}")
        report.append(f" • Redundant imports removed………… {self.stats['redundant_imports']}")
        report.append(f" • Total time elapsed………………… {elapsed_time:.2f} s\n")

        # Footer
        report.append(f"✅ Merge complete! Output saved to: {self.output_file.name}")
        report.append(f"   You can now run:  python {self.output_file.name}")

        return "\n".join(report)

    def _format_dependency_tree(self, report: List[str], node: str, depth: int):
        """Format the dependency tree recursively"""
        indent = "│  " * depth
        if depth == 0:
            report.append(f"{Path(node).name}")
        else:
            report.append(f"{indent}└─ {Path(node).name}")
        
        for dep in sorted(self.dependency_graph.get(node, [])):
            self._format_dependency_tree(report, dep, depth + 1)

def print_merge_report(report: MergeReport):
    """Print the merge report to console"""
    print(report.format_report()) 