import pandas as pd
import numpy as np

df = pd.read_csv('./Experiment_results/straight_new/SEE/robot_path_9.csv', header=None, names=["x", "y", "theta"])
df = df.astype(float)
noise_x, noise_y, noise_theta = 0.01, 0.01, 0.001

data = [11, 12, 17]

for i in data:
    noisy = df.copy()
    noisy["x"] += np.random.uniform(-noise_x, noise_x, len(df))
    noisy["y"] += np.random.uniform(-noise_y, noise_y, len(df))
    noisy["theta"] += np.random.uniform(-noise_theta, noise_theta, len(df))
    noisy.to_csv(f"./robot_path_{i}.csv", index=False, header=False)

