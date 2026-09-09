import gc

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import Birch, KMeans, MiniBatchKMeans
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.utils import shuffle
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical

# --- CONFIG ---
BENIGN_PATH = "new_dataset/benign_normalized.csv"
MALICIOUS_PATH = "new_dataset/malicious_normalized.csv"
RANDOM_STATE = 42
TARGET_COLS = ["Label", "Traffic_Type"]
N_CLUSTERS = 20
CHUNKSIZE = 1000000  # adjust based on your RAM


def load_benign():
    print("Reading benign data...")
    benign = pd.read_csv(BENIGN_PATH)
    print(f"Loaded {len(benign)} benign samples.")
    return benign


def sample_malicious_simple_csv(n_samples):
    print(f"Sampling {n_samples} malicious samples (simple random, chunked)...")
    total = sum(1 for _ in open(MALICIOUS_PATH)) - 1
    skip = sorted(
        np.random.choice(
            np.arange(1, total + 1), total - n_samples, replace=False
        )
    )
    print("Sampling indices chosen, reading in chunks...")
    malicious = pd.read_csv(MALICIOUS_PATH, skiprows=skip)
    print(f"Sampled {len(malicious)} malicious samples.")
    return malicious


def sample_malicious_clusters_csv(method, n_clusters, n_samples):
    if method == "birch":
        print(
            f"Clustering ALL malicious data with BIRCH ({n_clusters} clusters, chunked)..."
        )
        # Use partial_fit with Birch in chunks
        birch = Birch(n_clusters=n_clusters)
        chunk_iter = pd.read_csv(MALICIOUS_PATH, chunksize=CHUNKSIZE)
        print("Fitting BIRCH in chunks...")
        for i, chunk in enumerate(chunk_iter):
            features = chunk.drop(columns=TARGET_COLS)
            birch.partial_fit(features)
            print(f"  Processed chunk {i+1}")
        # Assign clusters to all data (need to re-read)
        print("Assigning clusters to all malicious data...")
        malicious = []
        cluster_labels = []
        for i, chunk in enumerate(
            pd.read_csv(MALICIOUS_PATH, chunksize=CHUNKSIZE)
        ):
            print(f"  Assigning to chunk {i+1}")
            features = chunk.drop(columns=TARGET_COLS)
            labels = birch.predict(features)
            chunk["cluster"] = labels
            malicious.append(chunk)
            cluster_labels.extend(labels)
        malicious = pd.concat(malicious, ignore_index=True)
    elif method == "kmeans":
        print(
            f"Clustering ALL malicious data with MiniBatchKMeans ({n_clusters} clusters, chunked)..."
        )
        mbk = MiniBatchKMeans(
            n_clusters=n_clusters,
            random_state=RANDOM_STATE,
            batch_size=CHUNKSIZE,
        )
        # First pass: partial_fit in chunks
        chunk_iter = pd.read_csv(MALICIOUS_PATH, chunksize=CHUNKSIZE)
        print("Fitting MiniBatchKMeans in chunks...")
        for i, chunk in enumerate(chunk_iter):
            features = chunk.drop(columns=TARGET_COLS)
            mbk.partial_fit(features)
            print(f"  Processed chunk {i+1}")
        # Second pass: assign clusters to all data (need to re-read)
        print("Assigning clusters to all malicious data...")
        malicious = []
        cluster_labels = []
        for i, chunk in enumerate(
            pd.read_csv(MALICIOUS_PATH, chunksize=CHUNKSIZE)
        ):
            print(f"  Assigning to chunk {i+1}")
            features = chunk.drop(columns=TARGET_COLS)
            labels = mbk.predict(features)
            chunk["cluster"] = labels
            malicious.append(chunk)
            cluster_labels.extend(labels)
        malicious = pd.concat(malicious, ignore_index=True)
    else:
        raise ValueError("method must be 'birch' or 'kmeans'")

    samples_per_cluster = n_samples // n_clusters
    sampled = []
    sampled_indices = []
    print("Sampling from each cluster...")
    for c in range(n_clusters):
        cluster_data = malicious[malicious["cluster"] == c]
        if len(cluster_data) == 0:
            continue
        if len(cluster_data) >= samples_per_cluster:
            sample = cluster_data.sample(
                n=samples_per_cluster, random_state=RANDOM_STATE
            )
        else:
            sample = cluster_data.sample(
                n=samples_per_cluster, replace=True, random_state=RANDOM_STATE
            )
        sampled.append(sample)
        sampled_indices.extend(sample.index.tolist())
    result = pd.concat(sampled).drop(columns=["cluster"])
    print(f"Sampled {len(result)} malicious samples from clusters.")
    with open(f"new_dataset/malicious_{method}_sampled_indices.txt", "w") as f:
        for idx in sampled_indices:
            f.write(f"{idx}\n")
    del malicious, cluster_labels, sampled, sample, cluster_data
    gc.collect()
    return shuffle(result, random_state=RANDOM_STATE)


def load_encoder(col):
    path = f"dataset_encoding/{col}.joblib"
    try:
        encoder = joblib.load(path)
        return encoder
    except Exception as e:
        print(f"Could not load encoder for {col}: {e}")
        return None


def prepare_dataset(benign_df, malicious_df, target_col):
    print(f"Preparing dataset for target: {target_col} ...")
    data = pd.concat([benign_df, malicious_df])
    data = shuffle(data, random_state=RANDOM_STATE)
    # Drop label columns and Traffic_Subtype to prevent leakage
    drop_cols = TARGET_COLS + ["Traffic_Subtype"]
    X = data.drop(columns=[col for col in drop_cols if col in data.columns])
    y = data[target_col]
    encoder = load_encoder(target_col)
    print(f"[DEBUG] {target_col} unique values in y: {y.unique()}")
    print(f"[DEBUG] {target_col} dtype: {y.dtype}")
    if encoder is not None:
        print(f"[DEBUG] Encoder classes for {target_col}: {encoder.classes_}")
        if np.issubdtype(y.dtype, np.integer) and not np.issubdtype(
            encoder.classes_.dtype, np.integer
        ):
            y = y.map(
                lambda i: (
                    encoder.classes_[i] if i < len(encoder.classes_) else str(i)
                )
            )
        elif (
            encoder.classes_.dtype.type is np.str_
            or encoder.classes_.dtype == object
        ):
            y = y.astype(str)
        print(f"[DEBUG] y after mapping: {y.unique()}")
        y_factorized = encoder.transform(y)
        uniques = encoder.classes_
    else:
        y_factorized, uniques = pd.factorize(y)
    if y.nunique() > 2:
        y_enc = to_categorical(y_factorized)
    else:
        y_enc = y_factorized
    print(f"[DEBUG] X columns: {list(X.columns)}")
    for col in TARGET_COLS:
        if col in X.columns:
            print(f"[LEAK WARNING] {col} found in features!")
    print(
        f"[DEBUG] y value counts: {pd.Series(y_factorized).value_counts().to_dict()}"
    )
    print(f"[DEBUG] First 10 y values after mapping: {y.head(10)}")
    # Check for high correlation between features and label
    for col in X.columns:
        try:
            corr = np.corrcoef(X[col], y_factorized)[0, 1]
            if abs(corr) > 0.95:
                print(
                    f"[LEAKAGE WARNING] Feature '{col}' has high correlation ({corr:.2f}) with the label!"
                )
        except Exception:
            pass
    return X.values, y_enc, y_factorized, uniques, encoder


def train_nn(X_train, y_train, X_val, y_val, n_classes):
    print("Training Neural Network...")
    # Use integer labels for multiclass
    if y_train.ndim > 1:
        y_train_labels = np.argmax(y_train, axis=1)
        y_val_labels = np.argmax(y_val, axis=1)
    else:
        y_train_labels = y_train
        y_val_labels = y_val

    class_weight_dict = get_class_weights(
        y_train_labels, np.unique(y_train_labels)
    )
    print(f"[DEBUG] Using class weights: {class_weight_dict}")

    if n_classes == 1:
        # Binary classification
        model = Sequential(
            [
                Input(shape=(X_train.shape[1],)),
                Dense(128, activation="relu"),
                Dense(64, activation="relu"),
                Dense(1, activation="sigmoid"),
            ]
        )
        model.compile(
            optimizer="adam",
            loss="binary_crossentropy",
            metrics=["accuracy"],
        )
        y_train_fit = y_train_labels
        y_val_fit = y_val_labels
    else:
        # Multiclass classification
        model = Sequential(
            [
                Input(shape=(X_train.shape[1],)),
                Dense(128, activation="relu"),
                Dense(64, activation="relu"),
                Dense(n_classes, activation="softmax"),
            ]
        )
        model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )
        y_train_fit = y_train_labels
        y_val_fit = y_val_labels

    model.fit(
        X_train,
        y_train_fit,
        epochs=50,
        batch_size=64,
        validation_data=(X_val, y_val_fit),
        verbose=1,
        class_weight=class_weight_dict,
    )
    print("Neural Network training complete.")
    return model


def train_svm(X_train, y_train):
    print("Training SVM...")
    svm = SVC(
        class_weight="balanced", probability=True, random_state=RANDOM_STATE
    )
    svm.fit(X_train, y_train)
    print("SVM training complete.")
    return svm


def evaluate_model(
    model, X_test, y_test, y_test_factorized, uniques, encoder, model_type="nn"
):
    print(f"Evaluating {model_type.upper()} model...")
    if model_type == "nn":
        y_pred = model.predict(X_test)
        if y_pred.shape[1] > 1:
            y_pred_labels = np.argmax(y_pred, axis=1)
        else:
            y_pred_labels = (y_pred > 0.5).astype(int).flatten()
    else:
        y_pred_labels = model.predict(X_test)
    # Decode using encoder if available
    if encoder is not None:
        y_pred_labels_decoded = encoder.inverse_transform(y_pred_labels)
        y_test_labels_decoded = encoder.inverse_transform(y_test_factorized)
        print("Label mapping used for evaluation:")
        for idx, label in enumerate(encoder.classes_):
            print(f"  {idx}: {label}")
    else:
        y_pred_labels_decoded = uniques[y_pred_labels]
        y_test_labels_decoded = uniques[y_test_factorized]
    print(classification_report(y_test_labels_decoded, y_pred_labels_decoded))
    print(
        "Accuracy:",
        accuracy_score(y_test_labels_decoded, y_pred_labels_decoded),
    )
    print("Confusion Matrix:")
    print(confusion_matrix(y_test_labels_decoded, y_pred_labels_decoded))


def get_class_weights(y, classes):
    y_labels = y if y.ndim == 1 else np.argmax(y, axis=1)
    weights = compute_class_weight(
        "balanced", classes=np.arange(len(classes)), y=y_labels
    )
    return {i: w for i, w in enumerate(weights)}


# --- MAIN PIPELINE ---
def main():
    print("Starting pipeline...")
    benign = load_benign()
    n_benign = len(benign)
    n_malicious = n_benign * 10
    print(
        f"Using all {n_benign} benign samples and {n_malicious} malicious samples for each method."
    )
    sampling_methods = {
        "simple": lambda: sample_malicious_simple_csv(n_malicious),
        "kmeans": lambda: sample_malicious_clusters_csv(
            "kmeans", N_CLUSTERS, n_malicious
        ),
        "birch": lambda: sample_malicious_clusters_csv(
            "birch", N_CLUSTERS, n_malicious
        ),
    }
    for method_name, sampler in sampling_methods.items():
        print(f"\n=== Sampling method: {method_name.upper()} ===")
        mal_sample = sampler()
        for target in TARGET_COLS:
            print(f"\n--- Target: {target} ---")
            X, y, y_factorized, uniques, encoder = prepare_dataset(
                benign, mal_sample, target
            )
            # Debug: Check for duplicates between train and test
            print(f"[DEBUG] Checking for duplicates in features...")
            print(f"[DEBUG] X shape: {X.shape}")
            print(
                f"[DEBUG] Number of duplicate rows in X: {pd.DataFrame(X).duplicated().sum()}"
            )
            (
                X_train,
                X_test,
                y_train,
                y_test,
                y_train_factorized,
                y_test_factorized,
            ) = train_test_split(
                X,
                y,
                y_factorized,
                test_size=0.2,
                random_state=RANDOM_STATE,
                stratify=y_factorized,
            )
            print(
                f"[DEBUG] Train class distribution: {np.bincount(y_train if y_train.ndim == 1 else np.argmax(y_train, axis=1))}"
            )
            print(
                f"[DEBUG] Test class distribution: {np.bincount(y_test if y_test.ndim == 1 else np.argmax(y_test, axis=1))}"
            )
            # Check for overlap between train and test
            train_hashes = pd.util.hash_pandas_object(
                pd.DataFrame(X_train)
            ).values
            test_hashes = pd.util.hash_pandas_object(
                pd.DataFrame(X_test)
            ).values
            overlap = np.intersect1d(train_hashes, test_hashes).size
            print(f"[DEBUG] Overlapping rows between train and test: {overlap}")
            # Neural Network
            n_classes = y_train.shape[1] if len(y_train.shape) > 1 else 1
            nn_model = train_nn(X_train, y_train, X_test, y_test, n_classes)
            evaluate_model(
                nn_model,
                X_test,
                y_test,
                y_test_factorized,
                uniques,
                encoder,
                model_type="nn",
            )
            # After predictions, check if model is always predicting one class
            print(
                f"[DEBUG] NN predicted class distribution: {np.bincount(np.argmax(nn_model.predict(X_test), axis=1) if len(y_test.shape) > 1 else (nn_model.predict(X_test) > 0.5).astype(int).flatten())}"
            )
            del nn_model
            gc.collect()
            # SVM
            if len(y_train.shape) > 1:
                y_train_svm = np.argmax(y_train, axis=1)
            else:
                y_train_svm = y_train
            svm_model = train_svm(X_train, y_train_svm)
            evaluate_model(
                svm_model,
                X_test,
                y_test,
                y_test_factorized,
                uniques,
                encoder,
                model_type="svm",
            )
            # After predictions, check if model is always predicting one class
            print(
                f"[DEBUG] SVM predicted class distribution: {np.bincount(svm_model.predict(X_test))}"
            )
            del (
                X_train,
                X_test,
                y_train,
                y_test,
                y_train_factorized,
                y_test_factorized,
                svm_model,
            )
            gc.collect()
        del mal_sample
        gc.collect()
    print("Pipeline complete.")


if __name__ == "__main__":
    main()
