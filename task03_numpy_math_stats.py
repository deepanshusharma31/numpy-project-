# Task 3: NumPy Mathematical & Statistical Operations
import numpy as np

# Dataset: marks of 10 students in two subjects
maths   = np.array([78, 85, 92, 67, 74, 88, 95, 60, 81, 70])
science = np.array([72, 80, 89, 70, 68, 91, 90, 65, 77, 75])
print("Maths  :", maths)
print("Science:", science)

print("\n--- Mathematical Operations (element-wise) ---")
print("Addition      :", maths + science)
print("Subtraction   :", maths - science)
print("Multiplication:", maths * science)
print("Division      :", np.round(maths / science, 2))

print("\n--- Statistical Functions (Maths) ---")
print("Mean              :", np.mean(maths))
print("Median            :", np.median(maths))
print("Minimum           :", np.min(maths))
print("Maximum           :", np.max(maths))
print("Standard Deviation:", round(float(np.std(maths)), 2))
print("Sum               :", np.sum(maths))

print("\n--- Statistical Functions (Science) ---")
print("Mean              :", np.mean(science))
print("Median            :", np.median(science))
print("Minimum           :", np.min(science))
print("Maximum           :", np.max(science))
print("Standard Deviation:", round(float(np.std(science)), 2))
print("Sum               :", np.sum(science))

# Bonus: 2-D statistics along axes
marks = np.vstack([maths, science])
print("\nMean per subject (axis=1):", np.mean(marks, axis=1))
print("Mean per student (axis=0):", np.mean(marks, axis=0))
