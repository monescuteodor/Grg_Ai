# Cryptography & Information Security Reference

## Symmetric Encryption
- **Block Ciphers**: Encrypt fixed-size blocks (e.g., 128 bits).
  - **AES (Advanced Encryption Standard)**: Rijndael algorithm. Substitution-Permutation Network. Key sizes: 128, 192, 256 bits.
  - **DES/3DES**: Older standards. DES is insecure (56-bit key). 3DES applies DES three times.
- **Stream Ciphers**: Encrypt bit-by-bit using a keystream.
  - **RC4**: Widely used but has vulnerabilities.
  - **ChaCha20**: Modern, fast, secure. Used in TLS.
- **Modes of Operation**:
  - **ECB (Electronic Codebook)**: Insecure for patterns.
  - **CBC (Cipher Block Chaining)**: Uses IV (Initialization Vector). Secure if IV is random.
  - **GCM (Galois/Counter Mode)**: Provides both confidentiality and integrity (AEAD).

## Asymmetric Encryption (Public-Key)
- **RSA**: Based on difficulty of factoring large integers.
  - Key generation: Choose primes p, q. n=pq. φ(n)=(p-1)(q-1). Choose e coprime to φ(n). d = e⁻¹ mod φ(n).
  - Public key: (n, e). Private key: (n, d).
  - Encryption: c = m^e mod n. Decryption: m = c^d mod n.
- **Elliptic Curve Cryptography (ECC)**: Based on discrete logarithm problem on elliptic curves.
  - Smaller keys for same security level as RSA.
  - Curve25519: Modern, fast, secure curve.
- **Diffie-Hellman (DH)**: Key exchange protocol. Allows two parties to establish shared secret over insecure channel.
  - ECDH: Elliptic Curve variant.

## Hash Functions
- **Properties**: Deterministic, pre-image resistant, second pre-image resistant, collision resistant.
- **SHA-256**: Secure Hash Algorithm. 256-bit output. Used in Bitcoin, TLS.
- **SHA-3**: Keccak algorithm. Different internal structure than SHA-2.
- **MD5/SHA-1**: Broken (collisions found). Do not use for security.
- **HMAC (Hash-based Message Authentication Code)**: Combines hash with secret key for integrity/authenticity.

## Digital Signatures
- **Purpose**: Authenticity, Integrity, Non-repudiation.
- **RSA Signature**: Sign with private key, verify with public key.
- **ECDSA (Elliptic Curve Digital Signature Algorithm)**: Used in Bitcoin, TLS.
- **EdDSA (Edwards-curve Digital Signature Algorithm)**: Faster, more secure than ECDSA. Uses Ed25519 curve.

## Protocols
- **TLS/SSL**: Secures web traffic. Handshake establishes session keys. Uses asymmetric for key exchange, symmetric for data.
- **SSH**: Secure Shell. Remote login. Uses public-key authentication.
- **PGP/GPG**: Pretty Good Privacy. Email encryption. Web of trust model.

## Attacks
- **Brute Force**: Try all keys. Prevented by long keys.
- **Side-Channel**: Analyze power consumption, timing, EM emissions.
- **Man-in-the-Middle (MitM)**: Intercept communication. Prevented by certificates/TLS.
- **Replay Attack**: Capture and resend valid data. Prevented by timestamps/nonces.