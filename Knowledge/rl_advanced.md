Reinforcement Learning Advanced Complete Reference
CHAPTER 1: GETTING STARTED WITH ADVANCED RL
Remarks
Reinforcement Learning (RL) trains agents to make sequential decisions by maximizing cumulative reward. Advanced topics: Policy Gradient methods (REINFORCE, PPO, TRPO), Actor-Critic architectures, Model-Based RL, Multi-Agent RL, Hierarchical RL, Offline RL, and Deep RL for continuous control. Applications: Robotics, Game Playing (AlphaGo, Dota 2), Autonomous Driving, Resource Management, Finance.
Tools: Python, PyTorch, TensorFlow, Stable Baselines3, Ray/RLLib, Gymnasium (OpenAI Gym successor), MuJoCo, Unity ML-Agents.
Hello RL
# hello_rl.py
"""
First RL program: Q-Learning on a simple grid world.
"""
import numpy as np
import random

class GridWorld:
    """Simple 4x4 grid world."""
    
    def __init__(self):
        self.size = 4
        self.state = 0  # Start at top-left
        self.goal = 15  # Bottom-right
        
    def reset(self):
        self.state = 0
        return self.state
    
    def step(self, action):
        """
        Actions: 0=Up, 1=Down, 2=Left, 3=Right
        Returns: (next_state, reward, done)
        """
        row, col = divmod(self.state, self.size)
        
        if action == 0:  # Up
            row = max(0, row - 1)
        elif action == 1:  # Down
            row = min(self.size - 1, row + 1)
        elif action == 2:  # Left
            col = max(0, col - 1)
        elif action == 3:  # Right
            col = min(self.size - 1, col + 1)
        
        next_state = row * self.size + col
        reward = -1  # Step penalty
        done = False
        
        if next_state == self.goal:
            reward = 100
            done = True
        
        self.state = next_state
        return next_state, reward, done

class QLearningAgent:
    """Q-Learning agent with epsilon-greedy exploration."""
    
    def __init__(self, n_states=16, n_actions=4, alpha=0.1, gamma=0.95, epsilon=0.1):
        self.q_table = np.zeros((n_states, n_actions))
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.n_actions = n_actions
    
    def choose_action(self, state):
        """Epsilon-greedy action selection."""
        if random.random() < self.epsilon:
            return random.randint(0, self.n_actions - 1)
        else:
            return np.argmax(self.q_table[state])
    
    def update(self, state, action, reward, next_state, done):
        """Update Q-value using Bellman equation."""
        best_next_q = np.max(self.q_table[next_state]) if not done else 0
        td_target = reward + self.gamma * best_next_q
        td_error = td_target - self.q_table[state, action]
        self.q_table[state, action] += self.alpha * td_error

# Training
env = GridWorld()
agent = QLearningAgent()

print("=== Q-Learning Training ===")
for episode in range(1000):
    state = env.reset()
    total_reward = 0
    
    while True:
        action = agent.choose_action(state)
        next_state, reward, done = env.step(action)
        agent.update(state, action, reward, next_state, done)
        
        total_reward += reward
        state = next_state
        
        if done:
            break
    
    if episode % 100 == 0:
        print(f"Episode {episode}: Total Reward = {total_reward}")

# Test the learned policy
print("\nLearned Q-Table:")
print(agent.q_table)

print("\nTest Run:")
state = env.reset()
path = [state]
for _ in range(20):
    action = np.argmax(agent.q_table[state])
    next_state, _, done = env.step(action)
    path.append(next_state)
    state = next_state
    if done:
        break

print(f"Path: {path}")
print(f"Goal reached: {state == 15}")

RL Taxonomy
# Value-Based Methods:
# - Learn value function V(s) or Q(s,a)
# - Examples: Q-Learning, DQN, Double DQN, Dueling DQN

# Policy-Based Methods:
# - Learn policy π(a|s) directly
# - Examples: REINFORCE, Policy Gradient

# Actor-Critic Methods:
# - Combine value and policy learning
# - Actor: learns policy
# - Critic: learns value function
# - Examples: A2C, A3C, PPO, SAC, TD3

# Model-Based vs Model-Free:
# - Model-Based: Learn environment dynamics (transition model)
# - Model-Free: Learn directly from experience

# On-Policy vs Off-Policy:
# - On-Policy: Learn from actions taken by current policy (e.g., SARSA, PPO)
# - Off-Policy: Learn from any data (e.g., Q-Learning, DQN)

CHAPTER 2: POLICY GRADIENT METHODS
REINFORCE Algorithm
# Monte Carlo Policy Gradient
# Update rule: θ ← θ + α * ∇log π(a|s; θ) * G_t
# where G_t is the return (cumulative discounted reward)

import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical

class REINFORCEAgent:
    """REINFORCE algorithm for discrete action spaces."""
    
    def __init__(self, state_dim, action_dim, lr=0.01, gamma=0.99):
        self.gamma = gamma
        
        # Policy network: states → action probabilities
        self.policy = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim),
            nn.Softmax(dim=-1)
        )
        
        self.optimizer = optim.Adam(self.policy.parameters(), lr=lr)
        self.log_probs = []
        self.rewards = []
    
    def select_action(self, state):
        """Sample action from policy distribution."""
        state = torch.FloatTensor(state).unsqueeze(0)
        probs = self.policy(state)
        dist = Categorical(probs)
        action = dist.sample()
        
        self.log_probs.append(dist.log_prob(action))
        return action.item()
    
    def update(self):
        """Update policy using collected trajectory."""
        # Calculate discounted returns
        returns = []
        R = 0
        for r in reversed(self.rewards):
            R = r + self.gamma * R
            returns.insert(0, R)
        
        # Normalize returns for stability
        returns = torch.tensor(returns)
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)
        
        # Policy gradient loss
        policy_loss = []
        for log_prob, G in zip(self.log_probs, returns):
            policy_loss.append(-log_prob * G)
        
        self.optimizer.zero_grad()
        loss = torch.cat(policy_loss).sum()
        loss.backward()
        self.optimizer.step()
        
        # Clear buffers
        self.log_probs = []
        self.rewards = []

# Example usage with CartPole-like environment
def train_reinforce(env_name='CartPole-v1', episodes=1000):
    import gymnasium as gym
    
    env = gym.make(env_name)
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n
    
    agent = REINFORCEAgent(state_dim, action_dim)
    
    for episode in range(episodes):
        state, _ = env.reset()
        episode_reward = 0
        
        while True:
            action = agent.select_action(state)
            next_state, reward, terminated, truncated, _ = env.step(action)
            
            agent.rewards.append(reward)
            episode_reward += reward
            
            state = next_state
            
            if terminated or truncated:
                break
        
        agent.update()
        
        if episode % 100 == 0:
            print(f"Episode {episode}: Reward = {episode_reward:.2f}")
    
    env.close()

# train_reinforce()

Baseline Reduction
# Subtract baseline b(s) to reduce variance
# Update: θ ← θ + α * ∇log π(a|s; θ) * (G_t - b(s))
# Common baseline: V(s) (state value function)

class ActorCriticBaseline:
    """Actor-Critic with baseline for variance reduction."""
    
    def __init__(self, state_dim, action_dim, lr_actor=0.001, lr_critic=0.001, gamma=0.99):
        self.gamma = gamma
        
        # Actor: policy network
        self.actor = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim),
            nn.Softmax(dim=-1)
        )
        
        # Critic: value network
        self.critic = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )
        
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=lr_actor)
        self.critic_optimizer = optim.Adam(self.critic.parameters(), lr=lr_critic)
        
        self.log_probs = []
        self.values = []
        self.rewards = []
    
    def select_action(self, state):
        state = torch.FloatTensor(state).unsqueeze(0)
        probs = self.actor(state)
        dist = Categorical(probs)
        action = dist.sample()
        
        value = self.critic(state).squeeze()
        
        self.log_probs.append(dist.log_prob(action))
        self.values.append(value)
        return action.item()
    
    def update(self):
        # Calculate advantages: A(s,a) = G_t - V(s)
        returns = []
        R = 0
        for r in reversed(self.rewards):
            R = r + self.gamma * R
            returns.insert(0, R)
        
        returns = torch.tensor(returns)
        values = torch.stack(self.values)
        
        # Advantage estimation
        advantages = returns - values.detach()
        
        # Normalize advantages
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        
        # Actor loss (policy gradient)
        actor_loss = -(torch.stack(self.log_probs) * advantages).mean()
        
        # Critic loss (MSE of value predictions)
        critic_loss = nn.MSELoss()(values, returns)
        
        # Update networks
        self.actor_optimizer.zero_grad()
        actor_loss.backward(retain_graph=True)
        self.actor_optimizer.step()
        
        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()
        
        # Clear buffers
        self.log_probs = []
        self.values = []
        self.rewards = []

CHAPTER 3: ACTOR-CRITIC METHODS
A2C (Advantage Actor-Critic)
# Synchronous version of A3C
# Uses multiple parallel environments on single machine
# Updates after fixed number of steps

class A2CAgent:
    """Advantage Actor-Critic (A2C) agent."""
    
    def __init__(self, state_dim, action_dim, lr=0.001, gamma=0.99, 
                 entropy_coef=0.01, value_coef=0.5):
        self.gamma = gamma
        self.entropy_coef = entropy_coef
        self.value_coef = value_coef
        
        # Shared backbone
        self.shared = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU()
        )
        
        # Actor head
        self.actor_head = nn.Linear(128, action_dim)
        
        # Critic head
        self.critic_head = nn.Linear(128, 1)
        
        self.optimizer = optim.Adam([
            {'params': self.shared.parameters()},
            {'params': self.actor_head.parameters()},
            {'params': self.critic_head.parameters()}
        ], lr=lr)
        
        self.log_probs = []
        self.values = []
        self.rewards = []
        self.entropies = []
    
    def forward(self, state):
        features = self.shared(torch.FloatTensor(state).unsqueeze(0))
        logits = self.actor_head(features)
        value = self.critic_head(features).squeeze()
        return logits, value
    
    def select_action(self, state):
        logits, value = self.forward(state)
        probs = torch.softmax(logits, dim=-1)
        dist = Categorical(probs)
        action = dist.sample()
        
        self.log_probs.append(dist.log_prob(action))
        self.values.append(value)
        self.entropies.append(dist.entropy())
        
        return action.item()
    
    def compute_returns(self, next_value=None, done=False):
        """Compute n-step returns."""
        returns = []
        R = next_value if not done else 0
        
        for r in reversed(self.rewards):
            R = r + self.gamma * R
            returns.insert(0, R)
        
        return torch.tensor(returns)
    
    def update(self, next_value=None, done=False):
        returns = self.compute_returns(next_value, done)
        values = torch.stack(self.values)
        
        # Advantages
        advantages = returns - values.detach()
        
        # Actor loss
        log_probs = torch.stack(self.log_probs)
        actor_loss = -(log_probs * advantages).mean()
        
        # Entropy bonus for exploration
        entropy_loss = -torch.stack(self.entropies).mean()
        
        # Critic loss
        critic_loss = nn.MSELoss()(values, returns)
        
        # Total loss
        loss = actor_loss + self.value_coef * critic_loss + self.entropy_coef * entropy_loss
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # Clear buffers
        self.log_probs = []
        self.values = []
        self.rewards = []
        self.entropies = []

A3C (Asynchronous Advantage Actor-Critic)
# Multiple agents run in parallel threads
# Each agent has its own copy of the network
# Gradients are asynchronously applied to global network

# Note: A3C is complex to implement due to threading
# Modern alternative: A2C with vectorized environments

PPO (Proximal Policy Optimization)
# Clips policy updates to prevent large changes
# More stable than vanilla policy gradient
# State-of-the-art for many tasks

class PPOAgent:
    """Proximal Policy Optimization agent."""
    
    def __init__(self, state_dim, action_dim, lr=0.0003, gamma=0.99, 
                 clip_epsilon=0.2, value_coef=0.5, entropy_coef=0.01,
                 ppo_epochs=10, mini_batch_size=64):
        self.gamma = gamma
        self.clip_epsilon = clip_epsilon
        self.value_coef = value_coef
        self.entropy_coef = entropy_coef
        self.ppo_epochs = ppo_epochs
        self.mini_batch_size = mini_batch_size
        
        # Actor-Critic network
        self.network = nn.Sequential(
            nn.Linear(state_dim, 256),
            nn.Tanh(),
            nn.Linear(256, 256),
            nn.Tanh()
        )
        
        self.actor_head = nn.Linear(256, action_dim)
        self.critic_head = nn.Linear(256, 1)
        
        self.optimizer = optim.Adam([
            {'params': self.network.parameters()},
            {'params': self.actor_head.parameters()},
            {'params': self.critic_head.parameters()}
        ], lr=lr)
        
        # Storage for batch updates
        self.states = []
        self.actions = []
        self.log_probs = []
        self.rewards = []
        self.values = []
        self.dones = []
    
    def select_action(self, state):
        state = torch.FloatTensor(state).unsqueeze(0)
        features = self.network(state)
        logits = self.actor_head(features)
        value = self.critic_head(features).squeeze()
        
        probs = torch.softmax(logits, dim=-1)
        dist = Categorical(probs)
        action = dist.sample()
        log_prob = dist.log_prob(action)
        
        self.states.append(state.squeeze().numpy())
        self.actions.append(action.item())
        self.log_probs.append(log_prob.item())
        self.values.append(value.item())
        
        return action.item()
    
    def store_transition(self, reward, done):
        self.rewards.append(reward)
        self.dones.append(done)
    
    def compute_gae(self, last_value=0, last_done=False):
        """Generalized Advantage Estimation."""
        advantages = []
        gae = 0
        
        values = self.values + [last_value if not last_done else 0]
        
        for t in reversed(range(len(self.rewards))):
            delta = (self.rewards[t] + 
                    self.gamma * values[t + 1] * (1 - int(self.dones[t])) - 
                    values[t])
            gae = delta + self.gamma * 0.95 * (1 - int(self.dones[t])) * gae
            advantages.insert(0, gae)
        
        returns = [adv + val for adv, val in zip(advantages, self.values)]
        
        return torch.tensor(advantages), torch.tensor(returns)
    
    def update(self, last_value=0, last_done=False):
        """PPO update with clipping."""
        advantages, returns = self.compute_gae(last_value, last_done)
        
        # Normalize advantages
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        
        # Convert to tensors
        states = torch.FloatTensor(np.array(self.states))
        actions = torch.LongTensor(self.actions)
        old_log_probs = torch.FloatTensor(self.log_probs)
        old_values = torch.FloatTensor(self.values)
        
        dataset_size = len(states)
        
        for _ in range(self.ppo_epochs):
            # Shuffle indices
            indices = torch.randperm(dataset_size)
            
            for start in range(0, dataset_size, self.mini_batch_size):
                end = start + self.mini_batch_size
                batch_indices = indices[start:end]
                
                batch_states = states[batch_indices]
                batch_actions = actions[batch_indices]
                batch_old_log_probs = old_log_probs[batch_indices]
                batch_advantages = advantages[batch_indices]
                batch_returns = returns[batch_indices]
                
                # Forward pass
                features = self.network(batch_states)
                logits = self.actor_head(features)
                values = self.critic_head(features).squeeze()
                
                probs = torch.softmax(logits, dim=-1)
                dist = Categorical(probs)
                new_log_probs = dist.log_prob(batch_actions)
                entropy = dist.entropy().mean()
                
                # Ratio: π_new / π_old
                ratio = torch.exp(new_log_probs - batch_old_log_probs)
                
                # Clipped surrogate objective
                surr1 = ratio * batch_advantages
                surr2 = torch.clamp(ratio, 1 - self.clip_epsilon, 
                                   1 + self.clip_epsilon) * batch_advantages
                actor_loss = -torch.min(surr1, surr2).mean()
                
                # Value loss
                critic_loss = nn.MSELoss()(values, batch_returns)
                
                # Total loss
                loss = actor_loss + self.value_coef * critic_loss - self.entropy_coef * entropy
                
                # Update
                self.optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(self.network.parameters(), 0.5)
                self.optimizer.step()
        
        # Clear storage
        self.states = []
        self.actions = []
        self.log_probs = []
        self.rewards = []
        self.values = []
        self.dones = []

CHAPTER 4: CONTINUOUS CONTROL ALGORITHMS
DDPG (Deep Deterministic Policy Gradient)
# For continuous action spaces
# Actor: deterministic policy μ(s|θ)
# Critic: Q-value function Q(s,a|φ)
# Target networks for stability

class DDPGAgent:
    """Deep Deterministic Policy Gradient agent."""
    
    def __init__(self, state_dim, action_dim, action_high=1.0, action_low=-1.0,
                 lr_actor=0.001, lr_critic=0.001, gamma=0.99, tau=0.001,
                 buffer_size=100000, batch_size=256):
        self.action_high = action_high
        self.action_low = action_low
        self.gamma = gamma
        self.tau = tau  # Soft update parameter
        self.batch_size = batch_size
        
        # Actor network
        self.actor = self._build_actor(state_dim, action_dim)
        self.actor_target = self._build_actor(state_dim, action_dim)
        self.actor_target.load_state_dict(self.actor.state_dict())
        
        # Critic network
        self.critic = self._build_critic(state_dim, action_dim)
        self.critic_target = self._build_critic(state_dim, action_dim)
        self.critic_target.load_state_dict(self.critic.state_dict())
        
        # Optimizers
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=lr_actor)
        self.critic_optimizer = optim.Adam(self.critic.parameters(), lr=lr_critic)
        
        # Replay buffer
        self.buffer = []
        self.buffer_size = buffer_size
    
    def _build_actor(self, state_dim, action_dim):
        return nn.Sequential(
            nn.Linear(state_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, action_dim),
            nn.Tanh()  # Output in [-1, 1]
        )
    
    def _build_critic(self, state_dim, action_dim):
        class CriticNet(nn.Module):
            def __init__(self):
                super().__init__()
                self.fc1 = nn.Linear(state_dim + action_dim, 256)
                self.fc2 = nn.Linear(256, 256)
                self.fc3 = nn.Linear(256, 1)
            
            def forward(self, state, action):
                x = torch.cat([state, action], dim=-1)
                x = torch.relu(self.fc1(x))
                x = torch.relu(self.fc2(x))
                return self.fc3(x)
        
        return CriticNet()
    
    def select_action(self, state, noise_scale=0.1):
        state = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            action = self.actor(state).squeeze().numpy()
        
        # Add exploration noise
        noise = np.random.normal(0, noise_scale, size=action.shape)
        action = np.clip(action + noise, self.action_low, self.action_high)
        
        return action
    
    def store_transition(self, state, action, reward, next_state, done):
        if len(self.buffer) >= self.buffer_size:
            self.buffer.pop(0)
        self.buffer.append((state, action, reward, next_state, done))
    
    def soft_update(self, target, source):
        for target_param, source_param in zip(target.parameters(), source.parameters()):
            target_param.data.copy_(
                self.tau * source_param.data + (1 - self.tau) * target_param.data
            )
    
    def update(self):
        if len(self.buffer) < self.batch_size:
            return
        
        # Sample batch
        batch = random.sample(self.buffer, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        
        states = torch.FloatTensor(np.array(states))
        actions = torch.FloatTensor(np.array(actions))
        rewards = torch.FloatTensor(rewards).unsqueeze(1)
        next_states = torch.FloatTensor(np.array(next_states))
        dones = torch.FloatTensor(dones).unsqueeze(1)
        
        # Update Critic
        with torch.no_grad():
            next_actions = self.actor_target(next_states)
            next_q_values = self.critic_target(next_states, next_actions)
            target_q = rewards + self.gamma * (1 - dones) * next_q_values
        
        current_q = self.critic(states, actions)
        critic_loss = nn.MSELoss()(current_q, target_q)
        
        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()
        
        # Update Actor
        actor_actions = self.actor(states)
        actor_q = self.critic(states, actor_actions)
        actor_loss = -actor_q.mean()
        
        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()
        
        # Soft update target networks
        self.soft_update(self.actor_target, self.actor)
        self.soft_update(self.critic_target, self.critic)

TD3 (Twin Delayed Deep Deterministic Policy Gradient)
# Improvements over DDPG:
# 1. Twin Critics: Use two Q-networks, take minimum to reduce overestimation
# 2. Delayed Policy Updates: Update actor less frequently than critic
# 3. Target Policy Smoothing: Add noise to target actions

class TD3Agent:
    """Twin Delayed DDPG agent."""
    
    def __init__(self, state_dim, action_dim, action_high=1.0, action_low=-1.0,
                 lr=0.001, gamma=0.99, tau=0.005, policy_delay=2,
                 buffer_size=100000, batch_size=256):
        self.action_high = action_high
        self.action_low = action_low
        self.gamma = gamma
        self.tau = tau
        self.policy_delay = policy_delay
        self.batch_size = batch_size
        self.update_counter = 0
        
        # Actor
        self.actor = self._build_actor(state_dim, action_dim)
        self.actor_target = self._build_actor(state_dim, action_dim)
        self.actor_target.load_state_dict(self.actor.state_dict())
        
        # Twin Critics
        self.critic1 = self._build_critic(state_dim, action_dim)
        self.critic2 = self._build_critic(state_dim, action_dim)
        self.critic1_target = self._build_critic(state_dim, action_dim)
        self.critic2_target = self._build_critic(state_dim, action_dim)
        
        self.critic1_target.load_state_dict(self.critic1.state_dict())
        self.critic2_target.load_state_dict(self.critic2.state_dict())
        
        # Optimizers
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=lr)
        self.critic_optimizer = optim.Adam(
            list(self.critic1.parameters()) + list(self.critic2.parameters()), lr=lr
        )
        
        self.buffer = []
        self.buffer_size = buffer_size
    
    def _build_actor(self, state_dim, action_dim):
        return nn.Sequential(
            nn.Linear(state_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, action_dim),
            nn.Tanh()
        )
    
    def _build_critic(self, state_dim, action_dim):
        class TwinCritic(nn.Module):
            def __init__(self):
                super().__init__()
                self.fc1 = nn.Linear(state_dim + action_dim, 256)
                self.fc2 = nn.Linear(256, 256)
                self.fc3 = nn.Linear(256, 1)
            
            def forward(self, state, action):
                x = torch.cat([state, action], dim=-1)
                x = torch.relu(self.fc1(x))
                x = torch.relu(self.fc2(x))
                return self.fc3(x)
        
        return TwinCritic()
    
    def select_action(self, state, noise_scale=0.1):
        state = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            action = self.actor(state).squeeze().numpy()
        
        noise = np.random.normal(0, noise_scale, size=action.shape)
        action = np.clip(action + noise, self.action_low, self.action_high)
        
        return action
    
    def store_transition(self, state, action, reward, next_state, done):
        if len(self.buffer) >= self.buffer_size:
            self.buffer.pop(0)
        self.buffer.append((state, action, reward, next_state, done))
    
    def soft_update(self, target, source):
        for target_param, source_param in zip(target.parameters(), source.parameters()):
            target_param.data.copy_(
                self.tau * source_param.data + (1 - self.tau) * target_param.data
            )
    
    def update(self):
        if len(self.buffer) < self.batch_size:
            return
        
        self.update_counter += 1
        
        # Sample batch
        batch = random.sample(self.buffer, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        
        states = torch.FloatTensor(np.array(states))
        actions = torch.FloatTensor(np.array(actions))
        rewards = torch.FloatTensor(rewards).unsqueeze(1)
        next_states = torch.FloatTensor(np.array(next_states))
        dones = torch.FloatTensor(dones).unsqueeze(1)
        
        # Update Critics
        with torch.no_grad():
            # Target policy smoothing
            noise = torch.clamp(torch.randn_like(actions) * 0.2, -0.5, 0.5)
            next_actions = torch.clamp(
                self.actor_target(next_states) + noise,
                self.action_low, self.action_high
            )
            
            # Twin Q-targets (take minimum)
            q1_target = self.critic1_target(next_states, next_actions)
            q2_target = self.critic2_target(next_states, next_actions)
            min_q_target = torch.min(q1_target, q2_target)
            
            target_q = rewards + self.gamma * (1 - dones) * min_q_target
        
        q1 = self.critic1(states, actions)
        q2 = self.critic2(states, actions)
        
        critic_loss = nn.MSELoss()(q1, target_q) + nn.MSELoss()(q2, target_q)
        
        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()
        
        # Delayed Actor update
        if self.update_counter % self.policy_delay == 0:
            actor_actions = self.actor(states)
            actor_q = self.critic1(states, actor_actions)
            actor_loss = -actor_q.mean()
            
            self.actor_optimizer.zero_grad()
            actor_loss.backward()
            self.actor_optimizer.step()
            
            # Soft update targets
            self.soft_update(self.actor_target, self.actor)
            self.soft_update(self.critic1_target, self.critic1)
            self.soft_update(self.critic2_target, self.critic2)

SAC (Soft Actor-Critic)
# Maximum entropy RL
# Encourages exploration by maximizing entropy
# Stochastic policy
# Automatically adjusts temperature parameter

class SACAgent:
    """Soft Actor-Critic agent."""
    
    def __init__(self, state_dim, action_dim, action_high=1.0, action_low=-1.0,
                 lr=0.0003, gamma=0.99, tau=0.005, alpha=0.2,
                 buffer_size=100000, batch_size=256):
        self.action_high = action_high
        self.action_low = action_low
        self.gamma = gamma
        self.tau = tau
        self.alpha = alpha  # Temperature parameter
        self.batch_size = batch_size
        
        # Actor (stochastic policy)
        self.actor = self._build_actor(state_dim, action_dim)
        
        # Twin Critics
        self.critic1 = self._build_critic(state_dim, action_dim)
        self.critic2 = self._build_critic(state_dim, action_dim)
        self.critic1_target = self._build_critic(state_dim, action_dim)
        self.critic2_target = self._build_critic(state_dim, action_dim)
        
        self.critic1_target.load_state_dict(self.critic1.state_dict())
        self.critic2_target.load_state_dict(self.critic2.state_dict())
        
        # Optimizers
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=lr)
        self.critic_optimizer = optim.Adam(
            list(self.critic1.parameters()) + list(self.critic2.parameters()), lr=lr
        )
        
        self.buffer = []
        self.buffer_size = buffer_size
    
    def _build_actor(self, state_dim, action_dim):
        class GaussianPolicy(nn.Module):
            def __init__(self):
                super().__init__()
                self.fc1 = nn.Linear(state_dim, 256)
                self.fc2 = nn.Linear(256, 256)
                self.mean_head = nn.Linear(256, action_dim)
                self.log_std_head = nn.Linear(256, action_dim)
            
            def forward(self, state):
                x = torch.relu(self.fc1(state))
                x = torch.relu(self.fc2(x))
                
                mean = self.mean_head(x)
                log_std = torch.clamp(self.log_std_head(x), -20, 2)
                std = torch.exp(log_std)
                
                return mean, std
        
        return GaussianPolicy()
    
    def _build_critic(self, state_dim, action_dim):
        class CriticNet(nn.Module):
            def __init__(self):
                super().__init__()
                self.fc1 = nn.Linear(state_dim + action_dim, 256)
                self.fc2 = nn.Linear(256, 256)
                self.fc3 = nn.Linear(256, 1)
            
            def forward(self, state, action):
                x = torch.cat([state, action], dim=-1)
                x = torch.relu(self.fc1(x))
                x = torch.relu(self.fc2(x))
                return self.fc3(x)
        
        return CriticNet()
    
    def select_action(self, state, deterministic=False):
        state = torch.FloatTensor(state).unsqueeze(0)
        
        with torch.no_grad():
            mean, std = self.actor(state)
            
            if deterministic:
                action = mean
            else:
                dist = torch.distributions.Normal(mean, std)
                action = dist.rsample()  # Reparameterization trick
            
            action = torch.tanh(action)  # Squash to [-1, 1]
        
        return action.squeeze().numpy()
    
    def store_transition(self, state, action, reward, next_state, done):
        if len(self.buffer) >= self.buffer_size:
            self.buffer.pop(0)
        self.buffer.append((state, action, reward, next_state, done))
    
    def soft_update(self, target, source):
        for target_param, source_param in zip(target.parameters(), source.parameters()):
            target_param.data.copy_(
                self.tau * source_param.data + (1 - self.tau) * target_param.data
            )
    
    def update(self):
        if len(self.buffer) < self.batch_size:
            return
        
        batch = random.sample(self.buffer, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        
        states = torch.FloatTensor(np.array(states))
        actions = torch.FloatTensor(np.array(actions))
        rewards = torch.FloatTensor(rewards).unsqueeze(1)
        next_states = torch.FloatTensor(np.array(next_states))
        dones = torch.FloatTensor(dones).unsqueeze(1)
        
        # Update Critics
        with torch.no_grad():
            next_mean, next_std = self.actor(next_states)
            next_dist = torch.distributions.Normal(next_mean, next_std)
            next_action = next_dist.rsample()
            next_action = torch.tanh(next_action)
            
            # Compute log probability with squash correction
            log_prob = next_dist.log_prob(next_action)
            log_prob -= torch.log(1 - next_action.pow(2) + 1e-6)
            log_prob = log_prob.sum(dim=-1, keepdim=True)
            
            q1_target = self.critic1_target(next_states, next_action)
            q2_target = self.critic2_target(next_states, next_action)
            min_q_target = torch.min(q1_target, q2_target)
            
            target_q = rewards + self.gamma * (1 - dones) * (min_q_target - self.alpha * log_prob)
        
        q1 = self.critic1(states, actions)
        q2 = self.critic2(states, actions)
        
        critic_loss = nn.MSELoss()(q1, target_q) + nn.MSELoss()(q2, target_q)
        
        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()
        
        # Update Actor
        mean, std = self.actor(states)
        dist = torch.distributions.Normal(mean, std)
        action = dist.rsample()
        action = torch.tanh(action)
        
        log_prob = dist.log_prob(action)
        log_prob -= torch.log(1 - action.pow(2) + 1e-6)
        log_prob = log_prob.sum(dim=-1, keepdim=True)
        
        q1_pi = self.critic1(states, action)
        q2_pi = self.critic2(states, action)
        min_q_pi = torch.min(q1_pi, q2_pi)
        
        actor_loss = (self.alpha * log_prob - min_q_pi).mean()
        
        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()
        
        # Soft update targets
        self.soft_update(self.critic1_target, self.critic1)
        self.soft_update(self.critic2_target, self.critic2)

CHAPTER 5: MODEL-BASED RL
World Models
# Learn environment dynamics model
# Use model for planning or data generation

class DynamicsModel:
    """Learned dynamics model: s_{t+1}, r_t = f(s_t, a_t)"""
    
    def __init__(self, state_dim, action_dim):
        self.model = nn.Sequential(
            nn.Linear(state_dim + action_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, state_dim + 1)  # next_state + reward
        )
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
    
    def predict(self, state, action):
        state = torch.FloatTensor(state).unsqueeze(0)
        action = torch.FloatTensor(action).unsqueeze(0)
        x = torch.cat([state, action], dim=-1)
        
        with torch.no_grad():
            output = self.model(x).squeeze()
        
        next_state = output[:-1].numpy()
        reward = output[-1].item()
        
        return next_state, reward
    
    def train_step(self, states, actions, next_states, rewards):
        states = torch.FloatTensor(states)
        actions = torch.FloatTensor(actions)
        next_states = torch.FloatTensor(next_states)
        rewards = torch.FloatTensor(rewards).unsqueeze(1)
        
        x = torch.cat([states, actions], dim=-1)
        y = torch.cat([next_states, rewards], dim=-1)
        
        prediction = self.model(x)
        loss = nn.MSELoss()(prediction, y)
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        return loss.item()

MBPO (Model-Based Policy Optimization)
# Combine model-free and model-based approaches
# Use learned model to generate synthetic data
# Train policy on real + synthetic data

class MBPOAgent:
    """Model-Based Policy Optimization."""
    
    def __init__(self, state_dim, action_dim):
        self.dynamics = DynamicsModel(state_dim, action_dim)
        self.policy = PPOAgent(state_dim, action_dim)
        self.real_buffer = []
        self.synth_buffer = []
    
    def collect_real_data(self, env, n_steps=1000):
        """Collect real experience."""
        state, _ = env.reset()
        for _ in range(n_steps):
            action = self.policy.select_action(state)
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            
            self.real_buffer.append((state, action, reward, next_state, done))
            
            # Train dynamics model
            if len(self.real_buffer) > 100:
                batch = random.sample(self.real_buffer, 100)
                states, actions, rewards, next_states, _ = zip(*batch)
                self.dynamics.train_step(states, actions, next_states, rewards)
            
            state = next_state
            if done:
                state, _ = env.reset()
    
    def generate_synthetic_data(self, n_samples=1000):
        """Generate synthetic trajectories using dynamics model."""
        if not self.real_buffer:
            return
        
        # Sample initial states from real buffer
        init_states = [s for s, _, _, _, _ in random.sample(self.real_buffer, min(100, len(self.real_buffer)))]
        
        for _ in range(n_samples):
            state = random.choice(init_states)
            for step in range(10):
                action = self.policy.select_action(state, deterministic=True)
                next_state, reward = self.dynamics.predict(state, action)
                
                self.synth_buffer.append((state, action, reward, next_state, False))
                state = next_state
    
    def update_policy(self):
        """Train policy on combined real + synthetic data."""
        # Combine buffers
        combined = self.real_buffer + self.synth_buffer
        
        # Train PPO on combined data
        # (Implementation details omitted for brevity)
        pass

CHAPTER 6: MULTI-AGENT RL
Independent Q-Learning
# Each agent learns independently
# Treat other agents as part of environment
# Simple but may not converge

class IndependentQLearning:
    """Independent Q-Learning for multi-agent systems."""
    
    def __init__(self, n_agents, state_dim, action_dim, lr=0.1, gamma=0.95, epsilon=0.1):
        self.agents = [
            QLearningAgent(state_dim, action_dim, lr, gamma, epsilon)
            for _ in range(n_agents)
        ]
    
    def select_actions(self, states):
        """Each agent selects action independently."""
        actions = []
        for i, state in enumerate(states):
            action = self.agents[i].choose_action(state)
            actions.append(action)
        return actions
    
    def update(self, states, actions, rewards, next_states, dones):
        """Update each agent independently."""
        for i, agent in enumerate(self.agents):
            agent.update(states[i], actions[i], rewards[i], next_states[i], dones[i])

MADDPG (Multi-Agent Deep Deterministic Policy Gradient)
# Centralized training, decentralized execution
# Critic sees all agents' actions during training
# Actor only sees own observation

class MADDPGAgent:
    """Multi-Agent DDPG."""
    
    def __init__(self, n_agents, obs_dims, action_dims, action_high=1.0, action_low=-1.0):
        self.n_agents = n_agents
        self.action_high = action_high
        self.action_low = action_low
        
        # Individual actors
        self.actors = [
            nn.Sequential(
                nn.Linear(obs_dims[i], 128),
                nn.ReLU(),
                nn.Linear(128, 128),
                nn.ReLU(),
                nn.Linear(128, action_dims[i]),
                nn.Tanh()
            ) for i in range(n_agents)
        ]
        
        # Centralized critic (sees all observations and actions)
        total_obs_dim = sum(obs_dims)
        total_action_dim = sum(action_dims)
        
        self.critic = nn.Sequential(
            nn.Linear(total_obs_dim + total_action_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 1)
        )
        
        # Target networks
        self.actors_target = [copy.deepcopy(actor) for actor in self.actors]
        self.critic_target = copy.deepcopy(self.critic)
        
        # Optimizers
        self.actor_optimizers = [optim.Adam(actor.parameters(), lr=0.001) for actor in self.actors]
        self.critic_optimizer = optim.Adam(self.critic.parameters(), lr=0.001)
    
    def select_actions(self, observations, noise_scale=0.1):
        """Decentralized action selection."""
        actions = []
        for i, obs in enumerate(observations):
            obs = torch.FloatTensor(obs).unsqueeze(0)
            with torch.no_grad():
                action = self.actors[i](obs).squeeze().numpy()
            
            noise = np.random.normal(0, noise_scale, size=action.shape)
            action = np.clip(action + noise, self.action_low, self.action_high)
            actions.append(action)
        
        return actions

CHAPTER 7: OFFLINE RL
Batch Constrained Q-Learning (BCQ)
# Learn from fixed dataset without environment interaction
# Constrain policy to stay close to data distribution

class BCQAgent:
    """Batch-Constrained Q-Learning."""
    
    def __init__(self, state_dim, action_dim, action_high=1.0, action_low=-1.0):
        self.action_high = action_high
        self.action_low = action_low
        
        # Q-network
        self.q_network = nn.Sequential(
            nn.Linear(state_dim + action_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 1)
        )
        
        # VAE for behavior cloning
        self.vae = self._build_vae(state_dim, action_dim)
        
        self.q_optimizer = optim.Adam(self.q_network.parameters(), lr=0.001)
        self.vae_optimizer = optim.Adam(self.vae.parameters(), lr=0.001)
    
    def _build_vae(self, state_dim, action_dim):
        class VAE(nn.Module):
            def __init__(self):
                super().__init__()
                # Encoder
                self.encoder = nn.Sequential(
                    nn.Linear(state_dim + action_dim, 256),
                    nn.ReLU(),
                    nn.Linear(256, 256)
                )
                self.mean_head = nn.Linear(256, action_dim)
                self.log_var_head = nn.Linear(256, action_dim)
                
                # Decoder
                self.decoder = nn.Sequential(
                    nn.Linear(state_dim + action_dim, 256),
                    nn.ReLU(),
                    nn.Linear(256, 256),
                    nn.ReLU(),
                    nn.Linear(256, action_dim),
                    nn.Tanh()
                )
            
            def encode(self, state, action):
                x = torch.cat([state, action], dim=-1)
                h = self.encoder(x)
                return self.mean_head(h), self.log_var_head(h)
            
            def decode(self, state, z):
                x = torch.cat([state, z], dim=-1)
                return self.decoder(x)
            
            def sample(self, state, n_samples=10):
                mean, log_var = self.encode(state, torch.zeros_like(state[:, :1]))
                std = torch.exp(0.5 * log_var)
                
                # Sample multiple actions
                z = torch.randn(n_samples, *std.shape) * std + mean
                actions = self.decode(state.repeat(n_samples, 1), z)
                
                return actions
        
        return VAE()
    
    def train_vae(self, states, actions):
        """Train VAE to mimic behavior policy."""
        states = torch.FloatTensor(states)
        actions = torch.FloatTensor(actions)
        
        mean, log_var = self.vae.encode(states, actions)
        std = torch.exp(0.5 * log_var)
        
        # Reparameterization
        z = mean + std * torch.randn_like(std)
        reconstructed = self.vae.decode(states, z)
        
        # Reconstruction loss
        recon_loss = nn.MSELoss()(reconstructed, actions)
        
        # KL divergence
        kl_loss = -0.5 * torch.mean(1 + log_var - mean.pow(2) - log_var.exp())
        
        vae_loss = recon_loss + 0.5 * kl_loss
        
        self.vae_optimizer.zero_grad()
        vae_loss.backward()
        self.vae_optimizer.step()
        
        return vae_loss.item()
    
    def select_action(self, state):
        """Select action by sampling from VAE and choosing best Q-value."""
        state = torch.FloatTensor(state).unsqueeze(0)
        
        with torch.no_grad():
            # Sample multiple actions from VAE
            actions = self.vae.sample(state, n_samples=10)
            
            # Evaluate Q-values
            state_expanded = state.repeat(10, 1)
            q_values = self.q_network(torch.cat([state_expanded, actions], dim=-1))
            
            # Choose action with highest Q-value
            best_idx = torch.argmax(q_values).item()
            action = actions[best_idx].squeeze().numpy()
        
        return action

CHAPTER 8: HIERARCHICAL RL
Options Framework
# High-level policy selects options (temporally extended actions)
# Low-level policies execute options

class Option:
    """An option consists of: initiation set, policy, termination condition."""
    
    def __init__(self, name, low_level_policy):
        self.name = name
        self.policy = low_level_policy
        self.termination_threshold = 0.1  # Probability of terminating
    
    def should_terminate(self, state):
        """Stochastic termination condition."""
        return random.random() < self.termination_threshold
    
    def select_action(self, state):
        return self.policy.select_action(state)

class HierarchicalAgent:
    """Two-level hierarchical RL agent."""
    
    def __init__(self, state_dim, action_dim, n_options=4):
        self.options = [
            Option(f"option_{i}", PPOAgent(state_dim, action_dim))
            for i in range(n_options)
        ]
        
        # High-level policy: selects which option to use
        self.high_level_policy = PPOAgent(state_dim, n_options)
        
        self.current_option = None
        self.option_start_time = 0
    
    def select_action(self, state):
        # Check if current option should terminate
        if (self.current_option is None or 
            self.current_option.should_terminate(state)):
            # Select new option
            option_idx = self.high_level_policy.select_action(state)
            self.current_option = self.options[option_idx]
            self.option_start_time = 0
        
        # Execute low-level policy
        action = self.current_option.select_action(state)
        self.option_start_time += 1
        
        return action

CHAPTER 9: EXPLORATION STRATEGIES
Curiosity-Driven Exploration
# Intrinsic motivation: reward for visiting novel states

class CuriosityModule:
    """Intrinsic curiosity module."""
    
    def __init__(self, state_dim, action_dim):
        # Forward model: predict next state
        self.forward_model = nn.Sequential(
            nn.Linear(state_dim + action_dim, 256),
            nn.ReLU(),
            nn.Linear(256, state_dim)
        )
        
        self.optimizer = optim.Adam(self.forward_model.parameters(), lr=0.001)
    
    def compute_intrinsic_reward(self, state, action, next_state):
        """Reward = prediction error of forward model."""
        state = torch.FloatTensor(state).unsqueeze(0)
        action = torch.FloatTensor(action).unsqueeze(0)
        next_state = torch.FloatTensor(next_state).unsqueeze(0)
        
        x = torch.cat([state, action], dim=-1)
        predicted_next = self.forward_model(x)
        
        intrinsic_reward = nn.MSELoss()(predicted_next, next_state).item()
        
        return intrinsic_reward
    
    def update(self, states, actions, next_states):
        states = torch.FloatTensor(states)
        actions = torch.FloatTensor(actions)
        next_states = torch.FloatTensor(next_states)
        
        x = torch.cat([states, actions], dim=-1)
        predicted = self.forward_model(x)
        
        loss = nn.MSELoss()(predicted, next_states)
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

Random Network Distillation (RND)
# Use prediction error of random features as exploration bonus

class RNDAgent:
    """Random Network Distillation for exploration."""
    
    def __init__(self, state_dim):
        # Fixed random target network
        self.target = nn.Sequential(
            nn.Linear(state_dim, 512),
            nn.ReLU(),
            nn.Linear(512, 512)
        )
        
        # Trainable predictor
        self.predictor = nn.Sequential(
            nn.Linear(state_dim, 512),
            nn.ReLU(),
            nn.Linear(512, 512)
        )
        
        # Freeze target network
        for param in self.target.parameters():
            param.requires_grad = False
        
        self.optimizer = optim.Adam(self.predictor.parameters(), lr=0.001)
    
    def compute_exploration_bonus(self, state):
        """Bonus = prediction error of random features."""
        state = torch.FloatTensor(state).unsqueeze(0)
        
        with torch.no_grad():
            target_features = self.target(state)
        
        predicted_features = self.predictor(state)
        
        bonus = nn.MSELoss()(predicted_features, target_features).item()
        
        return bonus
    
    def update(self, states):
        states = torch.FloatTensor(states)
        
        with torch.no_grad():
            target_features = self.target(states)
        
        predicted_features = self.predictor(states)
        
        loss = nn.MSELoss()(predicted_features, target_features)
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

CHAPTER 10: ADVANCED TOPICS AND RESOURCES
Meta-RL
# Learn to learn: adapt quickly to new tasks
# MAML (Model-Agnostic Meta-Learning)
# RL^2 (Reinforcement Learning squared)

Transfer Learning in RL
# Pre-train on source task, fine-tune on target task
# Feature reuse
# Policy distillation

Safety in RL
# Constrained MDPs
# Safe exploration
# Shielding: prevent unsafe actions

Scalability
# Distributed RL (Ray/RLLib)
# Asynchronous training
# Large-scale simulations

Recommended Reading
# - "Reinforcement Learning: An Introduction" by Sutton & Barto
# - "Deep Reinforcement Learning Hands-On" by Maxim Lapan
# - Papers: PPO (Schulman et al.), SAC (Haarnoja et al.), TD3 (Fujimoto et al.)
# - Spinning Up in Deep RL: https://spinningup.openai.com/
# - Stable Baselines3 documentation: https://stable-baselines3.readthedocs.io/

# Online Resources
# - OpenAI Gym/Gymnasium: https://gymnasium.farama.org/
# - Ray RLLib: https://docs.ray.io/en/latest/rllib/index.html
# - DeepMind Lab: https://github.com/deepmind/lab
# - Unity ML-Agents: https://unity.com/products/machine-learning-agents

# End of Reinforcement Learning Advanced Reference