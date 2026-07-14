Machine Learning from Scratch Complete Reference
CHAPTER 1: GETTING STARTED WITH MACHINE LEARNING
Remarks
Machine learning enables systems to learn from data without explicit programming. Core paradigms: supervised learning (classification, regression), unsupervised learning (clustering, dimensionality reduction), reinforcement learning (policy optimization). Deep learning uses neural networks with multiple layers.
Tools: Python, NumPy (linear algebra), Matplotlib (visualization), PyTorch/TensorFlow (production), scikit-learn (classical ML).
Hello Machine Learning
# hello_ml.py
"""
First ML program: linear regression from scratch.
"""
import numpy as np
import matplotlib.pyplot as plt

# Generate synthetic data
np.random.seed(42)
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1)  # y = 4 + 3x + noise

# Linear regression: y = w*x + b
# Loss: MSE = (1/n) * Σ(y_pred - y)²
# Gradient: dw = (2/n) * Σ(y_pred - y) * x
#           db = (2/n) * Σ(y_pred - y)

def linear_regression(X, y, lr=0.1, epochs=1000):
    """Train linear regression using gradient descent."""
    n = len(X)
    w = np.random.randn()
    b = np.random.randn()
    
    history = []
    
    for epoch in range(epochs):
        # Forward pass
        y_pred = w * X + b
        
        # Compute loss
        loss = np.mean((y_pred - y) ** 2)
        history.append(loss)
        
        # Compute gradients
        dw = (2/n) * np.sum((y_pred - y) * X)
        db = (2/n) * np.sum(y_pred - y)
        
        # Update parameters
        w -= lr * dw
        b -= lr * db
        
        if (epoch + 1) % 100 == 0:
            print(f"Epoch {epoch+1}: loss = {loss:.4f}, w = {w:.4f}, b = {b:.4f}")
    
    return w, b, history

w, b, history = linear_regression(X, y)
print(f"\nFinal: y = {w:.4f}x + {b:.4f}")
print(f"Expected: y ≈ 3.0x + 4.0")

# Plot
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.scatter(X, y, alpha=0.5, label='Data')
plt.plot(X, w * X + b, color='red', label='Fit')
plt.xlabel('X'); plt.ylabel('y')
plt.legend(); plt.title('Linear Regression')

plt.subplot(1, 2, 2)
plt.plot(history)
plt.xlabel('Epoch'); plt.ylabel('MSE Loss')
plt.title('Training Loss')
plt.yscale('log')
plt.tight_layout()
plt.show()

CHAPTER 2: LINEAR ALGEBRA FOR ML
Tensors and Operations
# Tensors: multi-dimensional arrays (scalars, vectors, matrices, higher-order)
# Rank-0: scalar, Rank-1: vector, Rank-2: matrix, Rank-3+: tensor

import numpy as np

# Scalar (rank 0)
scalar = np.array(5.0)

# Vector (rank 1)
vector = np.array([1, 2, 3, 4])

# Matrix (rank 2)
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

# 3D tensor (rank 3) - e.g., RGB image batch
tensor = np.random.randn(32, 28, 28)  # 32 images, 28x28 pixels

# Basic operations
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

# Element-wise operations
print("Add:", a + b)
print("Multiply:", a * b)  # element-wise
print("Power:", a ** 2)

# Matrix multiplication (dot product)
print("Dot product:\n", a @ b)  # or np.dot(a, b)

# Transpose
print("Transpose:\n", a.T)

# Broadcasting
x = np.array([1, 2, 3])
y = np.array([[1], [2], [3]])
print("Broadcast add:\n", x + y)  # (3,) + (3,1) → (3,3)

# Norms
v = np.array([3, 4])
print("L2 norm:", np.linalg.norm(v))  # 5.0
print("L1 norm:", np.sum(np.abs(v)))  # 7.0

# Eigenvalues and eigenvectors
A = np.array([[4, -2], [1, 1]])
eigenvalues, eigenvectors = np.linalg.eig(A)
print("Eigenvalues:", eigenvalues)
print("Eigenvectors:\n", eigenvectors)

# Singular Value Decomposition (SVD)
M = np.random.randn(5, 3)
U, S, Vt = np.linalg.svd(M, full_matrices=False)
print(f"SVD: U={U.shape}, S={S.shape}, Vt={Vt.shape}")

Automatic Differentiation (Autograd)
# Autograd: automatically compute gradients of functions.
# Foundation of PyTorch and TensorFlow.

class Tensor:
    """Simple autograd tensor."""
    
    def __init__(self, data, requires_grad=False, _children=()):
        self.data = np.array(data, dtype=np.float32)
        self.grad = np.zeros_like(self.data) if requires_grad else None
        self.requires_grad = requires_grad
        self._backward = lambda: None
        self._prev = set(_children)
    
    def __repr__(self):
        return f"Tensor({self.data}, grad={self.grad})"
    
    def __add__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(self.data + other.data, requires_grad=self.requires_grad or other.requires_grad, _children=(self, other))
        
        def _backward():
            if self.requires_grad:
                self.grad += out.grad
            if other.requires_grad:
                other.grad += out.grad
        out._backward = _backward
        return out
    
    def __mul__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(self.data * other.data, requires_grad=self.requires_grad or other.requires_grad, _children=(self, other))
        
        def _backward():
            if self.requires_grad:
                self.grad += other.data * out.grad
            if other.requires_grad:
                other.grad += self.data * out.grad
        out._backward = _backward
        return out
    
    def __pow__(self, n):
        out = Tensor(self.data ** n, requires_grad=self.requires_grad, _children=(self,))
        
        def _backward():
            if self.requires_grad:
                self.grad += n * (self.data ** (n - 1)) * out.grad
        out._backward = _backward
        return out
    
    def relu(self):
        out = Tensor(np.maximum(0, self.data), requires_grad=self.requires_grad, _children=(self,))
        
        def _backward():
            if self.requires_grad:
                self.grad += (out.data > 0) * out.grad
        out._backward = _backward
        return out
    
    def sum(self):
        out = Tensor(np.sum(self.data), requires_grad=self.requires_grad, _children=(self,))
        
        def _backward():
            if self.requires_grad:
                self.grad += np.ones_like(self.data) * out.grad
        out._backward = _backward
        return out
    
    def backward(self):
        # Topological sort
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)
        
        self.grad = np.ones_like(self.data)
        for v in reversed(topo):
            v._backward()
    
    def zero_grad(self):
        if self.grad is not None:
            self.grad.fill(0)

# Example: f(x) = x² + 2x + 1, df/dx = 2x + 2
x = Tensor(3.0, requires_grad=True)
f = x ** 2 + 2 * x + 1
f.backward()
print(f"f(3) = {f.data}, df/dx = {x.grad}")  # 16, 8

CHAPTER 3: NEURAL NETWORKS FROM SCRATCH
Perceptron and Multi-Layer Perceptron
# Perceptron: y = activation(w·x + b)
# MLP: stacked layers of perceptrons with non-linear activations

class Layer:
    """Dense (fully-connected) layer."""
    
    def __init__(self, input_size, output_size, activation='relu'):
        # Xavier/Glorot initialization
        scale = np.sqrt(2.0 / input_size)
        self.W = np.random.randn(input_size, output_size) * scale
        self.b = np.zeros((1, output_size))
        self.activation = activation
        
        # For backprop
        self.input = None
        self.z = None  # pre-activation
        self.a = None  # post-activation
        
        # Gradients
        self.dW = None
        self.db = None
    
    def _activate(self, z):
        if self.activation == 'relu':
            return np.maximum(0, z)
        elif self.activation == 'sigmoid':
            return 1 / (1 + np.exp(-np.clip(z, -500, 500)))
        elif self.activation == 'tanh':
            return np.tanh(z)
        elif self.activation == 'linear':
            return z
        elif self.activation == 'softmax':
            exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
            return exp_z / np.sum(exp_z, axis=1, keepdims=True)
        raise ValueError(f"Unknown activation: {self.activation}")
    
    def _activate_deriv(self, z, a):
        if self.activation == 'relu':
            return (z > 0).astype(float)
        elif self.activation == 'sigmoid':
            return a * (1 - a)
        elif self.activation == 'tanh':
            return 1 - a ** 2
        elif self.activation == 'linear':
            return np.ones_like(z)
        return np.ones_like(z)
    
    def forward(self, x):
        self.input = x
        self.z = x @ self.W + self.b
        self.a = self._activate(self.z)
        return self.a
    
    def backward(self, da, learning_rate):
        """Backpropagate gradient and update weights."""
        m = da.shape[0]
        
        # Activation derivative
        dz = da * self._activate_deriv(self.z, self.a)
        
        # Gradients
        self.dW = (self.input.T @ dz) / m
        self.db = np.sum(dz, axis=0, keepdims=True) / m
        
        # Gradient w.r.t. input (for previous layer)
        da_prev = dz @ self.W.T
        
        # Update parameters
        self.W -= learning_rate * self.dW
        self.b -= learning_rate * self.db
        
        return da_prev

class NeuralNetwork:
    """Multi-layer perceptron."""
    
    def __init__(self, layer_sizes, activations=None):
        """
        layer_sizes: [input, hidden1, hidden2, ..., output]
        activations: list of activation names for each layer
        """
        if activations is None:
            activations = ['relu'] * (len(layer_sizes) - 2) + ['linear']
        
        self.layers = []
        for i in range(len(layer_sizes) - 1):
            self.layers.append(Layer(layer_sizes[i], layer_sizes[i+1], activations[i]))
    
    def forward(self, X):
        a = X
        for layer in self.layers:
            a = layer.forward(a)
        return a
    
    def backward(self, y_true, learning_rate):
        """Compute loss gradient and backpropagate."""
        # MSE loss gradient: dL/da = 2*(a - y)/m
        a = self.layers[-1].a
        m = y_true.shape[0]
        da = 2 * (a - y_true) / m
        
        for layer in reversed(self.layers):
            da = layer.backward(da, learning_rate)
    
    def train(self, X, y, epochs=1000, learning_rate=0.01, verbose=True):
        history = []
        for epoch in range(epochs):
            y_pred = self.forward(X)
            loss = np.mean((y_pred - y) ** 2)
            history.append(loss)
            
            self.backward(y, learning_rate)
            
            if verbose and (epoch + 1) % 100 == 0:
                print(f"Epoch {epoch+1}/{epochs}: loss = {loss:.6f}")
        
        return history
    
    def predict(self, X):
        return self.forward(X)

# Example: learn XOR
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
y = np.array([[0], [1], [1], [0]], dtype=float)

nn = NeuralNetwork([2, 8, 4, 1], ['relu', 'relu', 'sigmoid'])
history = nn.train(X, y, epochs=2000, learning_rate=0.1)

print("\nXOR predictions:")
for xi, yi in zip(X, y):
    pred = nn.predict(xi.reshape(1, -1))[0, 0]
    print(f"  {xi} → {pred:.4f} (expected {yi[0]})")

CHAPTER 4: ACTIVATION AND LOSS FUNCTIONS
Activation Functions
# Non-linearities that enable neural networks to learn complex patterns.

import numpy as np
import matplotlib.pyplot as plt

def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

def sigmoid_deriv(a):
    return a * (1 - a)

def relu(z):
    return np.maximum(0, z)

def relu_deriv(z):
    return (z > 0).astype(float)

def tanh(z):
    return np.tanh(z)

def tanh_deriv(a):
    return 1 - a ** 2

def leaky_relu(z, alpha=0.01):
    return np.where(z > 0, z, alpha * z)

def gelu(z):
    """Gaussian Error Linear Unit (used in BERT, GPT)."""
    return 0.5 * z * (1 + np.tanh(np.sqrt(2/np.pi) * (z + 0.044715 * z**3)))

def swish(z):
    """Swish / SiLU activation."""
    return z * sigmoid(z)

# Plot activations
z = np.linspace(-5, 5, 200)
funcs = [
    ('Sigmoid', sigmoid),
    ('Tanh', tanh),
    ('ReLU', relu),
    ('Leaky ReLU', lambda x: leaky_relu(x, 0.1)),
    ('GELU', gelu),
    ('Swish', swish),
]

plt.figure(figsize=(12, 4))
for i, (name, fn) in enumerate(funcs):
    plt.subplot(2, 3, i+1)
    plt.plot(z, fn(z))
    plt.title(name)
    plt.grid(alpha=0.3)
    plt.axhline(0, color='k', linewidth=0.5)
    plt.axvline(0, color='k', linewidth=0.5)
plt.tight_layout()
plt.show()

Loss Functions
# Loss functions measure prediction error.

def mse_loss(y_pred, y_true):
    """Mean Squared Error (regression)."""
    return np.mean((y_pred - y_true) ** 2)

def mse_loss_grad(y_pred, y_true):
    return 2 * (y_pred - y_true) / y_true.shape[0]

def mae_loss(y_pred, y_true):
    """Mean Absolute Error (robust to outliers)."""
    return np.mean(np.abs(y_pred - y_true))

def binary_cross_entropy(y_pred, y_true):
    """Binary Cross-Entropy (binary classification)."""
    eps = 1e-15
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

def binary_cross_entropy_grad(y_pred, y_true):
    eps = 1e-15
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return (y_pred - y_true) / (y_pred * (1 - y_pred)) / y_true.shape[0]

def categorical_cross_entropy(y_pred, y_true):
    """Categorical Cross-Entropy (multi-class classification).
    y_pred: probabilities (softmax output), shape (batch, classes)
    y_true: one-hot encoded, shape (batch, classes)
    """
    eps = 1e-15
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -np.mean(np.sum(y_true * np.log(y_pred), axis=1))

def categorical_cross_entropy_grad(y_pred, y_true):
    """Gradient when combined with softmax (simplified)."""
    return (y_pred - y_true) / y_true.shape[0]

def huber_loss(y_pred, y_true, delta=1.0):
    """Huber loss (smooth L1, robust to outliers)."""
    diff = np.abs(y_pred - y_true)
    quadratic = np.minimum(diff, delta)
    linear = diff - quadratic
    return np.mean(0.5 * quadratic ** 2 + delta * linear)

# Example
y_true = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
y_pred = np.array([[0.7, 0.2, 0.1], [0.1, 0.8, 0.1], [0.2, 0.3, 0.5]])
print(f"CCE loss: {categorical_cross_entropy(y_pred, y_true):.4f}")

CHAPTER 5: OPTIMIZATION ALGORITHMS
Gradient Descent Variants
# Optimization: how to update weights to minimize loss.

class SGDOptimizer:
    """Stochastic Gradient Descent with momentum."""
    
    def __init__(self, params, lr=0.01, momentum=0.9):
        self.params = params  # list of (W, b) tuples
        self.lr = lr
        self.momentum = momentum
        self.velocities = [(np.zeros_like(W), np.zeros_like(b)) for W, b in params]
    
    def step(self, grads):
        """Update parameters using gradients."""
        for i, (W, b) in enumerate(self.params):
            dW, db = grads[i]
            vW, vb = self.velocities[i]
            
            # Momentum update
            vW = self.momentum * vW - self.lr * dW
            vb = self.momentum * vb - self.lr * db
            
            self.velocities[i] = (vW, vb)
            self.params[i] = (W + vW, b + vb)

class AdamOptimizer:
    """Adam optimizer (Adaptive Moment Estimation).
    Combines momentum with adaptive learning rates.
    """
    
    def __init__(self, params, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
        self.params = params
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.t = 0
        self.m = [(np.zeros_like(W), np.zeros_like(b)) for W, b in params]  # 1st moment
        self.v = [(np.zeros_like(W), np.zeros_like(b)) for W, b in params]  # 2nd moment
    
    def step(self, grads):
        self.t += 1
        for i, (W, b) in enumerate(self.params):
            dW, db = grads[i]
            
            # Update biased first moment
            self.m[i] = (
                self.beta1 * self.m[i][0] + (1 - self.beta1) * dW,
                self.beta1 * self.m[i][1] + (1 - self.beta1) * db
            )
            
            # Update biased second moment
            self.v[i] = (
                self.beta2 * self.v[i][0] + (1 - self.beta2) * dW**2,
                self.beta2 * self.v[i][1] + (1 - self.beta2) * db**2
            )
            
            # Bias correction
            m_hat = (self.m[i][0] / (1 - self.beta1**self.t),
                     self.m[i][1] / (1 - self.beta1**self.t))
            v_hat = (self.v[i][0] / (1 - self.beta2**self.t),
                     self.v[i][1] / (1 - self.beta2**self.t))
            
            # Update parameters
            new_W = W - self.lr * m_hat[0] / (np.sqrt(v_hat[0]) + self.eps)
            new_b = b - self.lr * m_hat[1] / (np.sqrt(v_hat[1]) + self.eps)
            self.params[i] = (new_W, new_b)

class RMSpropOptimizer:
    """RMSprop: adaptive learning rate per parameter."""
    
    def __init__(self, params, lr=0.001, decay=0.9, eps=1e-8):
        self.params = params
        self.lr = lr
        self.decay = decay
        self.eps = eps
        self.cache = [(np.zeros_like(W), np.zeros_like(b)) for W, b in params]
    
    def step(self, grads):
        for i, (W, b) in enumerate(self.params):
            dW, db = grads[i]
            cW, cb = self.cache[i]
            
            cW = self.decay * cW + (1 - self.decay) * dW**2
            cb = self.decay * cb + (1 - self.decay) * db**2
            self.cache[i] = (cW, cb)
            
            new_W = W - self.lr * dW / (np.sqrt(cW) + self.eps)
            new_b = b - self.lr * db / (np.sqrt(cb) + self.eps)
            self.params[i] = (new_W, new_b)

# Learning rate schedulers
def step_decay(epoch, initial_lr=0.1, decay_factor=0.5, decay_every=10):
    """Reduce LR by factor every N epochs."""
    return initial_lr * (decay_factor ** (epoch // decay_every))

def cosine_annealing(epoch, total_epochs, initial_lr=0.1, min_lr=1e-5):
    """Cosine annealing schedule."""
    return min_lr + 0.5 * (initial_lr - min_lr) * (1 + np.cos(np.pi * epoch / total_epochs))

def warmup_cosine(epoch, warmup_epochs, total_epochs, max_lr=0.1):
    """Linear warmup + cosine decay."""
    if epoch < warmup_epochs:
        return max_lr * (epoch + 1) / warmup_epochs
    progress = (epoch - warmup_epochs) / (total_epochs - warmup_epochs)
    return max_lr * 0.5 * (1 + np.cos(np.pi * progress))

# Visualize schedules
epochs = np.arange(200)
plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.plot(epochs, [step_decay(e) for e in epochs])
plt.title('Step Decay')
plt.subplot(1, 3, 2)
plt.plot(epochs, [cosine_annealing(e, 200) for e in epochs])
plt.title('Cosine Annealing')
plt.subplot(1, 3, 3)
plt.plot(epochs, [warmup_cosine(e, 20, 200) for e in epochs])
plt.title('Warmup + Cosine')
plt.tight_layout()
plt.show()

CHAPTER 6: CONVOLUTIONAL NEURAL NETWORKS
Convolution Operations
# CNNs: exploit spatial structure in images using convolution filters.

def conv2d(image, kernel, stride=1, padding=0):
    """2D convolution (single channel)."""
    if padding > 0:
        image = np.pad(image, padding, mode='constant')
    
    h, w = image.shape
    kh, kw = kernel.shape
    
    out_h = (h - kh) // stride + 1
    out_w = (w - kw) // stride + 1
    
    output = np.zeros((out_h, out_w))
    
    for i in range(out_h):
        for j in range(out_w):
            region = image[i*stride:i*stride+kh, j*stride:j*stride+kw]
            output[i, j] = np.sum(region * kernel)
    
    return output

def conv2d_multichannel(images, kernels, stride=1, padding=0):
    """Multi-channel convolution (batch of images, multiple filters).
    images: (batch, channels, h, w)
    kernels: (num_filters, channels, kh, kw)
    """
    batch, in_channels, h, w = images.shape
    num_filters, _, kh, kw = kernels.shape
    
    if padding > 0:
        images = np.pad(images, ((0,0), (0,0), (padding, padding), (padding, padding)))
        _, _, h, w = images.shape
    
    out_h = (h - kh) // stride + 1
    out_w = (w - kw) // stride + 1
    
    output = np.zeros((batch, num_filters, out_h, out_w))
    
    for b in range(batch):
        for f in range(num_filters):
            for c in range(in_channels):
                for i in range(out_h):
                    for j in range(out_w):
                        region = images[b, c, i*stride:i*stride+kh, j*stride:j*stride+kw]
                        output[b, f, i, j] += np.sum(region * kernels[f, c])
    
    return output

# Example: edge detection kernels
sobel_x = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]])

sobel_y = np.array([[-1, -2, -1],
                    [ 0,  0,  0],
                    [ 1,  2,  1]])

# Create test image (gradient)
img = np.zeros((20, 20))
img[:, 10:] = 1.0

edges_x = conv2d(img, sobel_x, padding=1)
edges_y = conv2d(img, sobel_y, padding=1)
edges = np.sqrt(edges_x**2 + edges_y**2)

print(f"Input shape: {img.shape}")
print(f"Edge map shape: {edges.shape}")

Pooling Layers
def max_pool2d(x, pool_size=2, stride=2):
    """2D max pooling."""
    batch, channels, h, w = x.shape
    out_h = (h - pool_size) // stride + 1
    out_w = (w - pool_size) // stride + 1
    
    output = np.zeros((batch, channels, out_h, out_w))
    
    for b in range(batch):
        for c in range(channels):
            for i in range(out_h):
                for j in range(out_w):
                    region = x[b, c, i*stride:i*stride+pool_size, j*stride:j*stride+pool_size]
                    output[b, c, i, j] = np.max(region)
    
    return output

def avg_pool2d(x, pool_size=2, stride=2):
    """2D average pooling."""
    batch, channels, h, w = x.shape
    out_h = (h - pool_size) // stride + 1
    out_w = (w - pool_size) // stride + 1
    
    output = np.zeros((batch, channels, out_h, out_w))
    
    for b in range(batch):
        for c in range(channels):
            for i in range(out_h):
                for j in range(out_w):
                    region = x[b, c, i*stride:i*stride+pool_size, j*stride:j*stride+pool_size]
                    output[b, c, i, j] = np.mean(region)
    
    return output

# Example
x = np.random.randn(2, 3, 8, 8)  # batch=2, channels=3, 8x8
pooled = max_pool2d(x, pool_size=2, stride=2)
print(f"Max pool: {x.shape} → {pooled.shape}")  # (2, 3, 4, 4)

CHAPTER 7: RECURRENT NEURAL NETWORKS
Vanilla RNN
# RNN: process sequences by maintaining hidden state.
# h_t = tanh(W_hh * h_{t-1} + W_xh * x_t + b_h)
# y_t = W_hy * h_t + b_y

class SimpleRNN:
    """Simple RNN from scratch."""
    
    def __init__(self, input_size, hidden_size, output_size):
        self.hidden_size = hidden_size
        
        # Initialize weights (Xavier)
        scale_x = np.sqrt(1.0 / input_size)
        scale_h = np.sqrt(1.0 / hidden_size)
        
        self.W_xh = np.random.randn(input_size, hidden_size) * scale_x
        self.W_hh = np.random.randn(hidden_size, hidden_size) * scale_h
        self.W_hy = np.random.randn(hidden_size, output_size) * scale_h
        
        self.b_h = np.zeros((1, hidden_size))
        self.b_y = np.zeros((1, output_size))
    
    def forward_step(self, x, h_prev):
        """Single time step."""
        h = np.tanh(x @ self.W_xh + h_prev @ self.W_hh + self.b_h)
        y = h @ self.W_hy + self.b_y
        return h, y
    
    def forward_sequence(self, X_seq):
        """Process entire sequence.
        X_seq: (seq_len, batch, input_size)
        """
        seq_len, batch, _ = X_seq.shape
        h = np.zeros((batch, self.hidden_size))
        
        H = []  # hidden states
        Y = []  # outputs
        
        for t in range(seq_len):
            h, y = self.forward_step(X_seq[t], h)
            H.append(h)
            Y.append(y)
        
        return np.array(H), np.array(Y)

# Example: sequence prediction
rnn = SimpleRNN(input_size=5, hidden_size=10, output_size=3)
X_seq = np.random.randn(20, 4, 5)  # 20 steps, batch=4, input=5
H, Y = rnn.forward_sequence(X_seq)
print(f"Input: {X_seq.shape} → Hidden: {H.shape}, Output: {Y.shape}")

LSTM (Long Short-Term Memory)
# LSTM: solves vanishing gradient with gates.
# Gates: forget (f), input (i), output (o), cell candidate (g)
# f_t = σ(W_f · [h_{t-1}, x_t] + b_f)
# i_t = σ(W_i · [h_{t-1}, x_t] + b_i)
# g_t = tanh(W_g · [h_{t-1}, x_t] + b_g)
# o_t = σ(W_o · [h_{t-1}, x_t] + b_o)
# c_t = f_t * c_{t-1} + i_t * g_t
# h_t = o_t * tanh(c_t)

class LSTMCell:
    """LSTM cell."""
    
    def __init__(self, input_size, hidden_size):
        self.hidden_size = hidden_size
        
        # Combined weights for all 4 gates
        scale = np.sqrt(1.0 / (input_size + hidden_size))
        self.W_f = np.random.randn(input_size + hidden_size, hidden_size) * scale
        self.W_i = np.random.randn(input_size + hidden_size, hidden_size) * scale
        self.W_g = np.random.randn(input_size + hidden_size, hidden_size) * scale
        self.W_o = np.random.randn(input_size + hidden_size, hidden_size) * scale
        
        self.b_f = np.ones((1, hidden_size))  # forget gate bias = 1 (helps gradient flow)
        self.b_i = np.zeros((1, hidden_size))
        self.b_g = np.zeros((1, hidden_size))
        self.b_o = np.zeros((1, hidden_size))
    
    def forward(self, x, h_prev, c_prev):
        """Single time step."""
        combined = np.concatenate([x, h_prev], axis=-1)
        
        f = 1 / (1 + np.exp(-(combined @ self.W_f + self.b_f)))  # forget
        i = 1 / (1 + np.exp(-(combined @ self.W_i + self.b_i)))  # input
        g = np.tanh(combined @ self.W_g + self.b_g)              # candidate
        o = 1 / (1 + np.exp(-(combined @ self.W_o + self.b_o)))  # output
        
        c = f * c_prev + i * g
        h = o * np.tanh(c)
        
        cache = (x, h_prev, c_prev, f, i, g, o, c, combined)
        return h, c, cache

class LSTM:
    """Multi-step LSTM."""
    
    def __init__(self, input_size, hidden_size):
        self.cell = LSTMCell(input_size, hidden_size)
        self.hidden_size = hidden_size
    
    def forward(self, X_seq, h0=None, c0=None):
        """Process sequence.
        X_seq: (seq_len, batch, input_size)
        """
        seq_len, batch, _ = X_seq.shape
        
        if h0 is None:
            h0 = np.zeros((batch, self.hidden_size))
        if c0 is None:
            c0 = np.zeros((batch, self.hidden_size))
        
        h, c = h0, c0
        H = []
        
        for t in range(seq_len):
            h, c, _ = self.cell.forward(X_seq[t], h, c)
            H.append(h)
        
        return np.array(H), h, c

# Example
lstm = LSTM(input_size=10, hidden_size=20)
X_seq = np.random.randn(15, 4, 10)  # 15 steps, batch=4, input=10
H, h_final, c_final = lstm.forward(X_seq)
print(f"LSTM: {X_seq.shape} → H: {H.shape}")

GRU (Gated Recurrent Unit)
# GRU: simpler than LSTM, 2 gates (reset, update).
# z_t = σ(W_z · [h_{t-1}, x_t])  # update gate
# r_t = σ(W_r · [h_{t-1}, x_t])  # reset gate
# h̃_t = tanh(W · [r_t * h_{t-1}, x_t])  # candidate
# h_t = (1 - z_t) * h_{t-1} + z_t * h̃_t

class GRUCell:
    """GRU cell."""
    
    def __init__(self, input_size, hidden_size):
        self.hidden_size = hidden_size
        scale = np.sqrt(1.0 / (input_size + hidden_size))
        
        self.W_z = np.random.randn(input_size + hidden_size, hidden_size) * scale
        self.W_r = np.random.randn(input_size + hidden_size, hidden_size) * scale
        self.W_h = np.random.randn(input_size + hidden_size, hidden_size) * scale
        
        self.b_z = np.zeros((1, hidden_size))
        self.b_r = np.zeros((1, hidden_size))
        self.b_h = np.zeros((1, hidden_size))
    
    def forward(self, x, h_prev):
        combined = np.concatenate([x, h_prev], axis=-1)
        
        z = 1 / (1 + np.exp(-(combined @ self.W_z + self.b_z)))
        r = 1 / (1 + np.exp(-(combined @ self.W_r + self.b_r)))
        
        # Reset gate applied to previous hidden state
        combined_h = np.concatenate([r * h_prev, x], axis=-1)
        h_tilde = np.tanh(combined_h @ self.W_h + self.b_h)
        
        h = (1 - z) * h_prev + z * h_tilde
        return h

# Example
gru = GRUCell(input_size=8, hidden_size=16)
x = np.random.randn(4, 8)
h = np.zeros((4, 16))
h_new = gru.forward(x, h)
print(f"GRU: h shape = {h_new.shape}")

CHAPTER 8: ATTENTION MECHANISM AND TRANSFORMERS
Scaled Dot-Product Attention
# Attention: "query looks at keys to find values"
# Attention(Q, K, V) = softmax(Q·K^T / √d_k) · V
# Multi-head: run h attention heads in parallel, concatenate

def softmax(x, axis=-1):
    """Numerically stable softmax."""
    e_x = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e_x / np.sum(e_x, axis=axis, keepdims=True)

def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Q, K, V: (batch, seq_len, d_k)
    mask: optional (batch, 1, seq_len, seq_len) for causal masking
    """
    d_k = Q.shape[-1]
    
    # Attention scores
    scores = Q @ K.transpose(0, 2, 1) / np.sqrt(d_k)  # (batch, seq, seq)
    
    # Apply mask (set masked positions to -inf)
    if mask is not None:
        scores = np.where(mask == 0, -1e9, scores)
    
    # Softmax over keys
    weights = softmax(scores, axis=-1)  # (batch, seq, seq)
    
    # Weighted sum of values
    output = weights @ V  # (batch, seq, d_v)
    
    return output, weights

# Example
batch, seq_len, d_k = 2, 5, 8
Q = np.random.randn(batch, seq_len, d_k)
K = np.random.randn(batch, seq_len, d_k)
V = np.random.randn(batch, seq_len, d_k)

output, weights = scaled_dot_product_attention(Q, K, V)
print(f"Attention output: {output.shape}")
print(f"Attention weights: {weights.shape}")
print(f"Weights sum to 1: {np.allclose(weights.sum(axis=-1), 1.0)}")

Multi-Head Attention
class MultiHeadAttention:
    """Multi-head attention mechanism."""
    
    def __init__(self, d_model, num_heads):
        assert d_model % num_heads == 0
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        scale = np.sqrt(1.0 / d_model)
        self.W_q = np.random.randn(d_model, d_model) * scale
        self.W_k = np.random.randn(d_model, d_model) * scale
        self.W_v = np.random.randn(d_model, d_model) * scale
        self.W_o = np.random.randn(d_model, d_model) * scale
    
    def forward(self, Q, K, V, mask=None):
        """
        Q, K, V: (batch, seq_len, d_model)
        """
        batch, seq_len, _ = Q.shape
        
        # Linear projections
        Q_proj = Q @ self.W_q  # (batch, seq, d_model)
        K_proj = K @ self.W_k
        V_proj = V @ self.W_v
        
        # Reshape to (batch, num_heads, seq_len, d_k)
        Q_proj = Q_proj.reshape(batch, seq_len, self.num_heads, self.d_k).transpose(0, 2, 1, 3)
        K_proj = K_proj.reshape(batch, seq_len, self.num_heads, self.d_k).transpose(0, 2, 1, 3)
        V_proj = V_proj.reshape(batch, seq_len, self.num_heads, self.d_k).transpose(0, 2, 1, 3)
        
        # Scaled dot-product attention
        attn_output, attn_weights = scaled_dot_product_attention(Q_proj, K_proj, V_proj, mask)
        
        # Concatenate heads: (batch, num_heads, seq, d_k) → (batch, seq, d_model)
        attn_output = attn_output.transpose(0, 2, 1, 3).reshape(batch, seq_len, self.d_model)
        
        # Final linear projection
        output = attn_output @ self.W_o
        
        return output, attn_weights

# Example
mha = MultiHeadAttention(d_model=64, num_heads=8)
X = np.random.randn(2, 10, 64)  # batch=2, seq=10, d_model=64
out, weights = mha.forward(X, X, X)
print(f"Multi-head attention: {X.shape} → {out.shape}")
print(f"Attention weights shape: {weights.shape}")

Transformer Block
class LayerNorm:
    """Layer normalization."""
    
    def __init__(self, d_model, eps=1e-5):
        self.eps = eps
        self.gamma = np.ones((1, 1, d_model))
        self.beta = np.zeros((1, 1, d_model))
    
    def forward(self, x):
        mean = np.mean(x, axis=-1, keepdims=True)
        var = np.var(x, axis=-1, keepdims=True)
        x_norm = (x - mean) / np.sqrt(var + self.eps)
        return self.gamma * x_norm + self.beta

class FeedForward:
    """Position-wise feed-forward network."""
    
    def __init__(self, d_model, d_ff):
        scale1 = np.sqrt(1.0 / d_model)
        scale2 = np.sqrt(1.0 / d_ff)
        self.W1 = np.random.randn(d_model, d_ff) * scale1
        self.b1 = np.zeros((1, 1, d_ff))
        self.W2 = np.random.randn(d_ff, d_model) * scale2
        self.b2 = np.zeros((1, 1, d_model))
    
    def forward(self, x):
        # GELU activation
        h = x @ self.W1 + self.b1
        h = 0.5 * h * (1 + np.tanh(np.sqrt(2/np.pi) * (h + 0.044715 * h**3)))
        return h @ self.W2 + self.b2

class PositionalEncoding:
    """Sinusoidal positional encoding."""
    
    def __init__(self, d_model, max_len=5000):
        pe = np.zeros((max_len, d_model))
        position = np.arange(max_len)[:, np.newaxis]
        div_term = np.exp(np.arange(0, d_model, 2) * (-np.log(10000.0) / d_model))
        
        pe[:, 0::2] = np.sin(position * div_term)
        pe[:, 1::2] = np.cos(position * div_term)
        
        self.pe = pe[np.newaxis, :, :]  # (1, max_len, d_model)
    
    def forward(self, x):
        seq_len = x.shape[1]
        return x + self.pe[:, :seq_len, :]

class TransformerEncoderLayer:
    """Single transformer encoder layer."""
    
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        self.attention = MultiHeadAttention(d_model, num_heads)
        self.norm1 = LayerNorm(d_model)
        self.norm2 = LayerNorm(d_model)
        self.ff = FeedForward(d_model, d_ff)
    
    def forward(self, x, mask=None):
        # Self-attention + residual + layer norm
        attn_out, _ = self.attention.forward(x, x, x, mask)
        x = self.norm1.forward(x + attn_out)
        
        # Feed-forward + residual + layer norm
        ff_out = self.ff.forward(x)
        x = self.norm2.forward(x + ff_out)
        
        return x

class TransformerDecoderLayer:
    """Single transformer decoder layer."""
    
    def __init__(self, d_model, num_heads, d_ff):
        self.self_attention = MultiHeadAttention(d_model, num_heads)
        self.cross_attention = MultiHeadAttention(d_model, num_heads)
        self.norm1 = LayerNorm(d_model)
        self.norm2 = LayerNorm(d_model)
        self.norm3 = LayerNorm(d_model)
        self.ff = FeedForward(d_model, d_ff)
    
    def forward(self, x, encoder_output, src_mask=None, tgt_mask=None):
        # Masked self-attention
        self_attn_out, _ = self.self_attention.forward(x, x, x, tgt_mask)
        x = self.norm1.forward(x + self_attn_out)
        
        # Cross-attention (query from decoder, key/value from encoder)
        cross_attn_out, _ = self.cross_attention.forward(x, encoder_output, encoder_output, src_mask)
        x = self.norm2.forward(x + cross_attn_out)
        
        # Feed-forward
        ff_out = self.ff.forward(x)
        x = self.norm3.forward(x + ff_out)
        
        return x

# Example: build a transformer
d_model, num_heads, d_ff = 64, 8, 256
encoder_layer = TransformerEncoderLayer(d_model, num_heads, d_ff)
decoder_layer = TransformerDecoderLayer(d_model, num_heads, d_ff)

# Encoder
src = np.random.randn(2, 10, d_model)
enc_out = encoder_layer.forward(src)
print(f"Encoder output: {enc_out.shape}")

# Decoder with causal mask
tgt = np.random.randn(2, 8, d_model)
causal_mask = np.tril(np.ones((8, 8)))  # lower triangular
dec_out = decoder_layer.forward(tgt, enc_out, tgt_mask=causal_mask)
print(f"Decoder output: {dec_out.shape}")

Full Transformer
class Transformer:
    """Complete Transformer model."""
    
    def __init__(self, src_vocab_size, tgt_vocab_size, d_model=512, num_heads=8,
                 num_layers=6, d_ff=2048, max_len=5000):
        self.d_model = d_model
        self.num_layers = num_layers
        
        # Embeddings
        self.src_embed = np.random.randn(src_vocab_size, d_model) * 0.02
        self.tgt_embed = np.random.randn(tgt_vocab_size, d_model) * 0.02
        
        # Positional encoding
        self.pos_enc = PositionalEncoding(d_model, max_len)
        
        # Encoder and decoder stacks
        self.encoder_layers = [TransformerEncoderLayer(d_model, num_heads, d_ff)
                               for _ in range(num_layers)]
        self.decoder_layers = [TransformerDecoderLayer(d_model, num_heads, d_ff)
                               for _ in range(num_layers)]
        
        # Output projection
        self.output_proj = np.random.randn(d_model, tgt_vocab_size) * 0.02
    
    def encode(self, src_tokens, src_mask=None):
        """Encode source sequence."""
        # Embed + positional encoding
        x = self.src_embed[src_tokens] * np.sqrt(self.d_model)
        x = self.pos_enc.forward(x)
        
        # Pass through encoder layers
        for layer in self.encoder_layers:
            x = layer.forward(x, src_mask)
        
        return x
    
    def decode(self, tgt_tokens, encoder_output, src_mask=None, tgt_mask=None):
        """Decode target sequence."""
        x = self.tgt_embed[tgt_tokens] * np.sqrt(self.d_model)
        x = self.pos_enc.forward(x)
        
        for layer in self.decoder_layers:
            x = layer.forward(x, encoder_output, src_mask, tgt_mask)
        
        # Project to vocabulary
        logits = x @ self.output_proj
        return logits
    
    def forward(self, src_tokens, tgt_tokens):
        """Full forward pass."""
        encoder_output = self.encode(src_tokens)
        
        # Causal mask for decoder
        seq_len = tgt_tokens.shape[1]
        tgt_mask = np.tril(np.ones((seq_len, seq_len)))
        
        logits = self.decode(tgt_tokens, encoder_output, tgt_mask=tgt_mask)
        return logits

# Example
transformer = Transformer(
    src_vocab_size=1000,
    tgt_vocab_size=1000,
    d_model=64,
    num_heads=4,
    num_layers=2,
    d_ff=256
)

src = np.random.randint(0, 1000, (2, 10))  # batch=2, seq=10
tgt = np.random.randint(0, 1000, (2, 8))

logits = transformer.forward(src, tgt)
print(f"Transformer logits: {logits.shape}")  # (2, 8, 1000)

CHAPTER 9: GENERATIVE MODELS
Variational Autoencoder (VAE)
# VAE: generative model that learns latent distribution.
# Encoder: q(z|x) = N(μ, σ²)
# Decoder: p(x|z)
# Loss: reconstruction + KL divergence

class VAE:
    """Variational Autoencoder."""
    
    def __init__(self, input_dim, hidden_dim, latent_dim):
        self.latent_dim = latent_dim
        
        # Encoder
        self.W_e1 = np.random.randn(input_dim, hidden_dim) * 0.05
        self.b_e1 = np.zeros(hidden_dim)
        self.W_mu = np.random.randn(hidden_dim, latent_dim) * 0.05
        self.b_mu = np.zeros(latent_dim)
        self.W_logvar = np.random.randn(hidden_dim, latent_dim) * 0.05
        self.b_logvar = np.zeros(latent_dim)
        
        # Decoder
        self.W_d1 = np.random.randn(latent_dim, hidden_dim) * 0.05
        self.b_d1 = np.zeros(hidden_dim)
        self.W_out = np.random.randn(hidden_dim, input_dim) * 0.05
        self.b_out = np.zeros(input_dim)
    
    def encode(self, x):
        """Encode input to latent distribution parameters."""
        h = np.tanh(x @ self.W_e1 + self.b_e1)
        mu = h @ self.W_mu + self.b_mu
        logvar = h @ self.W_logvar + self.b_logvar
        return mu, logvar
    
    def reparameterize(self, mu, logvar):
        """Sample z = μ + σ * ε, where ε ~ N(0,1)."""
        std = np.exp(0.5 * logvar)
        eps = np.random.randn_like(mu)
        return mu + std * eps
    
    def decode(self, z):
        """Decode latent vector to reconstruction."""
        h = np.tanh(z @ self.W_d1 + self.b_d1)
        x_recon = 1 / (1 + np.exp(-(h @ self.W_out + self.b_out)))  # sigmoid
        return x_recon
    
    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        x_recon = self.decode(z)
        return x_recon, mu, logvar
    
    def kl_divergence(self, mu, logvar):
        """KL(q(z|x) || p(z)) = -0.5 * Σ(1 + log(σ²) - μ² - σ²)."""
        return -0.5 * np.sum(1 + logvar - mu**2 - np.exp(logvar))
    
    def loss(self, x, x_recon, mu, logvar, beta=1.0):
        """VAE loss = reconstruction + β * KL."""
        recon_loss = np.mean((x - x_recon) ** 2)
        kl_loss = self.kl_divergence(mu, logvar) / x.shape[0]
        return recon_loss + beta * kl_loss, recon_loss, kl_loss
    
    def sample(self, n_samples):
        """Generate new samples from prior N(0, I)."""
        z = np.random.randn(n_samples, self.latent_dim)
        return self.decode(z)

# Example
vae = VAE(input_dim=784, hidden_dim=256, latent_dim=20)
x = np.random.rand(32, 784)  # batch of 32 flattened 28x28 images
x_recon, mu, logvar = vae.forward(x)
loss, recon, kl = vae.loss(x, x_recon, mu, logvar)
print(f"VAE loss: {loss:.4f} (recon={recon:.4f}, KL={kl:.4f})")

samples = vae.sample(10)
print(f"Generated samples shape: {samples.shape}")

Generative Adversarial Networks (GAN)
# GAN: generator G and discriminator D compete.
# G tries to fool D, D tries to distinguish real from fake.
# min_G max_D V(D, G) = E[log D(x)] + E[log(1 - D(G(z)))]

class Generator:
    """Simple MLP generator."""
    
    def __init__(self, latent_dim, hidden_dim, output_dim):
        self.W1 = np.random.randn(latent_dim, hidden_dim) * 0.05
        self.b1 = np.zeros(hidden_dim)
        self.W2 = np.random.randn(hidden_dim, output_dim) * 0.05
        self.b2 = np.zeros(output_dim)
    
    def forward(self, z):
        h = np.maximum(0, z @ self.W1 + self.b1)  # ReLU
        x = 1 / (1 + np.exp(-(h @ self.W2 + self.b2)))  # sigmoid
        return x

class Discriminator:
    """Simple MLP discriminator."""
    
    def __init__(self, input_dim, hidden_dim):
        self.W1 = np.random.randn(input_dim, hidden_dim) * 0.05
        self.b1 = np.zeros(hidden_dim)
        self.W2 = np.random.randn(hidden_dim, 1) * 0.05
        self.b2 = np.zeros(1)
    
    def forward(self, x):
        h = np.maximum(0, x @ self.W1 + self.b1)  # Leaky ReLU would be better
        logit = h @ self.W2 + self.b2
        return 1 / (1 + np.exp(-logit))  # sigmoid probability

class SimpleGAN:
    """GAN training loop."""
    
    def __init__(self, latent_dim, hidden_dim, data_dim):
        self.latent_dim = latent_dim
        self.G = Generator(latent_dim, hidden_dim, data_dim)
        self.D = Discriminator(data_dim, hidden_dim)
    
    def sample_noise(self, batch_size):
        return np.random.randn(batch_size, self.latent_dim)
    
    def train_step(self, real_data, lr_G=0.0002, lr_D=0.0002):
        """Single training step."""
        batch_size = real_data.shape[0]
        
        # Train Discriminator
        z = self.sample_noise(batch_size)
        fake_data = self.G.forward(z)
        
        d_real = self.D.forward(real_data)
        d_fake = self.D.forward(fake_data)
        
        # BCE loss for D: -[log(d_real) + log(1-d_fake)]
        # (gradients omitted for brevity)
        d_loss = -np.mean(np.log(d_real + 1e-8) + np.log(1 - d_fake + 1e-8))
        
        # Train Generator
        z = self.sample_noise(batch_size)
        fake_data = self.G.forward(z)
        d_fake = self.D.forward(fake_data)
        
        # G wants D to classify fake as real
        g_loss = -np.mean(np.log(d_fake + 1e-8))
        
        return d_loss, g_loss

# Example
gan = SimpleGAN(latent_dim=100, hidden_dim=256, data_dim=784)
real_data = np.random.rand(32, 784)
d_loss, g_loss = gan.train_step(real_data)
print(f"GAN losses: D={d_loss:.4f}, G={g_loss:.4f}")

CHAPTER 10: ADVANCED TOPICS AND RESOURCES
Modern Architectures Overview
# Vision: ResNet, EfficientNet, ViT (Vision Transformer), ConvNeXt
# NLP: BERT, GPT, T5, LLaMA, Mistral
# Multimodal: CLIP, DALL-E, Stable Diffusion
# Speech: Whisper, wav2vec 2.0
# Reinforcement Learning: PPO, DPO, RLHF

# Modern techniques:
# - Mixed precision training (FP16/BF16)
# - Gradient checkpointing (memory efficient)
# - Flash Attention (memory efficient attention)
# - LoRA/QLoRA (parameter-efficient fine-tuning)
# - Mixture of Experts (MoE)
# - Speculative decoding

Recommended Reading
# - "Deep Learning" by Goodfellow, Bengio, Courville (free online)
# - "Pattern Recognition and Machine Learning" by Bishop
# - "Hands-On Machine Learning" by Aurélien Géron
# - Andrej Karpathy's "Neural Networks: Zero to Hero" (YouTube)
# - Stanford CS231n (CNNs), CS224n (NLP), CS229 (ML)
# - Papers: Attention Is All You Need, BERT, GPT-3, Diffusion Models

# Code References
# - PyTorch: https://pytorch.org/tutorials/
# - NumPy documentation: https://numpy.org/doc/
# - The Illustrated Transformer: https://jalammar.github.io/illustrated-transformer/
# - Andrej Karpathy's micrograd, minGPT, nanoGPT (GitHub)

# End of Machine Learning from Scratch Reference