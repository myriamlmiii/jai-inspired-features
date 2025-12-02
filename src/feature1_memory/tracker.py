
"""
Memory Allocation Tracker
Uses: Hash Table (O(1)), DFS (O(V+E)), Union-Find (O(α(n)))
"""

import sys
import time
from typing import Any, Dict, List, Set


class HashTableAllocator:
    """Hash table for O(1) allocation tracking"""
    
    def __init__(self):
        self.allocations = {}
        self.total_allocated = 0
        
    def track(self, obj: Any, call_stack: List[str]) -> None:
        obj_id = id(obj)
        size = sys.getsizeof(obj)
        
        self.allocations[obj_id] = {
            'object': obj,
            'size': size,
            'call_stack': call_stack,
            'timestamp': time.time()
        }
        self.total_allocated += 1
    
    def get_stats(self) -> Dict:
        total_size = sum(a['size'] for a in self.allocations.values())
        return {
            'count': len(self.allocations),
            'total_bytes': total_size,
            'total_allocated': self.total_allocated
        }


class GraphTraverser:
    """DFS/BFS for object graph traversal"""
    
    def dfs(self, obj: Any, max_depth: int = 10) -> Set:
        """Depth-First Search - O(V+E)"""
        visited = set()
        
        def _dfs_helper(current, depth):
            if depth > max_depth or id(current) in visited:
                return
            
            visited.add(id(current))
            
            # Check references
            if hasattr(current, '__dict__'):
                for attr_value in current.__dict__.values():
                    _dfs_helper(attr_value, depth + 1)
            elif isinstance(current, (list, tuple)):
                for item in current:
                    _dfs_helper(item, depth + 1)
            elif isinstance(current, dict):
                for value in current.values():
                    _dfs_helper(value, depth + 1)
        
        _dfs_helper(obj, 0)
        return visited
    
    def bfs(self, obj: Any, max_depth: int = 10) -> Set:
        """Breadth-First Search - O(V+E)"""
        visited = set()
        queue = [(obj, 0)]
        visited.add(id(obj))
        
        while queue:
            current, depth = queue.pop(0)
            
            if depth >= max_depth:
                continue
            
            # Check references
            if hasattr(current, '__dict__'):
                for attr_value in current.__dict__.values():
                    if id(attr_value) not in visited:
                        visited.add(id(attr_value))
                        queue.append((attr_value, depth + 1))
            elif isinstance(current, (list, tuple)):
                for item in current:
                    if id(item) not in visited:
                        visited.add(id(item))
                        queue.append((item, depth + 1))
            elif isinstance(current, dict):
                for value in current.values():
                    if id(value) not in visited:
                        visited.add(id(value))
                        queue.append((value, depth + 1))
        
        return visited


class UnionFind:
    """Union-Find with path compression - O(α(n))"""
    
    def __init__(self):
        self.parent = {}
        self.rank = {}
    
    def make_set(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
    
    def find(self, x):
        """Find with path compression"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """Union by rank"""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return
        
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1


class MemoryTracker:
    """Main memory tracker combining all algorithms"""
    
    def __init__(self):
        self.allocator = HashTableAllocator()
        self.traverser = GraphTraverser()
        self.union_find = UnionFind()
        self.frame_data = []
        self.current_frame = 0
    
    def track(self, obj: Any) -> None:
        import traceback
        call_stack = [str(line) for line in traceback.extract_stack()[-3:-1]]
        self.allocator.track(obj, call_stack)
        self.union_find.make_set(id(obj))
    
    def next_frame(self) -> None:
        self.current_frame += 1
        stats = self.allocator.get_stats()
        self.frame_data.append({
            'frame': self.current_frame,
            'allocations': stats['count'],
            'bytes': stats['total_bytes']
        })
    
    def get_metrics(self) -> Dict:
        return {
            'frames': self.frame_data,
            'current_stats': self.allocator.get_stats()
        }
