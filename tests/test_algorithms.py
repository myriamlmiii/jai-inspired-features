"""
Test suite for all algorithms
"""

import sys
sys.path.insert(0, 'src')

from feature1_memory.tracker import HashTableAllocator, GraphTraverser, UnionFind


def test_hash_table():
    """Test hash table O(1) operations"""
    allocator = HashTableAllocator()
    
    # Track objects
    obj1 = "test1"
    obj2 = "test2"
    allocator.track(obj1, ["stack1"])
    allocator.track(obj2, ["stack2"])
    
    stats = allocator.get_stats()
    assert stats['count'] == 2
    assert stats['total_allocated'] == 2
    print("  Hash Table: PASS")


def test_dfs_bfs():
    """Test graph traversal"""
    traverser = GraphTraverser()
    
    # Create simple graph
    class Node:
        def __init__(self, val, next=None):
            self.val = val
            self.next = next
    
    head = Node(1)
    head.next = Node(2)
    head.next.next = Node(3)
    
    dfs_result = traverser.dfs(head)
    bfs_result = traverser.bfs(head)
    
    assert len(dfs_result) >= 3
    assert len(bfs_result) >= 3
    print("  DFS/BFS: PASS")


def test_union_find():
    """Test union-find operations"""
    uf = UnionFind()
    
    # Make sets
    for i in range(5):
        uf.make_set(i)
    
    # Union
    uf.union(0, 1)
    uf.union(2, 3)
    
    # Check
    assert uf.find(0) == uf.find(1)
    assert uf.find(2) == uf.find(3)
    assert uf.find(0) != uf.find(2)
    print("  Union-Find: PASS")


if __name__ == "__main__":
    print("\nRunning tests...\n")
    test_hash_table()
    test_dfs_bfs()
    test_union_find()
    print("\nAll tests passed!\n")