import math
import matplotlib.pyplot as plt
import mplcursors

# Input sizes as required
n = [10, 100, 1000]

# Calculate theoretical growth: n * log2(n)
values = [i * math.log2(i) for i in n]

# Print theoretical values
print("Theoretical Growth Values (n * log2(n)):")
print(f"{'Input Size (n)':<20} {'Growth Value':<20}")
print("-" * 40)
for i, v in zip(n, values):
    print(f"{i:<20} {v:<20.2f}")

# Algorithm explanations
print("\n--- Algorithm Explanations ---")
print("""
Merge Sort:
  - Divide the array into two halves.
  - Recursively sort both halves.
  - Merge the sorted halves.
  - Best, Average, Worst-case: O(n log n)

Quick Sort:
  - Select a pivot.
  - Partition the array around the pivot.
  - Recursively sort the partitions.
  - Best and Average-case: O(n log n)
  - Worst-case: O(n²)
""")

# Complexity comparison table
print("--- Time Complexity Comparison ---")
print(f"{'Algorithm':<15} {'Best':<15} {'Average':<15} {'Worst':<15}")
print("-" * 60)
print(f"{'Merge Sort':<15} {'O(n log n)':<15} {'O(n log n)':<15} {'O(n log n)':<15}")
print(f"{'Quick Sort':<15} {'O(n log n)':<15} {'O(n log n)':<15} {'O(n²)':<15}")

# Create graph
plt.figure(figsize=(10, 6))

merge, = plt.plot(n, values, marker='o',
                  color='blue', linewidth=2.5,
                  markersize=9, label='Merge Sort: O(n log n)')

quick, = plt.plot(n, values, marker='s',
                  color='red', linewidth=2,
                  linestyle='--', markersize=8,
                  label='Quick Sort Average: O(n log n)')

plt.title("Time Complexity Growth: Merge Sort vs Quick Sort",
          fontsize=15, fontweight='bold')
plt.xlabel("Input Size (n)", fontsize=12)
plt.ylabel("Theoretical Growth: n log₂(n)", fontsize=12)
plt.xticks(n)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(fontsize=11)
plt.tight_layout()

# Hover annotations
cursor = mplcursors.cursor([merge, quick], hover=True)

@cursor.connect("add")
def show_value(selection):
    index = min(int(selection.index), len(n) - 1)
    label = selection.artist.get_label()
    complexity = "O(n log n)" if "Merge" in label else "O(n log n) avg / O(n²) worst"
    selection.annotation.set_text(
        f"Algorithm: {label}\n"
        f"Input Size: {n[index]}\n"
        f"Theoretical Growth: {values[index]:.2f}\n"
        f"Time Complexity: {complexity}"
    )

# Save and display
plt.savefig("Visualization.png", dpi=300, bbox_inches="tight")
plt.show()
