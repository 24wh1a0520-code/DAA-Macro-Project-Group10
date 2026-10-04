"""
Project 5 - Divide-and-Conquer Matrix Multiplication
Strassen's Matrix Multiplication (recursive division into submatrices)
"""

# ---------- Helper functions ----------
def add(X, Y):
    return [[X[i][j] + Y[i][j] for j in range(len(X))] for i in range(len(X))]

def sub(X, Y):
    return [[X[i][j] - Y[i][j] for j in range(len(X))] for i in range(len(X))]

def split(M):
    """DIVIDE: split an n x n matrix into four (n/2 x n/2) submatrices."""
    h = len(M) // 2
    M11 = [row[:h] for row in M[:h]]
    M12 = [row[h:] for row in M[:h]]
    M21 = [row[:h] for row in M[h:]]
    M22 = [row[h:] for row in M[h:]]
    return M11, M12, M21, M22

def combine(C11, C12, C21, C22):
    """COMBINE: join four submatrices into one matrix."""
    top = [r1 + r2 for r1, r2 in zip(C11, C12)]
    bottom = [r1 + r2 for r1, r2 in zip(C21, C22)]
    return top + bottom

def standard_multiply(A, B):
    """Ordinary O(n^3) multiplication, used only for verification."""
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)]
            for i in range(n)]

def show(name, M):
    print(f"{name} = {M}")

# ---------- Strassen's algorithm (recursive) ----------
def strassen(A, B):
    n = len(A)
    if n == 1:                       # BASE CASE: 1x1 matrices
        return [[A[0][0] * B[0][0]]]

    A11, A12, A21, A22 = split(A)    # DIVIDE
    B11, B12, B21, B22 = split(B)

    # CONQUER: only 7 recursive multiplications
    M1 = strassen(add(A11, A22), add(B11, B22))
    M2 = strassen(add(A21, A22), B11)
    M3 = strassen(A11, sub(B12, B22))
    M4 = strassen(A22, sub(B21, B11))
    M5 = strassen(add(A11, A12), B22)
    M6 = strassen(sub(A21, A11), add(B11, B12))
    M7 = strassen(sub(A12, A22), add(B21, B22))

    C11 = add(sub(add(M1, M4), M5), M7)   # M1 + M4 - M5 + M7
    C12 = add(M3, M5)                     # M3 + M5
    C21 = add(M2, M4)                     # M2 + M4
    C22 = add(add(sub(M1, M2), M3), M6)   # M1 - M2 + M3 + M6

    return combine(C11, C12, C21, C22)    # COMBINE


# ---------- Step-by-step demonstration on the 2x2 example ----------
A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]

print("=== Strassen's Matrix Multiplication (Divide and Conquer) ===\n")
show("Matrix A", A)
show("Matrix B", B)

print("\n--- Step 1: DIVIDE into submatrices (each is 1x1 here) ---")
A11, A12, A21, A22 = split(A)
B11, B12, B21, B22 = split(B)
print("A11 =", A11, " A12 =", A12)
print("A21 =", A21, " A22 =", A22)
print("B11 =", B11, " B12 =", B12)
print("B21 =", B21, " B22 =", B22)

print("\n--- Step 2: Seven Strassen products ---")
M1 = strassen(add(A11, A22), add(B11, B22))
M2 = strassen(add(A21, A22), B11)
M3 = strassen(A11, sub(B12, B22))
M4 = strassen(A22, sub(B21, B11))
M5 = strassen(add(A11, A12), B22)
M6 = strassen(sub(A21, A11), add(B11, B12))
M7 = strassen(sub(A12, A22), add(B21, B22))
print("M1 = (A11 + A22)(B11 + B22) =", M1)
print("M2 = (A21 + A22) B11        =", M2)
print("M3 = A11 (B12 - B22)        =", M3)
print("M4 = A22 (B21 - B11)        =", M4)
print("M5 = (A11 + A12) B22        =", M5)
print("M6 = (A21 - A11)(B11 + B12) =", M6)
print("M7 = (A12 - A22)(B21 + B22) =", M7)

print("\n--- Step 3: Calculate C submatrices ---")
C11 = add(sub(add(M1, M4), M5), M7)
C12 = add(M3, M5)
C21 = add(M2, M4)
C22 = add(add(sub(M1, M2), M3), M6)
print("C11 = M1 + M4 - M5 + M7 =", C11)
print("C12 = M3 + M5           =", C12)
print("C21 = M2 + M4           =", C21)
print("C22 = M1 - M2 + M3 + M6 =", C22)

print("\n--- Step 4: COMBINE into final matrix C ---")
C = combine(C11, C12, C21, C22)
show("Strassen result C", C)

print("\n--- Verification ---")
D = standard_multiply(A, B)
show("Ordinary result  ", D)
print("Both results equal:", C == D)
print("Recursive strassen(A, B) gives:", strassen(A, B))


# ---------- Optional: draw Visualization.png ----------
def draw_diagram(filename="Visualization.png"):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch

    fig, ax = plt.subplots(figsize=(11, 16))
    ax.set_xlim(0, 100); ax.set_ylim(0, 145); ax.axis("off")

    def box(x, y, w, h, text, fc="#E8F0FE", ec="#1F4E79", fs=9, bold=False):
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                     boxstyle="round,pad=0.3", fc=fc, ec=ec, lw=1.4))
        ax.text(x, y, text, ha="center", va="center", fontsize=fs,
                fontweight="bold" if bold else "normal")

    def arrow(y1, y2):
        ax.annotate("", xy=(50, y2), xytext=(50, y1),
                    arrowprops=dict(arrowstyle="-|>", lw=2, color="#333"))

    ax.text(50, 141, "Strassen's Matrix Multiplication – Recursive Division",
            ha="center", fontsize=16, fontweight="bold")

    box(50, 133, 20, 5, "START", "#C8E6C9", "#2E7D32", 11, True)
    arrow(130.3, 127.5)
    box(50, 123, 64, 8, "Input Matrix A and Matrix B\n"
        "A = [[1, 2], [3, 4]]      B = [[5, 6], [7, 8]]", fs=10)
    arrow(118.8, 112)

    # Step 1: divide
    box(50, 100.5, 97, 22, "", "#FFF8E1", "#F9A825")
    ax.text(50, 109.3, "Step 1: DIVIDE  A and B into four submatrices",
            ha="center", fontsize=11, fontweight="bold")
    for cx, nm, vals in ((28, "A", (1, 2, 3, 4)), (72, "B", (5, 6, 7, 8))):
        ax.text(cx, 106, f"Matrix {nm}", ha="center", fontsize=9)
        names = [f"{nm}11 = {vals[0]}", f"{nm}12 = {vals[1]}",
                 f"{nm}21 = {vals[2]}", f"{nm}22 = {vals[3]}"]
        for k, t in enumerate(names):
            box(cx - 8 + 16 * (k % 2), 101 - 7 * (k // 2), 14, 5, t, "#FFFFFF", "#F9A825")
    arrow(89, 87.5)

    # Step 2: seven products
    box(50, 70.5, 97, 34, "", "#E3F2FD", "#1565C0")
    ax.text(50, 85, "Step 2: CONQUER  –  seven Strassen products (instead of eight)",
            ha="center", fontsize=11, fontweight="bold")
    prods = [("M1", "(A11 + A22)(B11 + B22)", "= 5 × 13 = 65"),
             ("M2", "(A21 + A22) B11", "= 7 × 5 = 35"),
             ("M3", "A11 (B12 − B22)", "= 1 × (−2) = −2"),
             ("M4", "A22 (B21 − B11)", "= 4 × 2 = 8"),
             ("M5", "(A11 + A12) B22", "= 3 × 8 = 24"),
             ("M6", "(A21 − A11)(B11 + B12)", "= 2 × 11 = 22"),
             ("M7", "(A12 − A22)(B21 + B22)", "= (−2) × 15 = −30")]
    pos = [(14, 77), (38, 77), (62, 77), (86, 77), (26, 63), (50, 63), (74, 63)]
    for (m, f, v), (x, y) in zip(prods, pos):
        box(x, y, 22, 10, f"{m} = {f}\n{v}", "#FFFFFF", "#1565C0", 8)
    arrow(53, 51.5)

    # Step 3: C formulas
    box(50, 42.5, 97, 18, "", "#E8F5E9", "#2E7D32")
    ax.text(50, 49.3, "Step 3: Calculate  C11, C12, C21, C22", ha="center",
            fontsize=11, fontweight="bold")
    cs = [("C11 = M1 + M4 − M5 + M7", "= 65+8−24−30 = 19"),
          ("C12 = M3 + M5", "= −2+24 = 22"),
          ("C21 = M2 + M4", "= 35+8 = 43"),
          ("C22 = M1 − M2 + M3 + M6", "= 65−35−2+22 = 50")]
    for (t, v), x in zip(cs, (14, 38, 62, 86)):
        box(x, 42, 22, 7, f"{t}\n{v}", "#FFFFFF", "#2E7D32", 8)
    arrow(33.3, 31.5)

    box(50, 27, 56, 8, "Step 4: COMBINE the four C submatrices\n"
        "C = [ C11  C12 ; C21  C22 ]", "#F3E5F5", "#6A1B9A", 10, True)
    arrow(22.7, 19)
    box(50, 13, 50, 10, "Final Matrix C = A × B\nC = [[19, 22], [43, 50]]",
        "#C8E6C9", "#2E7D32", 12, True)

    plt.savefig(filename, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("\nDiagram saved as", filename)

try:
    draw_diagram()
except ImportError:
    print("\n(matplotlib not installed - skipping diagram)")
