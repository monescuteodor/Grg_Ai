# Information Theory & Coding Reference

## Entropy & Information
- **Shannon Entropy H(X)**: Measure of uncertainty/randomness.
  - H(X) = -Σ P(x) log₂ P(x). Bits per symbol.
  - Max entropy for uniform distribution.
- **Joint Entropy H(X,Y)**: Uncertainty of pair (X,Y).
- **Conditional Entropy H(X|Y)**: Remaining uncertainty of X given Y.
- **Mutual Information I(X;Y)**: Amount of information shared between X and Y.
  - I(X;Y) = H(X) - H(X|Y) = H(Y) - H(Y|X).

## Source Coding (Compression)
- **Lossless Compression**: Original data can be perfectly reconstructed.
  - **Huffman Coding**: Variable-length codes based on frequency. Prefix-free. Optimal for symbol-by-symbol coding.
  - **LZW (Lempel-Ziv-Welch)**: Dictionary-based. Used in GIF, ZIP.
  - **Arithmetic Coding**: Encodes entire message into single number. More efficient than Huffman.
- **Lossy Compression**: Some data lost. Acceptable for audio/video/images.
  - **JPEG**: DCT (Discrete Cosine Transform), quantization, Huffman coding.
  - **MP3**: Psychoacoustic modeling, remove imperceptible frequencies.

## Channel Coding (Error Correction)
- **Goal**: Detect and correct errors introduced by noisy channel.
- **Hamming Distance**: Number of positions at which symbols differ.
  - Minimum distance d_min determines error detection/correction capability.
  - Detect up to d_min - 1 errors. Correct up to ⌊(d_min - 1)/2⌋ errors.
- **Parity Bit**: Simple error detection. Adds 1 bit to make total 1s even/odd.
- **Hamming Code**: Linear error-correcting code. Can correct 1-bit error.
- **Reed-Solomon Codes**: Block codes. Used in CDs, DVDs, QR codes, RAID. Corrects burst errors.
- **LDPC (Low-Density Parity-Check)**: Near-Shannon limit performance. Used in Wi-Fi, 5G.
- **Turbo Codes**: Iterative decoding. Used in 3G/4G.

## Channel Capacity
- **Shannon-Hartley Theorem**: C = B log₂(1 + S/N).
  - C: Channel capacity (bits/sec).
  - B: Bandwidth (Hz).
  - S/N: Signal-to-Noise ratio.
- **Nyquist Rate**: Maximum symbol rate for bandwidth B is 2B symbols/sec.

## Cryptography & Information Theory
- **Perfect Secrecy**: One-Time Pad. Key must be truly random, same length as message, used only once.
- **Entropy in Passwords**: Higher entropy = harder to guess. Mix characters, numbers, symbols.