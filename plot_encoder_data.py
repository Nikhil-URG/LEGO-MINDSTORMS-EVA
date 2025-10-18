import os
import glob
import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np
# Script for plots.....
# Config
# Define folders
left_data_folder = r'./Experiment_results/left_new/SEE'
right_data_folder = r'./Experiment_results/right_new/SEE'
forward_data_folder = r'./Experiment_results/straight_new/SEE'


# Define colors by direction
colors = {
    'forward': 'blue',
    'left': 'red',
    'right': 'green'
}

# Load and normalize all csv values
def load_and_normalize(filepath, direction):
    # Read space separated file
    df = pd.read_csv(filepath, sep=",", header=None, names=["x","y","theta"])
    # print(df)
    
    df["y"] = -df["y"]

    # Normalize coordinates so each trial starts from (0,0)
    x0, y0 = df.iloc[0][["x", "y"]]
    df["x"] = df["x"] - x0
    df["y"] = df["y"] - y0

    # Add direction + trial number
    df["direction"] = direction
    df["trial"] = re.search(r'(\d+)\.csv$', os.path.basename(filepath)).group(1)
    # print(df.head())

    return df

# Load all CSVs from all folders

all_data = []

for direction, folder in zip(["left", "right", "forward"],
                             [left_data_folder, right_data_folder, forward_data_folder]):
    pattern = os.path.join(folder, "robot_path_*.csv")
    print(pattern)
    files = sorted(glob.glob(pattern), key=lambda f: int(re.search(r'(\d+)\.csv$', f).group(1)))
    for f in files:
        all_data.append(load_and_normalize(f, direction))

# Combine all trials into one DataFrame
all_trials = pd.concat(all_data, ignore_index=True)

plt.figure(figsize=(10, 10))
plt.grid(True, linestyle='--', alpha=0.5)

# Mark start pose
plt.scatter(0, 0, color='darkred', marker='x', s=500, label='Start Pose')

# Plot each trial
for (direction, trial), df in all_trials.groupby(["direction", "trial"]):
    color = colors.get(direction.lower(), 'gray')
    plt.plot(df["x"], df["y"], linestyle=':', linewidth=1.3, color=color,
             label=f"{direction} (robot_path_{trial}.csv)")
    
    mid_idx = len(df) // 2
    plt.text(df["x"].iloc[mid_idx], df["y"].iloc[mid_idx],
             str(trial), fontsize=8, color=color)

    # Add final heading arrow
    x_end, y_end, theta_end = df.iloc[-1][["x", "y", "theta"]]
    arrow_len = 0.05
    plt.arrow(x_end, y_end,
              arrow_len * np.cos(theta_end),
              arrow_len * np.sin(theta_end),
              head_width=0.05, head_length=0.05,
              fc=color, ec=color, lw=0.5, alpha=0.8)

# Style
plt.xlabel("X [cm]", fontsize=12)
plt.ylabel("Y [cm]", fontsize=12)
plt.title("EV3 Encoder-Based Robot Paths (All Trials)", fontsize=13)
plt.legend(fontsize=8, loc='center left', bbox_to_anchor=(1.02, 0.5))
plt.axis('equal')
plt.tight_layout()
plt.show()