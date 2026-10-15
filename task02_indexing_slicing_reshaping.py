# Task 2: NumPy Indexing, Slicing & Reshaping
import numpy as np

arr = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120])
print("Original 1-D array:", arr)

# Indexing
print("\n--- Indexing ---")
print("First element   arr[0]  :", arr[0])
print("Fifth element   arr[4]  :", arr[4])
print("Last element    arr[-1] :", arr[-1])

# Slicing
print("\n--- Slicing ---")
print("arr[2:7]  :", arr[2:7])
print("arr[:4]   :", arr[:4])
print("arr[::3]  :", arr[::3])
print("arr[::-1] :", arr[::-1])

# 2-D array
arr_2d = np.array([[11, 12, 13, 14],
                   [21, 22, 23, 24],
                   [31, 32, 33, 34]])
print("\n--- 2-D array ---\n", arr_2d)
print("Element at row 1, col 2  arr_2d[1, 2]:", arr_2d[1, 2])
print("Row 0     arr_2d[0]     :", arr_2d[0])
print("Column 1  arr_2d[:, 1]  :", arr_2d[:, 1])
print("Sub-matrix arr_2d[0:2, 1:3]:\n", arr_2d[0:2, 1:3])

# Reshaping
print("\n--- Reshaping ---")
print("Original shape:", arr.shape)
r1 = arr.reshape(3, 4)
print("Reshaped to (3, 4):\n", r1)
r2 = arr.reshape(4, 3)
print("Reshaped to (4, 3):\n", r2)
r3 = arr.reshape(2, 2, 3)
print("Reshaped to (2, 2, 3):\n", r3)
print("Flattened back:", r3.flatten())
