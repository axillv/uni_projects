import csv
import os

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy.typing import ArrayLike
from sklearn.preprocessing import LabelEncoder, QuantileTransformer

# keep 0.15% of malicious samples aka ~10:1 to benign
MALICIOUS_SAMPLES_PERCENT = 0.0015
CHUNK_SIZE = 200000
FILE_PATH = "data_cut.csv"


def normalize_categorical(column: pd.Series) -> ArrayLike:
    """Normalizes categorical columns by converting them to numerical values. Saves the encoder to a file.
    Args:
        column (pd.Series): The column to normalize.
    Returns:
        ArrayLike: The normalized column as an array.
    """
    col_name = (
        str(column.name).replace(" ", "_").replace("/", "_").replace("-", "_")
    )
    encoder = LabelEncoder()
    encoder.fit(column)

    os.makedirs("dataset_encoding", exist_ok=True)
    joblib.dump(encoder, f"dataset_encoding/{col_name}.joblib")

    return encoder.transform(column)


def normalize_quantile(column: pd.Series) -> np.ndarray:
    """Normalizes quantile columns using quantile transformation. Saves the transformer to a file.
    Args:
        column (pd.Series): The column to normalize.
    Returns:
        ArrayLike: The normalized column as an array.
    """
    col_name = (
        str(column.name).replace(" ", "_").replace("/", "_").replace("-", "_")
    )

    transformer = QuantileTransformer(output_distribution="normal")
    transformer.fit(np.asarray(column).reshape(-1, 1))

    os.makedirs("dataset_encoding", exist_ok=True)
    joblib.dump(transformer, f"dataset_encoding/{col_name}.joblib")

    return transformer.transform(np.asarray(column).reshape(-1, 1)).flatten()


def normalize_quantile_most_common(
    column: pd.Series,
) -> tuple[np.ndarray, ArrayLike]:
    """Normalizes quantile columns using quantile transformation, while also returning a second array
    that indicates whether the value is the most common value. Saves the transformer to a file.
    Args:
        column (pd.Series): The column to normalize.
    Returns:
        tuple[ArrayLike, ArrayLike]: Tuple of (normalized array, most common mask).
    """
    col_name = (
        str(column.name).replace(" ", "_").replace("/", "_").replace("-", "_")
    )
    transformer = QuantileTransformer(output_distribution="normal")
    transformer.fit(np.asarray(column).reshape(-1, 1))

    os.makedirs("dataset_encoding", exist_ok=True)
    joblib.dump(transformer, f"dataset_encoding/{col_name}.joblib")

    normalized_column = transformer.transform(
        np.asarray(column).reshape(-1, 1)
    ).flatten()

    # Find the most common value in the original column
    vals, counts = np.unique(column, return_counts=True)
    most_common_value = vals[np.argmax(counts)]
    most_common_mask = np.where(column == most_common_value, 1, 0)

    with open(f"dataset_encoding/most_common_values", "a") as f:
        f.write(f"{col_name},{most_common_value}\n")

    return normalized_column, most_common_mask


def normalize_binary(column: pd.Series, target_value: float | int) -> ArrayLike:
    """Normalizes binary columns by converting them to 0 or 1 for the target value and the rest respectively. Saves the mapping to a file.
    Args:
        column (pd.Series): The column to normalize.
        target_value (float | int): The value to assign to 0. The rest gets assigned to 1.
    Returns:
        ArrayLike: The normalized column as an array.
    """
    col_name = (
        str(column.name).replace(" ", "_").replace("/", "_").replace("-", "_")
    )
    os.makedirs("dataset_encoding", exist_ok=True)
    with open(f"dataset_encoding/binary_values", "a") as f:
        f.write(f"{col_name},{target_value}\n")

    return np.where(column == target_value, 0, 1)


def normalize_ternary(
    column: pd.Series,
    target_value_1: float | int,
    target_value_2: float | int,
) -> ArrayLike:
    """Normalizes ternary columns by converting them to -1, 0, or 1 based on the provided values, as with normalize_binary, 1 gets assign to the rest. Saves the mapping to a file.
    Args:
        column (pd.Series): The column to normalize.
        target_value_1 (float | int): The value to assign to -1.
        target_value_2 (float | int): The value to assign to 0.
    Returns:
        ArrayLike: The normalized column as an array.
    """
    col_name = (
        str(column.name).replace(" ", "_").replace("/", "_").replace("-", "_")
    )
    os.makedirs("dataset_encoding", exist_ok=True)
    with open(f"dataset_encoding/ternary_values", "a") as f:
        f.write(f"{col_name},{target_value_1},{target_value_2}\n")

    return np.select(
        [
            column == target_value_1,
            column == target_value_2,
        ],
        [-1, 0],
        default=1,
    )


def normalize():
    categorical_cols = [
        "Label",
        "Protocol",
        "Traffic Subtype",
        "Traffic Type",
    ]

    quantile = [
        "Average Packet Size",
        "Flow Duration",
        "Flow IAT Min",
        "Flow Packets/s",
        "Fwd Header Length",
        "Src Port",
        "Total Length of Fwd Packet",
    ]

    is_most_common_quantile = [
        "Active Max",
        "Active Std",
        "Bwd Bulk Rate Avg",
        "Bwd Bytes/Bulk Avg",
        "Bwd IAT Max",
        "Bwd IAT Mean",
        "Bwd IAT Min",
        "Bwd IAT Total",
        "Bwd Packet Length Max",
        "Bwd Packet Length Mean",
        "Bwd Packet Length Min",
        "Bwd Packets/s",
        "Dst Port",
        "Flow Bytes/s",
        "Fwd IAT Std",
        "FWD Init Win Bytes",
        "Fwd Packet Length Std",
        "Fwd Seg Size Min",
        "Idle Max",
        "Idle Std",
        "Packet Length Min",
        "Packet Length Variance",
        "Subflow Bwd Bytes",
        "Subflow Fwd Bytes",
        "Total Length of Bwd Packet",
    ]

    binary_cols = [
        "Bwd Init Win Bytes",  # 0 else
        "CWR Flag Count",  # 0 else
        "Dst IP",  # 192.168.1.90 else
        "ECE Flag Count",  # 0 else
        "FIN Flag Count",  # 0 else
        "Fwd PSH Flags",
        "Fwd URG Flags",
        "Src IP",  # 192.168.1.70   else
        "SYN Flag Count",  # 0 else
        "URG Flag Count",  # 0 else
    ]

    ternary_cols = [
        "Bwd Header Length",  # 20,0,else
        "Down/Up Ratio",  # 0,1,else
        "RST Flag Count",  # 0,1,2
        "Total Bwd packets",  # 0,1,else
        "Total Fwd Packet",  # Symmetrical weird transformation 1,2,else
    ]

    # Create a temporary directory if it doesn't exist
    os.makedirs("new_dataset_temp", exist_ok=True)

    for col in categorical_cols:
        data = pd.read_csv(
            filepath_or_buffer=FILE_PATH, usecols=[col], chunksize=CHUNK_SIZE
        )
        data = pd.concat(data)
        normalized_data = normalize_categorical(data[col])

        col_name = (
            str(col).replace(" ", "_").replace("/", "_").replace("-", "_")
        )
        temp_file_path = f"new_dataset_temp/{col_name}_normalized.csv"
        pd.DataFrame({col_name: normalized_data}).to_csv(
            temp_file_path, index=False
        )

    for col in quantile:
        data = pd.read_csv(
            filepath_or_buffer=FILE_PATH, usecols=[col], chunksize=CHUNK_SIZE
        )
        data = pd.concat(data)
        normalized_data = normalize_quantile(data[col])

        col_name = (
            str(col).replace(" ", "_").replace("/", "_").replace("-", "_")
        )
        temp_file_path = f"new_dataset_temp/{col_name}_normalized.csv"
        pd.DataFrame({col_name: normalized_data}).to_csv(
            temp_file_path, index=False
        )

    for col in is_most_common_quantile:
        data = pd.read_csv(
            filepath_or_buffer=FILE_PATH, usecols=[col], chunksize=CHUNK_SIZE
        )
        data = pd.concat(data)
        normalized_data, most_common_mask = normalize_quantile_most_common(
            data[col]
        )

        col_name = (
            str(col).replace(" ", "_").replace("/", "_").replace("-", "_")
        )
        temp_file_path = f"new_dataset_temp/{col_name}_normalized.csv"
        pd.DataFrame({col_name: normalized_data}).to_csv(
            temp_file_path, index=False
        )

        pd.DataFrame({f"{col_name}_is_most_common": most_common_mask}).to_csv(
            f"new_dataset_temp/{col_name}_is_most_common.csv", index=False
        )

    for col in binary_cols:
        data = pd.read_csv(
            filepath_or_buffer=FILE_PATH, usecols=[col], chunksize=CHUNK_SIZE
        )
        data = pd.concat(data)
        target_value = data[col].mode()[0]
        normalized_data = normalize_binary(data[col], target_value)

        col_name = (
            str(col).replace(" ", "_").replace("/", "_").replace("-", "_")
        )
        temp_file_path = f"new_dataset_temp/{col_name}_normalized.csv"
        pd.DataFrame({col_name: normalized_data}).to_csv(
            temp_file_path, index=False
        )

    for col in ternary_cols:
        data = pd.read_csv(
            filepath_or_buffer=FILE_PATH, usecols=[col], chunksize=CHUNK_SIZE
        )
        data = pd.concat(data)

        target_values, counts = np.unique(data[col], return_counts=True)
        # Get indices of top 2 counts
        top2_idx = np.argsort(counts)[-2:]
        target_values = target_values[top2_idx]
        counts = counts[top2_idx]

        normalized_data = normalize_ternary(
            data[col], target_values[0], target_values[1]
        )

        col_name = (
            str(col).replace(" ", "_").replace("/", "_").replace("-", "_")
        )
        temp_file_path = f"new_dataset_temp/{col_name}_normalized.csv"
        pd.DataFrame({col_name: normalized_data}).to_csv(
            temp_file_path, index=False
        )


def reassemble_normalized_data():
    """Efficiently reassembles the normalized data from the temporary directory into two CSV files (benign and malicious) in chunks using CHUNK_SIZE, reading each file line-by-line to avoid repeated disk I/O. Does not save a combined normalized_dataset.csv file."""

    temp_files = os.listdir("new_dataset_temp")
    temp_files = [f for f in temp_files if f.endswith(".csv")]
    temp_files.sort()  # Ensure consistent order
    file_paths = [os.path.join("new_dataset_temp", f) for f in temp_files]

    os.makedirs("new_dataset", exist_ok=True)
    benign_path = "new_dataset/benign_normalized.csv"
    malicious_path = "new_dataset/malicious_normalized.csv"
    if os.path.exists(benign_path):
        os.remove(benign_path)
    if os.path.exists(malicious_path):
        os.remove(malicious_path)

    # Open all files and create csv readers
    files = [open(fp, newline="") for fp in file_paths]
    readers = [csv.reader(f) for f in files]
    # Read headers
    headers = [next(r) for r in readers]
    # Flatten headers
    flat_header = [h[0] for h in headers]

    with open(benign_path, "w", newline="") as benign_f, open(
        malicious_path, "w", newline=""
    ) as malicious_f:
        benign_writer = csv.writer(benign_f)
        malicious_writer = csv.writer(malicious_f)
        benign_writer.writerow(flat_header)
        malicious_writer.writerow(flat_header)
        label_idx = flat_header.index("Label")
        while True:
            for _ in range(CHUNK_SIZE):
                try:
                    row = [next(r) for r in readers]
                    flat_row = [item for sublist in row for item in sublist]
                    if flat_row[label_idx] == "0":
                        benign_writer.writerow(flat_row)
                    elif flat_row[label_idx] == "1":
                        malicious_writer.writerow(flat_row)
                except StopIteration:
                    break
            else:
                continue
            break

    for f in files:
        f.close()
    # Delete the entire temp directory
    for file_path in file_paths:
        os.remove(file_path)
    os.rmdir("new_dataset_temp")



def main():
    normalize()
    reassemble_normalized_data()
()


if __name__ == "__main__":
    main()
