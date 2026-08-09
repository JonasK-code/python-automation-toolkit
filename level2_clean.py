import pandas as pd

df = pd.read_csv("messy_leads.csv")

# 1. Drop exact duplicate rows
df = df.drop_duplicates()

# 2. Clean revenue: Strips everything except numbers and decimals
df["revenue"] = (
    df["revenue"]
    .astype(str)
    .str.replace(r"[^\d.]", "", regex=True)
)
df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce").fillna(0.0)

# 3. Standardize dates using format="mixed" to catch both / and -
df["signup_date"] = pd.to_datetime(
    df["signup_date"], format="mixed", errors="coerce"
).dt.strftime("%Y-%m-%d")

# 4. Clean names
df["name"] = df["name"].astype(str).str.strip().str.title()

# 📁 5. Save output to a new file!
output_file = "cleaned_level2.csv"
df.to_csv(output_file, index=False)

print("--- Fixed Output ---")
print(df)
print(f"\nSaved clean file as: {output_file}")