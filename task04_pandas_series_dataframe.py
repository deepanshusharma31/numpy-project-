# Task 4: Pandas Series & DataFrame
import pandas as pd

# Series
marks = pd.Series([88, 92, 79, 65, 94], index=["Aarav", "Diya", "Rohan", "Isha", "Kabir"], name="Marks")
print("Pandas Series:\n", marks)
print("Series mean:", marks.mean())

# DataFrame - student information
students = pd.DataFrame({
    "Name":   ["Aarav", "Diya", "Rohan", "Isha", "Kabir"],
    "Age":    [20, 21, 20, 22, 21],
    "Course": ["Economics", "Statistics", "Economics", "Commerce", "Statistics"],
    "Marks":  [88, 92, 79, 65, 94],
})
print("\nDataFrame:\n", students)
print("\nColumn names:", list(students.columns))
print("Index       :", students.index)

# Add new column
students["Result"] = students["Marks"].apply(lambda m: "Pass" if m >= 70 else "Needs Improvement")
students["Grade"] = pd.cut(students["Marks"], bins=[0, 69, 79, 89, 100], labels=["D", "C", "B", "A"])
print("\nUpdated DataFrame (with Result & Grade):\n", students)
