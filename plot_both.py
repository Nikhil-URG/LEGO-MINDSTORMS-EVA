import os
import glob
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Part 1: Load and Plot EV3 Encoder Paths ---
left_data_folder = '/home/jannen/Documents/MAS2025/Sem_2/SEE/Lect02/assignment02/my_group/Experiment_results/left_new/SEE'
right_data_folder = '/home/jannen/Documents/MAS2025/Sem_2/SEE/Lect02/assignment02/my_group/Experiment_results/right_new/SEE'
forward_data_folder = '/home/jannen/Documents/MAS2025/Sem_2/SEE/Lect02/assignment02/my_group/Experiment_results/straight_new/SEE'

# Define colors by direction
colors = {
    'forward': 'blue',
    'left': 'red',
    'right': 'green'
}

def load_and_normalize(filepath, direction):
    """Loads a trial CSV, normalizes its start to (0,0)"""
    df = pd.read_csv(filepath, sep=",", header=None, names=["x", "y", "theta"])
    df["y"] = -df["y"]
    x0, y0 = df.iloc[0][["x", "y"]]
    df["x"] = df["x"] - x0
    df["y"] = df["y"] - y0
    df["direction"] = direction
    df["trial"] = re.search(r'(\d+)\.csv$', os.path.basename(filepath)).group(1)
    return df

# Load all trial CSVs
all_data = []
for direction, folder in zip(["left", "right", "forward"],
                             [left_data_folder, right_data_folder, forward_data_folder]):
    pattern = os.path.join(folder, "robot_path_*.csv")
    files = sorted(glob.glob(pattern), key=lambda f: int(re.search(r'(\d+)\.csv$', f).group(1)))
    for f in files:
        all_data.append(load_and_normalize(f, direction))

all_trials = pd.concat(all_data, ignore_index=True)

# --- Part 2: Load Manual Measurement Data ---
manual_data_filename = '/home/jannen/Documents/MAS2025/Sem_2/SEE/Lect02/assignment02/my_group/manual_experiment.csv'
try:
    manual_df = pd.read_csv(manual_data_filename)
except FileNotFoundError:
    print(f"Error: Manual measurement file not found at '{manual_data_filename}'")
    exit()


# --- Part 3: Create the Combined Plot ---

plt.figure(figsize=(14, 14))
plt.grid(True, linestyle='--', alpha=0.6)

# Mark start pose
plt.scatter(0, 0, color='darkred', marker='x', s=100, label='Start Pose', zorder=10)

# A. Plot each EV3 trial path
for (direction, trial), df in all_trials.groupby(["direction", "trial"]):
    color = colors.get(direction.lower(), 'blue')
    plt.plot(df["x"], df["y"], linestyle=':', linewidth=1.5, color=color,
             label=f"Trial: {direction.capitalize()} {trial}")
    
    # Add final heading arrow for the trial
    x_end, y_end, theta_end = df.iloc[-1][["x", "y", "theta"]]
    arrow_len = 0.8
    # plt.arrow(x_end, y_end,
    #           arrow_len * np.cos(theta_end),
    #           arrow_len * np.sin(theta_end),
    #           head_width=0.4, head_length=0.4,
    #           fc=color, ec=color, lw=0.5, alpha=0.7)

# B. Plot the manual measurement points and orientations
plt.scatter(manual_df['x'], manual_df['y'], alpha=0.5, color='orange', marker='o', s=20,
            label='Manual Measurements', zorder=5)

# Add orientation arrows for manual data
manual_arrow_len = 1.0
for index, row in manual_df.iterrows():
    plt.arrow(
        row['x'], row['y'],
        manual_arrow_len * np.cos(row['orientation']),
        manual_arrow_len * np.sin(row['orientation']),
        head_width=0.4, head_length=0.4,
        fc='purple', ec='purple', alpha=0.9
    )

# --- Styling ---
plt.xlabel("X [cm]", fontsize=12)
plt.ylabel("Y [cm]", fontsize=12)
plt.title("Comparison of EV3 Encoder Paths and Manual Measurements", fontsize=15)
plt.legend(fontsize=9, loc='center left', bbox_to_anchor=(1.02, 0.5))
plt.axis('equal')
plt.tight_layout(rect=[0, 0, 0.85, 1]) # Adjust layout to make space for legend
plt.show()