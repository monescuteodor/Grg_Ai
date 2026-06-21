# Machine Learning Basics Complete Reference


---

# CHAPTER 1: FUNDAMENTALS


## Remarks

Machine Learning (ML) is a subfield of artificial intelligence where systems learn patterns from data instead of being explicitly programmed. Instead of writing rules ("if temperature > 30 AND humidity > 80 → rain"), ML learns rules FROM data (thousands of weather measurements + outcomes → predicts rain). Deep Learning is ML using neural networks with many layers.

Key concepts: **Supervised Learning** (labeled data → predict labels), **Unsupervised Learning** (find patterns in unlabeled data), **Reinforcement Learning** (learn by trial and reward), **Features** (input variables), **Labels** (output to predict), **Training** (fitting model to data), **Inference** (using trained model), **Overfitting** (memorizing training data, fails on new data).

Used by: every tech company. Recommendations (Netflix, YouTube), search (Google), translation (DeepL), self-driving (Tesla), medical imaging, fraud detection, ChatGPT/Claude.

Tools: **Python** (language of ML), **NumPy** (arrays), **Pandas** (data), **Scikit-learn** (classical ML), **PyTorch** (deep learning, research), **TensorFlow/Keras** (deep learning, production), **Jupyter** (notebooks), **Hugging Face** (pretrained models).


## Types of Machine Learning

```
SUPERVISED LEARNING:
  Input: labeled dataset (features + correct answers)
  Goal: learn mapping features → labels
  
  Types:
    Classification: predict CATEGORY
      - Is this email spam or not? (binary)
      - Which digit is this? 0-9 (multiclass)
      - What objects are in this image? (multilabel)
    
    Regression: predict NUMBER
      - What will the house price be?
      - How many sales tomorrow?
      - What temperature at 3pm?

  Examples:
    Features (X)              → Label (y)
    [age, income, debt]       → approve_loan? (yes/no)
    [pixels of image]         → digit (0-9)
    [bedrooms, sqft, location]→ house price ($)

UNSUPERVISED LEARNING:
  Input: unlabeled dataset (features only, no answers)
  Goal: find hidden patterns/structure
  
  Types:
    Clustering: group similar items
      - Customer segments
      - Topic discovery in documents
    
    Dimensionality Reduction: simplify data
      - PCA (compress 100 features → 10)
      - t-SNE (visualize high-D data in 2D)
    
    Anomaly Detection: find outliers
      - Fraud detection
      - Network intrusion

REINFORCEMENT LEARNING:
  Input: environment with actions and rewards
  Goal: learn policy that maximizes total reward
  
  Examples:
    - Game AI (AlphaGo, OpenAI Five)
    - Robot control
    - RLHF for ChatGPT/Claude
  
  Key concepts:
    Agent → takes Action → gets Reward + new State → repeat
    Policy: state → action mapping
    Value function: expected future reward from state
    Q-function: expected reward for action in state

SELF-SUPERVISED LEARNING:
  Creates labels FROM the data itself.
  Example: mask a word in sentence, predict masked word.
  Used by: BERT, GPT, all modern LLMs.
  Technically supervised, but labels are auto-generated.
```


## The ML Pipeline

```
1. PROBLEM DEFINITION
   What are we predicting? How will it be used?
   Classification? Regression? Ranking?
   What metric defines success?

2. DATA COLLECTION
   Where does data come from? (database, APIs, scraping, sensors)
   How much data? (more is usually better)
   Is it representative? (bias in data = bias in model)

3. DATA EXPLORATION (EDA)
   Distributions, correlations, missing values
   Visualizations: histograms, scatter plots, heatmaps
   Outliers, class imbalance

4. DATA PREPROCESSING
   Handle missing values (impute, drop)
   Encode categories (one-hot, label encoding)
   Scale features (normalization, standardization)
   Split: train/validation/test (70/15/15 or 80/10/10)

5. FEATURE ENGINEERING
   Create new features from existing ones
   Domain knowledge helps enormously
   Example: from "date" → day_of_week, is_weekend, month

6. MODEL SELECTION
   Try multiple algorithms
   Start simple (baseline), increase complexity
   Cross-validation to compare fairly

7. TRAINING
   Fit model on training data
   Tune hyperparameters
   Monitor for overfitting

8. EVALUATION
   Test on held-out test set (NEVER used during training)
   Compare metrics: accuracy, precision, recall, F1, AUC
   Error analysis: WHERE does the model fail?

9. DEPLOYMENT
   Serve model via API
   Monitor in production (data drift, performance degradation)
   Retrain periodically with new data

10. MONITORING
    Track prediction quality over time
    Alert on distribution shift
    A/B test model updates
```


---

# CHAPTER 2: CLASSICAL ML ALGORITHMS


## Linear Regression

```python
# Predict continuous value: y = wx + b
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Data
X = np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])
y = np.array([2.1, 4.0, 5.9, 8.1, 10.0, 12.1, 13.9, 16.0, 18.1, 20.0])

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
print(f"Coefficient (slope): {model.coef_[0]:.4f}")
print(f"Intercept: {model.intercept_:.4f}")
print(f"MSE: {mean_squared_error(y_test, y_pred):.4f}")
print(f"R² score: {r2_score(y_test, y_pred):.4f}")   # 1.0 = perfect

# When to use:
#   ✅ Linear relationship between features and target
#   ✅ Interpretability needed (coefficients show feature importance)
#   ✅ Fast training, fast inference
#   ❌ Non-linear relationships (use polynomial or tree-based)
```


## Logistic Regression (Classification)

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Binary classification: spam or not spam
X_train = [...]   # Feature vectors
y_train = [...]   # 0 = not spam, 1 = spam

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)   # Probability scores

print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

# Classification report shows:
#               precision  recall  f1-score  support
# not spam        0.95     0.98     0.96      500
# spam            0.92     0.85     0.88      200
#
# Precision: of all predicted spam, how many actually spam?
# Recall: of all actual spam, how many did we catch?
# F1: harmonic mean of precision and recall
```


## Decision Trees and Random Forests

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

# Decision Tree: learns if/else rules from data
#   if income > 50K AND debt < 10K → approve loan
#   Pros: interpretable, handles non-linear
#   Cons: overfits easily, unstable (small data change → different tree)

tree = DecisionTreeClassifier(max_depth=5)
tree.fit(X_train, y_train)

# Random Forest: ensemble of many trees (bagging)
#   Train N trees on random subsets of data
#   Each tree votes, majority wins
#   Pros: robust, handles overfitting, feature importance
#   Cons: slower, less interpretable, more memory

forest = RandomForestClassifier(
    n_estimators=100,          # Number of trees
    max_depth=10,              # Limit tree depth
    min_samples_split=5,       # Minimum samples to split
    max_features='sqrt',       # Features per split
    random_state=42,
    n_jobs=-1,                 # Use all CPU cores
)
forest.fit(X_train, y_train)

# Feature importance
importances = forest.feature_importances_
for name, importance in zip(feature_names, importances):
    print(f"{name}: {importance:.4f}")

# When to use Random Forest:
#   ✅ Tabular data (spreadsheets, databases)
#   ✅ Classification or regression
#   ✅ Don't want to tune much (works well out of box)
#   ✅ Need feature importance
#   ❌ Images, text, audio (use deep learning)
#   ❌ Very high-dimensional sparse data (use gradient boosting)
```


## Gradient Boosting (XGBoost, LightGBM)

```python
# XGBoost: state-of-the-art for tabular data
# Wins most Kaggle competitions on tabular data
import xgboost as xgb

model = xgb.XGBClassifier(
    n_estimators=500,
    max_depth=6,
    learning_rate=0.1,           # Lower = more robust, slower
    subsample=0.8,               # Row sampling
    colsample_bytree=0.8,        # Column sampling
    min_child_weight=5,
    reg_alpha=0.1,               # L1 regularization
    reg_lambda=1.0,              # L2 regularization
    use_label_encoder=False,
    eval_metric='logloss',
    early_stopping_rounds=50,    # Stop if no improvement
    random_state=42,
)

model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    verbose=False,
)

y_pred = model.predict(X_test)

# LightGBM: faster than XGBoost, similar accuracy
import lightgbm as lgb

model = lgb.LGBMClassifier(
    n_estimators=500,
    max_depth=-1,                # No limit (leaf-wise growth)
    learning_rate=0.1,
    num_leaves=31,
    min_child_samples=20,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
)
model.fit(X_train, y_train)

# When to use Gradient Boosting:
#   ✅ Tabular data (BEST algorithm for structured data)
#   ✅ Kaggle competitions
#   ✅ Large datasets (LightGBM handles millions of rows)
#   ❌ Very small datasets (overfits)
#   ❌ Real-time inference with strict latency (ensemble is slower)
```


## K-Means Clustering (Unsupervised)

```python
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Find natural groups in data (no labels!)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
kmeans.fit(X)

labels = kmeans.labels_             # Cluster assignment for each point
centers = kmeans.cluster_centers_   # Center of each cluster
inertia = kmeans.inertia_          # Sum of squared distances to centers

# Predict cluster for new data
new_cluster = kmeans.predict([[5.0, 3.0]])

# How to choose K (number of clusters)?
# Elbow method: plot inertia for K=1..10, find the "elbow"
inertias = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X)
    inertias.append(km.inertia_)

plt.plot(range(1, 11), inertias, 'bo-')
plt.xlabel('K')
plt.ylabel('Inertia')
plt.title('Elbow Method')
plt.savefig('elbow.png')

# Use cases:
#   Customer segmentation
#   Image color quantization
#   Document clustering
#   Anomaly detection (points far from any center)
```


---

# CHAPTER 3: NEURAL NETWORKS


## How Neural Networks Work

```
NEURON (Perceptron):
  Takes inputs x₁, x₂, ..., xₙ
  Multiplies each by a weight w₁, w₂, ..., wₙ
  Adds bias b
  Applies activation function f
  
  output = f(w₁x₁ + w₂x₂ + ... + wₙxₙ + b)
  output = f(Wx + b)

LAYER:
  Group of neurons processing same input.
  
  Input layer  → receives raw data
  Hidden layers → learn representations
  Output layer → produces predictions

NETWORK:
  input → hidden₁ → hidden₂ → ... → output
  
  Each layer transforms data into more abstract representation.
  Layer 1 might detect edges in images.
  Layer 2 detects shapes.
  Layer 3 detects objects.

ACTIVATION FUNCTIONS:
  ReLU:      f(x) = max(0, x)           Most common for hidden layers
  Sigmoid:   f(x) = 1 / (1 + e^(-x))   Binary classification output
  Softmax:   f(xᵢ) = e^xᵢ / Σe^xⱼ     Multiclass output (probabilities)
  Tanh:      f(x) = (e^x - e^(-x))/(e^x + e^(-x))   Range [-1, 1]
  GELU:      Used in transformers (smooth ReLU)

TRAINING (Backpropagation):
  1. Forward pass: compute output for given input
  2. Loss: compare output to correct answer (how wrong?)
  3. Backward pass: compute gradient of loss w.r.t. each weight
  4. Update: adjust weights in direction that reduces loss
  5. Repeat for thousands of iterations (epochs)

LOSS FUNCTIONS:
  MSE (Mean Squared Error):    regression
  Cross-Entropy:               classification
  Binary Cross-Entropy:        binary classification

OPTIMIZER (how to update weights):
  SGD:     Simple, slow convergence
  Adam:    Adaptive learning rate, most popular default
  AdamW:   Adam with weight decay (better regularization)
```


## PyTorch Basics

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# Check device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Tensors (like NumPy arrays but with GPU support + autograd)
x = torch.tensor([1.0, 2.0, 3.0])
y = torch.zeros(3, 4)                # 3x4 matrix of zeros
z = torch.randn(3, 4)                # Random normal
w = torch.ones(3, 4, requires_grad=True)   # Track gradients

# Operations
a = x + y[0]
b = torch.matmul(z, w.T)             # Matrix multiplication
c = x.reshape(1, 3)                   # Reshape

# Move to GPU
x_gpu = x.to(device)


# Define a neural network
class SimpleNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
        self.layer2 = nn.Linear(hidden_size, hidden_size)
        self.layer3 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        x = self.layer1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.layer2(x)
        x = self.relu(x)
        x = self.layer3(x)
        return x

# Instantiate
model = SimpleNet(input_size=784, hidden_size=256, num_classes=10)
model = model.to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 10

for epoch in range(num_epochs):
    model.train()                      # Training mode (dropout active)
    total_loss = 0

    for batch_X, batch_y in train_loader:
        batch_X, batch_y = batch_X.to(device), batch_y.to(device)

        # Forward pass
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)

        # Backward pass
        optimizer.zero_grad()          # Clear previous gradients
        loss.backward()                # Compute gradients
        optimizer.step()               # Update weights

        total_loss += loss.item()

    avg_loss = total_loss / len(train_loader)

    # Validation
    model.eval()                       # Eval mode (dropout off)
    correct = 0
    total = 0

    with torch.no_grad():             # Don't compute gradients
        for batch_X, batch_y in val_loader:
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)
            outputs = model(batch_X)
            _, predicted = torch.max(outputs, 1)
            total += batch_y.size(0)
            correct += (predicted == batch_y).sum().item()

    accuracy = correct / total
    print(f"Epoch {epoch+1}/{num_epochs} | Loss: {avg_loss:.4f} | Val Acc: {accuracy:.4f}")

# Save model
torch.save(model.state_dict(), 'model.pth')

# Load model
model.load_state_dict(torch.load('model.pth'))
model.eval()
```


## Convolutional Neural Networks (CNN)

```python
# Best for: images, spatial data, video frames

class CNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        # Convolutional layers (extract features)
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),   # 3 channels (RGB) → 32 filters
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),                            # Downsample by 2

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((4, 4)),                  # Fixed output size
        )

        # Classification head
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 4 * 4, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

# Key concepts:
#   Convolution: sliding filter detects local patterns (edges, textures)
#   Pooling: reduces spatial dimensions (shrinks image)
#   Feature maps: output of convolution (activation of detected features)
#   Stride: how far filter moves each step
#   Padding: add zeros around border to keep dimensions
#
# Layer 1 detects: edges, colors
# Layer 2 detects: textures, simple shapes
# Layer 3 detects: parts of objects (eyes, wheels)
# Layer 4 detects: whole objects (faces, cars)
```


## Recurrent Neural Networks (RNN) and Transformers

```python
# RNN: for sequential data (text, time series, audio)
# Problem: "vanishing gradient" — forgets long sequences

# LSTM: solves vanishing gradient with memory cell
class TextClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(
            embed_dim, hidden_dim,
            num_layers=2,
            batch_first=True,
            dropout=0.3,
            bidirectional=True,
        )
        self.fc = nn.Linear(hidden_dim * 2, num_classes)   # *2 for bidirectional

    def forward(self, x):
        embedded = self.embedding(x)               # (batch, seq_len, embed_dim)
        output, (hidden, cell) = self.lstm(embedded)
        # Use last hidden state from both directions
        hidden = torch.cat((hidden[-2], hidden[-1]), dim=1)
        return self.fc(hidden)


# TRANSFORMER: replaced RNNs for most NLP tasks
# Key innovation: ATTENTION mechanism
# "Which parts of the input are relevant to each other?"
#
# Self-Attention:
#   For each word, compute attention score with every other word
#   "The cat sat on the mat because it was tired"
#   "it" attends strongly to "cat" (learns the reference)
#
# Architecture:
#   Input → Embedding → Positional Encoding
#     → Multi-Head Self-Attention
#     → Feed-Forward Network
#     → (repeat N times)
#     → Output
#
# Used in: GPT (decoder-only), BERT (encoder-only),
#           T5 (encoder-decoder), Vision Transformer (ViT)
#
# Modern LLMs (GPT-4, Claude, Llama) are all transformers.
```


---

# CHAPTER 4: PRACTICAL ML


## Data Preprocessing

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer

# Load data
df = pd.read_csv('data.csv')

# Explore
print(df.shape)                    # (rows, columns)
print(df.info())                   # Types, null counts
print(df.describe())               # Statistics
print(df.isnull().sum())          # Missing values per column
print(df['target'].value_counts()) # Class distribution

# Handle missing values
# Strategy 1: Drop rows with missing (if few)
df_clean = df.dropna()

# Strategy 2: Impute (fill with mean/median/mode)
imputer = SimpleImputer(strategy='median')
df['age'] = imputer.fit_transform(df[['age']])

# Strategy 3: Fill with specific value
df['category'].fillna('unknown', inplace=True)

# Encode categorical variables
# One-hot encoding (for nominal categories: color, country)
df_encoded = pd.get_dummies(df, columns=['color', 'country'], drop_first=True)

# Label encoding (for ordinal categories: low/medium/high)
le = LabelEncoder()
df['size'] = le.fit_transform(df['size'])   # low=0, medium=1, high=2

# Feature scaling
# StandardScaler: mean=0, std=1 (for linear models, SVMs, neural nets)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)    # Fit on TRAIN only!
X_test_scaled = scaler.transform(X_test)    # Transform test with same params

# MinMaxScaler: scale to [0, 1] (for neural networks sometimes)
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X_train)

# IMPORTANT: fit scaler on TRAINING data only, then transform both.
# Otherwise: data leakage (test info leaks into training).
```


## Train/Validation/Test Split

```python
from sklearn.model_selection import train_test_split

# Standard split: 80% train, 10% validation, 10% test
X_train_full, X_test, y_train_full, y_test = train_test_split(
    X, y, test_size=0.1, random_state=42, stratify=y   # Preserve class ratio
)

X_train, X_val, y_train, y_val = train_test_split(
    X_train_full, y_train_full, test_size=0.11,    # 0.11 of 0.9 ≈ 0.1 of total
    random_state=42, stratify=y_train_full
)

print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")

# Cross-validation (better use of data for small datasets)
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f"CV Accuracy: {scores.mean():.4f} ± {scores.std():.4f}")

# WHY THREE SETS:
#   Train: model learns from this
#   Validation: tune hyperparameters, architecture decisions
#   Test: final evaluation (touch ONLY ONCE at the end!)
#
# If you tune on test set → overfitting to test set → overoptimistic results
```


## Overfitting vs Underfitting

```
UNDERFITTING (high bias):
  Model too simple. Doesn't capture patterns.
  Signs: low train accuracy, low test accuracy
  Fix: more features, more complex model, train longer

OVERFITTING (high variance):
  Model memorizes training data. Fails on new data.
  Signs: high train accuracy, LOW test accuracy
  Fix: more data, regularization, simpler model, dropout, early stopping

JUST RIGHT:
  Good train accuracy AND good test accuracy (close to each other)

REGULARIZATION TECHNIQUES:
  L1 (Lasso):  Adds |weights| to loss → pushes weights to 0 (feature selection)
  L2 (Ridge):  Adds weights² to loss → keeps weights small
  Dropout:     Randomly disable neurons during training (neural nets)
  Early stopping: Stop training when validation loss starts increasing
  Data augmentation: Create more training data (flip, rotate, crop images)
  Batch normalization: Normalize layer outputs (stabilizes training)

LEARNING CURVES:
  Plot train_loss and val_loss over epochs.
  
  Underfitting:
    train_loss:  high ────────────────
    val_loss:    high ────────────────
  
  Overfitting:
    train_loss:  low  ──────────────── (keeps decreasing)
    val_loss:    high ──────/ (starts going UP after some point)
  
  Good fit:
    train_loss:  low  ────────────────
    val_loss:    low  ──────────────── (close to train_loss)
```


## Evaluation Metrics

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_auc_score, mean_squared_error, mean_absolute_error,
)

# CLASSIFICATION METRICS:

# Accuracy: correct / total (misleading if imbalanced!)
accuracy = accuracy_score(y_true, y_pred)

# Precision: true positives / (true positives + false positives)
# "Of all predicted positive, how many actually positive?"
precision = precision_score(y_true, y_pred)

# Recall (Sensitivity): true positives / (true positives + false negatives)
# "Of all actual positive, how many did we catch?"
recall = recall_score(y_true, y_pred)

# F1 Score: harmonic mean of precision and recall
f1 = f1_score(y_true, y_pred)

# AUC-ROC: area under receiver operating characteristic curve
# 1.0 = perfect, 0.5 = random
auc = roc_auc_score(y_true, y_proba)

# Confusion Matrix:
#                 Predicted
#                 Neg    Pos
# Actual Neg  [  TN  |  FP  ]    TN=True Neg, FP=False Pos (Type I error)
# Actual Pos  [  FN  |  TP  ]    FN=False Neg (Type II), TP=True Pos
cm = confusion_matrix(y_true, y_pred)

# WHEN TO USE WHICH:
#   Balanced data:     Accuracy, F1
#   Imbalanced data:   F1, AUC-ROC, Precision/Recall
#   Spam detection:    Precision (don't want legit mail in spam)
#   Cancer detection:  Recall (don't want to MISS actual cancer)
#   Search ranking:    NDCG, MAP


# REGRESSION METRICS:

# MSE: average squared error (penalizes large errors more)
mse = mean_squared_error(y_true, y_pred)

# RMSE: square root of MSE (same units as target)
rmse = mean_squared_error(y_true, y_pred, squared=False)

# MAE: average absolute error (robust to outliers)
mae = mean_absolute_error(y_true, y_pred)

# R² Score: proportion of variance explained (1.0 = perfect)
from sklearn.metrics import r2_score
r2 = r2_score(y_true, y_pred)
```


---

# CHAPTER 5: LARGE LANGUAGE MODELS (LLMs)


## How LLMs Work

```
ARCHITECTURE: Transformer (decoder-only for GPT-like models)

TRAINING:
  1. Pre-training (self-supervised):
     - Given billions of text from internet
     - Task: predict next token
     - Input:  "The cat sat on the"
     - Output: "mat" (highest probability next token)
     - Learns language, facts, reasoning patterns
     - Costs millions of dollars (thousands of GPUs)

  2. Fine-tuning (supervised):
     - Curated instruction-response pairs
     - "[INST] Write a poem about cats [/INST] Soft paws..."
     - Teaches model to follow instructions
     - Much cheaper than pre-training

  3. RLHF (Reinforcement Learning from Human Feedback):
     - Model generates multiple responses
     - Humans rank them (best to worst)
     - Train reward model on human preferences
     - Use PPO/DPO to optimize model for high reward
     - Makes model helpful, harmless, honest

INFERENCE (how it generates text):
  1. Tokenize input text into tokens (subwords)
     "Hello world" → [15496, 995]
  
  2. Forward pass through transformer layers
     Each layer: self-attention + feed-forward network
  
  3. Output: probability distribution over ALL tokens
     P("the") = 0.15, P("a") = 0.10, P("cat") = 0.08, ...
  
  4. Sample next token using strategy:
     - Greedy: pick highest probability (deterministic)
     - Temperature: scale probabilities (higher = more random)
     - Top-k: sample from top k tokens only
     - Top-p (nucleus): sample from smallest set summing to p
  
  5. Append token to input, repeat from step 2
     This is why it's called "autoregressive" — each token depends on all previous

PARAMETERS:
  GPT-3:     175 billion parameters
  GPT-4:     ~1.8 trillion (estimated, mixture of experts)
  Llama 3:   8B, 70B, 405B versions
  Qwen 2.5:  0.5B, 1.5B, 3B, 7B, 14B, 32B, 72B versions
  Claude:    Unknown parameter count

QUANTIZATION:
  Full precision:  FP32 (4 bytes per param) → 175B × 4B = 700 GB
  Half precision:  FP16 (2 bytes) → 350 GB
  8-bit:           INT8 (1 byte) → 175 GB
  4-bit:           Q4 (0.5 bytes) → 87.5 GB
  2-bit:           Q2 (0.25 bytes) → minimal quality loss for small models

  Qwen 2.5 3B at Q4 → ~2 GB (runs on your Lenovo!)
```


## Using Hugging Face Transformers

```python
# pip install transformers torch

from transformers import pipeline

# Text generation
generator = pipeline("text-generation", model="gpt2")
result = generator("The future of AI is", max_length=50, num_return_sequences=1)
print(result[0]["generated_text"])

# Sentiment analysis
classifier = pipeline("sentiment-analysis")
result = classifier("This movie was absolutely fantastic!")
print(result)   # [{'label': 'POSITIVE', 'score': 0.9998}]

# Question answering
qa = pipeline("question-answering")
result = qa(
    question="What is Python?",
    context="Python is a high-level programming language created by Guido van Rossum."
)
print(result)   # {'answer': 'a high-level programming language', 'score': 0.95}

# Text summarization
summarizer = pipeline("summarization")
long_text = "..." * 500
summary = summarizer(long_text, max_length=130, min_length=30)
print(summary[0]["summary_text"])

# Zero-shot classification (no training needed!)
classifier = pipeline("zero-shot-classification")
result = classifier(
    "I need to book a flight to Paris next week",
    candidate_labels=["travel", "cooking", "sports", "technology"]
)
print(result)   # travel: 0.95


# Load specific model manually
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3-8B")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3-8B")

inputs = tokenizer("Hello, how are", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=50)
text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(text)
```


## RAG (Retrieval-Augmented Generation)

```
WHAT IS RAG:
  Combine LLM with external knowledge base.
  Instead of relying on training data (may be outdated/wrong),
  RETRIEVE relevant documents and include in prompt.

WHY RAG:
  - LLM knowledge is frozen at training time
  - Reduce hallucination (grounded in actual documents)
  - No need to fine-tune for new knowledge (just update docs)
  - Keep sensitive data private (docs stay on your server)

ARCHITECTURE:
  
  User Query
      │
      ▼
  Embedding Model (encode query → vector)
      │
      ▼
  Vector Database (find similar document chunks)
      │
      ▼
  Retrieved Chunks (top K most relevant)
      │
      ▼
  Construct Prompt:
    "Given this context: [retrieved chunks]
     Answer this question: [user query]"
      │
      ▼
  LLM generates answer grounded in context

COMPONENTS:
  1. Document Loader: read PDFs, markdown, web pages
  2. Text Splitter: chunk documents into 200-1000 char pieces
  3. Embedding Model: convert text → dense vector (768-1536 dims)
  4. Vector Store: ChromaDB, Pinecone, Weaviate, FAISS, pgvector
  5. Retriever: search vector store for relevant chunks
  6. LLM: generate answer using retrieved context

THIS IS EXACTLY WHAT GRG AI DOES!
  - Knowledge/*.md files → chunks → ChromaDB
  - User question → embedding → search ChromaDB
  - Top K chunks → injected into Qwen prompt
  - Qwen generates answer from context
```


---

# CHAPTER 6: COMMON PITFALLS


## ML Pitfalls

```
PITFALL 1: Data leakage
  Test data information leaks into training.
  Example: scaling with mean/std of ENTIRE dataset including test.
  Fix: fit preprocessing on train only, transform test separately.

PITFALL 2: Ignoring class imbalance
  99% negative, 1% positive → model always predicts negative → 99% accuracy!
  Fix: use F1/AUC, oversample minority (SMOTE), class weights, stratified split.

PITFALL 3: Not shuffling data
  If data is sorted by label → model learns order, not patterns.
  Fix: always shuffle before split.

PITFALL 4: Using accuracy on imbalanced data
  Misleading. Use precision, recall, F1, AUC instead.

PITFALL 5: Overfitting to validation set
  Tuning hyperparameters on validation repeatedly → overfitting to validation.
  Fix: use cross-validation, touch test set only once at the end.

PITFALL 6: Feature scaling forgotten
  Many algorithms (SVM, kNN, neural nets) need scaled features.
  Random forests and gradient boosting don't (tree-based).

PITFALL 7: Ignoring missing values
  Some algorithms crash, others handle silently (wrong).
  Fix: explicit strategy (impute, drop, or flag).

PITFALL 8: Too many features (curse of dimensionality)
  1000 features, 100 samples → model can't learn.
  Fix: feature selection, PCA, domain knowledge.

PITFALL 9: Not looking at errors
  Model accuracy is 90% — but WHERE does it fail?
  Fix: error analysis. Look at misclassified examples. Find patterns.

PITFALL 10: Deploying without monitoring
  Model works on test data. Production data changes over time (drift).
  Fix: monitor predictions, retrain periodically, alert on drift.

PITFALL 11: Treating ML as magic
  "Just throw data at neural network."
  Fix: understand the problem, clean the data, feature engineer.
  Garbage in → garbage out.

PITFALL 12: Not establishing a baseline
  Complex model achieves 85% accuracy. Good or bad?
  Fix: always compare to simple baseline (majority class, mean prediction, logistic regression).
  If baseline is 84% → your complex model adds little value.

PITFALL 13: Ignoring computational cost
  99.5% accuracy model runs 100x slower than 99.0% model.
  Fix: consider latency, memory, cost in production.

PITFALL 14: Training on future data
  Predicting stock prices, include tomorrow's data in training.
  Fix: time-series split (train on past, test on future).

PITFALL 15: Confusing correlation with causation
  Model finds: ice cream sales predict drowning deaths.
  Both are caused by summer heat, not by each other.
  ML finds correlations. Causation requires domain knowledge.
```