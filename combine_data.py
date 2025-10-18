import os
import glob
import pandas as pd
import re

# Folder containing the robot_path_*.csv files
data_folder = "./Experiment_results/right_new/SEE"   # Change this to your folder path

# Pattern to match files
pattern = os.path.join(data_folder, "robot_path_*.csv")
files = glob.glob(pattern)

all_data = []

for f in files:
    # Load each CSV (no header)
    df = pd.read_csv(f, header=None, names=["x", "y", "theta"])
    
    # Extract trial number from filename
    match = re.search(r'robot_path_(\d+)\.csv$', os.path.basename(f))
    # trial_num = match.group(1) if match else "unknown"
    
    # Add trial column
    # df["trial"] = trial_num
    
    all_data.append(df)

# Combine all dataframes
combined_df = pd.concat(all_data, ignore_index=True)

# Save to one CSV file
output_path = os.path.join(data_folder, "all_robot_paths.csv")
combined_df.to_csv("./right_path_combined.csv", index=False)

print(f"✅ Combined file saved as: {output_path}")
