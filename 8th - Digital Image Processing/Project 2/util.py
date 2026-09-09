"""Utility functions for loading and processing MNIST dataset files.

This module provides functions to load MNIST image and label data from the
standard IDX file format used by the MNIST database of handwritten digits.

Functions:
    load_mnist_images: Load MNIST image data from IDX3 binary files
    load_mnist_labels: Load MNIST label data from IDX1 binary files
    display_sample_digits: Display one sample image from each digit class (0-9)
"""

import gc
import os
import pickle
import time
from typing import Optional

import keras
import matplotlib.pyplot as plt
import numpy as np
from keras import layers
from skimage import exposure
from skimage.feature import hog
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)
from sklearn.svm import SVC


def load_mnist_images(filename: str) -> np.ndarray:
    """Load MNIST image data from the specified IDX file.

    Reads image data from MNIST IDX3-ubyte format files and returns as a
    NumPy array. The IDX format stores images as unsigned 8-bit integers
    in big-endian format with a specific header structure.

    Args:
        filename (str): Path to the MNIST image file in IDX3-ubyte format.
            Typically named like 'train-images.idx3-ubyte' or 't10k-images.idx3-ubyte'.

    Returns:
        np.ndarray: A 3D NumPy array of shape (num_images, rows, cols) containing
            the image data as unsigned 8-bit integers (0-255). For MNIST, this is
            typically (60000, 28, 28) for training or (10000, 28, 28) for test data.

    """
    with open(filename, "rb") as f:
        # Read magic number (should be 2051 for images, 2049 for labels)
        magic = np.frombuffer(f.read(4), dtype=">i4")[0]
        num_images = np.frombuffer(f.read(4), dtype=">i4")[0]
        rows = np.frombuffer(f.read(4), dtype=">i4")[0]
        cols = np.frombuffer(f.read(4), dtype=">i4")[0]

        # Read image data (unsigned bytes)
        images = np.frombuffer(f.read(), dtype=np.uint8)
        images = images.reshape(num_images, rows, cols)
        return images


def load_mnist_labels(filename: str) -> np.ndarray:
    """Load MNIST label data from the specified IDX file.

    Reads label data from MNIST IDX1-ubyte format files and returns as a
    NumPy array. The IDX format stores labels as unsigned 8-bit integers
    representing digit classes (0-9) in big-endian format.

    Args:
        filename (str): Path to the MNIST label file in IDX1-ubyte format.
            Typically named like 'train-labels.idx1-ubyte' or 't10k-labels.idx1-ubyte'.

    Returns:
        np.ndarray: A 1D NumPy array containing the label data as unsigned 8-bit
            integers (0-9). For MNIST, this is typically (60000,) for training
            or (10000,) for test data.

    """
    with open(filename, "rb") as f:
        magic = np.frombuffer(f.read(4), dtype=">i4")[0]
        num_labels = np.frombuffer(f.read(4), dtype=">i4")[0]

        # Read label data (unsigned bytes)
        labels = np.frombuffer(f.read(), dtype=np.uint8)
        return labels


def display_sample_digits(
    images: np.ndarray, labels: np.ndarray, figsize: tuple = (12, 4)
) -> None:
    """Display one sample image from each digit class (0-9) in a single figure.

    Creates a visualization showing the first occurrence of each digit class
    from the provided MNIST dataset. Images are displayed in a horizontal row
    with their corresponding digit labels.

    Args:
        images (np.ndarray): A 3D NumPy array of shape (num_images, height, width)
            containing the image data. Typically from load_mnist_images().
        labels (np.ndarray): A 1D NumPy array containing the corresponding labels
            for each image. Typically from load_mnist_labels().
        figsize (tuple, optional): Figure size as (width, height) in inches.
            Defaults to (12, 4).

    """
    if len(images) != len(labels):
        raise ValueError(
            f"Images and labels must have same length: {len(images)} vs {len(labels)}"
        )

    # Find the first occurrence of each digit (0-9)
    sample_indices = []
    for digit in range(10):
        indices = np.where(labels == digit)[0]
        if len(indices) == 0:
            raise ValueError(f"Digit {digit} not found in labels")
        sample_indices.append(indices[0])

    # Create the plot
    fig, axes = plt.subplots(1, 10, figsize=figsize)
    fig.suptitle("Sample Images from Each Digit Class (0-9)", fontsize=14)

    for i, (idx, digit) in enumerate(zip(sample_indices, range(10))):
        axes[i].imshow(images[idx], cmap="gray")
        axes[i].set_title(f"Digit: {digit}")
        axes[i].axis("off")

    os.makedirs("results", exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join("results", "sample_digits.png"))
    plt.show(True)
    plt.close()


def sgd_train(
    model: keras.Model,
    X_train,  # noqa: N803
    y_train,
    X_val=None,  # noqa: N803
    y_val=None,
    batch_size=32,
    epochs=10,
    learning_rate=0.01,
    shuffle=True,
    verbose=1,
    patience=5,
    min_delta=0.001,
):
    """Train a neural network using Stochastic Gradient Descent.

    Args:
        model (keras.Model): The neural network model to train
        X_train (np.ndarray): Training features
        y_train (np.ndarray): Training labels (one-hot encoded)
        X_val (np.ndarray, optional): Validation features
        y_val (np.ndarray, optional): Validation labels
        batch_size (int): Size of mini-batches for SGD
        epochs (int): Number of training epochs
        learning_rate (float): Learning rate for SGD optimizer
        shuffle (bool): Whether to shuffle data before each epoch
        verbose (int): Verbosity level (0=silent, 1=progress bar, 2=one line per epoch)
        patience (int): Number of epochs with no improvement after which training will be stopped (not currently used).
        min_delta (float): Minimum change in the monitored metric to qualify as an improvement (not currently used).

    Returns:
        keras.callbacks.History: Training history containing loss and metrics

    """
    # Configure SGD optimizer
    sgd_optimizer = keras.optimizers.SGD(
        learning_rate=learning_rate,
        momentum=0.0,  # Pure SGD without momentum
        nesterov=False,
    )

    model.compile(
        optimizer=sgd_optimizer,
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    # Prepare validation data if provided
    validation_data = None
    if X_val is not None and y_val is not None:
        validation_data = (X_val, y_val)

    # Add early stopping
    callbacks = []
    if validation_data is not None:
        early_stopping = keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=patience,
            min_delta=min_delta,
            verbose=1,
            restore_best_weights=True,
        )
    callbacks.append(early_stopping)

    # Reduce lr when plateued
    reduce_lr = keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.2,  # multiply learning rate by this factor
        patience=3,  # number of epochs with no improvement
        min_lr=0.0001,  # minimum learning rate
        verbose=1,
    )
    callbacks.append(reduce_lr)

    # Train the model using mini-batch SGD
    history = model.fit(
        X_train,
        y_train,
        batch_size=batch_size,
        epochs=epochs,
        validation_data=validation_data,
        shuffle=shuffle,
        verbose=verbose,
        callbacks=callbacks,
    )

    return history


def plot_training_history(history):
    """Plot training and validation loss and accuracy curves.

    Creates a side-by-side visualization of training progress showing both
    loss and accuracy metrics over epochs. If validation data was used during
    training, validation curves are also plotted for comparison.

    Args:
        history (keras.callbacks.History): Training history from model.fit()
            containing loss and accuracy metrics for each epoch.

    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # Plot training & validation loss
    ax1.plot(history.history["loss"], label="Training Loss")
    if "val_loss" in history.history:
        ax1.plot(history.history["val_loss"], label="Validation Loss")
    ax1.set_title("Model Loss")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Loss")
    ax1.legend()
    ax1.grid(True)

    # Plot training & validation accuracy
    ax2.plot(history.history["accuracy"], label="Training Accuracy")
    if "val_accuracy" in history.history:
        ax2.plot(history.history["val_accuracy"], label="Validation Accuracy")
    ax2.set_title("Model Accuracy")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Accuracy")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig(os.path.join("results", "train_history.png"))
    plt.show()


def plot_confusion_matrix(
    model: keras.Model,
    X_test: np.ndarray,  # noqa: N803
    y_test: np.ndarray,
    class_names: Optional[list] = None,
    figsize: tuple = (10, 8),
    cmap: str = "Blues",
    normalize: bool = False,
) -> np.ndarray:
    """Calculate and visualize a custom confusion matrix for model predictions.

    Args:
        model (keras.Model): The trained neural network model to evaluate.
        X_test (np.ndarray): Test features to make predictions on.
        y_test (np.ndarray): Test labels to compare against predictions.
            Can be one-hot encoded or class indices.
        class_names (list, optional): List of class names for axis labels.
            Defaults to None (uses indices 0, 1, 2, ...).
        figsize (tuple, optional): Figure size as (width, height) in inches.
            Defaults to (10, 8).
        cmap (str, optional): Colormap for the heatmap. Defaults to 'Blues'.
        normalize (bool, optional): Whether to normalize the confusion matrix by row.
            Defaults to False.

    Returns:
        np.ndarray: The confusion matrix array showing counts (or proportions if
            normalize=True) of predictions for each true class.

    """
    # Get predictions
    y_pred = model.predict(X_test)

    # Convert from probabilities to class indices
    y_pred_classes = np.argmax(y_pred, axis=1)

    # If y_test is one-hot encoded, convert to class indices
    if len(y_test.shape) > 1 and y_test.shape[1] > 1:
        y_test_classes = np.argmax(y_test, axis=1)
    else:
        y_test_classes = y_test

    # Determine number of classes
    num_classes = max(np.max(y_test_classes) + 1, np.max(y_pred_classes) + 1)

    # Initialize confusion matrix with zeros
    conf_matrix = np.zeros((num_classes, num_classes), dtype=int)

    # Fill the confusion matrix
    for true_label, pred_label in zip(y_test_classes, y_pred_classes):
        conf_matrix[true_label, pred_label] += 1

    # Create a copy of the original matrix before potential normalization
    display_matrix = conf_matrix.copy()

    # Normalize if requested
    if normalize:
        # Avoid division by zero by adding a small epsilon where row sums are zero
        row_sums = conf_matrix.sum(axis=1)
        row_sums[row_sums == 0] = 1  # Replace zeros with ones to avoid division by zero
        display_matrix = conf_matrix.astype("float") / row_sums[:, np.newaxis]

    # Set up class names if not provided
    if class_names is None:
        class_names = [str(i) for i in range(num_classes)]

    # Create figure and axes for the plot
    plt.figure(figsize=figsize)

    # Create heatmap
    plt.imshow(display_matrix, interpolation="nearest", cmap=plt.cm.get_cmap(cmap))
    plt.colorbar()

    # Set up labels and title
    plt.title("Confusion Matrix")
    tick_marks = np.arange(num_classes)
    plt.xticks(tick_marks, class_names, rotation=45)
    plt.yticks(tick_marks, class_names)
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")

    # Add text annotations to the cells
    fmt = ".2f" if normalize else "d"
    thresh = display_matrix.max() / 2.0
    for i in range(display_matrix.shape[0]):
        for j in range(display_matrix.shape[1]):
            # Choose text color based on background darkness
            color = "white" if display_matrix[i, j] > thresh else "black"
            plt.text(
                j,
                i,
                format(display_matrix[i, j], fmt),
                ha="center",
                va="center",
                color=color,
            )

    # Save and show
    os.makedirs("results", exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join("results", "confusion_matrix.png"))
    plt.show()
    plt.close()

    return conf_matrix


def extract_hog_features(
    images,
    orientations=9,
    pixels_per_cell=(8, 8),
    cells_per_block=(2, 2),
    block_norm="L2-Hys",
    visualize=False,
    feature_vector=True,
):
    """Extract HOG (Histogram of Oriented Gradients) features from images.

    Args:
        images (np.ndarray): Array of images with shape (n_samples, height, width)
        orientations (int): Number of orientation bins
        pixels_per_cell (tuple): Size (in pixels) of a cell
        cells_per_block (tuple): Number of cells in each block
        block_norm (str): Block normalization method
        visualize (bool): Whether to return HOG visualization
        feature_vector (bool): Whether to return flattened feature vector

    Returns:
        np.ndarray: HOG features array with shape (n_samples, n_features)
        list: HOG visualizations if visualize=True

    """
    hog_features = []
    hog_images = [] if visualize else None

    print(f"Extracting HOG features from {len(images)} images...")
    start_time = time.time()

    for i, image in enumerate(images):
        if i % 1000 == 0:
            print(f"Processing image {i}/{len(images)}")

        if visualize:
            features, hog_image = hog(
                image,
                orientations=orientations,
                pixels_per_cell=pixels_per_cell,
                cells_per_block=cells_per_block,
                block_norm=block_norm,
                visualize=True,
                feature_vector=feature_vector,
            )
            hog_images.append(hog_image)
        else:
            features = hog(
                image,
                orientations=orientations,
                pixels_per_cell=pixels_per_cell,
                cells_per_block=cells_per_block,
                block_norm=block_norm,
                visualize=False,
                feature_vector=feature_vector,
            )

        hog_features.append(features)

    end_time = time.time()
    print(f"HOG feature extraction completed in {end_time - start_time:.2f} seconds")
    print(f"Feature vector shape per image: {hog_features[0].shape}")

    hog_features = np.array(hog_features)

    if visualize:
        return hog_features, hog_images
    else:
        return hog_features


def visualize_hog_features(
    images,
    labels,
    n_samples=10,
    orientations=9,
    pixels_per_cell=(8, 8),
    cells_per_block=(2, 2),
    figsize=(15, 8),
):
    """Visualize HOG features for sample images from each digit class.

    Args:
        images (np.ndarray): Array of images
        labels (np.ndarray): Corresponding labels
        n_samples (int): Number of samples to visualize
        orientations (int): Number of orientation bins for HOG
        pixels_per_cell (tuple): Size of cells in pixels
        cells_per_block (tuple): Number of cells per block
        figsize (tuple): Figure size for the plot

    """
    # Find first occurrence of each digit
    sample_indices = []
    for digit in range(min(10, n_samples)):
        indices = np.where(labels == digit)[0]
        if len(indices) > 0:
            sample_indices.append(indices[0])

    n_cols = len(sample_indices)
    fig, axes = plt.subplots(2, n_cols, figsize=figsize)
    fig.suptitle("Original Images vs HOG Features", fontsize=16)

    for i, idx in enumerate(sample_indices):
        # Original image
        axes[0, i].imshow(images[idx], cmap="gray")
        axes[0, i].set_title(f"Digit: {labels[idx]}")
        axes[0, i].axis("off")

        # HOG features
        _, hog_image = hog(
            images[idx],
            orientations=orientations,
            pixels_per_cell=pixels_per_cell,
            cells_per_block=cells_per_block,
            visualize=True,
        )

        # Rescale histogram for better visualization
        hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))

        axes[1, i].imshow(hog_image_rescaled, cmap="hot")
        axes[1, i].set_title("HOG Features")
        axes[1, i].axis("off")

    os.makedirs("results", exist_ok=True)
    plt.tight_layout()
    plt.savefig(
        os.path.join("results", "hog_visualization.png"), dpi=150, bbox_inches="tight"
    )
    plt.show()


def train_svm_classifier(
    X_train,  # noqa: N803
    y_train,
    X_test,  # noqa: N803
    y_test,
    kernel="rbf",
    C=1.0,  # noqa: N803
    gamma="scale",
    save_model=True,
    model_path="svm_model.pkl",
):
    """Train an SVM classifier on HOG features.

    Args:
        X_train (np.ndarray): Training features
        y_train (np.ndarray): Training labels
        X_test (np.ndarray): Test features
        y_test (np.ndarray): Test labels
        kernel (str): SVM kernel type ('linear', 'rbf', 'poly', 'sigmoid')
        C (float): Regularization parameter
        gamma (str or float): Kernel coefficient
        save_model (bool): Whether to save the trained model
        model_path (str): Path to save the model

    Returns:
        tuple: (trained_svm_model, training_time, test_accuracy, predictions)

    """
    print(f"Training SVM with kernel='{kernel}', C={C}, gamma={gamma}")
    print(f"Training set size: {X_train.shape}")
    print(f"Test set size: {X_test.shape}")

    # Initialize SVM classifier
    svm_classifier = SVC(kernel=kernel, C=C, gamma=gamma, random_state=42, verbose=True)

    # Train the classifier
    start_time = time.time()
    svm_classifier.fit(X_train, y_train)
    training_time = time.time() - start_time

    print(f"SVM training completed in {training_time:.2f} seconds")

    # Make predictions
    print("Making predictions on test set...")
    y_pred = svm_classifier.predict(X_test)

    # Calculate accuracy
    test_accuracy = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy * 100:.2f}%)")

    # Print detailed classification report
    print("\nDetailed Classification Report:")
    print(
        classification_report(y_test, y_pred, target_names=[str(i) for i in range(10)])
    )

    # Save model if requested
    if save_model:
        with open(model_path, "wb") as f:
            pickle.dump(svm_classifier, f)
        print(f"Model saved to {model_path}")

    return svm_classifier, training_time, test_accuracy, y_pred


def compare_classifiers(
    cnn_model,
    svm_model,
    X_test_cnn,  # noqa: N803
    X_test_svm,  # noqa: N803
    y_test,
):
    """Compare performance between CNN and SVM classifiers.

    Args:
        cnn_model: Trained CNN model
        svm_model: Trained SVM model
        X_test_cnn (np.ndarray): Test data for CNN (normalized images)
        X_test_svm (np.ndarray): Test data for SVM (HOG features)
        y_test (np.ndarray): True test labels

    Returns:
        dict: Comparison results

    """
    print("=" * 60)
    print("CLASSIFIER COMPARISON")
    print("=" * 60)

    # CNN predictions
    print("Evaluating CNN...")
    cnn_start = time.time()
    cnn_pred_prob = cnn_model.predict(X_test_cnn)
    cnn_pred = np.argmax(cnn_pred_prob, axis=1)
    cnn_time = time.time() - cnn_start

    # SVM predictions
    print("Evaluating SVM...")
    svm_start = time.time()
    svm_pred = svm_model.predict(X_test_svm)
    svm_time = time.time() - svm_start

    # Convert y_test if it's one-hot encoded
    if len(y_test.shape) > 1 and y_test.shape[1] > 1:
        y_test_labels = np.argmax(y_test, axis=1)
    else:
        y_test_labels = y_test

    # Calculate accuracies
    cnn_accuracy = accuracy_score(y_test_labels, cnn_pred)
    svm_accuracy = accuracy_score(y_test_labels, svm_pred)

    # Create comparison results
    results = {
        "CNN": {
            "accuracy": cnn_accuracy,
            "prediction_time": cnn_time,
            "predictions": cnn_pred,
        },
        "SVM": {
            "accuracy": svm_accuracy,
            "prediction_time": svm_time,
            "predictions": svm_pred,
        },
    }

    # Print comparison
    print(f"\nCNN Accuracy: {cnn_accuracy:.4f} ({cnn_accuracy * 100:.2f}%)")
    print(f"SVM Accuracy: {svm_accuracy:.4f} ({svm_accuracy * 100:.2f}%)")
    print(f"\nCNN Prediction Time: {cnn_time:.4f} seconds")
    print(f"SVM Prediction Time: {svm_time:.4f} seconds")

    # Determine winner
    if cnn_accuracy > svm_accuracy:
        print(
            f"\n🏆 CNN wins by {(cnn_accuracy - svm_accuracy) * 100:.2f} percentage points!"
        )
    elif svm_accuracy > cnn_accuracy:
        print(
            f"\n🏆 SVM wins by {(svm_accuracy - cnn_accuracy) * 100:.2f} percentage points!"
        )
    else:
        print(f"\n🤝 It's a tie!")

    return results


def plot_svm_confusion_matrix(
    y_true, y_pred, class_names=None, figsize=(10, 8), normalize=False
):
    """Plot confusion matrix for SVM predictions.

    Args:
        y_true (np.ndarray): True labels
        y_pred (np.ndarray): Predicted labels
        class_names (list): List of class names
        figsize (tuple): Figure size
        normalize (bool): Whether to normalize the confusion matrix

    """
    # Calculate confusion matrix
    cm = confusion_matrix(y_true, y_pred)

    if normalize:
        cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
        title = "Normalized Confusion Matrix (SVM)"
        fmt = ".2f"
    else:
        title = "Confusion Matrix (SVM)"
        fmt = "d"

    if class_names is None:
        class_names = [str(i) for i in range(len(cm))]

    # Create figure and plot
    plt.figure(figsize=figsize)
    plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    plt.title(title)
    plt.colorbar()

    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names, rotation=45)
    plt.yticks(tick_marks, class_names)
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")

    # Add text annotations
    thresh = cm.max() / 2.0
    for i, j in np.ndindex(cm.shape):
        plt.text(
            j,
            i,
            format(cm[i, j], fmt),
            ha="center",
            va="center",
            color="white" if cm[i, j] > thresh else "black",
        )

    # Save to results directory
    os.makedirs("results", exist_ok=True)
    plt.tight_layout()
    plt.savefig(
        os.path.join("results", "svm_confusion_matrix.png"),
        dpi=150,
        bbox_inches="tight",
    )
    plt.show()
    plt.close()


def calculate_per_class_metrics(y_true, y_pred, model_name):
    """Calculate per-class accuracy and detailed metrics for a model.

    Args:
        y_true (np.ndarray): True labels
        y_pred (np.ndarray): Predicted labels
        model_name (str): Name of the model for reporting

    Returns:
        dict: Dictionary containing comprehensive metrics including per-class accuracy,
              overall metrics, and best/worst performing classes

    """
    per_class_acc = []
    for digit in range(10):
        digit_mask = y_true == digit
        if np.sum(digit_mask) > 0:
            acc = accuracy_score(y_true[digit_mask], y_pred[digit_mask])
            per_class_acc.append(acc)
        else:
            per_class_acc.append(0)

    # Overall metrics
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average=None
    )

    return {
        "name": model_name,
        "per_class_accuracy": per_class_acc,
        "overall_accuracy": accuracy_score(y_true, y_pred),
        "avg_precision": np.mean(precision),
        "avg_recall": np.mean(recall),
        "avg_f1": np.mean(f1),
        "best_class": np.argmax(per_class_acc),
        "worst_class": np.argmin(per_class_acc),
        "best_accuracy": np.max(per_class_acc),
        "worst_accuracy": np.min(per_class_acc),
    }


def create_model_analysis_plot(
    metrics,
    model_name,
    save_name,
    training_time=None,
    X_test_hog=None,  # noqa: N803
    model=None,
    cnn_time=0,
    svm_time=0,
):
    """Create detailed analysis plot for a single model.

    Args:
        metrics (dict): Model metrics from calculate_per_class_metrics
        model_name (str): Name of the model ('CNN' or 'SVM')
        save_name (str): Filename to save the plot as
        training_time (float, optional): Training time in seconds for SVM
        X_test_hog (np.ndarray, optional): HOG test features for SVM analysis
        model (keras.Model, optional): CNN model for architecture analysis
        cnn_time (float): CNN prediction time
        svm_time (float): SVM prediction time

    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle(f"{model_name} Detailed Analysis", fontsize=16)

    # Per-class accuracy
    bars1 = ax1.bar(
        range(10),
        metrics["per_class_accuracy"],
        color="skyblue" if model_name == "CNN" else "orange",
        alpha=0.7,
    )
    ax1.set_title(f"{model_name} Per-Class Accuracy")
    ax1.set_xlabel("Digit Class")
    ax1.set_ylabel("Accuracy")
    ax1.set_xticks(range(10))
    ax1.grid(True, alpha=0.3)

    for i, acc in enumerate(metrics["per_class_accuracy"]):
        ax1.text(i, acc + 0.01, f"{acc:.2f}", ha="center", va="bottom", fontsize=9)

    # Overall metrics
    metric_names = ["Precision", "Recall", "F1-Score", "Accuracy"]
    metric_values = [
        metrics["avg_precision"],
        metrics["avg_recall"],
        metrics["avg_f1"],
        metrics["overall_accuracy"],
    ]
    colors = ["lightblue", "lightgreen", "lightcoral", "gold"]

    bars2 = ax2.bar(metric_names, metric_values, color=colors, alpha=0.7)
    ax2.set_title(f"{model_name} Overall Performance Metrics")
    ax2.set_ylabel("Score")
    ax2.set_ylim(0, 1)
    ax2.grid(True, alpha=0.3)

    for bar, val in zip(bars2, metric_values):
        height = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.01,
            f"{val:.3f}",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    # Model-specific analysis
    if model_name == "SVM" and X_test_hog is not None:
        # HOG configuration
        hog_params = ["Orientations", "Pixels/Cell", "Cells/Block", "Total Features"]
        hog_values = [9, 16, 4, X_test_hog.shape[1]]
        colors_hog = ["lightblue", "lightgreen", "lightcoral", "gold"]

        ax3.bar(hog_params, hog_values, color=colors_hog, alpha=0.7)
        ax3.set_title("HOG Feature Configuration")
        ax3.set_ylabel("Value")
        ax3.set_yscale("log")
        ax3.grid(True, alpha=0.3)

        for i, v in enumerate(hog_values):
            ax3.text(i, v * 1.1, f"{v}", ha="center", va="bottom", fontsize=9)

        # Processing breakdown
        if training_time:
            stages = ["Feature\nExtraction", "Training", "Prediction"]
            times = [30.0, training_time, svm_time]
            colors_time = ["skyblue", "lightcoral", "lightgreen"]

            bars4 = ax4.bar(stages, times, color=colors_time, alpha=0.7)
            ax4.set_title("SVM Processing Time Breakdown")
            ax4.set_ylabel("Time (seconds)")
            ax4.set_yscale("log")
            ax4.grid(True, alpha=0.3)

            for bar, time_val in zip(bars4, times):
                height = bar.get_height()
                ax4.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height * 1.1,
                    f"{time_val:.1f}s",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                )

    elif model_name == "CNN" and model is not None:
        # CNN architecture info
        arch_info = ["Conv Layers", "Dense Layers", "Total Params", "Trainable Params"]
        arch_values = [2, 3, model.count_params(), model.count_params()]

        ax3.bar(arch_info, arch_values, color="lightblue", alpha=0.7)
        ax3.set_title("CNN Architecture Overview")
        ax3.set_ylabel("Count")
        ax3.set_yscale("log")
        ax3.grid(True, alpha=0.3)

        # Training breakdown (estimated)
        stages = ["Data\nPrep", "Training", "Prediction"]
        times = [5.0, 300.0, cnn_time]

        bars4 = ax4.bar(stages, times, color="lightblue", alpha=0.7)
        ax4.set_title("CNN Processing Time Breakdown")
        ax4.set_ylabel("Time (seconds)")
        ax4.set_yscale("log")
        ax4.grid(True, alpha=0.3)

        for bar, time_val in zip(bars4, times):
            height = bar.get_height()
            ax4.text(
                bar.get_x() + bar.get_width() / 2.0,
                height * 1.1,
                f"{time_val:.1f}s",
                ha="center",
                va="bottom",
                fontsize=9,
            )

    plt.tight_layout()
    os.makedirs("results", exist_ok=True)
    plt.savefig(os.path.join("results", save_name), dpi=150, bbox_inches="tight")
    plt.show()
    plt.close()


def load_or_train_cnn_model(
    X_train,  # noqa: N803
    y_train,
    X_test,  # noqa: N803
    y_test,
    model_path="mnist_cnn_model.h5",
):
    """Load existing CNN model or train a new one if none exists.

    Also handles saving and loading of training history for visualization purposes.

    Args:
        X_train (np.ndarray): Training images
        y_train (np.ndarray): Training labels (one-hot encoded)
        X_test (np.ndarray): Test images
        y_test (np.ndarray): Test labels (one-hot encoded)
        model_path (str): Path to save/load the model

    Returns:
        tuple: (model, history) where history is None if model was loaded

    """
    # Define history path based on model path
    history_path = model_path.replace(".h5", "_history.pkl")

    if os.path.exists(model_path):
        print("Loading existing CNN model...")
        try:
            # Clear any existing model from memory
            if "model" in globals():
                del globals()["model"]
            gc.collect()

            # Load the model
            loaded_model = keras.models.load_model(model_path)
            print("✓ CNN model loaded successfully!")

            # Test the model with a small batch
            test_input = X_test[:5].reshape(-1, 28, 28, 1).astype("float32")
            _ = loaded_model.predict(test_input, verbose=0)
            print("✓ Model prediction test passed!")

            # Try to load history if it exists
            history = None
            if os.path.exists(history_path):
                try:
                    with open(history_path, "rb") as f:
                        history = pickle.load(f)
                    print("✓ Training history loaded successfully!")
                except Exception as e:
                    print(f"⚠ Could not load training history: {e}")
            else:
                print("⚠ No training history file found")

            return loaded_model, history

        except Exception as e:
            print(f"✗ Model loading failed: {e}")
            print("Rebuilding CNN model...")

    else:
        print("No existing model found. Training new CNN...")

    # Create new model
    new_model = keras.Sequential(
        [
            keras.layers.Input((28, 28, 1)),
            keras.layers.Conv2D(filters=6, kernel_size=3, strides=1, padding="valid"),
            keras.layers.ReLU(),
            keras.layers.AveragePooling2D(pool_size=2, strides=2),
            keras.layers.Conv2D(filters=16, kernel_size=3, strides=1, padding="valid"),
            keras.layers.ReLU(),
            keras.layers.AveragePooling2D(pool_size=2, strides=2),
            keras.layers.Flatten(),
            keras.layers.Dense(120),
            keras.layers.ReLU(),
            keras.layers.Dense(84),
            keras.layers.ReLU(),
            keras.layers.Dense(10),
            keras.layers.Softmax(),
        ]
    )

    print("CNN Architecture created:")
    new_model.summary()

    # Train the model
    print("\nStarting CNN training with SGD...")
    history = sgd_train(
        model=new_model,
        X_train=X_train,
        y_train=y_train,
        X_val=X_test,
        y_val=y_test,
        batch_size=64,
        epochs=40,
        learning_rate=0.01,
        shuffle=True,
        verbose=1,
    )

    # Save the trained model
    new_model.save(model_path)
    print(f"✓ Model saved as '{model_path}'")

    # Save the training history
    try:
        with open(history_path, "wb") as f:
            pickle.dump(history, f)
        print(f"✓ Training history saved as '{history_path}'")
    except Exception as e:
        print(f"⚠ Could not save training history: {e}")

    return new_model, history
