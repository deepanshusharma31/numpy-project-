# Task 1: NumPy Introduction & Arrays
import numpy as np

# Array with 10+ numbers
arr = np.array([12, 7, 25, 3, 18, 41, 9, 30, 15, 22, 5, 36])
print("Array:", arr)
print("Shape:", arr.shape)
print("Size :", arr.size)
print("Data type:", arr.dtype)

# One-dimensional array
arr_1d = np.arange(1, 11)
print("\n1-D array:", arr_1d)
print("Dimensions:", arr_1d.ndim)

# Two-dimensional array
arr_2d = np.array([[1, 2, 3, 4],
                   [5, 6, 7, 8],
                   [9, 10, 11, 12]])
print("\n2-D array:\n", arr_2d)
print("Dimensions:", arr_2d.ndim, "| Shape:", arr_2d.shape, "| Size:", arr_2d.size, "| dtype:", arr_2d.dtype)
