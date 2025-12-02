
"""
Algorithm Benchmarks
Generates CSV data for analysis
"""

import sys
import time
import csv
import tracemalloc
from pathlib import Path

sys.path.insert(0, 'src')

from feature1_memory.tracker import HashTableAllocator, GraphTraverser, UnionFind


def benchmark_hash_table():
    """Benchmark hash table O(1)"""
    print("Running Hash Table benchmarks...")
    results = []
    
    for size in [100, 1000, 10000, 100000]:
        allocator = HashTableAllocator()
        
        # Create objects
        objects = [f"obj_{i}" for i in range(size)]
        for obj in objects:
            allocator.track(obj, ["test"])
        
        # Measure lookup
        times = []
        for _ in range(1000):
            start = time.perf_counter()
            _ = allocator.allocations.get(id(objects[size//2]))
            times.append((time.perf_counter() - start) * 1000000)
        
        results.append({
            'size': size,
            'avg_time_us': round(sum(times)/len(times), 4),
            'complexity': 'O(1)'
        })
        print(f"  Size {size}: {results[-1]['avg_time_us']:.4f} µs")
    
    # Save
    Path("outputs/metrics").mkdir(parents=True, exist_ok=True)
    with open('outputs/metrics/hash_table.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['size', 'avg_time_us', 'complexity'])
        writer.writeheader()
        writer.writerows(results)
    
    print("  Saved: outputs/metrics/hash_table.csv\n")
    return results


def benchmark_dfs_bfs():
    """Benchmark DFS vs BFS"""
    print("Running DFS vs BFS benchmarks...")
    results = []
    
    traverser = GraphTraverser()
    
    # Create deep graph
    class Node:
        def __init__(self, val, next=None):
            self.val = val
            self.next = next
    
    for depth in [10, 50, 100]:
        # Build linked list
        head = Node(0)
        current = head
        for i in range(1, depth):
            current.next = Node(i)
            current = current.next
        
        # Test DFS
        tracemalloc.start()
        start = time.perf_counter()
        dfs_result = traverser.dfs(head, depth+10)
        dfs_time = (time.perf_counter() - start) * 1000
        dfs_mem = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        
        # Test BFS
        tracemalloc.start()
        start = time.perf_counter()
        bfs_result = traverser.bfs(head, depth+10)
        bfs_time = (time.perf_counter() - start) * 1000
        bfs_mem = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        
        results.append({
            'depth': depth,
            'dfs_time_ms': round(dfs_time, 3),
            'dfs_memory_kb': round(dfs_mem/1024, 2),
            'bfs_time_ms': round(bfs_time, 3),
            'bfs_memory_kb': round(bfs_mem/1024, 2),
            'winner': 'DFS' if dfs_mem < bfs_mem else 'BFS'
        })
        print(f"  Depth {depth}: DFS {dfs_time:.2f}ms vs BFS {bfs_time:.2f}ms")
    
    # Save
    with open('outputs/metrics/dfs_vs_bfs.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    print("  Saved: outputs/metrics/dfs_vs_bfs.csv\n")
    return results


def benchmark_union_find():
    """Benchmark Union-Find"""
    print("Running Union-Find benchmarks...")
    results = []
    
    for n in [100, 1000, 10000]:
        # Union-Find
        uf = UnionFind()
        start = time.perf_counter()
        for i in range(n):
            uf.make_set(i)
        for i in range(0, n-1, 2):
            uf.union(i, i+1)
        for i in range(n):
            uf.find(i)
        uf_time = (time.perf_counter() - start) * 1000
        
        # Naive
        start = time.perf_counter()
        groups = {}
        for i in range(0, n-1, 2):
            key = min(i, i+1)
            if key not in groups:
                groups[key] = []
            groups[key].extend([i, i+1])
        for i in range(n):
            for group in groups.values():
                if i in group:
                    break
        naive_time = (time.perf_counter() - start) * 1000
        
        speedup = naive_time / uf_time if uf_time > 0 else 0
        
        results.append({
            'size': n,
            'uf_time_ms': round(uf_time, 3),
            'naive_time_ms': round(naive_time, 3),
            'speedup': round(speedup, 1)
        })
        print(f"  Size {n}: {speedup:.1f}x faster")
    
    # Save
    with open('outputs/metrics/union_find.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    print("  Saved: outputs/metrics/union_find.csv\n")
    return results


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  ALGORITHM BENCHMARKS")
    print("="*60 + "\n")
    
    benchmark_hash_table()
    benchmark_dfs_bfs()
    benchmark_union_find()
    
    print("="*60)
    print("All benchmarks complete!")
    print("Check outputs/metrics/ for CSV files")
    print("="*60 + "\n")
