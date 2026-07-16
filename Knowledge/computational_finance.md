Computational Finance & Algorithmic Trading Complete Reference
CHAPTER 1: GETTING STARTED WITH COMPUTATIONAL FINANCE
Remarks
Computational finance applies computer science and numerical methods to solve financial problems. Key areas: Algorithmic trading, risk management, derivative pricing (options, futures), portfolio optimization, and high-frequency trading (HFT). It combines stochastic calculus, statistics, and high-performance computing.
Tools: Python (NumPy, Pandas, SciPy), C++ (for low-latency execution), QuantLib, Zipline, Backtrader, Bloomberg API.
Hello Computational Finance
# hello_finance.py
"""
First finance program: Calculate simple and compound interest.
"""
import numpy as np

def simple_interest(principal, rate, time):
    """Calculate simple interest."""
    return principal * (1 + rate * time)

def compound_interest(principal, rate, time, n=1):
    """
    Calculate compound interest.
    n: number of times interest is compounded per year
    """
    return principal * (1 + rate/n)**(n*time)

def continuous_compounding(principal, rate, time):
    """Calculate continuous compounding."""
    return principal * np.exp(rate * time)

# Example
P = 1000  # Principal
r = 0.05  # Annual rate (5%)
t = 10    # Years

print("=== Interest Calculation ===")
print(f"Principal: ${P}")
print(f"Rate: {r*100}%")
print(f"Time: {t} years")
print(f"\nSimple Interest: ${simple_interest(P, r, t):.2f}")
print(f"Compound (Annual): ${compound_interest(P, r, t, n=1):.2f}")
print(f"Compound (Monthly): ${compound_interest(P, r, t, n=12):.2f}")
print(f"Continuous: ${continuous_compounding(P, r, t):.2f}")

Financial Data Structures
# Time Series: Ordered sequence of data points indexed in time order.
# OHLCV: Open, High, Low, Close, Volume (standard stock data format).
# Tick Data: Every single trade transaction (highest frequency).

import pandas as pd

def generate_sample_ohlcv(days=100):
    """Generate synthetic OHLCV data using random walk."""
    dates = pd.date_range(end=pd.Timestamp.today(), periods=days)
    prices = [100.0]
    
    for _ in range(days-1):
        change = np.random.normal(0, 1) # Random walk step
        prices.append(prices[-1] + change)
        
    df = pd.DataFrame({
        'Date': dates,
        'Open': prices,
        'High': [p + abs(np.random.normal(0, 0.5)) for p in prices],
        'Low': [p - abs(np.random.normal(0, 0.5)) for p in prices],
        'Close': prices,
        'Volume': np.random.randint(1000, 10000, days)
    })
    return df

df = generate_sample_ohlcv()
print("\nSample OHLCV Data:")
print(df.head())

CHAPTER 2: PORTFOLIO THEORY
Modern Portfolio Theory (MPT)
# Harry Markowitz (1952).
# Goal: Maximize expected return for a given level of risk.
# Risk is defined as variance (volatility) of returns.
# Efficient Frontier: Set of optimal portfolios offering highest return for each risk level.

def calculate_returns(prices):
    """Calculate daily logarithmic returns."""
    return np.log(prices / prices.shift(1)).dropna()

def portfolio_performance(weights, mean_returns, cov_matrix):
    """Calculate portfolio return and volatility."""
    port_return = np.sum(mean_returns * weights) * 252 # Annualize
    port_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix * 252, weights)))
    return port_return, port_vol

# Example: 3-Asset Portfolio
np.random.seed(42)
n_assets = 3
mean_returns = np.array([0.10, 0.15, 0.08]) # Expected annual returns
cov_matrix = np.array([
    [0.04, 0.006, 0.002],
    [0.006, 0.09, 0.004],
    [0.002, 0.004, 0.02]
])

# Equal weight portfolio
weights = np.array([1/3, 1/3, 1/3])
ret, vol = portfolio_performance(weights, mean_returns, cov_matrix)

print("\n=== Portfolio Performance ===")
print(f"Expected Annual Return: {ret:.2%}")
print(f"Annual Volatility (Risk): {vol:.2%}")
print(f"Sharpe Ratio (Rf=0): {ret/vol:.2f}")

Monte Carlo Simulation for Portfolios
# Simulate thousands of random weight combinations to find the Efficient Frontier.

def simulate_portfolios(n_assets, n_portfolios=10000):
    results = np.zeros((3, n_portfolios))
    
    for i in range(n_portfolios):
        weights = np.random.random(n_assets)
        weights /= np.sum(weights) # Normalize
        
        port_ret, port_vol = portfolio_performance(weights, mean_returns, cov_matrix)
        
        results[0, i] = port_vol
        results[1, i] = port_ret
        results[2, i] = port_ret / port_vol # Sharpe Ratio
        
    return results

results = simulate_portfolios(n_assets)

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.scatter(results[0, :], results[1, :], c=results[2, :], cmap='viridis', marker='o', s=10, alpha=0.6)
plt.colorbar(label='Sharpe Ratio')
plt.xlabel('Volatility (Risk)')
plt.ylabel('Expected Return')
plt.title('Efficient Frontier Simulation')
plt.grid(True)
plt.show()

CHAPTER 3: OPTION PRICING
Black-Scholes Model
# Analytical formula for pricing European options.
# Assumptions: Log-normal distribution, constant volatility, no dividends.

from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type='call'):
    """
    S: Spot price
    K: Strike price
    T: Time to maturity (years)
    r: Risk-free rate
    sigma: Volatility
    """
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2)*T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
    else: # put
        price = K * np.exp(-r*T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        
    return price

# Example
S = 100   # Stock price
K = 100   # At-the-money strike
T = 1     # 1 year
r = 0.05  # 5% risk-free rate
sigma = 0.2 # 20% volatility

call_price = black_scholes(S, K, T, r, sigma, 'call')
put_price = black_scholes(S, K, T, r, sigma, 'put')

print("\n=== Black-Scholes Pricing ===")
print(f"Call Option Price: ${call_price:.2f}")
print(f"Put Option Price: ${put_price:.2f}")
print(f"Put-Call Parity Check: {call_price - put_price:.2f} vs {S - K*np.exp(-r*T):.2f}")

Binomial Tree Model
# Numerical method for pricing options (can handle American options).
# Discretizes time into steps.

def binomial_tree(S, K, T, r, sigma, N=100, option_type='call'):
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r*dt) - d) / (u - d)
    
    # Initialize asset prices at maturity
    asset_prices = np.zeros(N+1)
    for j in range(N+1):
        asset_prices[j] = S * (u**j) * (d**(N-j))
        
    # Initialize option values at maturity
    option_values = np.zeros(N+1)
    for j in range(N+1):
        if option_type == 'call':
            option_values[j] = max(0, asset_prices[j] - K)
        else:
            option_values[j] = max(0, K - asset_prices[j])
            
    # Step back through tree
    for i in range(N-1, -1, -1):
        for j in range(i+1):
            option_values[j] = np.exp(-r*dt) * (p * option_values[j+1] + (1-p) * option_values[j])
            
    return option_values[0]

binomial_price = binomial_tree(S, K, T, r, sigma, N=100)
print(f"Binomial Tree Price: ${binomial_price:.2f}")

Greeks
# Sensitivities of option price to underlying parameters.
# Delta: Change in option price w.r.t. asset price.
# Gamma: Change in Delta w.r.t. asset price.
# Vega: Change in option price w.r.t. volatility.
# Theta: Change in option price w.r.t. time.
# Rho: Change in option price w.r.t. interest rate.

def calculate_delta(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2)*T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

delta = calculate_delta(S, K, T, r, sigma)
print(f"Call Delta: {delta:.4f}")

CHAPTER 4: ALGORITHMIC TRADING STRATEGIES
Moving Average Crossover
# Trend-following strategy.
# Buy when short-term MA crosses above long-term MA (Golden Cross).
# Sell when short-term MA crosses below long-term MA (Death Cross).

def moving_average_strategy(prices, short_window=20, long_window=50):
    signals = pd.DataFrame(index=prices.index)
    signals['price'] = prices
    
    signals['short_mavg'] = prices.rolling(window=short_window, min_periods=1).mean()
    signals['long_mavg'] = prices.rolling(window=long_window, min_periods=1).mean()
    
    signals['signal'] = 0.0
    signals['signal'][short_window:] = np.where(
        signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0
    )
    
    # Generate trading orders
    signals['positions'] = signals['signal'].diff()
    
    return signals

# Apply to sample data
signals = moving_average_strategy(df['Close'])
print("\n=== Moving Average Strategy Signals ===")
print(signals.tail(10))

Mean Reversion (Bollinger Bands)
# Assumes price will revert to its mean.
# Buy when price touches lower band.
# Sell when price touches upper band.

def bollinger_bands_strategy(prices, window=20, num_std=2):
    rolling_mean = prices.rolling(window=window).mean()
    rolling_std = prices.rolling(window=window).std()
    
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    
    signals = pd.DataFrame(index=prices.index)
    signals['price'] = prices
    signals['upper'] = upper_band
    signals['lower'] = lower_band
    
    signals['signal'] = 0.0
    signals['signal'] = np.where(prices < lower_band, 1.0, 0.0) # Buy
    signals['signal'] = np.where(prices > upper_band, -1.0, signals['signal']) # Sell
    
    return signals

bb_signals = bollinger_bands_strategy(df['Close'])
print("\n=== Bollinger Bands Signals ===")
print(bb_signals.tail(10))

Pairs Trading (Statistical Arbitrage)
# Identify two correlated assets.
# When spread diverges from historical mean, short the outperformer and buy the underperformer.
# Bet on convergence.

def pairs_trading_signal(price_a, price_b, window=60):
    # Calculate spread (log ratio)
    spread = np.log(price_a) - np.log(price_b)
    
    rolling_mean = spread.rolling(window=window).mean()
    rolling_std = spread.rolling(window=window).std()
    
    z_score = (spread - rolling_mean) / rolling_std
    
    signals = pd.DataFrame(index=price_a.index)
    signals['z_score'] = z_score
    signals['signal'] = 0.0
    
    # Entry thresholds
    signals['signal'] = np.where(z_score > 2, -1.0, signals['signal']) # Short A, Long B
    signals['signal'] = np.where(z_score < -2, 1.0, signals['signal']) # Long A, Short B
    
    # Exit when mean reverts
    signals['signal'] = np.where(np.abs(z_score) < 0.5, 0.0, signals['signal'])
    
    return signals

CHAPTER 5: RISK MANAGEMENT
Value at Risk (VaR)
# Maximum potential loss over a specific time period at a given confidence level.
# Methods: Historical, Parametric (Variance-Covariance), Monte Carlo.

def var_historical(returns, confidence_level=0.95):
    """Historical VaR."""
    return np.percentile(returns, (1 - confidence_level) * 100)

def var_parametric(mean, std, confidence_level=0.95):
    """Parametric VaR assuming normal distribution."""
    z_score = norm.ppf(1 - confidence_level)
    return mean + z_score * std

# Example
daily_returns = df['Close'].pct_change().dropna()
hist_var = var_historical(daily_returns)
param_var = var_parametric(daily_returns.mean(), daily_returns.std())

print("\n=== Value at Risk (Daily) ===")
print(f"Historical VaR (95%): {hist_var:.2%}")
print(f"Parametric VaR (95%): {param_var:.2%}")

Conditional Value at Risk (CVaR / Expected Shortfall)
# Average loss beyond the VaR threshold.
# More coherent risk measure than VaR.

def cvar_historical(returns, confidence_level=0.95):
    var_threshold = var_historical(returns, confidence_level)
    return returns[returns <= var_threshold].mean()

cvar = cvar_historical(daily_returns)
print(f"Conditional VaR (95%): {cvar:.2%}")

Maximum Drawdown
# Largest peak-to-trough decline in portfolio value.
# Measure of downside risk.

def max_drawdown(prices):
    cumulative_max = prices.cummax()
    drawdown = (prices - cumulative_max) / cumulative_max
    return drawdown.min()

mdd = max_drawdown(df['Close'])
print(f"Maximum Drawdown: {mdd:.2%}")

CHAPTER 6: HIGH-FREQUENCY TRADING (HFT) CONCEPTS
Market Microstructure
# Order Book: List of buy (bid) and sell (ask) orders.
# Spread: Difference between best bid and best ask.
# Liquidity: Ability to execute large orders without moving price.

# Limit Order: Execute at specified price or better.
# Market Order: Execute immediately at best available price.

Latency Arbitrage
# Exploiting speed differences in data transmission.
# Co-location: Placing servers physically close to exchange servers.
# FPGA/ASIC: Hardware acceleration for faster order processing.

Order Execution Algorithms
# VWAP (Volume Weighted Average Price): Execute orders proportional to historical volume profile.
# TWAP (Time Weighted Average Price): Execute orders evenly over time.
# Iceberg Orders: Hide large order size by showing only small portions.

CHAPTER 7: ADVANCED TOPICS AND RESOURCES
Machine Learning in Finance
# Feature Engineering: Technical indicators, sentiment analysis, macroeconomic data.
# Models: LSTM for time series, Random Forest for classification, Reinforcement Learning for execution.
# Challenges: Overfitting, non-stationarity, look-ahead bias.

Cryptocurrency Finance
# DeFi (Decentralized Finance): Automated Market Makers (AMMs), Yield Farming.
# On-chain Analysis: Tracking whale movements, gas fees.
# Volatility Modeling: GARCH models for crypto assets.

Regulatory Compliance
# MiFID II (Europe), Dodd-Frank (USA).
# Best Execution, Transaction Reporting, Algorithmic Trading Controls.

Recommended Reading
# - "Options, Futures, and Other Derivatives" by John C. Hull
# - "Algorithmic Trading" by Ernest Chan
# - "Advances in Financial Machine Learning" by Marcos López de Prado
# - "Quantitative Finance" by Paul Wilmott

# Online Resources
# - QuantConnect: https://www.quantconnect.com/
# - WorldQuant BRAIN: https://worldquantbrain.com/
# - Kaggle Finance Competitions: https://www.kaggle.com/competitions

# End of Computational Finance Reference