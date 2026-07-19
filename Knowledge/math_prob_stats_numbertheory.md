# Probability, Statistics & Number Theory Reference

## Probability Theory
### Basic Rules
- **Sample Space S**: Set of all possible outcomes.
- **Probability Axioms**: P(E) ≥ 0; P(S)=1; P(A∪B) = P(A)+P(B) if disjoint.
- **Conditional Probability**: P(A|B) = P(A∩B)/P(B).
- **Bayes' Theorem**: P(A|B) = [P(B|A)P(A)] / P(B). Updates belief based on evidence.
- **Independence**: P(A∩B) = P(A)P(B). Occurrence of one does not affect the other.

### Random Variables & Distributions
- **Discrete**: PMF P(X=x). Mean μ=ΣxP(x); Variance σ²=Σ(x-μ)²P(x).
- **Continuous**: PDF f(x). P(a≤X≤b)=∫_a^b f(x)dx. Mean μ=∫xf(x)dx.
- **Binomial Distribution**: P(X=k) = C(n,k)p^k(1-p)^(n-k). n trials, k successes.
- **Normal (Gaussian) Distribution**: f(x) = (1/σ√2π)e^(-(x-μ)²/2σ²). Bell curve. 68-95-99.7 rule.
- **Poisson Distribution**: P(X=k) = (λ^k e^-λ)/k!. Rare events in fixed interval.
- **Central Limit Theorem**: Sum of independent random variables tends toward Normal distribution as n→∞.

## Statistical Inference
### Estimation & Testing
- **Point Estimate**: Single value estimate of parameter (e.g., sample mean x̄ for μ).
- **Confidence Interval**: Range likely to contain true parameter. 95% CI: x̄ ± 1.96(σ/√n).
- **Hypothesis Testing**:
  - H₀ (Null Hypothesis): Default assumption (e.g., no effect).
  - H₁ (Alternative Hypothesis): Claim to test.
  - p-value: Probability of observing data if H₀ is true. p < 0.05 → Reject H₀.
- **Type I Error**: False Positive (Reject H₀ when true).
- **Type II Error**: False Negative (Fail to reject H₀ when false).
- **t-test**: Compares means of two groups. z-test for large samples/known σ.

### Regression & Correlation
- **Correlation Coefficient r**: Measures linear relationship strength (-1 to 1).
- **Linear Regression**: y = mx + b. Least squares method minimizes Σ(y_i - ŷ_i)².
- **R-squared**: Proportion of variance in dependent variable explained by model.

## Number Theory
### Divisibility & Primes
- **Prime Number**: Integer >1 with only divisors 1 and itself.
- **Fundamental Theorem of Arithmetic**: Every integer >1 has unique prime factorization.
- **Euclidean Algorithm**: Efficiently finds gcd(a,b). gcd(a,b) = gcd(b, a mod b).
- **Bezout's Identity**: gcd(a,b) = ax + by for some integers x,y.

### Modular Arithmetic
- **Congruence**: a ≡ b (mod n) if n|(a-b).
- **Fermat's Little Theorem**: If p is prime and p∤a, then a^(p-1) ≡ 1 (mod p).
- **Euler's Totient Function φ(n)**: Count of integers ≤n coprime to n. φ(p) = p-1 for prime p.
- **Euler's Theorem**: a^φ(n) ≡ 1 (mod n) if gcd(a,n)=1.
- **Chinese Remainder Theorem**: System of congruences x≡a_i (mod n_i) has unique solution mod N=Πn_i if n_i pairwise coprime.

### Cryptography Basics
- **RSA Encryption**:
  1. Choose primes p,q. Compute n=pq, φ(n)=(p-1)(q-1).
  2. Choose e coprime to φ(n). Compute d such that ed ≡ 1 (mod φ(n)).
  3. Public key (n,e); Private key (n,d).
  4. Encrypt: c = m^e mod n. Decrypt: m = c^d mod n.
- **Security**: Relies on difficulty of factoring large n.