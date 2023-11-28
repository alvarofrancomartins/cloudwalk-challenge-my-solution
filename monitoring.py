"""
This Python code is designed to visualize and animate real-time anomalies detections in transaction data. 
It utilizes the matplotlib library for plotting and animation, along with pandas and numpy for data manipulation.
"""

# Importing necessary libraries
import sys
import pickle

import numpy             as np
import pandas            as pd
import matplotlib.pyplot as plt

from datetime             import datetime, date, timedelta
from matplotlib.dates     import DateFormatter
from IPython.display      import HTML, display, clear_output
from matplotlib.animation import FuncAnimation

# Function to detect anomalies based on mean and standard deviation
def detect_anomalies_in_real_time(mean_regularday, std_regularday, current_value, threshold=3):
    z_score = (current_value - mean_regularday) / std_regularday
    return np.abs(z_score) > threshold

# Function to animate the status plot in real-time
def animate_status(ax, fig, interval, status, df, max_frames, transaction):
    mean_regularday, std_regularday = transactions_regulardays[transaction][status][0], transactions_regulardays[transaction][status][1]

    x_data = [datetime.combine(date.today(), t) for t in df[status].index]
    y_data = df[status].values

    # Initialize the plot with the first data point
    line, = ax.plot(x_data[:1], y_data[:1], color=colors_dict[status])

    # Set the y label for each status
    ax.set_ylabel(status.capitalize(), fontsize=15)
    
    # Annotations to display information about anomalies
    annotation1 = ax.annotate("", xy=(0.5, 1.1), xycoords='axes fraction', ha='center', va='center', fontsize=15,
                              bbox=dict(boxstyle="round,pad=0.3", ec="k", fc='w', lw=0.9))
    annotation2 = ax.annotate("", xy=(0.5, 0.9), xycoords='axes fraction', ha='center', va='center', fontsize=12,
                              bbox=dict(boxstyle="round,pad=0.3", ec="k", fc='w', lw=0.9))

    # Update function for animation
    def update(frame):
        new_value = y_data[frame]

        line.set_data(x_data[:frame + 1], y_data[:frame + 1])

        # Detect anomalies in real-time
        is_anomalous = detect_anomalies_in_real_time(mean_regularday, std_regularday, new_value, threshold=3)

        if is_anomalous:
            # Highlight anomalous points (starred points)
            ax.scatter(x=x_data[frame], y=new_value, marker='*', zorder=10, s=250, color='#fdb863', edgecolor='k')
            
            annotation1.set_text(f"{status.capitalize()} is above normal!")
            annotation1.set_color(colors_dict[status])
            
            annotation2.set_text(f"Lastest possible anomaly: {new_value} transactions {status} at {x_data[frame].time()}")
            annotation2.set_color('k')
        else:
            annotation1.set_text("")

        # Try and except here to prevent an error when the animation stops and we can't index using frame + 1 anymore
        try:
            ax.set_xlim(x_data[0] - timedelta(minutes=1), x_data[frame + 1])

            # Adjust the y-axis to new data
            max_y = max(y_data[:frame + 1])
            buffer = 0.4 * max_y + 0.01
            ax.set_ylim(0, max_y + buffer)
        except IndexError:
            pass

        ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    # Create the animation
    anim = FuncAnimation(fig, update, interval=interval, frames = max_frames, blit=False, repeat = False)
    
    clear_output(wait=True)
    display(fig)
    
    return anim

# Get the command-line argument so we know which transactions file to use
transactions = sys.argv[1]

# Get the command-line interval argument to use in the animation
interval = sys.argv[2]

# Load precomputed regular days means and stds
transactions_regulardays = pickle.load(open("transactions_datasets/transactions_regulardays_dict.p", "rb"))

# Read transactions data from a CSV file
transactions_df = pd.read_csv(f'transactions_datasets/{transactions}.csv', names=['time', 'status', 'F1'], header=0)

# Preprocess the time colummn in the DataFrame
transactions_df['time'] = transactions_df.time.apply(lambda x: x.replace('h ', ':'))
transactions_df['time'] = pd.to_datetime(transactions_df['time'], format='%H:%M').dt.time

# Pivot the DataFrame to prepare for plotting
df = transactions_df.pivot_table(index='time', columns='status', values='F1', aggfunc='max', fill_value=0)

# Create subplots for each status
fig, axs = plt.subplots(nrows=3, figsize=(10, 10))

# Define each status' color
statuses = ['denied', 'failed', 'reversed']
colors = ['#e41a1c', '#a65628', '#4daf4a']
colors_dict = dict(zip(statuses, colors))

# Max number of frames should be set equal to the size of the time series
max_frames = len(df.index)

# Create animations for each status subplot
animations = [animate_status(ax, fig, interval, status, df, max_frames, transactions) for ax, status in zip(axs, statuses)]

axs[-1].set_xlabel('Time', fontsize=15, labelpad=8)

# Adjust layout for better visualization
plt.subplots_adjust(hspace=0.43)

# Show the plot
plt.show()