import os
import glob
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =============================================================================
# PART 1: LOAD DATA FOR "MY GROUP" (FROM FOLDERS)
# =============================================================================
print("Loading data for 'My Group'...")

my_group_manual_file = '/home/jannen/Documents/MAS2025/Sem_2/SEE/Lect02/assignment02/my_group/manual_experiment.csv'

def load_and_normalize_my_group(filepath, direction):
    """Loads a trial CSV for My Group and normalizes its start to (0,0)"""
    df = pd.read_csv(filepath, sep=",", header=None, names=["x", "y", "theta"])
    df["y"] = -df["y"]
    x0, y0 = df.iloc[0][["x", "y"]]
    df["x"] = df["x"] - x0
    df["y"] = df["y"] - y0
    df["direction"] = direction
    return df

# Load all trial trajectories for My Group
# my_group_trials_data = []
# for direction, folder in my_group_folders.items():
#     pattern = os.path.join(folder, "robot_path_*.csv")
#     files = glob.glob(pattern)
#     for f in files:
#         my_group_trials_data.append(load_and_normalize_my_group(f, direction))
# my_group_trials = pd.concat(my_group_trials_data, ignore_index=True)

# Load manual measurements for My Group
my_group_manual = pd.read_csv(my_group_manual_file)


# =============================================================================
# PART 2: LOAD DATA FOR "OTHER GROUP" (FROM CSV FILES)
# =============================================================================
print("Loading data for 'Other Group'...")



# --- Load Manual Measurement Data ---
# ✨ IMPORTANT: Adjust 'X', 'Y', and 'Direction' if the column names
# in Robot_End_Poses_Manual.csv are different.
try:
    other_group_manual = pd.read_csv('/home/jannen/Documents/MAS2025/Sem_2/SEE/Lect02/assignment02/Bhavesh/Robot_End_Poses_Manual.csv')
    # The script assumes columns 'X' and 'Y'. If they are named differently,
    # you must rename them for the plot to work.
    other_group_manual = other_group_manual.rename(columns={'X': 'x', 'Y': 'y'})
except FileNotFoundError:
    print("Error: 'Robot_End_Poses_Manual.csv' not found.")
    exit()


# =============================================================================
# PART 3: CREATE THE COMBINED PLOT
# =============================================================================
print("Generating combined plot...")
plt.figure(figsize=(16, 16))
plt.grid(True, linestyle='--', alpha=0.6)

# --- Plot "My Group" Data (in Blue) ---
# Plot trajectories
# for direction in my_group_trials['direction'].unique():
#     df = my_group_trials[my_group_trials['direction'] == direction]
#     plt.plot(df['x'], df['y'], color='blue', linestyle='--', linewidth=1.5, label=f"My Group Trials" if direction=='left' else "")
# Plot manual points
plt.scatter(my_group_manual['x'], my_group_manual['y'], color='blue', marker='o', s=80,
            label='My Group Manual', zorder=5, edgecolors='black')


# --- Plot "Other Group" Data (in Red) ---
# Plot trajectories
# for direction in other_group_trials['direction'].unique():
#     df = other_group_trials[other_group_trials['direction'] == direction]
#     plt.plot(df['x'], df['y'], color='red', linestyle=':', linewidth=1.5, label=f"Other Group Trials" if direction=='left' else "")
# Plot manual points
plt.scatter(other_group_manual['x'], other_group_manual['y'], color='red', marker='^', s=80,
            label='Bhavesh Group Manual', zorder=5, edgecolors='black')


# =============================================================================
# PART 4: STYLE AND SAVE THE PLOT
# =============================================================================
plt.xlabel("X [cm]", fontsize=12)
plt.ylabel("Y [cm]", fontsize=12)
plt.title("Comparison of Trials Between My Group and Other Group", fontsize=16)
plt.axis('equal')
plt.legend(fontsize=12)
plt.tight_layout()

# Save the combined figure
output_filename = "plot_group_comparison.png"
plt.savefig(output_filename)
print(f"\nSuccessfully saved combined plot to {output_filename}")

plt.show()