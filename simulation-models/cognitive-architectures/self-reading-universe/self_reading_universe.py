"""
Self-Reading Universe Simulation
--------------------------------
This model operationalizes the synthesis of Agüera y Arcas (Life as Computation) 
and Krakauer (Intelligence as Compression) from the essay `emergence-origin-intelligence.md`.

It creates a closed loop where:
1. A continuous cellular automaton (CA) generates patterns (Calculation / Life).
2. A Neural Network Autoencoder compresses them (Compression / Intelligence).
3. The compression error downward-causatively alters the CA's physical laws (mu).

Dependencies: numpy, matplotlib, torch
"""

import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from scipy.signal import convolve2d
import sys

# --- 1. The Substrate: Continuous Cellular Automaton ---
class ContinuousCA:
    def __init__(self, size=64):
        self.size = size
        self.grid = np.random.rand(size, size)
        
        # Base Lenia-like parameters
        self.R = 5
        self.T = 1.0  # Time step
        
        # The mutable parameter dictated by Downward Causation
        self.mu = 0.15   # Growth center (starts static/dead)
        self.sigma = 0.015 # Growth width
        
        # Create circular kernel
        y, x = np.ogrid[-self.R:self.R+1, -self.R:self.R+1]
        mask = x*x + y*y <= self.R*self.R
        self.kernel = np.zeros((2*self.R+1, 2*self.R+1))
        self.kernel[mask] = 1.0
        # Normalize to sum to 1
        self.kernel = self.kernel / np.sum(self.kernel)

    def growth_function(self, U):
        # Bell-shaped growth curve centered at mu
        return 2.0 * np.exp(-((U - self.mu)**2) / (2 * self.sigma**2)) - 1.0

    def step(self):
        # Calculate neighborhood sums
        U = convolve2d(self.grid, self.kernel, mode='same', boundary='wrap')
        
        # Calculate growth
        G = self.growth_function(U)
        
        # Update grid
        self.grid = np.clip(self.grid + self.T * G, 0, 1)
        return self.grid


# --- 2. The Observer: Autoencoder ---
class ObserverAutoencoder(nn.Module):
    def __init__(self, input_dim=64*64, hidden_dim=64):
        super().__init__()
        # Extreme compression: 4096 pixels -> 64 latent variables -> 4096 pixels
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Linear(256, hidden_dim),
            nn.Sigmoid()
        )
        self.decoder = nn.Sequential(
            nn.Linear(hidden_dim, 256),
            nn.ReLU(),
            nn.Linear(256, input_dim),
            nn.Sigmoid()
        )

    def forward(self, x):
        latent = self.encoder(x)
        reconstructed = self.decoder(latent)
        return reconstructed

# --- 3. The Universe (Feedback Loop) ---
class SelfReadingUniverse:
    def __init__(self, grid_size=64):
        self.ca = ContinuousCA(size=grid_size)
        
        # Setup Neural Net
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = ObserverAutoencoder(input_dim=grid_size*grid_size, hidden_dim=32).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.005)
        self.criterion = nn.MSELoss()
        
        # History for plotting
        self.history_loss = []
        self.history_mu = []
        
        # Target Loss (Edge of Chaos)
        # If loss is too low (e.g. 0.0), it's static/trivial.
        # If loss is too high (e.g. 0.2), it's noise/chaos.
        self.target_loss = 0.05
        
        # Meta-learning rate for downward causation
        self.meta_lr = 0.001

    def run_step(self):
        # 1. CA Computing (Life)
        grid = self.ca.step()
        
        # Prepare for Observer
        grid_tensor = torch.FloatTensor(grid.flatten()).unsqueeze(0).to(self.device)
        
        # 2. Observer Compressing (Intelligence)
        self.optimizer.zero_grad()
        reconstructed = self.model(grid_tensor)
        loss = self.criterion(reconstructed, grid_tensor)
        
        # Train Observer
        loss.backward()
        self.optimizer.step()
        
        current_loss = loss.item()
        
        # 3. Downward Causation (Consciousness Feedback)
        # Shift the CA's physics to maintain the 'target_loss'
        loss_error = self.target_loss - current_loss
        
        # If loss is too low (trivial), increase mu to cause more activity
        # If loss is too high (noise), decrease mu to stabilize
        # We perturb mu slightly based on this error
        self.ca.mu -= self.meta_lr * np.sign(loss_error)
        
        # Keep mu in sensible bounds for this CA type
        self.ca.mu = np.clip(self.ca.mu, 0.05, 0.3)
        
        # Inject slight noise to prevent absolute death if completely static
        if np.std(self.ca.grid) < 0.01:
            self.ca.grid += np.random.rand(*self.ca.grid.shape) * 0.1
            self.ca.grid = np.clip(self.ca.grid, 0, 1)

        # Logging
        self.history_loss.append(current_loss)
        self.history_mu.append(self.ca.mu)
        
        recon_grid = reconstructed.detach().cpu().numpy().reshape((self.ca.size, self.ca.size))
        
        return grid, recon_grid, current_loss


# --- 4. Visualization ---
def run_simulation(steps=500):
    print("Starting Self-Reading Universe Simulation...")
    print("Close the window to stop early.")
    
    universe = SelfReadingUniverse(grid_size=64)
    
    plt.ion()
    fig = plt.figure(figsize=(12, 10))
    fig.canvas.manager.set_window_title('The Self-Reading Universe')
    
    ax1 = plt.subplot(221)
    ax2 = plt.subplot(222)
    ax3 = plt.subplot(223)
    ax4 = plt.subplot(224)
    
    im1 = ax1.imshow(universe.ca.grid, cmap='magma', vmin=0, vmax=1)
    ax1.set_title("The World (CA Substrate)")
    ax1.axis('off')
    
    im2 = ax2.imshow(np.zeros((64, 64)), cmap='magma', vmin=0, vmax=1)
    ax2.set_title("The Memory (Autoencoder Reconstruction)")
    ax2.axis('off')
    
    line_loss, = ax3.plot([], [], color='red', label='Reconstruction Loss (Surprise)')
    line_target, = ax3.plot([], [], color='gray', linestyle='--', label='Target Loss (Edge of Chaos)')
    ax3.set_title("Observer Compression Error")
    ax3.set_xlim(0, 100)
    ax3.set_ylim(0, 0.15)
    ax3.legend()
    
    line_mu, = ax4.plot([], [], color='blue')
    ax4.set_title("Downward Causation: Shifting Physics (mu)")
    ax4.set_xlim(0, 100)
    ax4.set_ylim(0.0, 0.4)
    
    plt.tight_layout()
    
    try:
        for i in range(steps):
            if not plt.fignum_exists(fig.number):
                break
                
            grid, recon_grid, loss = universe.run_step()
            
            # Update visuals every few steps to speed up calculation
            if i % 2 == 0:
                im1.set_data(grid)
                im2.set_data(recon_grid)
                
                # Update plots
                x_data = range(len(universe.history_loss))
                line_loss.set_data(x_data, universe.history_loss)
                line_target.set_data(x_data, [universe.target_loss]*len(x_data))
                
                line_mu.set_data(x_data, universe.history_mu)
                
                # Adjust x-axis if needed
                if len(x_data) > 100:
                    ax3.set_xlim(0, len(x_data))
                    ax4.set_xlim(0, len(x_data))
                
                fig.canvas.draw()
                fig.canvas.flush_events()
                
            if i % 50 == 0:
                print(f"Step {i:04d} | Loss: {loss:.4f} | Target: {universe.target_loss:.4f} | Physics (mu): {universe.ca.mu:.4f}")
                
    except KeyboardInterrupt:
        print("Simulation stopped by user.")
    
    print("Simulation finished.")
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    run_simulation(steps=1000)
