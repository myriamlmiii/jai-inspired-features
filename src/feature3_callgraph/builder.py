
"""
Call Graph Builder
Uses: Topological Sort (O(V+E)), Tarjan's Algorithm for cycles
"""

from typing import Dict, List, Set
from collections import defaultdict, deque


class CallGraphBuilder:
    """Builds function call graph"""
    
    def __init__(self):
        self.graph = defaultdict(list)
        self.functions = set()
    
    def add_call(self, caller: str, callee: str) -> None:
        """Add function call edge"""
        self.graph[caller].append(callee)
        self.functions.add(caller)
        self.functions.add(callee)
    
    def topological_sort(self) -> List[str]:
        """Topological sort - O(V+E)"""
        in_degree = defaultdict(int)
        
        for node in self.functions:
            in_degree[node] = 0
        
        for node in self.graph:
            for neighbor in self.graph[node]:
                in_degree[neighbor] += 1
        
        queue = deque([node for node in self.functions if in_degree[node] == 0])
        result = []
        
        while queue:
            node = queue.popleft()
            result.append(node)
            
            for neighbor in self.graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return result
    
    def detect_cycles(self) -> List[List[str]]:
        """Tarjan's algorithm for cycle detection - O(V+E)"""
        index_counter = [0]
        stack = []
        lowlinks = {}
        index = {}
        on_stack = defaultdict(bool)
        sccs = []
        
        def strongconnect(node):
            index[node] = index_counter[0]
            lowlinks[node] = index_counter[0]
            index_counter[0] += 1
            stack.append(node)
            on_stack[node] = True
            
            for successor in self.graph[node]:
                if successor not in index:
                    strongconnect(successor)
                    lowlinks[node] = min(lowlinks[node], lowlinks[successor])
                elif on_stack[successor]:
                    lowlinks[node] = min(lowlinks[node], index[successor])
            
            if lowlinks[node] == index[node]:
                component = []
                while True:
                    successor = stack.pop()
                    on_stack[successor] = False
                    component.append(successor)
                    if successor == node:
                        break
                if len(component) > 1:
                    sccs.append(component)
        
        for node in self.functions:
            if node not in index:
                strongconnect(node)
        
        return sccs
