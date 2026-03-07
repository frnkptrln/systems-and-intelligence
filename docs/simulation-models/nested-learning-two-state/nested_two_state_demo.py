import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION (Keeping the stable rate) ---
NUM_STEPS = 5000         
LEARNING_RATE = 0.001    # Low rate for stability
P_CHANGE = 0.2           

# --- AGENT B: THE OBSERVER ---
M = np.random.rand(2, 2)
M = M / M.sum(axis=1, keepdims=True) 

error_history = []
m_history = [M.copy()]

# --- AGENT A: THE SYSTEM ---
system_state = 0 # State 0 or 1
M_TRUE = np.array([[1 - P_CHANGE, P_CHANGE], [P_CHANGE, 1 - P_CHANGE]])

print(f"Simulation started. True P(switch) = {P_CHANGE}. CORRECTED LEARNING RULE.")

# --- SIMULATION LOOP ---
for t in range(NUM_STEPS):
    # Current state (index)
    current_state_index = system_state
    
    # 1. PREDICTION (The prediction vector $\hat{O}_{t+1}$ is the corresponding row in M)
    prediction = M[current_state_index, :] # <- This is the vector of prediction probabilities

    # System step: Determine next state
    if np.random.rand() < P_CHANGE:
        system_state = 1 - system_state
    
    # Next observation (Actual reality: O_{t+1}) as vector
    next_obs = np.array([1.0, 0.0] if system_state == 0 else [0.0, 1.0])

    # 2. LEARNING LOOP (Update the matrix)
    error = next_obs - prediction # Error is the difference between reality and prediction
    
    # IMPORTANT: Corrected rule: Only adjust the row of the current state!
    # The adjustment is made along the error vector.
    M[current_state_index, :] += LEARNING_RATE * error

    # 3. NORMALIZATION and CLIPPING (Safeguard against instability)
    M = np.clip(M, 0.0001, 1.0)
    M = M / M.sum(axis=1, keepdims=True) 

    step_error = np.sum(error**2)
    error_history.append(step_error)
    m_history.append(M.copy())


# --- VISUALIZATION ---
window_size = 50 
smoothed_error = np.convolve(error_history, np.ones(window_size)/window_size, mode='valid')
m_history = np.array(m_history)
learned_transition_prob = m_history[:, 0, 1] 

print("\n--- RESULT ---")
print(f"True transition matrix (P_TRUE):\n {M_TRUE.round(4)}")
print(f"Learned transition matrix (M_FINAL):\n {M.round(4)}")
print(f"Avg. error (start): {np.mean(error_history[:500]):.4f}")
print(f"Avg. error (end): {np.mean(error_history[-500:]):.4f}")

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(smoothed_error)
plt.title('Emergent Behavior: Reduction of Prediction Error (Surprise)')
plt.xlabel('Time (Simulation Steps)')
plt.ylabel('Smoothed Squared Error')
plt.grid(True, alpha=0.5)

plt.subplot(1, 2, 2)
plt.plot(learned_transition_prob, label=r'Learned $P(S_2 | S_1)$')
plt.axhline(P_CHANGE, color='red', linestyle='--', label=r'True $P(S_2 | S_1)$')
plt.title('Agent Learns the System Rule (Convergence)')
plt.xlabel('Time (Simulation Steps)')
plt.ylabel('Probability Value')
plt.legend()
plt.grid(True, alpha=0.5)

plt.tight_layout()
plt.show()
