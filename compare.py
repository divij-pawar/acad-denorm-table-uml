import pandas as pd

# Load both Excel files
df1 = pd.read_excel("output.xlsx")
df2 = pd.read_excel("09_Blue_Book_Prelim_View.xlsx")

# Ensure both have the same column order
df2 = df2[df1.columns]

# Reset indices to align
df1 = df1.reset_index(drop=True)
df2 = df2.reset_index(drop=True)

# Compare values
comparison = df1.compare(df2)

# Save output
comparison.to_excel("differences.xlsx")

print("Comparison complete.")