import os

# basic data engineering
import pandas as pd

# plotting
import matplotlib.pyplot as plt

from utils import pair_sensor_files, merge_sensor_data

data_path = os.path.join(os.getcwd(), "data")

# All subdirs
classes_folders_list = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]

labels_dict = {}

# Create plots directory if it doesn't exist
plots_dir = os.path.join(os.getcwd(), "plots")
os.makedirs(plots_dir, exist_ok=True)

print(classes_folders_list)

for class_folder in classes_folders_list:
    folder_path = os.path.join(data_path, class_folder)
    # All files of folder
    files_in_folder = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Full paths for reading files
    full_paths = [os.path.join(folder_path, f) for f in files_in_folder]

    # Pair session files together (acc+gyro)
    sessionfile_pairs = pair_sensor_files(full_paths)


    for session_name, sessionFiles in sessionfile_pairs.items():
        print(f"Dataset: {session_name}")
        # print(f"  Gyroscope file: {sessionFiles['gyro']}")
        # print(f"  Accelerometer file: {sessionFiles['acc']}")
        gyro_df = pd.read_csv(os.path.join(folder_path, sessionFiles['gyro']))
        acc_df = pd.read_csv(os.path.join(folder_path, sessionFiles['acc']))
        merged_df = merge_sensor_data(acc_df, gyro_df)

        if merged_df.empty:
            print(f"[EMPTY MERGE] ACC: {sessionFiles['acc']} | GYRO: {sessionFiles['gyro']}")
            continue

        print("Available columns in merged_df:", merged_df.columns.tolist())
        
        # Extract only accelerometer and gyroscope values
        sensor_columns = ['epoch (ms)', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z']
        sensor_data = merged_df[sensor_columns].copy()
        
        print("Sensor data shape:", sensor_data.shape)
        print("Sensor data columns:", sensor_data.columns.tolist())
        
        # Create a plot of the sensor data
        fig, axes = plt.subplots(2, 1, figsize=(15, 10))
        
        # Disable scientific notation and offset for x-axis
        from matplotlib.ticker import ScalarFormatter
        axes[0].xaxis.set_major_formatter(ScalarFormatter(useOffset=False))
        axes[0].ticklabel_format(style='plain', axis='x')
        axes[1].xaxis.set_major_formatter(ScalarFormatter(useOffset=False))
        axes[1].ticklabel_format(style='plain', axis='x')
        
        # Plot accelerometer data
        axes[0].plot(sensor_data['epoch (ms)'], sensor_data['acc_x'], label='Acc X', alpha=0.8)
        axes[0].plot(sensor_data['epoch (ms)'], sensor_data['acc_y'], label='Acc Y', alpha=0.8)
        axes[0].plot(sensor_data['epoch (ms)'], sensor_data['acc_z'], label='Acc Z', alpha=0.8)
        axes[0].set_title(f'Accelerometer Data - {class_folder} - {session_name}')
        axes[0].set_ylabel('Acceleration (g)')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Plot gyroscope data
        axes[1].plot(sensor_data['epoch (ms)'], sensor_data['gyro_x'], label='Gyro X', alpha=0.8)
        axes[1].plot(sensor_data['epoch (ms)'], sensor_data['gyro_y'], label='Gyro Y', alpha=0.8)
        axes[1].plot(sensor_data['epoch (ms)'], sensor_data['gyro_z'], label='Gyro Z', alpha=0.8)
        axes[1].set_title(f'Gyroscope Data - {class_folder} - {session_name}')
        axes[1].set_xlabel('Epoch (ms)')
        axes[1].set_ylabel('Angular Velocity (deg/s)')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        # Save plot to file instead of showing
        # Sanitize session_name for filename
        import re
        safe_session_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', session_name)
        plot_filename = f"{class_folder}_{safe_session_name}.png"
        plot_path = os.path.join(plots_dir, plot_filename)
        plt.savefig(plot_path)
        # plt.show()
        plt.close(fig)
        print(f"Plot saved to {plot_path}")
        
    break