# Intelligent Water-Jug Problem Solver

A Python project that solves the classic two-jug problem using BFS, DFS, UCS,
Greedy Best-First Search and A*. It includes a Streamlit web interface and a
Tkinter desktop interface.

## Requirements
- Python 3.10 or newer
- Install dependencies: `pip install -r requirements.txt`
- Tkinter is included with most standard Windows Python installations.

## Run the web application
```bash
streamlit run app.py
```

## Run the desktop application
```bash
python desktop_app.py
```

## Example
- Jug A capacity: 4 litres
- Jug B capacity: 3 litres
- Target: 2 litres

## Search representation
A state `(a, b)` stores the amount of water in Jug A and Jug B.
The initial state is `(0, 0)`. A goal is reached when either jug contains
the target quantity. Available actions are fill, empty, and pour.

All actions have unit cost. BFS and UCS return a minimum-operation solution.
DFS is not guaranteed to return the shortest solution. Greedy is guided by
distance to the target. A* uses an admissible but weak heuristic:
h(n) = 0 for a goal state and 1 otherwise.




