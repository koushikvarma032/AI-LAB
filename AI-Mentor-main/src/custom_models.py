"""
Custom Implementations of Machine Learning Models:
1. k-Nearest Neighbors (k-NN)
2. Decision Tree Classifier (Gini Impurity)
3. Gaussian Naive Bayes Classifier
4. Perceptron Classifier
"""

import numpy as np

# =====================================================================
# 1. k-Nearest Neighbors Classifier
# =====================================================================
class KNNClassifier:
    def __init__(self, k=5, distance_metric='euclidean'):
        self.k = k
        self.distance_metric = distance_metric
        self.X_train = None
        self.y_train = None

    def fit(self, X, y):
        self.X_train = np.array(X, dtype=float)
        self.y_train = np.array(y, dtype=int)
        return self

    def _compute_distance(self, x1, x2):
        if self.distance_metric == 'euclidean':
            return np.sqrt(np.sum((x1 - x2) ** 2, axis=-1))
        elif self.distance_metric == 'manhattan':
            return np.sum(np.abs(x1 - x2), axis=-1)
        else:
            raise ValueError(f"Unsupported distance metric: {self.distance_metric}")

    def predict_single(self, x):
        distances = self._compute_distance(self.X_train, x)
        k_indices = np.argsort(distances)[:self.k]
        k_nearest_labels = self.y_train[k_indices]
        
        # Majority voting
        values, counts = np.unique(k_nearest_labels, return_counts=True)
        return values[np.argmax(counts)]

    def predict(self, X):
        X = np.array(X, dtype=float)
        return np.array([self.predict_single(x) for x in X])


# =====================================================================
# 2. Decision Tree Classifier
# =====================================================================
class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature          # Index of feature to split on
        self.threshold = threshold      # Threshold value for split
        self.left = left                # Left subtree
        self.right = right              # Right subtree
        self.value = value              # Leaf node prediction class

    @property
    def is_leaf(self):
        return self.value is not None


class DecisionTreeClassifier:
    def __init__(self, max_depth=5, min_samples_split=4):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root = None

    def _gini(self, y):
        if len(y) == 0:
            return 0
        p = np.bincount(y) / len(y)
        return 1.0 - np.sum(p ** 2)

    def _best_split(self, X, y):
        best_gain = -1
        split_feat, split_thresh = None, None
        current_impurity = self._gini(y)
        n_samples, n_features = X.shape

        for feat_idx in range(n_features):
            X_column = X[:, feat_idx]
            thresholds = np.unique(X_column)
            for thresh in thresholds:
                left_mask = X_column <= thresh
                right_mask = ~left_mask

                if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
                    continue

                left_gini = self._gini(y[left_mask])
                right_gini = self._gini(y[right_mask])
                weighted_gini = (np.sum(left_mask) / n_samples) * left_gini + \
                                (np.sum(right_mask) / n_samples) * right_gini

                gain = current_impurity - weighted_gini
                if gain > best_gain:
                    best_gain = gain
                    split_feat = feat_idx
                    split_thresh = thresh

        return split_feat, split_thresh

    def _build_tree(self, X, y, depth=0):
        n_samples = len(y)
        n_labels = len(np.unique(y))

        # Stopping criteria
        if depth >= self.max_depth or n_labels <= 1 or n_samples < self.min_samples_split:
            leaf_val = np.bincount(y).argmax() if n_samples > 0 else 0
            return Node(value=leaf_val)

        feat_idx, thresh = self._best_split(X, y)
        if feat_idx is None:
            leaf_val = np.bincount(y).argmax()
            return Node(value=leaf_val)

        left_mask = X[:, feat_idx] <= thresh
        right_mask = ~left_mask

        left_child = self._build_tree(X[left_mask], y[left_mask], depth + 1)
        right_child = self._build_tree(X[right_mask], y[right_mask], depth + 1)

        return Node(feature=feat_idx, threshold=thresh, left=left_child, right=right_child)

    def fit(self, X, y):
        X = np.array(X, dtype=float)
        y = np.array(y, dtype=int)
        self.root = self._build_tree(X, y)
        return self

    def _traverse(self, x, node):
        if node.is_leaf:
            return node.value
        if x[node.feature] <= node.threshold:
            return self._traverse(x, node.left)
        return self._traverse(x, node.right)

    def predict(self, X):
        X = np.array(X, dtype=float)
        return np.array([self._traverse(x, self.root) for x in X])


# =====================================================================
# 3. Gaussian Naive Bayes Classifier
# =====================================================================
class GaussianNaiveBayesClassifier:
    def __init__(self, var_smoothing=1e-9):
        self.var_smoothing = var_smoothing
        self.classes = None
        self.mean = {}
        self.var = {}
        self.priors = {}

    def fit(self, X, y):
        X = np.array(X, dtype=float)
        y = np.array(y, dtype=int)
        self.classes = np.unique(y)
        n_samples = len(y)

        for c in self.classes:
            X_c = X[y == c]
            self.mean[c] = np.mean(X_c, axis=0)
            self.var[c] = np.var(X_c, axis=0) + self.var_smoothing
            self.priors[c] = len(X_c) / n_samples
        return self

    def _pdf(self, class_idx, x):
        mean = self.mean[class_idx]
        var = self.var[class_idx]
        numerator = np.exp(-((x - mean) ** 2) / (2 * var))
        denominator = np.sqrt(2 * np.pi * var)
        return numerator / denominator

    def predict_single(self, x):
        posteriors = []
        for c in self.classes:
            prior = np.log(self.priors[c])
            pdf = self._pdf(c, x)
            # Clip PDF to avoid log(0)
            pdf = np.clip(pdf, 1e-12, None)
            conditional = np.sum(np.log(pdf))
            posteriors.append(prior + conditional)
        return self.classes[np.argmax(posteriors)]

    def predict(self, X):
        X = np.array(X, dtype=float)
        return np.array([self.predict_single(x) for x in X])


# =====================================================================
# 4. Perceptron Classifier
# =====================================================================
class PerceptronClassifier:
    def __init__(self, learning_rate=0.01, n_epochs=100, random_state=42):
        self.lr = learning_rate
        self.n_epochs = n_epochs
        self.random_state = random_state
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        X = np.array(X, dtype=float)
        y = np.array(y, dtype=int)
        
        # Map labels {0, 1} to {-1, +1} for Perceptron rule
        y_binary = np.where(y <= 0, -1, 1)

        rng = np.random.RandomState(self.random_state)
        n_features = X.shape[1]
        self.weights = rng.normal(loc=0.0, scale=0.01, size=n_features)
        self.bias = 0.0

        for _ in range(self.n_epochs):
            for xi, target in zip(X, y_binary):
                linear_output = np.dot(xi, self.weights) + self.bias
                y_pred = 1 if linear_output >= 0.0 else -1
                
                # Weight update rule
                update = self.lr * (target - y_pred)
                self.weights += update * xi
                self.bias += update
        return self

    def predict(self, X):
        X = np.array(X, dtype=float)
        linear_output = np.dot(X, self.weights) + self.bias
        # Map back {-1, 1} to {0, 1}
        return np.where(linear_output >= 0.0, 1, 0)
