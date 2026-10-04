# Traveling Salesperson Problem using Dynamic Programming

**DAA Macro Project | Group G10 | Unit III - Dynamic Programming | Project 7: Traveling Salesperson DP Table**

## 1. Description

The **Traveling Salesperson Problem (TSP)** asks: a salesperson must visit every city exactly once and come back to the starting city. Each pair of cities has a travel cost (distance, time or money).

**Objective:** find the tour with the **minimum total cost**.

**Why Dynamic Programming?** Trying every possible tour (brute force) takes (n-1)! time. In brute force the same partial routes are recalculated again and again. Dynamic Programming (the **Held-Karp** method) stores the best cost for every "visited cities + current city" situation and reuses it, so each sub-problem is solved only once.

## 2. Problem Statement

Given 4 cities **A, B, C, D** and the cost between each pair, start at **A**, visit B, C and D exactly once, return to **A**, and find the minimum-cost tour. Visualize the DP state transitions between subsets of visited cities.

## 3. Input / Cost Matrix

| From \ To | A | B | C | D |
|-----------|---|---|---|---|
| **A** | 0 | 10 | 15 | 20 |
| **B** | 10 | 0 | 35 | 25 |
| **C** | 15 | 35 | 0 | 30 |
| **D** | 20 | 25 | 30 | 0 |

## 4. Dynamic Programming Approach

The DP state is

```
dp[subset][current_city]
```

- **subset** = the set of cities already visited (it always contains A).
- **current_city** = the city where the salesperson is standing now (it must be in the subset).
- **value** = the minimum cost to start at A, visit exactly the cities in the subset, and end at current_city.

Example: `dp[{A,B,D}][D] = 35` means the cheapest way to start at A, visit B and D, and finish at D costs 35 (A -> B -> D = 10 + 25).

The program stores a subset as a bitmask (bit 0 = A, bit 1 = B, bit 2 = C, bit 3 = D), e.g. `0111` = {A,B,C}.

## 5. State Transitions

A transition moves from a smaller subset to a bigger one by travelling to one **unvisited** city:

- {A} -> {A,B} (go A to B, cost 10)
- {A} -> {A,C} (go A to C, cost 15)
- {A} -> {A,D} (go A to D, cost 20)
- {A,B} -> {A,B,C} (go B to C, cost 35)
- {A,B} -> {A,B,D} (go B to D, cost 25)
- {A,B,D} -> {A,B,C,D} (go D to C, cost 30)

The algorithm processes subsets in order of size: 1 city, then 2, then 3, then all 4.

## 6. Recurrence

```
dp[{A}][A] = 0

dp[S][j] = min over i in S - {j}  of  ( dp[S - {j}][i] + cost(i, j) )

Minimum tour cost = min over j != A  of  ( dp[{A,B,C,D}][j] + cost(j, A) )
```

In simple words:
- `dp[{A}][A] = 0`: at the start we are at A and nothing has cost anything yet.
- `S - {j}`: the subset *before* we arrived at j.
- `i`: the city we were at just before j (the previous city); we try every possible one.
- `dp[S - {j}][i] + cost(i, j)`: best cost to reach i with the earlier cities, plus the cost of moving from i to j.
- `min`: keep the cheapest option.
- Last line: once all cities are visited, add the cost of returning to A from the final city and pick the smallest total.

## 7. Algorithm / Pseudocode

```
TSP_DP(cost, n):
    dp[all subsets][all cities] = infinity
    dp[{A}][A] = 0

    for each subset S in increasing order of size (S contains A):
        for each city j in S with dp[S][j] < infinity:
            for each city k not in S:
                newS = S + {k}
                dp[newS][k] = min( dp[newS][k], dp[S][j] + cost[j][k] )
                (remember j as the parent of state (newS, k))

    answer = infinity
    for each city j != A:
        answer = min( answer, dp[{A,B,C,D}][j] + cost[j][A] )

    rebuild the tour by following the stored parents backwards
    return answer and tour
```

## 8. Implementation

`Project7_TSP_DP.py` (plain Python, no extra libraries):
- stores the 4 x 4 cost matrix and uses bitmasks for subsets;
- fills the `dp` table from smaller subsets to larger subsets;
- prints every transition (`{A,B} at B --> go to C (+35) --> {A,B,C} at C: candidate = 45`);
- prints the full DP table, the minimum cost and the optimal tour (rebuilt using a `parent` table).

Run it with: `python Project7_TSP_DP.py`

## 9. Visualization

`Visualization.png` shows the DP as a state-transition graph, left to right:

- **Subsets:** {A} -> {A,B}, {A,C}, {A,D} -> {A,B,C}, {A,B,D}, {A,C,D} -> {A,B,C,D}.
- **DP states:** each box has the subset, the current city and its dp value.
- **Transitions:** arrows from smaller to larger subsets; the label `+x` is the cost of the move taken from the cost matrix.
- **Best vs worse transitions:** solid arrows give the minimum value of a state; dashed grey arrows are more expensive choices that are not used.
- **Final state:** the three {A,B,C,D} states, each with the cost of returning to A (`+10 = 80`, `+15 = 80`, `+20 = 95`).
- **Return to starting city:** all final states connect to "Back at A".
- **Optimal tour:** highlighted in red: A -> B -> D -> C -> A, cost 80.

The picture also contains the cost matrix and the recurrence.

## 10. Result

Output of `Project7_TSP_DP.py`:

| Subset | end B | end C | end D |
|--------|-------|-------|-------|
| {A,B} | 10 | - | - |
| {A,C} | - | 15 | - |
| {A,D} | - | - | 20 |
| {A,B,C} | 50 | 45 | - |
| {A,B,D} | 45 | - | 35 |
| {A,C,D} | - | 50 | 45 |
| {A,B,C,D} | 70 | 65 | 75 |

Closing the tour: end at B: 70 + 10 = 80, end at C: 65 + 15 = 80, end at D: 75 + 20 = 95.

- **Optimal tour: A -> B -> D -> C -> A**
- **Minimum cost: 80** (10 + 25 + 30 + 15)

The reverse tour A -> C -> D -> B -> A also costs 80 because the matrix is symmetric. The program reports the first one.

## 11. Complexity Analysis

- **Time Complexity: O(n^2 * 2^n).** There are about n * 2^n states (subset, current city) and each state tries up to n next cities. For n = 4 that is only a few dozen calculations. Brute force needs O((n-1)!) tours.
- **Space Complexity: O(n * 2^n)**, for the `dp` table (and the same size for the `parent` table).

## 12. Learning Outcome

- Understand how a hard problem is broken into overlapping sub-problems.
- Learn to define a DP state (`subset`, `current city`) and write a recurrence for it.
- See how bitmasks represent subsets and how a table is filled from smaller to larger subsets.
- Learn to rebuild the answer (the tour) from stored parent information.

## 13. Files

| File | Purpose |
|------|---------|
| `Project7_TSP_DP.py` | Python implementation of Held-Karp TSP for 4 cities; prints transitions, DP table, tour and cost |
| `Prompt.txt` | The detailed prompt used to create the visualization |
| `Visualization.png` | State-transition graph of DP subsets, costs and the optimal tour |
| `README.md` | Project documentation (this file) |

## 14. Conclusion

Using Dynamic Programming, the 4-city TSP is solved by building the best cost for every (subset, current city) state, moving from small subsets to the full set, and then returning to A. The minimum tour is **A -> B -> D -> C -> A with cost 80**. The table and graph make each step easy to verify by hand, and the same idea scales to larger inputs far better than brute force.
