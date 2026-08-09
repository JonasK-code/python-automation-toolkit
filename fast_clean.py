import pandas as pd

# 1. Load the CSV file
df = pd.read_csv("messy_leads.csv")

# 2. Drop rows where age isn't a valid number or email is missing an '@'
df["age"] = pd.to_numeric(df["age"], errors="coerce")
df = df.dropna(subset=["age", "name"])
df = df[df["email"].str.contains("@", na=False)]

# 3. Clean and format strings properly
df["name"] = df["name"].str.strip().str.title()
df["email"] = df["email"].str.strip().str.lower()

# 4. Save the clean output
df.to_csv("cleaned_leads.csv", index=False)

print("--- Cleaned Data Output ---")
print(df)