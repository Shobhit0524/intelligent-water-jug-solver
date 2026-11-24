from collections import deque
import heapq
from itertools import count
from math import gcd
from time import perf_counter


def is_goal(state, target):
    return state[0] == target or state[1] == target


def successors(state, cap_a, cap_b):
    a, b = state
    moves = []

    # Fill either jug
    moves.append(((cap_a, b), "Fill Jug A"))
    moves.append(((a, cap_b), "Fill Jug B"))

    # Empty either jug
    moves.append(((0, b), "Empty Jug A"))
    moves.append(((a, 0), "Empty Jug B"))

    # Pour A into B
    transfer = min(a, cap_b - b)
    moves.append(((a - transfer, b + transfer), "Pour Jug A -> Jug B"))

    # Pour B into A
    transfer = min(b, cap_a - a)
    moves.append(((a + transfer, b - transfer), "Pour Jug B -> Jug A"))

    # Remove no-op moves and duplicate states while preserving order.
    result, seen = [], set()
    for next_state, action in moves:
        if next_state != state and next_state not in seen:
            result.append((next_state, action))
            seen.add(next_state)
    return result


def reconstruct(parent, goal):
    states = [goal]
    actions = []
    current = goal
    while parent[current][0] is not None:
        previous, action = parent[current]
        actions.append(action)
        states.append(previous)
        current = previous
    states.reverse()
    actions.reverse()
    return states, actions


def solve(cap_a, cap_b, target, algorithm="BFS"):
    if not all(isinstance(x, int) for x in (cap_a, cap_b, target)):
        raise ValueError("Capacities and target must be whole numbers.")
    if cap_a <= 0 or cap_b <= 0:
        raise ValueError("Jug capacities must be greater than zero.")
    if target < 0 or target > max(cap_a, cap_b):
        raise ValueError("Target must be between 0 and the larger jug capacity.")
    if target == 0:
        return {"found": True, "states": [(0, 0)], "actions": [],
                "expanded": 0, "elapsed_ms": 0.0, "algorithm": algorithm}
    if target % gcd(cap_a, cap_b) != 0:
        return {"found": False, "states": [], "actions": [],
                "expanded": 0, "elapsed_ms": 0.0, "algorithm": algorithm,
                "message": "No solution: target must be divisible by gcd(capacity A, capacity B)."}

    start = (0, 0)
    parent = {start: (None, None)}
    expanded = 0
    begin = perf_counter()
    algorithm = algorithm.upper()

    if algorithm == "BFS":
        frontier = deque([start])
        while frontier:
            state = frontier.popleft()
            if is_goal(state, target):
                states, actions = reconstruct(parent, state)
                return _result(True, states, actions, expanded, begin, algorithm)
            expanded += 1
            for nxt, action in successors(state, cap_a, cap_b):
                if nxt not in parent:
                    parent[nxt] = (state, action)
                    frontier.append(nxt)

    elif algorithm == "DFS":
        frontier = [start]
        while frontier:
            state = frontier.pop()
            if is_goal(state, target):
                states, actions = reconstruct(parent, state)
                return _result(True, states, actions, expanded, begin, algorithm)
            expanded += 1
            for nxt, action in reversed(successors(state, cap_a, cap_b)):
                if nxt not in parent:
                    parent[nxt] = (state, action)
                    frontier.append(nxt)

    elif algorithm in ("UCS", "GREEDY", "ASTAR"):
        serial = count()
        # Priority entries: (priority, tie-breaker, state, path_cost)
        heap = [(0, next(serial), start, 0)]
        best_cost = {start: 0}
        while heap:
            priority, _, state, cost = heapq.heappop(heap)
            if cost != best_cost.get(state):
                continue
            if is_goal(state, target):
                states, actions = reconstruct(parent, state)
                return _result(True, states, actions, expanded, begin, algorithm)
            expanded += 1
            for nxt, action in successors(state, cap_a, cap_b):
                new_cost = cost + 1
                if new_cost < best_cost.get(nxt, float("inf")):
                    best_cost[nxt] = new_cost
                    parent[nxt] = (state, action)
                    if algorithm == "UCS":
                        score = new_cost
                    elif algorithm == "GREEDY":
                        score = min(abs(nxt[0] - target), abs(nxt[1] - target))
                    else:  # A*: admissible, though intentionally simple, h=1 for non-goal
                        score = new_cost + (0 if is_goal(nxt, target) else 1)
                    heapq.heappush(heap, (score, next(serial), nxt, new_cost))
    else:
        raise ValueError("Choose BFS, DFS, UCS, GREEDY, or ASTAR.")

    return _result(False, [], [], expanded, begin, algorithm,
                   "No solution found.")


def _result(found, states, actions, expanded, begin, algorithm, message=None):
    result = {
        "found": found,
        "states": states,
        "actions": actions,
        "expanded": expanded,
        "elapsed_ms": (perf_counter() - begin) * 1000,
        "algorithm": algorithm,
    }
    if message:
        result["message"] = message
    return result


