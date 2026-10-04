# Graph Coloring Using Backtracking

**DAA Macro Project | Group G10 | Unit IV - Backtracking | Project 12**

## 1. Description

- **Graph coloring:** giving a color to every vertex of a graph so that connected vertices never share a color.
- **Vertex:** a point (node) of the graph. Here the vertices are A, B, C, D.
- **Edge:** a line joining two vertices. It means those two vertices are *adjacent*.
- **Color assignment:** choosing one color (Red, Green or Blue) for a vertex.
- **Why adjacent vertices cannot match:** that is the rule of the problem. Think of exam timetabling: two subjects that share a student (an edge) cannot use the same time slot (a color).
- **How backtracking helps:** we color vertices one by one. If a vertex ends up with no usable color, an earlier choice must have been wrong, so we go back (backtrack), undo that choice, try another color and continue.

## 2. Problem Statement

"Illustrate backtracking steps for coloring a 4-vertex graph using 3 colors."

Expected outcome: "Flowchart showing color assignments and backtracks."

## 3. Graph Used

Vertices: **A, B, C, D**

Edges: **A-B, A-C, B-C, B-D, C-D** (these are the pairs of adjacent vertices; A and D are *not* connected).

```
      A
     / \
    B---C
     \ /
      D
```

Adjacency matrix used in the code (1 = edge):

| | A | B | C | D |
|---|---|---|---|---|
| **A** | 0 | 1 | 1 | 0 |
| **B** | 1 | 0 | 1 | 1 |
| **C** | 1 | 1 | 0 | 1 |
| **D** | 0 | 1 | 1 | 0 |

## 4. Colors Used

- 1 = Red
- 2 = Green
- 3 = Blue

Colors are always tried in the order Red, Green, Blue, and vertices in the order A, B, C, D.

**Extra rule (important):** *Blue is not allowed on vertex C.* For this graph, with colors tried in the order Red, Green, Blue, plain backtracking never gets stuck: A = Red, B = Green, C = Blue, D = Red is found directly with **no** backtrack. (This is true for every 3-colorable 4-vertex graph, since two non-adjacent vertices always get the same first-fit color.) To demonstrate real backtracking, we add one restriction, like a real constraint where a resource is unavailable for one item. It is the array `ALLOWED` in the code. Setting `ALLOWED[2][3]` to `true` removes the rule and gives the plain run with zero backtracks.

## 5. Backtracking Approach

1. Select an uncolored vertex (A first, then B, C, D).
2. Try a color (Red first).
3. Check whether the color is safe: it must be allowed on that vertex, and no neighbor may already have it.
4. If safe, assign it.
5. Move to the next vertex.
6. If no color works for a vertex, backtrack.
7. Go back to the previous vertex, remove its color and try its next color.
8. Continue until all 4 vertices are colored (solution found).

## 6. Algorithm / Pseudocode

```
START

solve(vertex):
    If all vertices are colored:
        return true

    For each color in (Red, Green, Blue):
        If color is safe for vertex:
            Assign color to vertex

            If solve(next vertex) is true:
                return true

            Remove color from vertex        // backtrack

    return false

END
```

In simple words: `solve(vertex)` tries each color on the current vertex. A safe color is assigned and the next vertex is attempted. If the next vertex (or later ones) fail, the color is removed and the next color is tried. If all colors fail, `false` is returned, which makes the *previous* vertex change its color. That is the backtrack.

## 7. Visualization

`Visualization.png` has two parts:

- **Left: the algorithm flowchart** - START, initialize, select vertex, try a color, safety check (decision), assign color, "all 4 colored?" check, "any color left?" check and the BACKTRACK box that loops back to change the previous vertex's color.
- **Right: the actual run of the Python program**, step by step:
  1. A: Red is safe -> A = Red
  2. B: Red fails (A has Red), Green is safe -> B = Green
  3. C: Red fails (A), Green fails (B), Blue is not allowed -> **no valid color**
  4. **BACKTRACK #1** to B: remove Green, Blue is safe -> B = Blue
  5. C again: Red fails (A), Green is safe -> C = Green
  6. D: Red is safe -> D = Red
- **Bottom:** the final colored graph and a check that every edge joins two different colors.

Color selection, safety checking, assignment, failure, backtracking, trying another color and the final solution are all shown. Failed choices are in red, successful ones in green.

## 8. Result

Output of `Project12_GraphColoring.py`:

| Vertex | Color |
|---|---|
| A | Red |
| B | Blue |
| C | Green |
| D | Red |

Found after **1 backtrack**. Edge check: A-B Red/Blue, A-C Red/Green, B-C Blue/Green, B-D Blue/Red, C-D Green/Red. No edge has equal colors, so the coloring is valid.

Run it with: `python Project12_GraphColoring.py`

## 9. Complexity Analysis

- **Time complexity:** worst case **O(M^V)**, because each of the V vertices can try M colors. Here V = 4 and M = 3, so at most 3^4 = 81 complete assignments (each safety check also looks at up to V neighbors, which adds a small factor). Backtracking usually does much less work because wrong choices are cut early.
- **Space complexity:** **O(V)** extra space: the `color` array of size V and the recursion depth of at most V. (The adjacency matrix itself needs O(V^2).)

## 10. Learning Outcome

- Understood graph coloring.
- Understood the backtracking technique.
- Learned how invalid choices (a vertex with no usable color) cause backtracking.
- Learned how flowcharts can visualize recursive algorithms.

## 11. Files

- `Project12_GraphColoring.py` -> Python implementation
- `Prompt.txt` -> AI visualization prompt
- `Visualization.png` -> Graph-coloring backtracking flowchart
- `README.md` -> Project documentation

## 12. Conclusion

Backtracking colors the vertices one at a time and tries the colors in order. When a vertex has no valid color, the algorithm goes back to the previous vertex, changes its color and continues. In this project, vertex C had no valid color after A = Red and B = Green, so the algorithm backtracked once to B, changed it to Blue and finished with the valid coloring A = Red, B = Blue, C = Green, D = Red.
