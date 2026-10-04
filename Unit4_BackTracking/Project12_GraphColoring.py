# Project 12 (Unit IV - Backtracking)
# Graph Coloring using Backtracking: 4 vertices (A, B, C, D) and 3 colors

V = 4                                   # number of vertices
M = 3                                   # number of colors
VERTEX = ["A", "B", "C", "D"]
COLOR = ["Uncolored", "Red", "Green", "Blue"]    # 1 = Red, 2 = Green, 3 = Blue

# Adjacency matrix: GRAPH[i][j] = 1 means vertices i and j are connected
# Edges: A-B, A-C, B-C, B-D, C-D
GRAPH = [
    # A  B  C  D
    [0, 1, 1, 0],   # A
    [1, 0, 1, 1],   # B
    [1, 1, 0, 1],   # C
    [0, 1, 1, 0],   # D
]

# ALLOWED[v][c] = True if color c may be used on vertex v.
# Extra rule used to make the backtracking visible: Blue is NOT allowed on vertex C.
# (Change ALLOWED[2][3] to True to run the plain problem; then no backtracking is needed.)
ALLOWED = [
    #  -     Red   Green  Blue
    [False, True, True, True],     # A
    [False, True, True, True],     # B
    [False, True, True, False],    # C  (Blue not allowed)
    [False, True, True, True],     # D
]

color = [0] * V                         # 0 = uncolored, 1..3 = assigned color
backtracks = 0


def check_color(v, c):
    """Return None if color c is safe for vertex v, otherwise the reason it is not safe."""
    if not ALLOWED[v][c]:
        return f"{COLOR[c]} is not allowed on {VERTEX[v]}"
    for u in range(V):
        if GRAPH[v][u] == 1 and color[u] == c:
            return f"neighbor {VERTEX[u]} already has {COLOR[c]}"
    return None


def solve(v):
    """Try to color vertices v, v+1, ..., V-1. Returns True if it succeeds."""
    global backtracks
    if v == V:
        return True                     # all vertices are colored

    print(f"Vertex {VERTEX[v]}:")
    for c in range(1, M + 1):
        problem = check_color(v, c)
        if problem is not None:
            print(f"  Try {COLOR[c]} -> not safe ({problem})")
            continue

        color[v] = c                    # safe: assign the color
        print(f"  Try {COLOR[c]} -> safe, assign {VERTEX[v]} = {COLOR[c]}")

        if solve(v + 1):
            return True                 # the rest was colored successfully

        # the next vertices failed, so undo this choice and try the next color
        backtracks += 1
        print(f"BACKTRACK #{backtracks}: back at vertex {VERTEX[v]}, "
              f"remove {COLOR[c]}, try another color")
        color[v] = 0

    print(f"  No valid color for vertex {VERTEX[v]}")
    return False


if __name__ == "__main__":
    print("Graph coloring using backtracking (4 vertices, 3 colors)")
    print("Edges: A-B, A-C, B-C, B-D, C-D")
    print("Colors: 1 = Red, 2 = Green, 3 = Blue")
    print("Extra rule: Blue is not allowed on vertex C")
    print()
    print("Start: all vertices uncolored\n")

    if solve(0):
        print(f"\nSolution found after {backtracks} backtrack(s):")
        for i in range(V):
            print(f"  Vertex {VERTEX[i]} -> {COLOR[color[i]]}")
        print("\nChecking every edge:")
        for i in range(V):
            for j in range(i + 1, V):
                if GRAPH[i][j] == 1:
                    status = "OK" if color[i] != color[j] else "CONFLICT"
                    print(f"  {VERTEX[i]}-{VERTEX[j]}: {COLOR[color[i]]} vs {COLOR[color[j]]}  {status}")
    else:
        print("No valid coloring exists.")
