Computer Vision Advanced Complete Reference
CHAPTER 1: GETTING STARTED WITH COMPUTER VISION
Remarks
Computer vision enables machines to interpret and understand visual information from the world. Key areas: image processing (filters, transformations), feature detection (corners, keypoints), object detection (bounding boxes, classification), segmentation (pixel-level labeling), 3D vision (depth, stereo, reconstruction), tracking (optical flow, object tracking). Modern approaches combine classical algorithms with deep learning (CNNs, Transformers).
Tools: Python, NumPy (numerical ops), OpenCV (classical CV), Pillow (image I/O), Matplotlib (visualization), PyTorch/TensorFlow (deep learning), scikit-image (scientific image processing).
Hello Computer Vision
# hello_cv.py
"""
First CV program: load, display, and manipulate an image.
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Load image (OpenCV uses BGR format)
img = cv2.imread('sample.jpg')
if img is None:
    # Create synthetic image if file not found
    img = np.zeros((400, 600, 3), dtype=np.uint8)
    cv2.rectangle(img, (50, 50), (550, 350), (0, 255, 0), 3)
    cv2.putText(img, "Hello CV!", (150, 220), cv2.FONT_HERSHEY_SIMPLEX, 
                2, (255, 255, 255), 3)

print(f"Image shape: {img.shape}")  # (height, width, channels)
print(f"Image dtype: {img.dtype}")  # uint8 (0-255)
print(f"Image size: {img.size} pixels")

# Convert BGR to RGB for matplotlib
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Basic operations
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(img, (5, 5), 0)
edges = cv2.Canny(img, 100, 200)

# Display
plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
plt.imshow(img_rgb)
plt.title('Original')
plt.axis('off')

plt.subplot(2, 2, 2)
plt.imshow(gray, cmap='gray')
plt.title('Grayscale')
plt.axis('off')

plt.subplot(2, 2, 3)
plt.imshow(cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB))
plt.title('Gaussian Blur')
plt.axis('off')

plt.subplot(2, 2, 4)
plt.imshow(edges, cmap='gray')
plt.title('Canny Edges')
plt.axis('off')

plt.tight_layout()
plt.savefig('hello_cv.png', dpi=100)
plt.show()

# Image properties
print(f"\nGrayscale stats:")
print(f"  Min: {gray.min()}, Max: {gray.max()}, Mean: {gray.mean():.2f}")

# Save result
cv2.imwrite('output.jpg', img)

Image Representation
# Images are multi-dimensional arrays:
# - Grayscale: (H, W) - single channel
# - Color (RGB/BGR): (H, W, 3) - three channels
# - RGBA: (H, W, 4) - with alpha (transparency)
# - Multi-spectral: (H, W, N) - N channels (satellite, medical)

# Data types:
# - uint8: 0-255 (most common, 8-bit per channel)
# - uint16: 0-65535 (medical imaging, HDR)
# - float32: 0.0-1.0 or arbitrary range (processing)

import numpy as np

def create_gradient_image(width=400, height=300):
    """Create a gradient image from scratch."""
    # Horizontal gradient
    x = np.linspace(0, 255, width, dtype=np.uint8)
    gradient = np.tile(x, (height, 1))
    return gradient

def create_color_wheel(size=300):
    """Create HSV color wheel."""
    # Create coordinate grid
    y, x = np.ogrid[-size//2:size//2, -size//2:size//2]
    
    # Convert to polar coordinates
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    
    # HSV: hue from angle, saturation from radius
    hue = ((theta + np.pi) / (2 * np.pi) * 180).astype(np.uint8)
    saturation = np.clip(r * 255 / (size // 2), 0, 255).astype(np.uint8)
    value = np.full_like(hue, 255)
    
    # Stack into HSV image
    hsv = np.stack([hue, saturation, value], axis=-1)
    
    # Convert to RGB
    rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    
    # Mask circular region
    mask = r <= size // 2
    rgb[~mask] = 0
    
    return rgb

# Example
gradient = create_gradient_image()
color_wheel = create_color_wheel(400)

plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.imshow(gradient, cmap='gray')
plt.title('Gradient')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(color_wheel)
plt.title('HSV Color Wheel')
plt.axis('off')

plt.tight_layout()
plt.show()

# Channel manipulation
def split_and_merge_channels(img):
    """Demonstrate channel operations."""
    b, g, r = cv2.split(img)
    
    # Modify individual channels
    r_enhanced = np.clip(r * 1.5, 0, 255).astype(np.uint8)
    b_reduced = (b * 0.5).astype(np.uint8)
    
    # Merge back
    modified = cv2.merge([b_reduced, g, r_enhanced])
    return modified

# Pixel access (slow - use vectorized operations instead)
def count_pixels_by_intensity(img):
    """Count pixels in intensity ranges."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    dark = np.sum(gray < 85)
    medium = np.sum((gray >= 85) & (gray < 170))
    bright = np.sum(gray >= 170)
    
    total = gray.size
    print(f"Dark (<85): {dark} ({dark/total*100:.1f}%)")
    print(f"Medium (85-170): {medium} ({medium/total*100:.1f}%)")
    print(f"Bright (>=170): {bright} ({bright/total*100:.1f}%)")

count_pixels_by_intensity(img)

CHAPTER 2: IMAGE PROCESSING FUNDAMENTALS
Convolution and Filtering
# Convolution: fundamental operation in image processing
# Output[x,y] = ΣΣ Kernel[i,j] * Input[x+i, y+j]
# Used for: blurring, sharpening, edge detection, feature extraction

import numpy as np
import cv2

def convolve2d_manual(image, kernel):
    """Manual 2D convolution (educational, slow)."""
    h, w = image.shape
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2
    
    # Pad image
    padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
    output = np.zeros_like(image, dtype=np.float32)
    
    # Convolve
    for i in range(h):
        for j in range(w):
            region = padded[i:i+kh, j:j+kw]
            output[i, j] = np.sum(region * kernel)
    
    return output

def convolve2d_fft(image, kernel):
    """FFT-based convolution (fast for large kernels)."""
    # Pad to avoid circular convolution artifacts
    h, w = image.shape
    kh, kw = kernel.shape
    pad_h, pad_w = h + kh - 1, w + kw - 1
    
    # FFT
    img_fft = np.fft.fft2(image, s=(pad_h, pad_w))
    ker_fft = np.fft.fft2(kernel, s=(pad_h, pad_w))
    
    # Multiply in frequency domain
    result_fft = img_fft * ker_fft
    
    # Inverse FFT
    result = np.fft.ifft2(result_fft).real
    
    # Crop to original size
    start_h, start_w = kh // 2, kw // 2
    return result[start_h:start_h+h, start_w:start_w+w]

# Common kernels
kernels = {
    'blur_3x3': np.ones((3, 3)) / 9,
    'blur_5x5': np.ones((5, 5)) / 25,
    'gaussian_3x3': np.array([[1, 2, 1],
                               [2, 4, 2],
                               [1, 2, 1]]) / 16,
    'sharpen': np.array([[0, -1, 0],
                         [-1, 5, -1],
                         [0, -1, 0]]),
    'edge_detect': np.array([[-1, -1, -1],
                             [-1, 8, -1],
                             [-1, -1, -1]]),
    'sobel_x': np.array([[-1, 0, 1],
                         [-2, 0, 2],
                         [-1, 0, 1]]),
    'sobel_y': np.array([[-1, -2, -1],
                         [0, 0, 0],
                         [1, 2, 1]]),
    'laplacian': np.array([[0, 1, 0],
                           [1, -4, 1],
                           [0, 1, 0]])
}

# Example: apply different filters
img = cv2.imread('sample.jpg', cv2.IMREAD_GRAYSCALE)
if img is None:
    img = np.random.randint(0, 256, (200, 300), dtype=np.uint8)

plt.figure(figsize=(14, 8))
for i, (name, kernel) in enumerate(kernels.items()):
    result = cv2.filter2D(img, -1, kernel)
    plt.subplot(2, 4, i+1)
    plt.imshow(result, cmap='gray')
    plt.title(name)
    plt.axis('off')
plt.tight_layout()
plt.show()

Gaussian Filter
# Gaussian blur: weighted average with Gaussian kernel
# G(x,y) = (1 / 2πσ²) * exp(-(x² + y²) / 2σ²)
# σ controls blur amount

def create_gaussian_kernel(size, sigma):
    """Create 2D Gaussian kernel."""
    kernel = np.zeros((size, size))
    center = size // 2
    
    for i in range(size):
        for j in range(size):
            x, y = i - center, j - center
            kernel[i, j] = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    
    # Normalize
    kernel /= kernel.sum()
    return kernel

def gaussian_blur_manual(image, size=5, sigma=1.0):
    """Apply Gaussian blur manually."""
    kernel = create_gaussian_kernel(size, sigma)
    return convolve2d_manual(image.astype(np.float32), kernel)

# Compare with OpenCV
img_float = img.astype(np.float32)
blur_manual = gaussian_blur_manual(img, size=7, sigma=2.0)
blur_opencv = cv2.GaussianBlur(img, (7, 7), 2.0)

print(f"Manual blur shape: {blur_manual.shape}")
print(f"OpenCV blur shape: {blur_opencv.shape}")
print(f"Difference: {np.max(np.abs(blur_manual - blur_opencv)):.4f}")

# Effect of sigma
plt.figure(figsize=(12, 4))
for i, sigma in enumerate([0.5, 1.0, 2.0, 4.0]):
    blurred = cv2.GaussianBlur(img, (0, 0), sigma)
    plt.subplot(1, 4, i+1)
    plt.imshow(blurred, cmap='gray')
    plt.title(f'σ = {sigma}')
    plt.axis('off')
plt.tight_layout()
plt.show()

Edge Detection
# Edge detection: find rapid intensity changes
# Methods: Sobel, Prewitt, Canny, Laplacian

def sobel_edge_detection(image):
    """Sobel edge detection (magnitude and direction)."""
    # Sobel kernels
    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]], dtype=np.float32)
    sobel_y = np.array([[-1, -2, -1],
                        [0, 0, 0],
                        [1, 2, 1]], dtype=np.float32)
    
    # Compute gradients
    gx = cv2.filter2D(image.astype(np.float32), -1, sobel_x)
    gy = cv2.filter2D(image.astype(np.float32), -1, sobel_y)
    
    # Magnitude and direction
    magnitude = np.sqrt(gx**2 + gy**2)
    direction = np.arctan2(gy, gx)
    
    # Normalize magnitude to 0-255
    magnitude = (magnitude / magnitude.max() * 255).astype(np.uint8)
    
    return magnitude, direction

def canny_edge_detection(image, low_thresh=50, high_thresh=150):
    """Canny edge detection (multi-stage)."""
    # 1. Gaussian blur (noise reduction)
    blurred = cv2.GaussianBlur(image, (5, 5), 1.4)
    
    # 2. Compute gradients (Sobel)
    gx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
    
    magnitude = np.sqrt(gx**2 + gy**2)
    direction = np.arctan2(gy, gx)
    
    # 3. Non-maximum suppression
    h, w = image.shape
    nms = np.zeros_like(magnitude)
    
    for i in range(1, h-1):
        for j in range(1, w-1):
            angle = direction[i, j] * 180 / np.pi
            angle = angle if angle >= 0 else angle + 180
            
            # Determine neighbors to compare
            if (0 <= angle < 22.5) or (157.5 <= angle <= 180):
                n1, n2 = magnitude[i, j+1], magnitude[i, j-1]
            elif 22.5 <= angle < 67.5:
                n1, n2 = magnitude[i+1, j-1], magnitude[i-1, j+1]
            elif 67.5 <= angle < 112.5:
                n1, n2 = magnitude[i+1, j], magnitude[i-1, j]
            else:
                n1, n2 = magnitude[i-1, j-1], magnitude[i+1, j+1]
            
            # Keep only local maxima
            if magnitude[i, j] >= n1 and magnitude[i, j] >= n2:
                nms[i, j] = magnitude[i, j]
    
    # 4. Double thresholding
    strong = nms >= high_thresh
    weak = (nms >= low_thresh) & (nms < high_thresh)
    
    # 5. Hysteresis (connect weak edges to strong)
    edges = np.zeros_like(nms)
    edges[strong] = 255
    
    # Simple hysteresis: keep weak if connected to strong
    for i in range(1, h-1):
        for j in range(1, w-1):
            if weak[i, j]:
                if np.any(strong[i-1:i+2, j-1:j+2]):
                    edges[i, j] = 255
    
    return edges.astype(np.uint8)

# Compare methods
plt.figure(figsize=(14, 8))

plt.subplot(2, 3, 1)
plt.imshow(img, cmap='gray')
plt.title('Original')
plt.axis('off')

# Sobel
sobel_mag, sobel_dir = sobel_edge_detection(img)
plt.subplot(2, 3, 2)
plt.imshow(sobel_mag, cmap='gray')
plt.title('Sobel Magnitude')
plt.axis('off')

plt.subplot(2, 3, 3)
plt.imshow(sobel_dir * 180 / np.pi, cmap='hsv')
plt.title('Sobel Direction')
plt.axis('off')

# Canny (manual)
canny_manual = canny_edge_detection(img, 50, 150)
plt.subplot(2, 3, 4)
plt.imshow(canny_manual, cmap='gray')
plt.title('Canny (Manual)')
plt.axis('off')

# Canny (OpenCV)
canny_opencv = cv2.Canny(img, 50, 150)
plt.subplot(2, 3, 5)
plt.imshow(canny_opencv, cmap='gray')
plt.title('Canny (OpenCV)')
plt.axis('off')

# Laplacian
laplacian = cv2.Laplacian(img, cv2.CV_64F)
laplacian = np.abs(laplacian).astype(np.uint8)
plt.subplot(2, 3, 6)
plt.imshow(laplacian, cmap='gray')
plt.title('Laplacian')
plt.axis('off')

plt.tight_layout()
plt.show()

Morphological Operations
# Morphological operations: process images based on shapes
# Uses structuring element (kernel)
# Basic operations: erosion, dilation, opening, closing

def erode(image, kernel_size=3, iterations=1):
    """Erosion: shrink foreground regions."""
    kernel = np.ones((kernel_size, kernel_size), dtype=np.uint8)
    return cv2.erode(image, kernel, iterations=iterations)

def dilate(image, kernel_size=3, iterations=1):
    """Dilation: expand foreground regions."""
    kernel = np.ones((kernel_size, kernel_size), dtype=np.uint8)
    return cv2.dilate(image, kernel, iterations=iterations)

def opening(image, kernel_size=3):
    """Opening: erosion followed by dilation (removes small objects)."""
    kernel = np.ones((kernel_size, kernel_size), dtype=np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

def closing(image, kernel_size=3):
    """Closing: dilation followed by erosion (fills small holes)."""
    kernel = np.ones((kernel_size, kernel_size), dtype=np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

def morphological_gradient(image, kernel_size=3):
    """Gradient: dilation - erosion (edge detection)."""
    kernel = np.ones((kernel_size, kernel_size), dtype=np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)

def top_hat(image, kernel_size=15):
    """Top-hat: original - opening (bright spots on dark background)."""
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    return cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)

def black_hat(image, kernel_size=15):
    """Black-hat: closing - original (dark spots on bright background)."""
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    return cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernel)

# Example: clean up binary image
# Create synthetic binary image with noise
binary = np.zeros((200, 300), dtype=np.uint8)
cv2.rectangle(binary, (50, 50), (250, 150), 255, -1)
cv2.circle(binary, (150, 100), 30, 255, -1)

# Add noise
noise = np.random.randint(0, 2, (200, 300), dtype=np.uint8) * 255
binary_noisy = cv2.bitwise_or(binary, noise)

# Apply morphological operations
plt.figure(figsize=(14, 10))

plt.subplot(2, 4, 1)
plt.imshow(binary_noisy, cmap='gray')
plt.title('Noisy Binary')
plt.axis('off')

plt.subplot(2, 4, 2)
plt.imshow(erode(binary_noisy), cmap='gray')
plt.title('Erosion')
plt.axis('off')

plt.subplot(2, 4, 3)
plt.imshow(dilate(binary_noisy), cmap='gray')
plt.title('Dilation')
plt.axis('off')

plt.subplot(2, 4, 4)
plt.imshow(opening(binary_noisy), cmap='gray')
plt.title('Opening')
plt.axis('off')

plt.subplot(2, 4, 5)
plt.imshow(closing(binary_noisy), cmap='gray')
plt.title('Closing')
plt.axis('off')

plt.subplot(2, 4, 6)
plt.imshow(morphological_gradient(binary_noisy), cmap='gray')
plt.title('Gradient')
plt.axis('off')

plt.subplot(2, 4, 7)
plt.imshow(top_hat(binary_noisy), cmap='gray')
plt.title('Top-Hat')
plt.axis('off')

plt.subplot(2, 4, 8)
plt.imshow(black_hat(binary_noisy), cmap='gray')
plt.title('Black-Hat')
plt.axis('off')

plt.tight_layout()
plt.show()

CHAPTER 3: FEATURE DETECTION
Harris Corner Detector
# Harris corner detector: finds corners (interest points)
# Corner: region with large intensity variation in all directions
# Used for: image matching, tracking, 3D reconstruction

def harris_corner_detector(image, k=0.04, threshold=0.01):
    """Harris corner detection from scratch."""
    # Convert to float
    img_float = image.astype(np.float32)
    
    # Compute gradients
    Ix = cv2.Sobel(img_float, cv2.CV_64F, 1, 0, ksize=3)
    Iy = cv2.Sobel(img_float, cv2.CV_64F, 0, 1, ksize=3)
    
    # Compute products of derivatives
    Ixx = Ix**2
    Iyy = Iy**2
    Ixy = Ix * Iy
    
    # Gaussian weighting
    gaussian = cv2.getGaussianKernel(5, 1.0)
    gaussian_2d = gaussian @ gaussian.T
    
    # Sum over window
    Sxx = cv2.filter2D(Ixx, -1, gaussian_2d)
    Syy = cv2.filter2D(Iyy, -1, gaussian_2d)
    Sxy = cv2.filter2D(Ixy, -1, gaussian_2d)
    
    # Harris response: R = det(M) - k * trace(M)^2
    # M = [[Sxx, Sxy], [Sxy, Syy]]
    det_M = Sxx * Syy - Sxy**2
    trace_M = Sxx + Syy
    R = det_M - k * trace_M**2
    
    # Threshold
    R_max = R.max()
    R_norm = R / R_max if R_max > 0 else R
    
    # Non-maximum suppression
    corners = []
    h, w = image.shape
    for i in range(1, h-1):
        for j in range(1, w-1):
            if R_norm[i, j] > threshold:
                # Check if local maximum in 3x3 neighborhood
                if R_norm[i, j] == R_norm[i-1:i+2, j-1:j+2].max():
                    corners.append((j, i, R_norm[i, j]))
    
    return corners, R_norm

# Example
img = cv2.imread('chessboard.jpg', cv2.IMREAD_GRAYSCALE)
if img is None:
    # Create synthetic image with corners
    img = np.zeros((300, 400), dtype=np.uint8)
    for i in range(0, 300, 50):
        for j in range(0, 400, 50):
            cv2.rectangle(img, (j, i), (j+40, i+40), 255, -1)

corners, response = harris_corner_detector(img, k=0.04, threshold=0.01)
print(f"Detected {len(corners)} corners")

# Visualize
img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
for x, y, strength in corners[:100]:  # Show top 100
    cv2.circle(img_color, (int(x), int(y)), 5, (0, 0, 255), 2)

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.imshow(response, cmap='hot')
plt.title('Harris Response')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB))
plt.title(f'Corners ({len(corners)} detected)')
plt.axis('off')

plt.tight_layout()
plt.show()

# Compare with OpenCV
corners_cv = cv2.cornerHarris(img, blockSize=5, ksize=3, k=0.04)
corners_cv = cv2.dilate(corners_cv, None)
corners_cv = (corners_cv > 0.01 * corners_cv.max())
print(f"OpenCV detected {corners_cv.sum()} corners")

SIFT (Scale-Invariant Feature Transform)
# SIFT: detects and describes local features
# Invariant to: scale, rotation, illumination
# Steps: scale-space extrema detection, keypoint localization, 
#        orientation assignment, descriptor generation

def sift_from_scratch_simplified(image):
    """Simplified SIFT-like feature detection (educational)."""
    # 1. Build scale space (Gaussian pyramid)
    num_octaves = 4
    num_scales = 3
    sigma_init = 1.6
    k_scale = 2 ** 0.5
    
    keypoints = []
    
    for octave in range(num_octaves):
        # Downsample for next octave
        if octave > 0:
            image = cv2.pyrDown(image)
        
        # Build Gaussian pyramid for this octave
        sigmas = [sigma_init * (k_scale ** i) for i in range(num_scales + 3)]
        gaussian_pyr = []
        
        for sigma in sigmas:
            blurred = cv2.GaussianBlur(image, (0, 0), sigma)
            gaussian_pyr.append(blurred)
        
        # 2. Build Difference of Gaussians (DoG)
        dog_pyr = []
        for i in range(len(gaussian_pyr) - 1):
            dog = gaussian_pyr[i+1] - gaussian_pyr[i]
            dog_pyr.append(dog)
        
        # 3. Find scale-space extrema
        for i in range(1, len(dog_pyr) - 1):
            h, w = dog_pyr[i].shape
            for y in range(5, h-5):
                for x in range(5, w-5):
                    # Check if local extremum in 3x3x3 neighborhood
                    center = dog_pyr[i][y, x]
                    
                    # Compare with 26 neighbors
                    is_max = True
                    is_min = True
                    
                    for di in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            for dx in [-1, 0, 1]:
                                if di == 0 and dy == 0 and dx == 0:
                                    continue
                                neighbor = dog_pyr[i+di][y+dy, x+dx]
                                if neighbor >= center:
                                    is_max = False
                                if neighbor <= center:
                                    is_min = False
                    
                    if is_max or is_min:
                        keypoints.append({
                            'x': x * (2 ** octave),
                            'y': y * (2 ** octave),
                            'scale': i,
                            'octave': octave,
                            'response': abs(center)
                        })
    
    return keypoints

# Example
img = cv2.imread('scene.jpg', cv2.IMREAD_GRAYSCALE)
if img is None:
    img = np.random.randint(0, 256, (300, 400), dtype=np.uint8)

keypoints_simplified = sift_from_scratch_simplified(img)
print(f"Simplified SIFT: {len(keypoints_simplified)} keypoints")

# Compare with OpenCV SIFT
sift = cv2.SIFT_create()
keypoints_cv, descriptors = sift.detectAndCompute(img, None)
print(f"OpenCV SIFT: {len(keypoints_cv)} keypoints")

# Visualize
img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
img_sift = cv2.drawKeypoints(img_color, keypoints_cv, None, 
                              flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(img_color, cmap='gray')
for kp in keypoints_simplified[:100]:
    cv2.circle(img_color, (int(kp['x']), int(kp['y'])), 3, (0, 255, 0), -1)
plt.imshow(img_color)
plt.title(f'Simplified SIFT ({len(keypoints_simplified)} keypoints)')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(img_sift, cv2.COLOR_BGR2RGB))
plt.title(f'OpenCV SIFT ({len(keypoints_cv)} keypoints)')
plt.axis('off')

plt.tight_layout()
plt.show()

ORB (Oriented FAST and Rotated BRIEF)
# ORB: fast alternative to SIFT
# FAST keypoint detector + BRIEF descriptor with rotation
# Free to use (SIFT was patented until 2020)

def orb_feature_matching(img1, img2):
    """Match features between two images using ORB."""
    # Create ORB detector
    orb = cv2.ORB_create(nfeatures=1000)
    
    # Detect keypoints and compute descriptors
    kp1, desc1 = orb.detectAndCompute(img1, None)
    kp2, desc2 = orb.detectAndCompute(img2, None)
    
    if desc1 is None or desc2 is None:
        print("Not enough features detected")
        return None
    
    # BFMatcher with Hamming distance (for binary descriptors)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    
    # Match descriptors
    matches = bf.match(desc1, desc2)
    
    # Sort by distance (lower is better)
    matches = sorted(matches, key=lambda x: x.distance)
    
    return kp1, kp2, matches

# Example: create two similar images
img1 = np.zeros((300, 400), dtype=np.uint8)
cv2.rectangle(img1, (50, 50), (150, 150), 255, -1)
cv2.circle(img1, (250, 150), 50, 255, -1)
cv2.putText(img1, "ABC", (100, 250), cv2.FONT_HERSHEY_SIMPLEX, 2, 255, 3)

# Transform img2 (rotation + translation)
M = cv2.getRotationMatrix2D((200, 150), 15, 1.0)
M[0, 2] += 20  # Translate
M[1, 2] += 10
img2 = cv2.warpAffine(img1, M, (400, 300))

# Match features
result = orb_feature_matching(img1, img2)
if result:
    kp1, kp2, matches = result
    
    print(f"ORB detected: {len(kp1)} keypoints in img1, {len(kp2)} in img2")
    print(f"Found {len(matches)} matches")
    
    # Draw matches
    img_matches = cv2.drawMatches(img1, kp1, img2, kp2, matches[:50], None,
                                   flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    
    plt.figure(figsize=(12, 5))
    plt.imshow(img_matches)
    plt.title(f'ORB Feature Matching (top 50 of {len(matches)} matches)')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

CHAPTER 4: IMAGE SEGMENTATION
Thresholding
# Thresholding: convert grayscale to binary
# Simple: pixel > threshold → white, else black
# Adaptive: threshold varies across image

def threshold_manual(image, thresh):
    """Manual binary thresholding."""
    return (image > thresh).astype(np.uint8) * 255

def otsu_threshold(image):
    """Otsu's method: automatic threshold selection."""
    # Compute histogram
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    hist = hist.ravel()
    
    # Total pixels
    total = image.size
    
    # Find optimal threshold
    best_thresh = 0
    best_variance = 0
    
    sum_all = np.sum(np.arange(256) * hist)
    
    sum_bg = 0
    weight_bg = 0
    
    for t in range(256):
        weight_bg += hist[t]
        if weight_bg == 0:
            continue
        
        weight_fg = total - weight_bg
        if weight_fg == 0:
            break
        
        sum_bg += t * hist[t]
        mean_bg = sum_bg / weight_bg
        mean_fg = (sum_all - sum_bg) / weight_fg
        
        # Between-class variance
        variance = weight_bg * weight_fg * (mean_bg - mean_fg) ** 2
        
        if variance > best_variance:
            best_variance = variance
            best_thresh = t
    
    return best_thresh

# Example
img = cv2.imread('document.jpg', cv2.IMREAD_GRAYSCALE)
if img is None:
    # Create synthetic image with text
    img = np.ones((300, 400), dtype=np.uint8) * 200
    cv2.putText(img, "Hello World", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 
                2, 0, 3)
    # Add noise
    img = img + np.random.randint(-30, 30, img.shape)
    img = np.clip(img, 0, 255).astype(np.uint8)

# Different thresholding methods
plt.figure(figsize=(14, 8))

plt.subplot(2, 3, 1)
plt.imshow(img, cmap='gray')
plt.title('Original')
plt.axis('off')

# Simple threshold
_, thresh_simple = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
plt.subplot(2, 3, 2)
plt.imshow(thresh_simple, cmap='gray')
plt.title('Simple (thresh=127)')
plt.axis('off')

# Otsu's method
thresh_otsu = otsu_threshold(img)
_, binary_otsu = cv2.threshold(img, thresh_otsu, 255, cv2.THRESH_BINARY)
plt.subplot(2, 3, 3)
plt.imshow(binary_otsu, cmap='gray')
plt.title(f'Otsu (thresh={thresh_otsu})')
plt.axis('off')

# Adaptive threshold (mean)
thresh_adaptive_mean = cv2.adaptiveThreshold(img, 255, 
    cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
plt.subplot(2, 3, 4)
plt.imshow(thresh_adaptive_mean, cmap='gray')
plt.title('Adaptive (Mean)')
plt.axis('off')

# Adaptive threshold (Gaussian)
thresh_adaptive_gauss = cv2.adaptiveThreshold(img, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
plt.subplot(2, 3, 5)
plt.imshow(thresh_adaptive_gauss, cmap='gray')
plt.title('Adaptive (Gaussian)')
plt.axis('off')

# Histogram
hist = cv2.calcHist([img], [0], None, [256], [0, 256])
plt.subplot(2, 3, 6)
plt.plot(hist)
plt.axvline(thresh_otsu, color='r', linestyle='--', label=f'Otsu: {thresh_otsu}')
plt.title('Histogram')
plt.xlabel('Intensity')
plt.ylabel('Count')
plt.legend()

plt.tight_layout()
plt.show()

Watershed Segmentation
# Watershed: treats image as topographic surface
# Floods from markers, boundaries form segment borders
# Used for: separating touching objects

def watershed_segmentation(image):
    """Watershed segmentation."""
    # 1. Thresholding
    _, binary = cv2.threshold(image, 0, 255, 
                              cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # 2. Noise removal
    kernel = np.ones((3, 3), dtype=np.uint8)
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)
    
    # 3. Sure background (dilation)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    
    # 4. Sure foreground (distance transform + threshold)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 
                                255, 0)
    sure_fg = np.uint8(sure_fg)
    
    # 5. Unknown region (background - foreground)
    unknown = cv2.subtract(sure_bg, sure_fg)
    
    # 6. Marker labeling
    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1  # Background is 1, not 0
    markers[unknown == 255] = 0  # Unknown is 0
    
    # 7. Apply watershed
    markers = cv2.watershed(cv2.cvtColor(image, cv2.COLOR_GRAY2BGR), markers)
    
    # Mark boundaries
    result = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    result[markers == -1] = [0, 0, 255]  # Red boundaries
    
    return result, markers

# Example: separate touching circles
img = np.zeros((300, 400), dtype=np.uint8)
cv2.circle(img, (100, 150), 50, 255, -1)
cv2.circle(img, (160, 150), 50, 255, -1)  # Overlapping
cv2.circle(img, (280, 150), 60, 255, -1)

# Add noise
img = img + np.random.randint(0, 30, img.shape)
img = np.clip(img, 0, 255).astype(np.uint8)

result, markers = watershed_segmentation(img)

plt.figure(figsize=(12, 5))
plt.subplot(1, 3, 1)
plt.imshow(img, cmap='gray')
plt.title('Original (Touching Objects)')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(markers, cmap='nipy_spectral')
plt.title('Watershed Markers')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.title('Segmentation Result')
plt.axis('off')

plt.tight_layout()
plt.show()

GrabCut (Interactive Segmentation)
# GrabCut: graph-based segmentation with user input
# User provides rough bounding box or mask
# Algorithm iteratively refines segmentation

def grabcut_segmentation(image, iterations=5):
    """GrabCut segmentation."""
    # Initialize mask
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    
    # Define rectangle (foreground)
    h, w = image.shape[:2]
    rect = (int(w*0.1), int(h*0.1), int(w*0.8), int(h*0.8))
    
    # Initialize background and foreground models
    bgd_model = np.zeros((1, 65), dtype=np.float64)
    fgd_model = np.zeros((1, 65), dtype=np.float64)
    
    # Apply GrabCut
    cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 
                iterations, cv2.GC_INIT_WITH_RECT)
    
    # Create binary mask
    mask_binary = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    
    # Apply mask
    result = image * mask_binary[:, :, np.newaxis]
    
    return result, mask_binary

# Example
img = cv2.imread('person.jpg')
if img is None:
    # Create synthetic image
    img = np.zeros((400, 300, 3), dtype=np.uint8)
    cv2.rectangle(img, (100, 50), (200, 350), (100, 150, 200), -1)
    cv2.circle(img, (150, 100), 30, (200, 180, 150), -1)

result, mask = grabcut_segmentation(img)

plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Original')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(mask, cmap='gray')
plt.title('GrabCut Mask')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.title('Segmented')
plt.axis('off')

plt.tight_layout()
plt.show()

CHAPTER 5: OBJECT DETECTION
Template Matching
# Template matching: slide template over image, find best match
# Methods: correlation, squared difference, coefficient

def template_matching(image, template, method=cv2.TM_CCOEFF_NORMED):
    """Template matching."""
    result = cv2.matchTemplate(image, template, method)
    
    # Find locations above threshold
    threshold = 0.8
    locations = np.where(result >= threshold)
    
    # Get template size
    h, w = template.shape[:2]
    
    # Draw rectangles
    result_img = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    for pt in zip(*locations[::-1]):
        cv2.rectangle(result_img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
    
    # Find best match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        best_loc = min_loc
    else:
        best_loc = max_loc
    
    return result_img, result, best_loc

# Example: find objects in image
img = cv2.imread('scene.jpg', cv2.IMREAD_GRAYSCALE)
if img is None:
    # Create synthetic scene
    img = np.zeros((400, 600), dtype=np.uint8)
    # Add multiple instances of a pattern
    for pos in [(100, 100), (300, 150), (450, 250)]:
        cv2.rectangle(img, pos, (pos[0]+50, pos[1]+50), 200, -1)
        cv2.circle(img, (pos[0]+25, pos[1]+25), 15, 100, -1)

# Template (one instance)
template = img[100:150, 100:150].copy()

result_img, match_result, best_loc = template_matching(img, template)

plt.figure(figsize=(12, 5))
plt.subplot(1, 3, 1)
plt.imshow(img, cmap='gray')
plt.title('Image')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(template, cmap='gray')
plt.title('Template')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(match_result, cmap='hot')
plt.title('Match Result')
plt.axis('off')

plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
plt.imshow(cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB))
plt.title(f'Detected Objects (best at {best_loc})')
plt.axis('off')
plt.show()

HOG + SVM (Histogram of Oriented Gradients)
# HOG: feature descriptor for object detection
# Counts gradient orientations in localized regions
# Combined with SVM classifier for detection

def compute_hog_features(image, cell_size=8, bins=9):
    """Compute HOG features."""
    # Compute gradients
    gx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    
    # Magnitude and orientation
    magnitude = np.sqrt(gx**2 + gy**2)
    orientation = np.arctan2(gy, gx) * (180 / np.pi) % 180
    
    # Divide into cells
    h, w = image.shape
    cell_h, cell_w = cell_size, cell_size
    n_cells_h = h // cell_h
    n_cells_w = w // cell_w
    
    # Compute histogram for each cell
    hog_features = []
    
    for i in range(n_cells_h):
        for j in range(n_cells_w):
            cell_mag = magnitude[i*cell_h:(i+1)*cell_h, 
                                 j*cell_w:(j+1)*cell_w]
            cell_ori = orientation[i*cell_h:(i+1)*cell_h, 
                                   j*cell_w:(j+1)*cell_w]
            
            # Histogram
            hist = np.zeros(bins)
            for k in range(bins):
                mask = (cell_ori >= k * 180/bins) & \
                       (cell_ori < (k+1) * 180/bins)
                hist[k] = np.sum(cell_mag[mask])
            
            # Normalize
            hist = hist / (np.linalg.norm(hist) + 1e-6)
            hog_features.extend(hist)
    
    return np.array(hog_features)

# Example: pedestrian detection (simplified)
# In practice, use pre-trained HOG detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

img = cv2.imread('street.jpg')
if img is None:
    img = np.zeros((400, 600, 3), dtype=np.uint8)
    # Draw simple pedestrian-like shapes
    for x in [150, 300, 450]:
        cv2.rectangle(img, (x, 100), (x+50, 350), (100, 100, 100), -1)
        cv2.circle(img, (x+25, 80), 20, (100, 100, 100), -1)

# Detect pedestrians
rects, weights = hog.detectMultiScale(img, winStride=(8, 8), 
                                       padding=(8, 8), scale=1.05)

print(f"Detected {len(rects)} pedestrians")

# Draw rectangles
for (x, y, w, h) in rects:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

plt.figure(figsize=(10, 5))
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title(f'HOG Pedestrian Detection ({len(rects)} detected)')
plt.axis('off')
plt.show()

Haar Cascades
# Haar cascades: machine learning-based object detection
# Uses Haar-like features and cascade of classifiers
# Fast but less accurate than deep learning methods

def detect_faces_haar(image):
    """Detect faces using Haar cascades."""
    # Load cascade classifier
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    eye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_eye.xml'
    )
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, 
                                           minNeighbors=5, minSize=(30, 30))
    
    # Detect eyes for each face
    result = image.copy()
    for (x, y, w, h) in faces:
        # Draw face rectangle
        cv2.rectangle(result, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # ROI for eyes
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = result[y:y+h, x:x+w]
        
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
    
    return result, faces

# Example
img = cv2.imread('faces.jpg')
if img is None:
    # Create synthetic face-like image
    img = np.ones((400, 400, 3), dtype=np.uint8) * 200
    # Face
    cv2.circle(img, (200, 200), 100, (180, 150, 120), -1)
    # Eyes
    cv2.circle(img, (160, 180), 15, (255, 255, 255), -1)
    cv2.circle(img, (240, 180), 15, (255, 255, 255), -1)
    cv2.circle(img, (160, 180), 8, (0, 0, 0), -1)
    cv2.circle(img, (240, 180), 8, (0, 0, 0), -1)
    # Mouth
    cv2.ellipse(img, (200, 250), (30, 15), 0, 0, 180, (0, 0, 0), 2)

result, faces = detect_faces_haar(img)
print(f"Detected {len(faces)} faces")

plt.figure(figsize=(8, 5))
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.title(f'Face Detection ({len(faces)} faces)')
plt.axis('off')
plt.show()

CHAPTER 6: DEEP LEARNING FOR COMPUTER VISION
CNN Basics
# Convolutional Neural Network: learns hierarchical features
# Layers: convolution, pooling, fully connected
# Used for: classification, detection, segmentation

import numpy as np

class Conv2D:
    """2D Convolution layer."""
    
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0):
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        
        # Initialize weights (Xavier initialization)
        scale = np.sqrt(2.0 / (in_channels * kernel_size * kernel_size))
        self.weights = np.random.randn(out_channels, in_channels, 
                                        kernel_size, kernel_size) * scale
        self.bias = np.zeros(out_channels)
    
    def forward(self, x):
        """Forward pass."""
        batch_size, in_channels, h, w = x.shape
        
        # Padding
        if self.padding > 0:
            x = np.pad(x, ((0, 0), (0, 0), 
                           (self.padding, self.padding), 
                           (self.padding, self.padding)))
        
        # Output dimensions
        h_out = (h + 2*self.padding - self.kernel_size) // self.stride + 1
        w_out = (w + 2*self.padding - self.kernel_size) // self.stride + 1
        
        output = np.zeros((batch_size, self.out_channels, h_out, w_out))
        
        # Convolution
        for i in range(h_out):
            for j in range(w_out):
                # Extract receptive field
                h_start = i * self.stride
                h_end = h_start + self.kernel_size
                w_start = j * self.stride
                w_end = w_start + self.kernel_size
                
                x_field = x[:, :, h_start:h_end, w_start:w_end]
                
                # Compute convolution
                for c in range(self.out_channels):
                    output[:, c, i, j] = np.sum(
                        x_field * self.weights[c], axis=(1, 2, 3)
                    ) + self.bias[c]
        
        return output

class MaxPool2D:
    """2D Max Pooling layer."""
    
    def __init__(self, kernel_size, stride=None):
        self.kernel_size = kernel_size
        self.stride = stride if stride else kernel_size
    
    def forward(self, x):
        """Forward pass."""
        batch_size, channels, h, w = x.shape
        
        h_out = (h - self.kernel_size) // self.stride + 1
        w_out = (w - self.kernel_size) // self.stride + 1
        
        output = np.zeros((batch_size, channels, h_out, w_out))
        
        for i in range(h_out):
            for j in range(w_out):
                h_start = i * self.stride
                h_end = h_start + self.kernel_size
                w_start = j * self.stride
                w_end = w_start + self.kernel_size
                
                output[:, :, i, j] = np.max(
                    x[:, :, h_start:h_end, w_start:w_end], axis=(2, 3)
                )
        
        return output

class ReLU:
    """ReLU activation."""
    
    def forward(self, x):
        return np.maximum(0, x)

class SimpleCNN:
    """Simple CNN for image classification."""
    
    def __init__(self, num_classes=10):
        # Conv -> ReLU -> Pool -> Conv -> ReLU -> Pool -> FC
        self.conv1 = Conv2D(3, 16, kernel_size=3, padding=1)
        self.relu1 = ReLU()
        self.pool1 = MaxPool2D(2)
        
        self.conv2 = Conv2D(16, 32, kernel_size=3, padding=1)
        self.relu2 = ReLU()
        self.pool2 = MaxPool2D(2)
        
        self.num_classes = num_classes
    
    def forward(self, x):
        """Forward pass."""
        # x shape: (batch, 3, 224, 224)
        x = self.conv1.forward(x)
        x = self.relu1.forward(x)
        x = self.pool1.forward(x)  # (batch, 16, 112, 112)
        
        x = self.conv2.forward(x)
        x = self.relu2.forward(x)
        x = self.pool2.forward(x)  # (batch, 32, 56, 56)
        
        # Flatten
        batch_size = x.shape[0]
        x = x.reshape(batch_size, -1)  # (batch, 32*56*56)
        
        # FC layer (simplified)
        fc_weights = np.random.randn(x.shape[1], self.num_classes) * 0.01
        output = x @ fc_weights
        
        return output

# Example
cnn = SimpleCNN(num_classes=10)
dummy_input = np.random.randn(2, 3, 224, 224)  # Batch of 2 images
output = cnn.forward(dummy_input)
print(f"CNN output shape: {output.shape}")  # (2, 10)

YOLO (You Only Look Once)
# YOLO: real-time object detection
# Single neural network predicts bounding boxes and class probabilities
# Fast: processes images in real-time

# YOLO architecture (simplified):
# 1. Backbone: feature extraction (Darknet, CSPDarknet)
# 2. Neck: feature fusion (FPN, PAN)
# 3. Head: prediction (bounding boxes, objectness, classes)

def yolo_prediction_demo():
    """Demonstrate YOLO-style prediction (simplified)."""
    # In practice, use pre-trained YOLO model
    # from ultralytics import YOLO
    # model = YOLO('yolov8n.pt')
    # results = model('image.jpg')
    
    # Simulated prediction
    img = np.zeros((416, 416, 3), dtype=np.uint8)
    
    # Simulated detections
    detections = [
        {'class': 'person', 'confidence': 0.95, 'bbox': (100, 100, 200, 300)},
        {'class': 'car', 'confidence': 0.87, 'bbox': (250, 200, 350, 280)},
        {'class': 'dog', 'confidence': 0.78, 'bbox': (50, 250, 120, 320)},
    ]
    
    # Draw detections
    colors = {'person': (0, 255, 0), 'car': (255, 0, 0), 'dog': (0, 0, 255)}
    
    for det in detections:
        x1, y1, x2, y2 = det['bbox']
        color = colors[det['class']]
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        
        label = f"{det['class']} {det['confidence']:.2f}"
        cv2.putText(img, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, color, 2)
    
    return img, detections

result_img, detections = yolo_prediction_demo()

plt.figure(figsize=(8, 5))
plt.imshow(result_img)
plt.title(f'YOLO Detection ({len(detections)} objects)')
plt.axis('off')
plt.show()

for det in detections:
    print(f"  {det['class']}: {det['confidence']:.2f} at {det['bbox']}")

Transfer Learning
# Transfer learning: use pre-trained model, fine-tune for specific task
# Benefits: faster training, better performance with less data

# Example: fine-tune ResNet for custom classification
def transfer_learning_example():
    """Transfer learning with pre-trained model (conceptual)."""
    # In practice:
    # import torch
    # import torchvision.models as models
    # 
    # # Load pre-trained ResNet
    # model = models.resnet50(pretrained=True)
    # 
    # # Freeze all layers
    # for param in model.parameters():
    #     param.requires_grad = False
    # 
    # # Replace final layer for custom classes
    # num_classes = 5  # Your dataset
    # model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
    # 
    # # Train only final layer
    # optimizer = torch.optim.Adam(model.fc.parameters(), lr=0.001)
    
    print("Transfer learning example (conceptual)")
    print("1. Load pre-trained model (ResNet, VGG, EfficientNet)")
    print("2. Freeze feature extractor layers")
    print("3. Replace classifier head for your task")
    print("4. Fine-tune on your dataset")
    print("5. Optionally unfreeze and train entire network")

transfer_learning_example()

CHAPTER 7: IMAGE GEOMETRY AND TRANSFORMATIONS
Geometric Transformations
# Geometric transformations: change image geometry
# Types: translation, rotation, scaling, affine, perspective

def translate_image(image, tx, ty):
    """Translate image by (tx, ty)."""
    h, w = image.shape[:2]
    M = np.float32([[1, 0, tx], [0, 1, ty]])
    return cv2.warpAffine(image, M, (w, h))

def rotate_image(image, angle, center=None, scale=1.0):
    """Rotate image by angle (degrees)."""
    h, w = image.shape[:2]
    if center is None:
        center = (w // 2, h // 2)
    
    M = cv2.getRotationMatrix2D(center, angle, scale)
    return cv2.warpAffine(image, M, (w, h))

def scale_image(image, fx, fy):
    """Scale image by factors (fx, fy)."""
    return cv2.resize(image, None, fx=fx, fy=fy, interpolation=cv2.INTER_LINEAR)

def affine_transform(image, pts_src, pts_dst):
    """Affine transformation (preserve parallel lines)."""
    M = cv2.getAffineTransform(pts_src.astype(np.float32), 
                                pts_dst.astype(np.float32))
    h, w = image.shape[:2]
    return cv2.warpAffine(image, M, (w, h))

def perspective_transform(image, pts_src, pts_dst):
    """Perspective transformation (projective)."""
    M = cv2.getPerspectiveTransform(pts_src.astype(np.float32), 
                                     pts_dst.astype(np.float32))
    h, w = image.shape[:2]
    return cv2.warpPerspective(image, M, (w, h))

# Example
img = cv2.imread('document.jpg')
if img is None:
    img = np.zeros((300, 400, 3), dtype=np.uint8)
    cv2.rectangle(img, (50, 50), (350, 250), (0, 255, 0), 3)
    cv2.putText(img, "Transform", (100, 160), cv2.FONT_HERSHEY_SIMPLEX, 
                2, (255, 255, 255), 3)

plt.figure(figsize=(14, 8))

plt.subplot(2, 3, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Original')
plt.axis('off')

plt.subplot(2, 3, 2)
translated = translate_image(img, 50, 30)
plt.imshow(cv2.cvtColor(translated, cv2.COLOR_BGR2RGB))
plt.title('Translation (50, 30)')
plt.axis('off')

plt.subplot(2, 3, 3)
rotated = rotate_image(img, 30)
plt.imshow(cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB))
plt.title('Rotation (30°)')
plt.axis('off')

plt.subplot(2, 3, 4)
scaled = scale_image(img, 1.5, 1.5)
plt.imshow(cv2.cvtColor(scaled, cv2.COLOR_BGR2RGB))
plt.title('Scaling (1.5x)')
plt.axis('off')

# Affine transformation
h, w = img.shape[:2]
pts_src = np.array([[0, 0], [w-1, 0], [0, h-1]])
pts_dst = np.array([[0, h*0.25], [w*0.85, h*0.15], [w*0.15, h*0.7]])
affine = affine_transform(img, pts_src, pts_dst)
plt.subplot(2, 3, 5)
plt.imshow(cv2.cvtColor(affine, cv2.COLOR_BGR2RGB))
plt.title('Affine Transform')
plt.axis('off')

# Perspective transformation
pts_src = np.array([[0, 0], [w-1, 0], [w-1, h-1], [0, h-1]])
pts_dst = np.array([[w*0.1, h*0.1], [w*0.9, 0], [w, h], [0, h*0.9]])
perspective = perspective_transform(img, pts_src, pts_dst)
plt.subplot(2, 3, 6)
plt.imshow(cv2.cvtColor(perspective, cv2.COLOR_BGR2RGB))
plt.title('Perspective Transform')
plt.axis('off')

plt.tight_layout()
plt.show()

Homography
# Homography: 3x3 matrix mapping points between two planes
# Used for: image stitching, augmented reality, document scanning

def compute_homography(pts1, pts2):
    """Compute homography matrix using DLT (Direct Linear Transform)."""
    # Build system of equations
    A = []
    for i in range(len(pts1)):
        x1, y1 = pts1[i]
        x2, y2 = pts2[i]
        A.append([-x1, -y1, -1, 0, 0, 0, x2*x1, x2*y1, x2])
        A.append([0, 0, 0, -x1, -y1, -1, y2*x1, y2*y1, y2])
    
    A = np.array(A)
    
    # Solve using SVD
    U, S, Vt = np.linalg.svd(A)
    H = Vt[-1].reshape(3, 3)
    H = H / H[2, 2]  # Normalize
    
    return H

def apply_homography(points, H):
    """Apply homography to points."""
    points = np.array(points)
    points_homogeneous = np.column_stack([points, np.ones(len(points))])
    
    # Apply transformation
    transformed = points_homogeneous @ H.T
    transformed = transformed[:, :2] / transformed[:, 2:3]
    
    return transformed

# Example: image stitching
def stitch_images(img1, img2):
    """Stitch two images using homography."""
    # Detect features
    orb = cv2.ORB_create(1000)
    kp1, desc1 = orb.detectAndCompute(img1, None)
    kp2, desc2 = orb.detectAndCompute(img2, None)
    
    if desc1 is None or desc2 is None:
        return None
    
    # Match features
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(desc1, desc2)
    matches = sorted(matches, key=lambda x: x.distance)
    
    # Extract matched points
    pts1 = np.float32([kp1[m.queryIdx].pt for m in matches[:50]]).reshape(-1, 1, 2)
    pts2 = np.float32([kp2[m.trainIdx].pt for m in matches[:50]]).reshape(-1, 1, 2)
    
    # Compute homography
    H, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC, 5.0)
    
    # Warp img1
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    
    img1_warped = cv2.warpPerspective(img1, H, (w1+w2, max(h1, h2)))
    
    # Blend
    result = img1_warped.copy()
    result[0:h2, 0:w2] = img2
    
    return result

# Example
img1 = cv2.imread('left.jpg')
img2 = cv2.imread('right.jpg')

if img1 is not None and img2 is not None:
    stitched = stitch_images(img1, img2)
    if stitched is not None:
        plt.figure(figsize=(12, 5))
        plt.imshow(cv2.cvtColor(stitched, cv2.COLOR_BGR2RGB))
        plt.title('Stitched Image')
        plt.axis('off')
        plt.show()

CHAPTER 8: 3D VISION AND DEPTH
Stereo Vision
# Stereo vision: compute depth from two cameras
# Disparity = x_left - x_right
# Depth = (focal_length * baseline) / disparity

def compute_disparity_map(img_left, img_right, num_disparities=16, block_size=15):
    """Compute disparity map using block matching."""
    # Convert to grayscale
    gray_left = cv2.cvtColor(img_left, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2GRAY)
    
    # Stereo block matching
    stereo = cv2.StereoBM_create(numDisparities=num_disparities, 
                                  blockSize=block_size)
    disparity = stereo.compute(gray_left, gray_right)
    
    # Normalize for visualization
    disparity_norm = cv2.normalize(disparity, None, 0, 255, 
                                    cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    
    return disparity, disparity_norm

def disparity_to_depth(disparity, focal_length, baseline):
    """Convert disparity to depth."""
    # Avoid division by zero
    disparity = np.where(disparity > 0, disparity, 1)
    depth = (focal_length * baseline) / disparity
    return depth

# Example: synthetic stereo pair
def create_synthetic_stereo():
    """Create synthetic stereo pair with known depth."""
    # Create scene with objects at different depths
    img_left = np.zeros((400, 600, 3), dtype=np.uint8)
    img_right = np.zeros((400, 600, 3), dtype=np.uint8)
    
    # Object 1 (close, large disparity)
    cv2.rectangle(img_left, (100, 100), (200, 200), (255, 0, 0), -1)
    cv2.rectangle(img_right, (120, 100), (220, 200), (255, 0, 0), -1)  # Shifted right
    
    # Object 2 (medium depth)
    cv2.circle(img_left, (400, 200), 50, (0, 255, 0), -1)
    cv2.circle(img_right, (410, 200), 50, (0, 255, 0), -1)
    
    # Object 3 (far, small disparity)
    cv2.rectangle(img_left, (450, 280), (550, 350), (0, 0, 255), -1)
    cv2.rectangle(img_right, (455, 280), (555, 350), (0, 0, 255), -1)
    
    return img_left, img_right

img_left, img_right = create_synthetic_stereo()
disparity, disparity_norm = compute_disparity_map(img_left, img_right)

# Convert to depth (assuming focal_length=500, baseline=0.1m)
depth = disparity_to_depth(disparity, focal_length=500, baseline=0.1)

plt.figure(figsize=(14, 8))

plt.subplot(2, 2, 1)
plt.imshow(cv2.cvtColor(img_left, cv2.COLOR_BGR2RGB))
plt.title('Left Image')
plt.axis('off')

plt.subplot(2, 2, 2)
plt.imshow(cv2.cvtColor(img_right, cv2.COLOR_BGR2RGB))
plt.title('Right Image')
plt.axis('off')

plt.subplot(2, 2, 3)
plt.imshow(disparity_norm, cmap='jet')
plt.title('Disparity Map')
plt.axis('off')
plt.colorbar(label='Disparity')

plt.subplot(2, 2, 4)
plt.imshow(depth, cmap='jet', vmin=0, vmax=10)
plt.title('Depth Map')
plt.axis('off')
plt.colorbar(label='Depth (m)')

plt.tight_layout()
plt.show()

Point Clouds
# Point cloud: set of 3D points (X, Y, Z)
# Can be colored with RGB values
# Used for: 3D reconstruction, SLAM, object recognition

def depth_to_point_cloud(depth, rgb, fx, fy, cx, cy):
    """Convert depth map to point cloud."""
    h, w = depth.shape
    points = []
    colors = []
    
    for v in range(h):
        for u in range(w):
            Z = depth[v, u]
            if Z > 0:  # Valid depth
                # Back-project to 3D
                X = (u - cx) * Z / fx
                Y = (v - cy) * Z / fy
                
                points.append([X, Y, Z])
                colors.append(rgb[v, u])
    
    return np.array(points), np.array(colors)

def visualize_point_cloud(points, colors=None):
    """Visualize point cloud (simplified 2D projection)."""
    # Simple orthographic projection
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    
    # Color by depth
    if colors is None:
        colors = z
    
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(x, y, c=colors, s=1, cmap='jet')
    plt.colorbar(scatter, label='Depth')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Point Cloud (Top View)')
    plt.axis('equal')
    plt.grid(alpha=0.3)
    plt.show()

# Example: create point cloud from synthetic depth
h, w = 100, 100
depth_map = np.zeros((h, w))

# Create simple scene
for i in range(h):
    for j in range(w):
        # Sphere at center
        dist = np.sqrt((i - h/2)**2 + (j - w/2)**2)
        if dist < 30:
            depth_map[i, j] = 2.0 + dist * 0.05
        else:
            depth_map[i, j] = 5.0

# Create RGB image
rgb = np.zeros((h, w, 3), dtype=np.uint8)
rgb[:, :, 0] = (depth_map * 50).astype(np.uint8)  # Red channel
rgb[:, :, 1] = 128
rgb[:, :, 2] = 255 - (depth_map * 50).astype(np.uint8)

# Convert to point cloud
fx, fy = 500, 500
cx, cy = w/2, h/2
points, colors = depth_to_point_cloud(depth_map, rgb, fx, fy, cx, cy)

print(f"Point cloud: {len(points)} points")
visualize_point_cloud(points, depth_map)

Structure from Motion (SfM)
# SfM: reconstruct 3D structure from 2D images
# Steps: feature detection, matching, epipolar geometry, 
#        triangulation, bundle adjustment

def triangulate_points(P1, P2, pts1, pts2):
    """Triangulate 3D points from two views."""
    pts_4d = []
    
    for i in range(len(pts1)):
        # Build system of equations
        A = np.array([
            pts1[i, 0] * P1[2, :] - P1[0, :],
            pts1[i, 1] * P1[2, :] - P1[1, :],
            pts2[i, 0] * P2[2, :] - P2[0, :],
            pts2[i, 1] * P2[2, :] - P2[1, :]
        ])
        
        # Solve using SVD
        U, S, Vt = np.linalg.svd(A)
        X = Vt[-1]
        X = X / X[3]  # Convert to 3D
        
        pts_4d.append(X[:3])
    
    return np.array(pts_4d)

# Example: simple two-view reconstruction
def simple_sfm_demo():
    """Demonstrate SfM with synthetic data."""
    # 3D points (ground truth)
    pts_3d = np.array([
        [0, 0, 5],
        [1, 0, 5],
        [0, 1, 5],
        [1, 1, 5],
        [0.5, 0.5, 6]
    ])
    
    # Camera matrices (simplified)
    K = np.array([[500, 0, 320],
                  [0, 500, 240],
                  [0, 0, 1]])
    
    # Camera 1: at origin
    R1 = np.eye(3)
    t1 = np.zeros(3)
    P1 = K @ np.hstack([R1, t1.reshape(3, 1)])
    
    # Camera 2: translated
    R2 = np.eye(3)
    t2 = np.array([1, 0, 0])
    P2 = K @ np.hstack([R2, t2.reshape(3, 1)])
    
    # Project to 2D
    def project(pts, P):
        pts_hom = np.column_stack([pts, np.ones(len(pts))])
        pts_proj = pts_hom @ P.T
        pts_proj = pts_proj[:, :2] / pts_proj[:, 2:3]
        return pts_proj
    
    pts1 = project(pts_3d, P1)
    pts2 = project(pts_3d, P2)
    
    # Triangulate
    pts_reconstructed = triangulate_points(P1, P2, pts1, pts2)
    
    # Compute error
    error = np.linalg.norm(pts_3d - pts_reconstructed, axis=1)
    print(f"Reconstruction error: {error.mean():.4f} (mean), {error.max():.4f} (max)")
    
    return pts_3d, pts_reconstructed

pts_gt, pts_recon = simple_sfm_demo()

# Visualize
fig = plt.figure(figsize=(12, 5))

ax1 = fig.add_subplot(121, projection='3d')
ax1.scatter(pts_gt[:, 0], pts_gt[:, 1], pts_gt[:, 2], c='g', s=50, label='Ground Truth')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')
ax1.set_title('Ground Truth 3D Points')
ax1.legend()

ax2 = fig.add_subplot(122, projection='3d')
ax2.scatter(pts_recon[:, 0], pts_recon[:, 1], pts_recon[:, 2], c='r', s=50, label='Reconstructed')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
ax2.set_title('Reconstructed 3D Points')
ax2.legend()

plt.tight_layout()
plt.show()

CHAPTER 9: OPTICAL FLOW AND TRACKING
Optical Flow (Lucas-Kanade)
# Optical flow: estimate motion between frames
# Lucas-Kanade: sparse optical flow (track features)
# Farnebäck: dense optical flow (all pixels)

def lucas_kanade_optical_flow(prev_frame, curr_frame, prev_points):
    """Lucas-Kanade sparse optical flow."""
    # Parameters
    lk_params = dict(winSize=(15, 15),
                     maxLevel=2,
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 
                              10, 0.03))
    
    # Calculate optical flow
    curr_points, status, error = cv2.calcOpticalFlowPyrLK(
        prev_frame, curr_frame, prev_points, None, **lk_params
    )
    
    # Select good points
    good_prev = prev_points[status == 1]
    good_curr = curr_points[status == 1]
    
    return good_prev, good_curr, status

def farneback_dense_optical_flow(prev_frame, curr_frame):
    """Farnebäck dense optical flow."""
    flow = cv2.calcOpticalFlowFarneback(
        prev_frame, curr_frame, None,
        pyr_scale=0.5, levels=3, winsize=15,
        iterations=3, poly_n=5, poly_sigma=1.2, flags=0
    )
    
    # Convert to magnitude and angle
    magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    
    return flow, magnitude, angle

# Example: track features in video
def track_features_video():
    """Track features in synthetic video."""
    # Create synthetic video frames
    frames = []
    for i in range(30):
        frame = np.zeros((400, 600), dtype=np.uint8)
        
        # Moving object
        x = 100 + i * 10
        y = 200 + int(50 * np.sin(i * 0.2))
        cv2.rectangle(frame, (x, y), (x+50, y+50), 255, -1)
        
        # Static background features
        cv2.circle(frame, (50, 50), 10, 128, -1)
        cv2.circle(frame, (550, 350), 15, 128, -1)
        
        frames.append(frame)
    
    # Detect features in first frame
    feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7)
    prev_gray = frames[0]
    prev_points = cv2.goodFeaturesToTrack(prev_gray, **feature_params)
    
    # Track through frames
    tracks = []
    for i in range(1, len(frames)):
        curr_gray = frames[i]
        prev_pts, curr_pts, status = lucas_kanade_optical_flow(
            prev_gray, curr_gray, prev_points
        )
        
        tracks.append((prev_pts, curr_pts))
        prev_gray = curr_gray
        prev_points = curr_pts
    
    return frames, tracks

frames, tracks = track_features_video()

# Visualize
fig, axes = plt.subplots(2, 3, figsize=(14, 8))

for i, ax in enumerate(axes.flat):
    if i < len(frames):
        frame = cv2.cvtColor(frames[i], cv2.COLOR_GRAY2BGR)
        
        # Draw tracks
        if i > 0 and i-1 < len(tracks):
            prev_pts, curr_pts = tracks[i-1]
            for j, (p1, p2) in enumerate(zip(prev_pts, curr_pts)):
                x1, y1 = int(p1[0]), int(p1[1])
                x2, y2 = int(p2[0]), int(p2[1])
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(frame, (x2, y2), 5, (0, 0, 255), -1)
        
        ax.imshow(frame)
        ax.set_title(f'Frame {i}')
        ax.axis('off')

plt.tight_layout()
plt.show()

# Dense optical flow
prev_frame = frames[10]
curr_frame = frames[15]
flow, magnitude, angle = farneback_dense_optical_flow(prev_frame, curr_frame)

plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.imshow(prev_frame, cmap='gray')
plt.title('Previous Frame')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(magnitude, cmap='hot')
plt.title('Flow Magnitude')
plt.axis('off')
plt.colorbar()

plt.subplot(1, 3, 3)
plt.imshow(angle, cmap='hsv')
plt.title('Flow Direction')
plt.axis('off')
plt.colorbar()

plt.tight_layout()
plt.show()

Object Tracking (KCF, MOSSE)
# KCF (Kernelized Correlation Filter): fast object tracker
# MOSSE: very fast, robust to illumination changes

def kcf_tracking_demo():
    """Demonstrate KCF tracking."""
    # Create video with moving object
    frames = []
    for i in range(50):
        frame = np.zeros((400, 600, 3), dtype=np.uint8)
        
        # Moving object
        x = 100 + i * 5
        y = 200 + int(30 * np.sin(i * 0.1))
        cv2.rectangle(frame, (x, y), (x+80, y+80), (0, 255, 0), -1)
        cv2.putText(frame, "Target", (x+10, y+45), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Background
        cv2.circle(frame, (50, 50), 20, (255, 0, 0), -1)
        cv2.circle(frame, (550, 350), 25, (0, 0, 255), -1)
        
        frames.append(frame)
    
    # Initialize tracker
    tracker = cv2.TrackerKCF_create()
    
    # Initialize with first frame and bounding box
    bbox = (100, 200, 80, 80)  # (x, y, w, h)
    tracker.init(frames[0], bbox)
    
    # Track through frames
    tracked_frames = []
    for i, frame in enumerate(frames):
        success, bbox = tracker.update(frame)
        
        if success:
            x, y, w, h = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
            cv2.putText(frame, f"Tracking (Frame {i})", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        tracked_frames.append(frame)
    
    return tracked_frames

tracked = kcf_tracking_demo()

# Visualize
fig, axes = plt.subplots(2, 3, figsize=(14, 8))
frame_indices = [0, 10, 20, 30, 40, 49]

for i, (ax, idx) in enumerate(zip(axes.flat, frame_indices)):
    if idx < len(tracked):
        ax.imshow(cv2.cvtColor(tracked[idx], cv2.COLOR_BGR2RGB))
        ax.set_title(f'Frame {idx}')
        ax.axis('off')

plt.tight_layout()
plt.show()

CHAPTER 10: ADVANCED TOPICS AND RESOURCES
Modern CV Architectures
# Vision Transformers (ViT): attention-based models
# ConvNeXt: modernized ConvNets
# DETR: end-to-end object detection with Transformers
# Segment Anything (SAM): universal segmentation

# ViT concept (simplified):
# 1. Split image into patches (e.g., 16x16)
# 2. Flatten and embed patches
# 3. Add positional encoding
# 4. Apply Transformer encoder
# 5. Classify using [CLS] token

def patch_embedding_demo(image, patch_size=16):
    """Demonstrate patch embedding for ViT."""
    h, w = image.shape[:2]
    
    # Extract patches
    patches = []
    for i in range(0, h, patch_size):
        for j in range(0, w, patch_size):
            patch = image[i:i+patch_size, j:j+patch_size]
            if patch.shape[:2] == (patch_size, patch_size):
                patches.append(patch.flatten())
    
    patches = np.array(patches)
    print(f"Image {h}x{w} → {len(patches)} patches of size {patch_size}x{patch_size}")
    print(f"Patch matrix shape: {patches.shape}")
    
    return patches

# Example
img = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
patches = patch_embedding_demo(img, patch_size=16)

# Visualization
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(img)
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(patches[:100].reshape(10, 10, -1)[:, :, :3] / 255.0)
plt.title('First 100 Patches (visualized)')
plt.axis('off')

plt.tight_layout()
plt.show()

Data Augmentation
# Data augmentation: artificially expand training dataset
# Techniques: rotation, flip, crop, color jitter, cutout, mixup

def augment_image(image):
    """Apply random augmentations."""
    augmented = image.copy()
    
    # Random horizontal flip
    if np.random.rand() > 0.5:
        augmented = cv2.flip(augmented, 1)
    
    # Random rotation
    angle = np.random.uniform(-15, 15)
    h, w = augmented.shape[:2]
    M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1.0)
    augmented = cv2.warpAffine(augmented, M, (w, h))
    
    # Random brightness
    brightness = np.random.uniform(0.8, 1.2)
    augmented = np.clip(augmented * brightness, 0, 255).astype(np.uint8)
    
    # Random contrast
    contrast = np.random.uniform(0.8, 1.2)
    mean = np.mean(augmented, axis=(0, 1), keepdims=True)
    augmented = np.clip((augmented - mean) * contrast + mean, 0, 255).astype(np.uint8)
    
    # Random crop and resize
    if np.random.rand() > 0.5:
        crop_size = int(min(h, w) * np.random.uniform(0.8, 1.0))
        x = np.random.randint(0, w - crop_size + 1)
        y = np.random.randint(0, h - crop_size + 1)
        cropped = augmented[y:y+crop_size, x:x+crop_size]
        augmented = cv2.resize(cropped, (w, h))
    
    return augmented

# Example
img = cv2.imread('cat.jpg')
if img is None:
    img = np.zeros((300, 400, 3), dtype=np.uint8)
    cv2.rectangle(img, (100, 50), (300, 250), (100, 150, 200), -1)
    cv2.circle(img, (200, 150), 50, (200, 180, 150), -1)

plt.figure(figsize=(14, 8))
plt.subplot(2, 4, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Original')
plt.axis('off')

for i in range(2, 9):
    augmented = augment_image(img)
    plt.subplot(2, 4, i)
    plt.imshow(cv2.cvtColor(augmented, cv2.COLOR_BGR2RGB))
    plt.title(f'Augmented {i-1}')
    plt.axis('off')

plt.tight_layout()
plt.show()

Evaluation Metrics
# Classification: accuracy, precision, recall, F1, confusion matrix
# Detection: IoU, mAP, precision-recall curves
# Segmentation: IoU, Dice coefficient, pixel accuracy

def compute_iou(box1, box2):
    """Compute Intersection over Union."""
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    
    # Intersection
    xi1 = max(x1, x2)
    yi1 = max(y1, y2)
    xi2 = min(x1 + w1, x2 + w2)
    yi2 = min(y1 + h1, y2 + h2)
    
    inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)
    
    # Union
    union_area = w1 * h1 + w2 * h2 - inter_area
    
    iou = inter_area / union_area if union_area > 0 else 0
    return iou

def compute_confusion_matrix(y_true, y_pred, num_classes):
    """Compute confusion matrix."""
    cm = np.zeros((num_classes, num_classes), dtype=int)
    for true, pred in zip(y_true, y_pred):
        cm[true, pred] += 1
    return cm

def compute_metrics(cm):
    """Compute precision, recall, F1 from confusion matrix."""
    precision = np.zeros(cm.shape[0])
    recall = np.zeros(cm.shape[0])
    f1 = np.zeros(cm.shape[0])
    
    for i in range(cm.shape[0]):
        tp = cm[i, i]
        fp = cm[:, i].sum() - tp
        fn = cm[i, :].sum() - tp
        
        precision[i] = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall[i] = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1[i] = 2 * precision[i] * recall[i] / (precision[i] + recall[i]) \
                if (precision[i] + recall[i]) > 0 else 0
    
    return precision, recall, f1

# Example
y_true = [0, 0, 1, 1, 2, 2, 0, 1, 2, 1]
y_pred = [0, 1, 1, 1, 2, 0, 0, 1, 2, 2]

cm = compute_confusion_matrix(y_true, y_pred, num_classes=3)
precision, recall, f1 = compute_metrics(cm)

print("Confusion Matrix:")
print(cm)
print(f"\nClass 0: P={precision[0]:.2f}, R={recall[0]:.2f}, F1={f1[0]:.2f}")
print(f"Class 1: P={precision[1]:.2f}, R={recall[1]:.2f}, F1={f1[1]:.2f}")
print(f"Class 2: P={precision[2]:.2f}, R={recall[2]:.2f}, F1={f1[2]:.2f}")

# IoU example
box1 = (100, 100, 50, 50)
box2 = (120, 120, 50, 50)
iou = compute_iou(box1, box2)
print(f"\nIoU between {box1} and {box2}: {iou:.3f}")

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].imshow(cm, cmap='Blues')
axes[0].set_title('Confusion Matrix')
axes[0].set_xlabel('Predicted')
axes[0].set_ylabel('True')
for i in range(3):
    for j in range(3):
        axes[0].text(j, i, str(cm[i, j]), ha='center', va='center')

# IoU visualization
img = np.zeros((300, 300, 3), dtype=np.uint8)
x1, y1, w1, h1 = box1
x2, y2, w2, h2 = box2
cv2.rectangle(img, (x1, y1), (x1+w1, y1+h1), (255, 0, 0), 2)
cv2.rectangle(img, (x2, y2), (x2+w2, y2+h2), (0, 255, 0), 2)

# Intersection
xi1, yi1 = max(x1, x2), max(y1, y2)
xi2, yi2 = min(x1+w1, x2+w2), min(y1+h1, y2+h2)
cv2.rectangle(img, (xi1, yi1), (xi2, yi2), (0, 0, 255), -1)

axes[1].imshow(img)
axes[1].set_title(f'IoU = {iou:.3f}')
axes[1].axis('off')

plt.tight_layout()
plt.show()

Recommended Reading
# - "Computer Vision: Algorithms and Applications" by Szeliski (free online)
# - "Multiple View Geometry in Computer Vision" by Hartley & Zisserman
# - "Deep Learning" by Goodfellow et al. (Chapter on CNNs)
# - "Programming Computer Vision with Python" by Jan Erik Solem

# Online Resources
# - OpenCV documentation: https://docs.opencv.org/
# - PyTorch Vision: https://pytorch.org/vision/
# - Papers with Code (CV): https://paperswithcode.com/area/computer-vision
# - Roboflow blog: https://blog.roboflow.com/
# - CVPR, ICCV, ECCV conference proceedings

# End of Computer Vision Reference