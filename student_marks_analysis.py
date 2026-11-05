# Student Marks Analysis Project
# Libraries: NumPy, Pandas, Matplotlib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Load dataset
df = pd.read_csv("student_marks.csv")

subjects = ["Maths", "Science", "English", "History", "Computer"]
max_marks_per_subject = 100
pass_mark = 35  # minimum marks required in each subject

# 2. Display original data
print("\n===== STUDENT MARKS DATA =====")
print(df.to_string(index=False))

# 3. Calculate total, percentage, average and result
df["Total"] = df[subjects].sum(axis=1)
df["Percentage"] = (df["Total"] / (len(subjects) * max_marks_per_subject)) * 100
df["Average"] = df[subjects].mean(axis=1)
df["Result"] = np.where((df[subjects] >= pass_mark).all(axis=1), "Pass", "Fail")

# 4. Assign grades based on percentage
def get_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 35:
        return "D"
    return "F"

df["Grade"] = df["Percentage"].apply(get_grade)

# 5. Rank students by percentage
df["Rank"] = df["Percentage"].rank(method="min", ascending=False).astype(int)
df = df.sort_values("Rank")

print("\n===== ANALYSIS REPORT =====")
print(df[["Name", "Total", "Percentage", "Average", "Result", "Grade", "Rank"]].round(2).to_string(index=False))

# 6. NumPy summary statistics
marks_array = df[subjects].to_numpy()
print("\n===== SUBJECT STATISTICS (NumPy) =====")
print("Overall average mark:", round(np.mean(marks_array), 2))
print("Highest individual mark:", np.max(marks_array))
print("Lowest individual mark:", np.min(marks_array))

# 7. Pandas subject-wise summary
print("\n===== SUBJECT-WISE SUMMARY (Pandas) =====")
print(df[subjects].agg(["mean", "max", "min"]).round(2))

print("\nTopper:", df.iloc[0]["Name"], "-", round(df.iloc[0]["Percentage"], 2), "%")
print("Pass students:", int((df["Result"] == "Pass").sum()))
print("Fail students:", int((df["Result"] == "Fail").sum()))

# 8. Save analyzed results
df.to_csv("student_analysis_report.csv", index=False)
print("\nSaved results to student_analysis_report.csv")

# 9. Chart 1: Student percentages
plt.figure(figsize=(10, 5))
plt.bar(df["Name"], df["Percentage"])
plt.title("Student Percentage Comparison")
plt.xlabel("Student")
plt.ylabel("Percentage (%)")
plt.ylim(0, 100)
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("student_percentages.png", dpi=150)
plt.show()

# 10. Chart 2: Average marks by subject
subject_averages = df[subjects].mean()
plt.figure(figsize=(8, 5))
plt.bar(subject_averages.index, subject_averages.values)
plt.title("Average Marks by Subject")
plt.xlabel("Subject")
plt.ylabel("Average Marks")
plt.ylim(0, 100)
plt.tight_layout()
plt.savefig("subject_averages.png", dpi=150)
plt.show()

# 11. Chart 3: Pass/Fail distribution
result_counts = df["Result"].value_counts()
plt.figure(figsize=(6, 6))
plt.pie(result_counts.values, labels=result_counts.index, autopct="%1.1f%%", startangle=90)
plt.title("Pass vs Fail Distribution")
plt.tight_layout()
plt.savefig("pass_fail_pie.png", dpi=150)
plt.show()
