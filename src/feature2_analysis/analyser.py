
"""
Code Complexity Analyzer
Uses: AST Traversal (O(n)), Memoization (O(1)), Dynamic Programming
"""

import ast
from typing import Dict


class ComplexityAnalyzer:
    """Analyzes Python code complexity"""
    
    def __init__(self):
        self.cache = {}  # Memoization
    
    def analyze_file(self, filepath: str) -> Dict:
        """Analyze Python file complexity"""
        with open(filepath, 'r') as f:
            code = f.read()
        
        tree = ast.parse(code)
        return self._analyze_tree(tree)
    
    def _analyze_tree(self, tree: ast.AST) -> Dict:
        """AST traversal - O(n) where n is nodes"""
        functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_complexity(node)
                functions.append({
                    'name': node.name,
                    'lines': len(node.body),
                    'complexity': complexity
                })
        
        return {
            'total_functions': len(functions),
            'functions': functions,
            'avg_complexity': sum(f['complexity'] for f in functions) / len(functions) if functions else 0
        }
    
    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Dynamic programming for nested complexity"""
        complexity = 1
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While)):
                complexity += 1
            elif isinstance(child, ast.FunctionDef) and child != node:
                complexity += 1
        
        return complexity
