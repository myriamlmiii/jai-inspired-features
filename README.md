# Jai-Inspired Python Implementation of debugging tools

In this project, we implemented debugging features inspired by Jonathan Blow's Jai programming language. Jai is a new systems programming language created by Jonathan Blow, an independent game developer known for creating games like Braid and The Witness. His work was really impressive and he made us develop interest on game development  . Jai emphasizes fast compile times, better debugging tools, and more control over memory management compared to traditional languages.

We adapted Jai's debugging philosophy to Python by implementing three key features using efficient algorithms. While Python has built-in debugging tools, they often lack the speed and real-time capabilities that Jai provides. Our implementation bridges this gap by using optimized data structures and algorithms to achieve similar functionality in Python.


## Team Members
- Meriem Lmoubariki
- Charvi 
- Arpita Arora

## Project Overview

We worked on 3 features : 

1. **Memory Allocation Tracker** - Real-time tracking with Hash Table (O(1)), DFS/BFS (O(V+E)), Union-Find (O(α(n)))
2. **Code Complexity Analyzer** - AST traversal with memoization and dynamic programming
3. **Call Graph Builder** - Topological sort and Tarjan's algorithm for cycle detection

## Methodology 

### Feature 1: Memory Allocation Tracker

**What it does:** Tracks every object allocation in real-time

**Algorithms used:**
- **Hash Table (O(1))** - Store allocation records by object ID for instant lookup
- **DFS (O(V+E))** - Traverse object references to find memory leaks (good for deep graphs)
- **BFS (O(V+E))** - Alternative traversal for wide graphs, finds shortest path
- **Union-Find (O(α(n)))** - Group related allocations by function/type

**Why these algorithms:**
- Hash Table: Need fast lookup to track thousands of allocations
- DFS/BFS: Walk object graph to find what's still reachable (leak detection)
- Union-Find: Fast grouping of allocations from same source

### Feature 2: Code Complexity Analyzer

**What it does:** Analyzes Python code to calculate cyclomatic complexity

**Algorithms used:**
- **AST Traversal (O(n))** - Walk through parsed code structure
- **Memoization (O(1))** - Cache complexity calculations
- **Dynamic Programming** - Calculate nested complexity efficiently

**Why these algorithms:**
- AST: Accurate parsing (better than regex)
- Memoization: Avoid recomputing same functions
- Dynamic Programming: Reuse subproblem solutions for nested functions

### Feature 3: Call Graph Builder

**What it does:** Maps which functions call which other functions

**Algorithms used:**
- **Topological Sort (O(V+E))** - Order functions by dependencies
- **Tarjan's Algorithm (O(V+E))** - Detect circular dependencies (cycles)

**Why these algorithms:**
- Topological Sort: Know execution order, find initialization sequence
- Tarjan's: Detect infinite recursion risks before runtime

## Generated Files

After running the project, you'll have:

### CSV Data (outputs/metrics/):
- `hash_table.csv` - Hash table O(1) performance data
- `dfs_vs_bfs.csv` - DFS vs BFS comparison
- `union_find.csv` - Union-Find speedup measurements
- `game_metrics.csv` - Game session data

### Analysis Reports (outputs/analysis/):
- `ALGORITHM_ANALYSIS.txt` - Complexity tables and empirical verification
- `FEATURE_ANALYSIS.txt` - Feature benefits with real experiment data

### Experiment Data (outputs/experiments/):
- `overhead_data.csv` - Overhead comparison vs Python tools
- `leak_detection_data.csv` - Leak detection speed comparison
- `grouping_data.csv` - Grouping performance data

### Visualizations (outputs/visualizations/):
- `algorithm_dashboard.html` - Algorithm performance dashboard
- `feature_comparison.html` - Feature benefits comparison
- `interactive_dashboard.html` - Combined interactive dashboard
- `memory_3d.html` - 3D memory allocation view
- `graph_traversal_3d.html` - 3D DFS vs BFS visualization
- `union_find_3d.html` - 3D object grouping visualization

## Commands Reference

### Run Everything (Recommended Order):
```bash
# Step 1: Run tests to verify implementation
python tests/test_algorithms.py

# Step 2: Generate benchmark data
python benchmarks.py

# Step 3: Generate algorithm analysis (uses benchmark data)
python analysis_algorithms.py

# Step 4: Generate feature analysis (runs NEW experiments)
python features_analysis.py

# Step 5: Create visualizations
python visualizations.py

# Step 6: Play the game (optional demo)
python game.py
```

### Individual Components:
```bash
# Just run benchmarks
python benchmarks.py

# Just play game
python game.py

# Just generate analysis from existing data
python analysis_algorithms.py
```

## Game Controls

When you run `python game.py`:

**Map Legend:**
- `P` = You (Player)
- `C` = Collectible cube (◆)
- `*` = Particle effects
- `.` = Empty space

**Controls:**
- Type `w` and press ENTER = Move up
- Type `s` and press ENTER = Move down
- Type `a` and press ENTER = Move left
- Type `d` and press ENTER = Move right
- Type `q` and press ENTER = Quit

**Goal:** Collect all cubes while memory tracker runs in real-time showing:
- Memory usage in KB
- Number of tracked objects
- Active particles

**Output:** Game session data saved to `outputs/metrics/game_metrics.csv`

## Visualizations Guide

Open these HTML files in your browser for interactive charts:

1. **algorithm_dashboard.html** - Main algorithm performance charts
   - Hash Table O(1) verification
   - DFS vs BFS memory comparison
   - Union-Find speedup visualization

2. **feature_comparison.html** - Feature benefits
   - Overhead comparison
   - Leak detection speed
   - Grouping performance

3. **3D Visualizations** (interactive - rotate with mouse, zoom with scroll):
   - `memory_3d.html` - Memory allocations in 3D space
   - `graph_traversal_3d.html` - DFS vs BFS traversal visualization
   - `union_find_3d.html` - Object grouping by color



## Analysis Framework Applied

### Problem
Traditional Python debuggers are too slow for real-time use. Python lacks:
- Real-time memory tracking (tracemalloc has 10x overhead)
- Automatic leak detection (manual inspection required)
- Fast complexity analysis (pylint is slow)
- Call graph visualization (not built-in)

### Solution
Implement fast debugging tools using efficient algorithms:
- O(1) hash table for instant allocation lookup
- O(V+E) graph traversal for reference tracking
- O(α(n)) union-find for grouping operations
- O(V+E) topological sort for dependency ordering

### Verification
All complexity claims verified empirically:
- Hash Table: Confirmed O(1) (time variance < 2µs across 100K elements)
- DFS/BFS: Confirmed O(V+E) (both scale linearly)
- Union-Find: Confirmed O(α(n)) (up to 111x faster than naive O(n²))

See `outputs/analysis/ALGORITHM_ANALYSIS.txt` for detailed verification.

## Key Results

From empirical measurements:

**Algorithm Performance:**
- Hash Table: O(1) lookup verified (0.16µs avg, constant across sizes)
- DFS vs BFS: Both O(V+E), memory usage varies by graph structure
- Union-Find: 133x faster than naive approach at 10K elements

**Feature Benefits:**
- Memory tracking overhead: 338.6% less overhead than Python's tracemalloc
- Leak detection: 2.3x faster than Python's gc.get_objects()
- Object grouping: 2.4x faster than Python dict approach

See `outputs/analysis/FEATURE_ANALYSIS.txt` for detailed measurements.

## Dependencies

**Required:**
- Python 3.7+
- Standard library only (csv, time, tracemalloc, gc, pathlib, etc.)

**Optional (for enhanced visualizations):**
```bash
pip install plotly
```

If plotly not installed, visualizations fall back to simple HTML.

## Testing

Run the test suite:
```bash
python tests/test_algorithms.py
```

Expected output:
```
Running tests...
  Hash Table: PASS
  DFS/BFS: PASS
  Union-Find: PASS
All tests passed!
```

## References

1. Blow, J. (2025). "Jai Programming Language Demo." LambdaConf 2025.  
   https://www.youtube.com/watch?v=TH9VCN6UkyQ

2. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009).  
   *Introduction to Algorithms* (3rd ed.). MIT Press.

3. Python Software Foundation. (2024). Python AST Documentation.  
   https://docs.python.org/3/library/ast.html

4. Tarjan, R. (1972). "Depth-First Search and Linear Graph Algorithms."  
   *SIAM Journal on Computing*, 1(2), 146-160.

5. Galil, Z., & Italiano, G. F. (1991). "Data Structures and Algorithms for Disjoint Set Union Problems."  
   *ACM Computing Surveys*, 23(3), 319-344.

6. MIT OpenCourseWare. (2011). "Hashing with Chaining." MIT 6.006 Introduction to Algorithms.  
   https://www.youtube.com/watch?v=0M_kIqhwbFo

7. Murphy, J. (mCoding). (2021). "Python Memory Management and Tips." YouTube.  
   https://www.youtube.com/watch?v=F6u5rhUQ6dU

All theoretical complexity claims and conclusions are justified by measured data in CSV files and analysis reports.

