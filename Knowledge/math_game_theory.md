# Game Theory & Decision Theory Reference

## Normal Form Games
### Basic Concepts
- **Players**: N = {1, 2, ..., n}.
- **Strategies**: Sᵢ for player i. Strategy profile s = (s₁, ..., sₙ).
- **Payoffs**: uᵢ(s) for player i. Rational players maximize payoff.

### Nash Equilibrium
- **Definition**: No player can improve payoff by unilaterally changing strategy.
- **Existence**: Every finite game has at least one Nash equilibrium (possibly mixed).
- **Pure vs Mixed**: Pure = deterministic choice. Mixed = probability distribution over strategies.

### Dominance
- **Strictly Dominated**: Strategy sᵢ is strictly dominated if another strategy sᵢ' always yields higher payoff.
- **Iterated Elimination**: Remove dominated strategies repeatedly. May simplify game.

## Specific Games
### Prisoner's Dilemma
- **Structure**: Two players, Cooperate (C) or Defect (D).
- **Payoffs**: T > R > P > S (Temptation > Reward > Punishment > Sucker).
- **Outcome**: Both defect (D,D) is Nash equilibrium, but (C,C) is Pareto optimal. Social dilemma.

### Battle of the Sexes
- **Coordination Game**: Two equilibria (A,A) and (B,B). Players prefer different equilibria.
- **Mixed Strategy**: Randomize to make opponent indifferent.

### Zero-Sum Games
- **Sum of Payoffs**: u₁(s) + u₂(s) = 0. One wins, other loses.
- **Minimax Theorem**: Maxmin = Minmax. Value of game V.
- **Solution**: Linear programming can find optimal mixed strategies.

## Extensive Form Games
### Game Trees
- **Nodes**: Decision points.
- **Edges**: Actions.
- **Information Sets**: Nodes indistinguishable to player. Imperfect information.

### Subgame Perfect Equilibrium (SPE)
- **Backward Induction**: Solve from end of tree to root.
- **Requirement**: Nash equilibrium in every subgame. Eliminates non-credible threats.

### Bayesian Games
- **Incomplete Information**: Players have private types.
- **Beliefs**: Probability distribution over opponents' types.
- **Bayesian Nash Equilibrium**: Strategy maximizes expected payoff given beliefs.

## Mechanism Design
### Inverse Game Theory
- **Goal**: Design rules/game so that rational play leads to desired outcome.
- **Incentive Compatibility**: Truth-telling is dominant strategy.
- **Vickrey-Clarke-Groves (VCG)**: Mechanism for efficient allocation with truthful bidding. Second-price auction.

### Auctions
- **First-Price**: Highest bidder pays bid. Shading strategy.
- **Second-Price (Vickrey)**: Highest bidder pays second-highest bid. Truthful bidding is dominant.
- **English/Dutch**: Open ascending/descending price.
- **Revenue Equivalence**: Under certain conditions, all standard auctions yield same expected revenue.