import pandas as pd

# Path to your conn.log
log_path = "hulk.log"
csv_output = "conn_hulk.csv"

# Read the log, skipping metadata lines (those starting with #)
with open(log_path, "r") as file:
    lines = file.readlines()

# Extract header fields from the Zeek log
for line in lines:
    if line.startswith("#fields"):
        fields = line.strip().split("\t")[1:]  # skip "#fields"
        break

# Filter out only the data lines (not metadata)
data_lines = [line for line in lines if not line.startswith("#")]

# Split each line into its columns
data = [line.strip().split("\t") for line in data_lines]

# Create a DataFrame
df = pd.DataFrame(data, columns=fields)

# Optional: Save to CSV
df.to_csv(csv_output, index=False)

print(f"Saved {log_path} to {csv_output} with {len(df)} rows and {len(df.columns)} columns.")
