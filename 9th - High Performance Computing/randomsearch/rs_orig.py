import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# -----------------------------
# 1. Big, sparse-signal problem
# -----------------------------
# Key: HUGE dimensionality, tiny number of informative features,
# no label noise, reasonable class separation.
X, y = make_classification(
    n_samples=100000,       # big-ish, still manageable
    n_features=200,       # many features -> overfitting risk
    n_informative=10,      # tiny true signal
    n_redundant=10,
    n_repeated=0,
    n_classes=2,
    n_clusters_per_class=2,
    class_sep=1.2,         # fairly separable if you keep the right features
    flip_y=0.08,            # no label noise, so best C can get very high acc
    weights=[0.5, 0.5],
    random_state=42,
)

X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Scale features for better convergence and to make C more meaningful
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)

# -----------------------------
# 2. Single-parameter HPO on C
#    (log-uniform random search)
# -----------------------------
rng = np.random.default_rng(0)
n_trials = 32
results = []

# Cs = np.logspace(-5, -1, 32)  # 1e-4 ... 1e-1
# for i, C in enumerate(Cs):

for i in range(n_trials):
    # log-uniform C in [1e-5, 1e+2]
    C = 10 ** rng.uniform(-5, -1)

    clf = LogisticRegression(
        C=C,
        penalty="l1",
        solver="saga",      # supports L1 on large, high-dim problems
        max_iter=3000,
        n_jobs=1,
    )

    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_val)
    acc = accuracy_score(y_val, y_pred)

    print(f"{i:02d}: C={C:.3e}, acc={acc:.4f}")
    results.append((C, acc))

# -----------------------------
# 3. Best C
# -----------------------------
best_C, best_acc = max(results, key=lambda t: t[1])
print("\nBest result:")
print(f"C={best_C:.3e}, acc={best_acc:.4f}")
