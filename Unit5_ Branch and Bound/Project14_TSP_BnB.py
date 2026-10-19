"""
Project 14 : TSP Branch-and-Bound Search Tree  (DAA Macro Project, Group G10)
Faculty prompt: "Draw a search tree showing bounding and pruning for TSP with 4 cities."

What this program does
----------------------
1. Solves the 4-city Traveling Salesperson Problem with Branch and Bound (DFS style).
2. Prints every important step (path cost, lower bound, pruning decisions).
3. Records every node of the search tree and draws it as Visualization.png
   (the drawing uses ONLY the numbers computed here - nothing is typed by hand).

Run:   python Project14_TSP_BnB.py
(The picture needs matplotlib:  pip install matplotlib. The algorithm itself uses only the standard library.)
"""

import math

# ----------------------------------------------------------------------------
# 1. Problem setup (same matrix is used in README, Prompt.txt and the picture)
# ----------------------------------------------------------------------------
CITIES = ["A", "B", "C", "D"]
COST = {
    "A": {"A": 0,  "B": 10, "C": 15, "D": 20},
    "B": {"A": 10, "B": 0,  "C": 35, "D": 25},
    "C": {"A": 15, "B": 35, "C": 0,  "D": 30},
    "D": {"A": 20, "B": 25, "C": 30, "D": 0},
}
START = "A"


# ----------------------------------------------------------------------------
# 2. Lower bound  (minimum outgoing-edge relaxation)
# ----------------------------------------------------------------------------
def lower_bound(path, path_cost):
    """
    LB = path cost so far
         + cheapest edge that can leave the LAST city of the path
         + for every unvisited city u, the cheapest edge that can leave u.

    Any completion of the path must leave the last city once and leave every
    unvisited city once, and those edges can only go to a city that is still
    unvisited or back to the start A.  So each term below is <= the edge the
    real completion uses, which means  LB <= cost of the best completion.
    The bound is therefore SAFE (never too big), so pruning with it is correct.
    """
    unvisited = [c for c in CITIES if c not in path]
    last = path[-1]

    if not unvisited:                       # complete route: only the return edge is left
        return path_cost + COST[last][START]

    # edge leaving the last city: it must go to some unvisited city
    bound = path_cost + min(COST[last][u] for u in unvisited)

    # edge leaving each unvisited city: to another unvisited city or back to A
    for u in unvisited:
        options = [COST[u][v] for v in unvisited if v != u] + [COST[u][START]]
        bound += min(options)
    return bound


# ----------------------------------------------------------------------------
# 3. Branch and Bound
# ----------------------------------------------------------------------------
class Node:
    """One box of the search tree (kept so we can draw it later)."""
    def __init__(self, nid, path, g, lb, parent):
        self.id = nid            # creation number
        self.path = path         # e.g. ['A','B']
        self.g = g               # path cost so far (for complete tours: full cycle cost)
        self.lb = lb             # lower bound
        self.parent = parent     # parent Node id (None for root)
        self.children = []
        self.status = "expanded" # expanded | pruned | best | complete
        self.best_when_checked = None   # incumbent value when the decision was made
        self.visit_order = None  # order in which the DFS reached the node


nodes = []
best_cost = math.inf
best_tour = None
counter = {"visit": 0}


def make_node(path, g, parent):
    lb = lower_bound(path, g)
    n = Node(len(nodes), path, g, lb, parent.id if parent else None)
    nodes.append(n)
    if parent:
        parent.children.append(n.id)
    return n


def fmt(path):
    return " -> ".join(path)


def branch_and_bound(node):
    """Depth-first Branch and Bound; children are tried cheapest-bound first."""
    global best_cost, best_tour
    node.visit_order = counter["visit"] = counter["visit"] + 1
    node.best_when_checked = best_cost
    shown_best = "inf" if best_cost == math.inf else best_cost

    # ---- complete tour? (all 4 cities visited, then return to A) ----
    if len(node.path) == len(CITIES):
        total = node.lb                       # for a complete route LB == real cost
        node.g = total
        tour = node.path + [START]
        if total < best_cost:
            print(f"  [{node.visit_order:2}] Complete tour {fmt(tour)} cost = {total}"
                  f"  < best ({shown_best})  -> NEW BEST (incumbent updated)")
            best_cost, best_tour = total, tour
            node.status = "best"
        else:
            print(f"  [{node.visit_order:2}] Complete tour {fmt(tour)} cost = {total}"
                  f"  >= best ({shown_best})  -> not better, ignored")
            node.status = "complete"
        return

    # ---- bounding test for a partial tour ----
    if node.lb >= best_cost:
        print(f"  [{node.visit_order:2}] {fmt(node.path):<14} path cost = {node.g:<3} LB = {node.lb:<3}"
              f" >= best ({shown_best})  -> PRUNED")
        node.status = "pruned"
        return

    print(f"  [{node.visit_order:2}] {fmt(node.path):<14} path cost = {node.g:<3} LB = {node.lb:<3}"
          f" <  best ({shown_best})  -> EXPAND")
    node.status = "expanded"

    # ---- branching: create one child per unvisited city ----
    kids = []
    for city in CITIES:
        if city not in node.path:
            g = node.g + COST[node.path[-1]][city]
            kids.append(make_node(node.path + [city], g, node))
    kids.sort(key=lambda k: (k.lb, k.path[-1]))   # most promising (smallest LB) first
    node.children = [k.id for k in kids]
    for k in kids:
        branch_and_bound(k)


# ----------------------------------------------------------------------------
# 4. Visualization (uses the recorded nodes only)
# ----------------------------------------------------------------------------
def draw_tree(filename="Visualization.png"):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, Patch

    # --- layout: leaves get consecutive x slots, parents sit above the middle of their children
    pos = {}
    slot = [0]

    def layout(nid, depth):
        n = nodes[nid]
        if not n.children:
            x = slot[0]; slot[0] += 1
        else:
            xs = [layout(c, depth + 1) for c in n.children]
            x = (xs[0] + xs[-1]) / 2
        pos[nid] = (x, -depth)
        return x
    layout(0, 0)
    width = slot[0]

    fig = plt.figure(figsize=(20, 11.5), dpi=130)
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.80])
    ax.set_xlim(-0.8, width - 0.2 + 0.5)
    ax.set_ylim(-4.6, 0.7)
    ax.axis("off")

    style = {   # face colour, edge colour, line style
        "expanded": ("#dbeafe", "#1d4ed8", "-"),
        "pruned":   ("#fee2e2", "#dc2626", "--"),
        "complete": ("#fef9c3", "#a16207", "-"),
        "best":     ("#bbf7d0", "#15803d", "-"),
    }
    BW, BH = 0.88, 0.80

    # --- edges (draw first, so boxes cover the line ends)
    for n in nodes:
        if n.parent is None:
            continue
        x1, y1 = pos[n.parent]; x2, y2 = pos[n.id]
        col = "#dc2626" if n.status == "pruned" else "#374151"
        ax.annotate("", xy=(x2, y2 + BH / 2), xytext=(x1, y1 - BH / 2),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.6,
                                    linestyle="--" if n.status == "pruned" else "-"))
        ax.text((x1 + x2) / 2 + 0.03, (y1 + y2) / 2 + 0.02, f"+{COST[nodes[n.parent].path[-1]][n.path[-1]]}",
                fontsize=8.5, color="#6b7280", ha="center", va="center",
                bbox=dict(fc="white", ec="none", pad=0.6))

    # --- node boxes
    optimal_ids = set()
    for n in nodes:
        if n.status == "best" and n.g == best_cost:
            optimal_ids.add(n.id)
    for n in nodes:
        x, y = pos[n.id]
        fc, ec, ls = style[n.status]
        lw = 3.2 if n.id in optimal_ids else 1.8
        ax.add_patch(FancyBboxPatch((x - BW / 2, y - BH / 2), BW, BH, boxstyle="round,pad=0.02,rounding_size=0.08",
                                    fc=fc, ec=ec, lw=lw, ls=ls, zorder=3))
        full = len(n.path) == len(CITIES)
        route = " > ".join(n.path + ([START] if full else []))
        if full:
            lines = [route, f"Tour cost = {n.g}"]
        else:
            lines = [route, f"Path cost g = {n.g}", f"Lower bound = {n.lb}"]
        ax.text(x, y + 0.24, lines[0], ha="center", va="center", fontsize=9.5, weight="bold", zorder=4)
        for i, t in enumerate(lines[1:]):
            ax.text(x, y + 0.03 - 0.19 * i, t, ha="center", va="center", fontsize=8.6, zorder=4)
        ax.text(x - BW / 2 + 0.03, y + BH / 2 - 0.02, f"#{n.visit_order}", fontsize=8, color="#111827",
                weight="bold", ha="left", va="bottom", zorder=5)

        # extra labels below the box
        if n.status == "pruned":
            ax.plot([x - 0.18, x + 0.18], [y - 0.62, y - 0.40], color="#dc2626", lw=3, zorder=5)
            ax.plot([x - 0.18, x + 0.18], [y - 0.40, y - 0.62], color="#dc2626", lw=3, zorder=5)
            ax.text(x, y - 0.74, "PRUNED", color="#dc2626", weight="bold", fontsize=9.5, ha="center", va="center")
            ax.text(x, y - 0.93, f"LB {n.lb} >= best {n.best_when_checked}", color="#dc2626", fontsize=8,
                    ha="center", va="center")
        elif n.status == "complete":
            ax.text(x, y - 0.55, "not better", color="#a16207", fontsize=8.5, ha="center", va="center", weight="bold")
            ax.text(x, y - 0.74, f"{n.g} >= best {n.best_when_checked}", color="#a16207", fontsize=8,
                    ha="center", va="center")
        elif n.status == "best":
            tag = "OPTIMAL TOUR" if n.id in optimal_ids else "BEST"
            ax.text(x, y - 0.55, "NEW BEST", color="#15803d", fontsize=8.5, ha="center", va="center", weight="bold")
            ax.text(x, y - 0.74, tag if tag == "OPTIMAL TOUR" else "", color="#15803d", fontsize=9.5,
                    ha="center", va="center", weight="bold")

    # level captions
    for d, name in enumerate(["Level 0", "Level 1", "Level 2", "Level 3"]):
        ax.text(-0.75, -d, name, fontsize=8.5, color="#6b7280", ha="left", va="center", style="italic")

    # --- title and header panels
    fig.text(0.5, 0.965, "TSP Using Branch and Bound \u2014 Search Tree for 4 Cities", ha="center", va="center",
             fontsize=21, weight="bold")
    fig.text(0.5, 0.932, "Start city A, visit B, C, D exactly once, return to A.  Numbers #1, #2, ... show the order "
             "in which the algorithm visits each node.", ha="center", va="center", fontsize=10.5, color="#374151")

    # cost matrix
    mx = fig.add_axes([0.02, 0.835, 0.22, 0.075]); mx.axis("off")
    tbl = mx.table(cellText=[[str(COST[r][c]) for c in CITIES] for r in CITIES],
                   rowLabels=CITIES, colLabels=CITIES, loc="center", cellLoc="center")
    tbl.auto_set_font_size(False); tbl.set_fontsize(9); tbl.scale(1, 1.05)
    fig.text(0.13, 0.917, "Cost matrix", ha="center", fontsize=10, weight="bold")

    # lower-bound formula
    fig.text(0.27, 0.905, "Lower bound (minimum outgoing-edge relaxation)", fontsize=10, weight="bold", va="center")
    fig.text(0.27, 0.865, "LB = g  +  min edge leaving the last city (to an unvisited city)\n"
                          "       +  \u03a3 over unvisited cities u : min edge leaving u (to an unvisited city or to A)\n"
                          "Prune a partial tour when  LB \u2265 best complete tour found so far.",
             fontsize=9.3, va="center", linespacing=1.5, family="DejaVu Sans")

    # result
    fig.text(0.70, 0.905, "Result", fontsize=10, weight="bold", va="center")
    fig.text(0.70, 0.862, f"Optimal tour : {' > '.join(best_tour)}\nMinimum cost : {best_cost}\n"
                          f"Nodes created : {len(nodes)}   Pruned : {sum(n.status == 'pruned' for n in nodes)}",
             fontsize=10, va="center", linespacing=1.5)

    # legend
    handles = [
        Patch(fc=style["expanded"][0], ec=style["expanded"][1], label="Expanded node (LB < best, explored further)"),
        Patch(fc=style["pruned"][0], ec=style["pruned"][1], ls="--", label="Pruned node (LB \u2265 best, discarded)"),
        Patch(fc=style["complete"][0], ec=style["complete"][1], label="Complete tour, not better than best"),
        Patch(fc=style["best"][0], ec=style["best"][1], label="Complete tour that became the new best"),
        Patch(fc=style["best"][0], ec=style["best"][1], lw=3, label="OPTIMAL TOUR (thick border)"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=3, fontsize=9.5, frameon=True, bbox_to_anchor=(0.5, 0.0))
    fig.text(0.98, 0.04, "Edge label +k = cost of the road added.  Arrows follow the DFS search order.",
             fontsize=8.5, ha="right", color="#6b7280")
    fig.savefig(filename, facecolor="white")
    plt.close(fig)
    print(f"\nVisualization saved as {filename}")


# ----------------------------------------------------------------------------
# 5. Main program
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    print("TSP with Branch and Bound  (4 cities, start = A)")
    print("Cost matrix:")
    print("      " + "".join(f"{c:>4}" for c in CITIES))
    for r in CITIES:
        print(f"   {r}  " + "".join(f"{COST[r][c]:>4}" for c in CITIES))
    print("\nSearch steps (g = path cost so far, LB = lower bound, best = incumbent):\n")

    root = make_node([START], 0, None)
    branch_and_bound(root)

    print("\n" + "=" * 60)
    print("Optimal tour :", fmt(best_tour))
    print("Minimum cost :", best_cost)
    print(f"Nodes created: {len(nodes)} | pruned: {sum(n.status == 'pruned' for n in nodes)}"
          f" | complete tours reached: {sum(len(n.path) == len(CITIES) for n in nodes if n.visit_order)}")

    # cross-check with brute force (all 3! = 6 tours)
    from itertools import permutations
    print("\nBrute-force check of all complete tours:")
    allt = []
    for p in permutations(CITIES[1:]):
        t = [START] + list(p) + [START]
        c = sum(COST[t[i]][t[i + 1]] for i in range(len(t) - 1))
        allt.append((c, t)); print(f"   {fmt(t)} = {c}")
    assert min(allt)[0] == best_cost, "Branch and Bound result disagrees with brute force!"
    print("Brute-force minimum =", min(allt)[0], "-> matches Branch and Bound.")

    try:
        draw_tree("Visualization.png")
    except ImportError:
        print("matplotlib not installed - skipping picture (pip install matplotlib).")
