# Project 7 (Unit III - Dynamic Programming)
# Traveling Salesperson Problem using Held-Karp DP for 4 cities (A, B, C, D)

INF = float("inf")

CITIES = ["A", "B", "C", "D"]
N = len(CITIES)

# COST[i][j] = cost of travelling from city i to city j
COST = [
    #  A   B   C   D
    [0, 10, 15, 20],  # A
    [10, 0, 35, 25],  # B
    [15, 35, 0, 30],  # C
    [20, 25, 30, 0],  # D
]


def subset_name(mask):
    """Convert a bitmask into a readable subset, e.g. 0b0111 -> {A,B,C}."""
    return "{" + ",".join(CITIES[i] for i in range(N) if mask & (1 << i)) + "}"


def tsp_dp(verbose=True):
    """
    State : dp[mask][j] = minimum cost to start at A, visit exactly the cities
            in 'mask', and end at city j (j is in mask).
    Bit i of mask is 1 if city i has been visited. Bit 0 (city A) is always 1.
    """
    FULL = (1 << N) - 1                      # 1111 = {A,B,C,D}
    dp = [[INF] * N for _ in range(1 << N)]
    parent = [[-1] * N for _ in range(1 << N)]

    dp[1][0] = 0                             # base case: only A visited, standing at A
    if verbose:
        print("Base state: dp[{A}][A] = 0\n")

    # Increasing mask order guarantees smaller subsets are processed first
    for mask in range(1, 1 << N):
        if not (mask & 1):                   # every valid subset contains A
            continue
        for j in range(N):
            if not (mask & (1 << j)) or dp[mask][j] == INF:
                continue
            for k in range(N):               # try to go from j to a new city k
                if mask & (1 << k):
                    continue
                new_mask = mask | (1 << k)
                new_cost = dp[mask][j] + COST[j][k]
                if verbose:
                    print(f"{subset_name(mask)} at {CITIES[j]} (cost {dp[mask][j]}) "
                          f"--> go to {CITIES[k]} (+{COST[j][k]}) "
                          f"--> {subset_name(new_mask)} at {CITIES[k]}: candidate = {new_cost}")
                if new_cost < dp[new_mask][k]:
                    dp[new_mask][k] = new_cost
                    parent[new_mask][k] = j

    # Close the tour: from the last city go back to A
    best_cost, last = INF, -1
    if verbose:
        print("\nReturn to A from the full set {A,B,C,D}:")
    for j in range(N - 1, 0, -1):            # D, C, B (so ties pick the later city)
        total = dp[FULL][j] + COST[j][0]
        if verbose:
            print(f"  end at {CITIES[j]}: dp = {dp[FULL][j]}, "
                  f"+ cost({CITIES[j]}->A) = {COST[j][0]}  => total {total}")
        if total < best_cost:
            best_cost, last = total, j

    # Reconstruct the tour by following parents backwards
    path, mask, cur = [], FULL, last
    while cur != -1:
        path.append(CITIES[cur])
        prev = parent[mask][cur]
        mask ^= (1 << cur)
        cur = prev
    path.reverse()
    path.append("A")
    return dp, parent, best_cost, path


def print_dp_table(dp):
    print("\nDP table: dp[subset][last city]  (- means state not possible)")
    print(f"{'Subset':<12}" + "".join(f"{'end ' + c:>8}" for c in CITIES))
    for mask in sorted(range(1, 1 << N), key=lambda m: (bin(m).count("1"), m)):
        if not (mask & 1):
            continue
        row = ""
        for j in range(N):
            v = dp[mask][j]
            row += f"{'-' if v == INF else v:>8}"
        print(f"{subset_name(mask):<12}" + row)


if __name__ == "__main__":
    print("Cost matrix:")
    print("    " + "".join(f"{c:>4}" for c in CITIES))
    for i in range(N):
        print(f"{CITIES[i]:>3} " + "".join(f"{COST[i][j]:>4}" for j in range(N)))
    print()

    dp, parent, best_cost, path = tsp_dp()
    print_dp_table(dp)
    print("\nOptimal tour :", " -> ".join(path))
    print("Minimum cost :", best_cost)
