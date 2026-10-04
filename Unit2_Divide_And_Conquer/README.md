# Strassen's Matrix Multiplication

*DAA Macro Project 5 – Divide-and-Conquer Matrix Multiplication*

## 1. Description

Strassen's algorithm is a **Divide-and-Conquer** algorithm for multiplying two square matrices. A matrix is divided into four smaller submatrices (quadrants), the smaller problems are solved, and the answers are combined.

The ordinary divide-and-conquer method needs **eight** recursive multiplications of submatrices. Strassen's clever idea reduces this to only **seven** multiplications (at the cost of a few extra additions and subtractions). Since multiplication is the expensive step, this makes the algorithm faster for large matrices.

## 2. Problem Statement

**Faculty requirement:** "Illustrate recursive division of matrices in Strassen's algorithm."

**Expected outcome:** "Block diagram of submatrix operations."

This project shows how the matrices are divided, how the seven products are computed, and how the result is combined, using a Python program and a block diagram.

## 3. Algorithm

1. **Divide** matrices A and B into four submatrices each (A11, A12, A21, A22 and B11, B12, B21, B22).
2. **Calculate** the seven Strassen products M1 to M7 (each is a recursive call).
3. **Calculate** C11, C12, C21 and C22 using additions/subtractions of M1 to M7.
4. **Combine** the four submatrices into one matrix.
5. **Obtain** the final matrix C = A × B.

Base case: when the matrices are 1 × 1, simply multiply the two numbers.

## 4. Pseudocode

```
START
Input matrices A and B (n x n, n a power of 2)
If n == 1:
    return A * B                      (base case)
Divide A into A11, A12, A21, A22
Divide B into B11, B12, B21, B22
Calculate M1 to M7 (each by a recursive call to Strassen)
Calculate C11, C12, C21, C22
Combine C11, C12, C21, C22 into C
Display result
END
```

## 5. Strassen's Seven Multiplications

| Product | Formula |
|---|---|
| M1 | (A11 + A22)(B11 + B22) |
| M2 | (A21 + A22) B11 |
| M3 | A11 (B12 − B22) |
| M4 | A22 (B21 − B11) |
| M5 | (A11 + A12) B22 |
| M6 | (A21 − A11)(B11 + B12) |
| M7 | (A12 − A22)(B21 + B22) |

The result submatrices are built from these products:

```
C11 = M1 + M4 - M5 + M7
C12 = M3 + M5
C21 = M2 + M4
C22 = M1 - M2 + M3 + M6
```

## 6. Visualization

`Visualization.png` is a block diagram titled *"Strassen's Matrix Multiplication – Recursive Division"*. Read it from top to bottom. It shows:

* **Matrix division** – A and B split into A11–A22 and B11–B22
* **Submatrix operations** – the additions/subtractions applied to the submatrices
* **Seven multiplication operations** – M1 to M7 with their values for the example
* **Recombination of submatrices** – formulas for C11, C12, C21, C22, then joined together
* **Final matrix** – C = [[19, 22], [43, 50]]

## 7. Complexity Analysis

| Method | Time complexity |
|---|---|
| Standard matrix multiplication | O(n³) |
| Strassen's algorithm | O(n^log₂7) ≈ O(n^2.81) |

The standard divide-and-conquer method gives the recurrence T(n) = 8T(n/2) + O(n²), which solves to O(n³). Strassen uses only seven recursive calls: T(n) = 7T(n/2) + O(n²), which solves to O(n^log₂7), approximately O(n^2.81).

Because 2.81 < 3, Strassen grows more slowly, so it wins for sufficiently large matrices. For small matrices the extra additions and overhead make it slower in practice.

## 8. Example

A = [[1, 2], [3, 4]], B = [[5, 6], [7, 8]]

Submatrices (each is 1 × 1): A11 = 1, A12 = 2, A21 = 3, A22 = 4; B11 = 5, B12 = 6, B21 = 7, B22 = 8.

| Product | Calculation | Value |
|---|---|---|
| M1 | (1 + 4)(5 + 8) = 5 × 13 | 65 |
| M2 | (3 + 4)(5) = 7 × 5 | 35 |
| M3 | 1 × (6 − 8) | −2 |
| M4 | 4 × (7 − 5) | 8 |
| M5 | (1 + 2)(8) = 3 × 8 | 24 |
| M6 | (3 − 1)(5 + 6) = 2 × 11 | 22 |
| M7 | (2 − 4)(7 + 8) = (−2) × 15 | −30 |

* C11 = 65 + 8 − 24 − 30 = **19**
* C12 = −2 + 24 = **22**
* C21 = 35 + 8 = **43**
* C22 = 65 − 35 − 2 + 22 = **50**

**Final result:** C = [[19, 22], [43, 50]]

The ordinary multiplication gives the same result, and the program prints `Both results equal: True`.

## 9. Learning Outcome

This project demonstrates:

* Divide-and-Conquer
* Matrix partitioning
* Recursive problem solving
* Strassen's seven multiplication technique
* Combining subproblem results
* Complexity analysis

## 10. Files

| File | Purpose |
|---|---|
| `Project5_Strassen.py` | Python program: recursive Strassen multiplication, step-by-step output for the 2×2 example, verification against ordinary multiplication, and generation of the diagram (needs matplotlib) |
| `Prompt.txt` | The faculty prompt and the detailed visualization prompt |
| `Visualization.png` | Block diagram of the submatrix operations |
| `README.md` | Project documentation (this file) |

Run with: `python Project5_Strassen.py`

## 11. Conclusion

Strassen's algorithm is a clear example of Divide-and-Conquer: a matrix is divided into smaller submatrices, the subproblems are solved using only seven multiplications instead of eight, and their results are combined to form the final matrix. This reduces the running time from O(n³) to about O(n^2.81).
