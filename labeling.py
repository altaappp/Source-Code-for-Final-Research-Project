import pandas as pd

# Load both CSV files
benign_df = pd.read_csv("conn.csv")
attack_df = pd.read_csv("conn_golden.csv")

# Add a new column "Label" to each
benign_df["Label"] = "BENIGN"
attack_df["Label"] = "ANOMALY"

# Combine them into one DataFrame
combined_df = pd.concat([benign_df, attack_df], ignore_index=True)

# Optional: Shuffle the combined dataset
# combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save to a new CSV
combined_df.to_csv("conn_combined_golden.csv", index=False)

print(f"Saved combined dataset with {len(combined_df)} rows.")
