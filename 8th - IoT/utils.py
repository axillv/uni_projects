from os import listdir
from os.path import basename, isfile, join
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
import seaborn as sns
from skinematics.imus import Madgwick
from skinematics.quat import q_conj, q_mult
from skinematics.vector import rotate_vector
from sklearn import preprocessing


def sliding_window_pd(
    df, ws=500, overlap=250, w_type="hann", w_center=True, print_stats=False
) -> list:
    """Applies the sliding window algorithm to the DataFrame rows.

    Args:
        df: The DataFrame with all the values that will be inserted to the
            sliding window algorithm.
        ws: The window size in number of samples.
        overlap: The hop length in number of samples.
        w_type: The windowing function.
        w_center: If False, set the window labels as the right edge of the
            window index. If True, set the window labels as the center of the
            window index.
        print_stats: Print statistical inferences from the process. Defaults
            to False.

    Returns:
        A list of DataFrames each one corresponding to a produced window.
    """
    counter = 0
    windows_list = list()
    # min_periods: Minimum number of observations in window required to have
    # a value;
    # For a window that is specified by an integer, min_periods will default
    # to the size of the window.
    for window in df.rolling(
        window=ws,
        step=overlap,
        min_periods=ws,
        win_type=w_type,
        center=w_center,
    ):
        if window[window.columns[0]].count() >= ws:
            if print_stats:
                print("Print Window:", counter)
                print("Number of samples:", window[window.columns[0]].count())
            windows_list.append(window)
        counter += 1
    if print_stats:
        print("List number of window instances:", len(windows_list))

    return windows_list


def apply_filter(arr, order=5, wn=0.1, filter_type="lowpass") -> np.ndarray:
    """Applies filter to the multi-axis signal.

    Args:
        arr: The initial NumPy signal array values.
        order: The order of the filter.
        wn: The critical frequency or frequencies.
        filter_type: The type of filter. {‘lowpass’, ‘highpass’, ‘bandpass’,
            ‘bandstop’}

    Returns:
        NumPy Array with the filtered signal.
    """
    fbd_filter = scipy.signal.butter(
        N=order, Wn=wn, btype=filter_type, output="sos"
    )
    filtered_signal = scipy.signal.sosfiltfilt(sos=fbd_filter, x=arr, padlen=0)

    return filtered_signal


def flatten_instances_df(instances_list: list) -> pd.DataFrame:
    """Flattens each instance and create a DataFrame with the whole flattened
        instances.

    Args:
        instances_list: The list of DataFrames to be flattened

    Returns:
        A DataFrame that includes the whole flattened DataFrames
    """
    flattened_instances_list = list()
    for item in instances_list:
        instance = item.to_numpy().flatten()
        flattened_instances_list.append(instance)
    df = pd.DataFrame(flattened_instances_list)

    return df


def df_rebase(
    df: pd.DataFrame, target_list: list, ref_list: list
) -> pd.DataFrame:
    """Changes the order and name of DataFrame columns to the project's needs
        for readability.

    Args:
        df: The pandas DataFrame.
        order_list: List object that contains the proper order of the default
             column names.
        ref_list: List object that contains the renaming list based
            on the project needs.

    Returns:
        A DataFrame with the new columns order and names.
    """
    print("Initial columns:", list(df.columns))

    if are_lists_equal(list(df.columns), ref_list):
        pass

    else:
        if len(target_list) == len(ref_list):
            # keep and re-order only the necessary columns of the initial DataFrame
            df = df[target_list]
            rename_dict = dict(zip(target_list, ref_list))
            df = df.rename(columns=rename_dict)  # rename the columns
        else:
            print(
                "The length of the target list and the reference list is not equal."
            )

    print("Processed columns:", list(df.columns))

    return df


def rename_df_column_values(
    np_array: np.ndarray,
    y: list,
    columns_names: tuple = ("acc_x", "acc_y", "acc_z"),
):
    """Creates a DataFrame with a "y" label column and replaces the values of the y with the index
    of the unique values of y.

    Args:
        np_array: 2D NumPy array.
        y: List with the y labels
        columns_names: List with the DF columns names.

    Returns:
        DataFrame with the multi-axes values and the target labels column.
    """
    arr_y = np.array(y)  # list to numpy array
    unique_values_list = np.unique(arr_y)  # unique list of values

    df = pd.DataFrame(np_array, columns=columns_names)
    df["y"] = y

    # replace the row item value in the y column of the df, with its index in the unique list
    for idx, x in enumerate(unique_values_list):
        df["y"] = np.where(df["y"] == x, idx, df["y"])

    return df


def are_lists_equal(list1: list, list2: list) -> bool:
    return set(list1) == set(list2)


def encode_labels(instances_list) -> np.ndarray:
    """Encodes target labels.

    Args:
        instances_list: List of instances to be encoded.

    Returns:
        The encoded array.
    """
    le = preprocessing.LabelEncoder()
    le.fit(instances_list)
    instances_arr = le.transform(instances_list)

    return instances_arr


def list_files_in_folder(folder_path) -> list:
    """Returns a list with the files in the folder.

    Args:
        folder_path:

    Returns:

    """
    files_list = list()
    for f in listdir(folder_path):
        if isfile(join(folder_path, f)):
            if f.endswith(".csv"):
                files_list.append(f)

    return files_list


def merge_sensor_data(
    acc_df: pd.DataFrame,
    gyro_df: pd.DataFrame,
    output_file: Optional[str] = None,
) -> pd.DataFrame:
    """
    Merges accelerometer and gyroscope DataFrames by syncing on truncated timestamps
    (e.g., removing the last digit for slight desyncs of ~1-9ms).
    On 200Hz sampling, there is no information lost.

    Args:
        acc_df (pd.DataFrame): Accelerometer data with "epoch (ms)", "x-axis (g)", "y-axis (g)", "z-axis (g)".
        gyro_df (pd.DataFrame): Gyroscope data with "epoch (ms)", "x-axis (deg/s)", "y-axis (deg/s)", "z-axis (deg/s)".
        output_file (Optional[str]): Path to save the merged DataFrame as CSV. Defaults to None.

    Returns:
        pd.DataFrame: Merged DataFrame synced on truncated epoch timestamps.
    """

    # Ensure timestamps are integers.
    acc_df["epoch (ms)"] = acc_df["epoch (ms)"].astype(np.int64)
    gyro_df["epoch (ms)"] = gyro_df["epoch (ms)"].astype(np.int64)

    # Truncate the timestamps (remove last digit)
    acc_df["truncated_epoch"] = acc_df["epoch (ms)"] // 10
    gyro_df["truncated_epoch"] = gyro_df["epoch (ms)"] // 10

    # Rename columns for clarity
    acc_df = acc_df.rename(
        columns={
            "x-axis (g)": "acc_x",
            "y-axis (g)": "acc_y",
            "z-axis (g)": "acc_z",
        }
    )

    gyro_df = gyro_df.rename(
        columns={
            "x-axis (deg/s)": "gyro_x",
            "y-axis (deg/s)": "gyro_y",
            "z-axis (deg/s)": "gyro_z",
        }
    )

    # Merge on truncated timestamp
    merged_df = pd.merge(
        acc_df[["epoch (ms)", "acc_x", "acc_y", "acc_z", "truncated_epoch"]],
        gyro_df[["gyro_x", "gyro_y", "gyro_z", "truncated_epoch"]],
        on="truncated_epoch",
        how="inner",
    )

    # Optionally drop truncated_epoch
    merged_df.drop(columns=["truncated_epoch"], inplace=True)

    # Save if needed
    if output_file:
        merged_df.to_csv(output_file, index=False)
        print(f"Merged data saved to {output_file}")

    return merged_df


def pair_sensor_files(files_list: list[str]) -> dict[str, dict[str, str]]:
    """
    Pairs accelerometer and gyroscope files based on their naming scheme.

    Scans a list of file paths and groups them into pairs (accelerometer and gyroscope)
    according to their base name. Only pairs containing both sensor types are returned.

    Args:
        files_list (list[str]): List of file paths (typically all files in a folder).

    Returns:
        dict[str, dict[str, str]]: Dictionary where each key is the base name and the value
            is a dict with keys "acc" and "gyro" mapping to their respective file paths.
            Example:
                {
                    "subject1_session1_": {
                        "acc": "path/to/subject1_session1_Accelerometer_.csv",
                        "gyro": "path/to/subject1_session1_Gyroscope_.csv"
                    },
                    ...
                }
    """
    paired_files: dict[str, dict[str, str]] = {}

    for file in files_list:
        filename = basename(file)
        if "Accelerometer" in filename:
            base_name = filename.replace("_Accelerometer_", "_")
            if base_name not in paired_files:
                paired_files[base_name] = {}
            paired_files[base_name]["acc"] = file
        elif "Gyroscope" in filename:
            base_name = filename.replace("_Gyroscope_", "_")
            if base_name not in paired_files:
                paired_files[base_name] = {}
            paired_files[base_name]["gyro"] = file

    # Filter out pairs with missing acc or gyro
    paired_files = {
        base_name: sensors
        for base_name, sensors in paired_files.items()
        if "acc" in sensors and "gyro" in sensors
    }

    return paired_files


def transform_imu_to_world(acc_data, gyr_data, rate=100):
    """Simplified and robust world-frame transformation with adaptive fallback.

    This implementation focuses on reliability over complex filter accuracy.
    When perfect transformation is not possible, it provides a graceful fallback
    that still produces usable results for activity recognition tasks.

    Args:
        acc_data: Accelerometer data (Nx3 numpy array)
        gyr_data: Gyroscope data (Nx3 numpy array)
        rate: Sampling rate in Hz (default: 100)

    Returns:
        acc_world: World-frame accelerometer data (Nx3 numpy array)
    """
    # Input validation
    if acc_data.size == 0 or gyr_data.size == 0:
        print("Warning: Empty input data in transform_imu_to_world")
        return np.zeros_like(acc_data)

    # Get number of samples
    N = acc_data.shape[0]

    # Initialize output array
    acc_world = np.zeros_like(acc_data)

    # Use a simplified gravity-based approach rather than complex integration
    # This is more robust for activity recognition and less error-prone
    try:
        # Estimate gravity direction from initial samples (when device is relatively stable)
        window_size = min(
            int(rate * 0.5), N
        )  # Use up to 0.5 seconds of initial data
        if window_size < 10:  # Need minimum samples for stable estimate
            raise ValueError("Not enough samples for stable gravity estimation")

        # Calculate average acceleration vector (primarily gravity during initial period)
        gravity_vector = np.mean(acc_data[:window_size], axis=0)
        gravity_magnitude = np.linalg.norm(gravity_vector)

        if (
            gravity_magnitude < 0.5
        ):  # Sanity check - gravity should be around 1g
            print(
                "Warning: Weak gravity signal detected, using default orientation"
            )
            gravity_vector = np.array([0, 0, 1.0])  # Default Z-axis gravity
            gravity_magnitude = 1.0

        # Normalize gravity vector
        gravity_unit = gravity_vector / gravity_magnitude

        # Create a basic rotation matrix that aligns device's gravity with world Z
        # Find rotation axis (cross product of device gravity and world Z)
        world_z = np.array([0, 0, 1.0])
        rotation_axis = np.cross(gravity_unit, world_z)
        rotation_axis_norm = np.linalg.norm(rotation_axis)

        # If gravity already aligned with Z, no rotation needed
        if rotation_axis_norm < 1e-6:
            # Check if aligned or anti-aligned
            if gravity_unit[2] > 0:
                # Already aligned, use identity rotation
                rotation_matrix = np.eye(3)
            else:
                # Anti-aligned (device upside down), rotate 180° around X
                rotation_matrix = np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]])
        else:
            # Normalize rotation axis
            rotation_axis = rotation_axis / rotation_axis_norm

            # Calculate rotation angle (dot product of vectors)
            rotation_angle = np.arccos(
                np.clip(np.dot(gravity_unit, world_z), -1.0, 1.0)
            )

            # Rodrigues' rotation formula for 3D rotation matrix
            K = np.array(
                [
                    [0, -rotation_axis[2], rotation_axis[1]],
                    [rotation_axis[2], 0, -rotation_axis[0]],
                    [-rotation_axis[1], rotation_axis[0], 0],
                ]
            )

            rotation_matrix = (
                np.eye(3)
                + np.sin(rotation_angle) * K
                + (1 - np.cos(rotation_angle)) * (K @ K)
            )

        # Apply rotation to all accelerometer samples
        for i in range(N):
            # Apply rotation
            rotated_acc = rotation_matrix @ acc_data[i]

            # Remove gravity component (subtract 1g from z-axis)
            # This creates a linear acceleration estimate
            acc_world[i] = rotated_acc.copy()
            acc_world[i, 2] -= gravity_magnitude  # Subtract gravity

        # No errors if we reach here
        return acc_world

    except Exception as e:
        print(f"Warning: Using fallback transformation due to: {e}")
        # Fallback to simple subtraction of estimated gravity

        # Attempt to estimate gravity direction from mean acceleration
        try:
            gravity_est = np.mean(acc_data, axis=0)
            gravity_norm = np.linalg.norm(gravity_est)

            if gravity_norm > 0.5:
                # Apply a very basic gravity removal
                gravity_unit = gravity_est / gravity_norm
                for i in range(N):
                    # Project acceleration onto gravity vector to estimate gravity component
                    gravity_component = (
                        np.dot(acc_data[i], gravity_unit) * gravity_unit
                    )
                    # Subtract gravity component to get linear acceleration
                    acc_world[i] = acc_data[i] - gravity_component
            else:
                # If gravity estimation fails, use original data
                acc_world = acc_data.copy()

        except Exception:
            # Ultimate fallback: return original data
            acc_world = acc_data.copy()

        print(f"Using fallback transformation for all {N} samples")
        return acc_world


def check_transformation_quality(acc_world):
    """Validate transformation results with enhanced diagnostics

    Args:
        acc_world: World-frame accelerometer data (Nx3 numpy array)

    Returns:
        Dictionary of quality metrics
    """
    # Basic validation - check if data exists
    if acc_world.size == 0:
        return {"valid": False, "error": "Empty input data"}

    # Calculate magnitude of acceleration at each point
    magnitudes = np.linalg.norm(acc_world, axis=1)

    # Check for NaN or inf values
    if np.any(np.isnan(acc_world)) or np.any(np.isinf(acc_world)):
        return {
            "valid": False,
            "error": "Contains NaN or Inf values",
            "nan_count": np.sum(np.isnan(acc_world)),
            "inf_count": np.sum(np.isinf(acc_world)),
        }

    # Calculate quality metrics
    metrics = {
        "valid": True,
        "z_mean": float(np.mean(acc_world[:, 2])),
        "z_std": float(np.std(acc_world[:, 2])),
        "xy_mean": [
            float(np.mean(acc_world[:, 0])),
            float(np.mean(acc_world[:, 1])),
        ],
        "xy_std": [
            float(np.std(acc_world[:, 0])),
            float(np.std(acc_world[:, 1])),
        ],
        "avg_magnitude": float(np.mean(magnitudes)),
        "min_magnitude": float(np.min(magnitudes)),
        "max_magnitude": float(np.max(magnitudes)),
    }

    # Sanity checks - add warnings for unusual values
    warnings = []

    # Check if mean Z close to -9.81 (would indicate gravity wasn't removed)
    if (
        isinstance(metrics["z_mean"], float)
        and abs(metrics["z_mean"] + 9.81) < 1.0
    ):
        warnings.append("Z-axis still contains gravity component")

    # Optionally, check if both XY means are close to zero (indicating no lateral movement)
    if isinstance(metrics["xy_mean"], list) and all(
        isinstance(x, float) and abs(x) < 0.05 for x in metrics["xy_mean"]
    ):
        warnings.append(
            "Very low XY mean values - possible lack of movement in XY plane"
        )

    # Check if magnitudes are extremely large (indicating possible errors)
    if (
        isinstance(metrics["max_magnitude"], float)
        and metrics["max_magnitude"] > 20
    ):
        warnings.append(
            f"Very large acceleration detected: {metrics['max_magnitude']:.2f}g"
        )

    # Check if data is mostly zero (indicating possible failed transformation)
    if (
        isinstance(metrics["avg_magnitude"], float)
        and metrics["avg_magnitude"] < 0.05
    ):
        warnings.append("Very low overall activity - possible data loss")

    metrics["warnings"] = warnings
    metrics["warning_count"] = len(warnings)

    return metrics
