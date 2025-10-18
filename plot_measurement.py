""" import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file
# Make sure the CSV file is in the same directory as the script,
# or provide the full path to the file.
df = pd.read_csv('/home/jannen/Documents/MAS2025/Sem_2/SEE/Lect02/assignment02/my_group/manual_experiment.csv')

# Create a scatter plot
plt.figure(figsize=(10, 10))
plt.scatter(df['x'], df['y'], alpha=0.6)

# Style the plot
plt.grid(True, linestyle='--', alpha=0.5)
plt.xlabel("X [cm]", fontsize=12)
plt.ylabel("Y [cm]", fontsize=12)
plt.title("Scatter Plot of Manual Measurement Data", fontsize=13)
plt.axis('equal')
plt.tight_layout()

# Save the plot to a file
# plt.savefig('scatter_plot.png')

# To display the plot in a notebook or interactive environment, you would use:
plt.show() """


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data from the CSV file.
# Make sure your file has the columns: 'x', 'y', and 'orientation'.
try:
    df = pd.read_csv('./Manual Measurements - new-coordinate system.csv')
except FileNotFoundError:
    print("Error: Make sure your CSV file is named 'your_data_with_orientation.csv' and is in the same folder.")
    exit()

# plot
plt.figure(figsize=(12, 12))

# Plot the points themselves
plt.scatter(0,0, alpha=1, s=100, c='green', label='Start Pose (0,0)')
plt.scatter(df['y'], df['x'], alpha=0.5, s=50, label='Measured Position')
arrow_legend = plt.quiver([], [], [], [],
                angles='xy',
                scale_units='xy',
                scale=1,
                color='red',
                width=0.003,
                alpha=0.6,
                label='Orientation')

# Add an orientation arrow for each point
arrow_len = 2  # You can adjust the length of the arrows

for index, row in df.iterrows():
    # Get the x, y, and orientation (theta) for each row
    x = row['x']
    y = row['y']
    theta = np.deg2rad(row['orientation'])

    # Calculate the arrow's change in x and y based on the angle
    u = np.sin(theta) * arrow_len   # y-direction (horizontal)
    v = np.cos(theta) * arrow_len   # x-direction (forward)

    plt.quiver(y, x, u, v,
               angles='xy',
               scale_units='xy',
               scale=1,
               width=0.003,
               color='red')

    

# visualize
plt.grid(True, linestyle='--', alpha=0.5)
plt.xlabel("Y [cm]", fontsize=12)
plt.ylabel("X [cm]", fontsize=12)
plt.title("Manual Measurements with Position and Orientation", fontsize=14)
plt.axis('equal')
plt.legend()
plt.tight_layout()

# Save the plot to a file
plt.savefig('scatter_plot_with_orientation.png')

plt.show()