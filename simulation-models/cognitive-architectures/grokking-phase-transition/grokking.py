"""
The Grokking Phase Transition
-----------------------------
A visual simulation based on "Grokking: Generalization Beyond Overfitting 
on Small Algorithmic Datasets" (Power et al., 2022).

This script trains a small neural network on modular arithmetic (e.g., a + b = c mod P).
It visualizes the phenomenon where the network rapidly memorizes the training data 
(Train Loss -> 0, Test Loss remains high), but if trained LONG past memorization,
it suddenly undergoes a phase transition ("grokking"). At this point, it discovers 
the true underlying algorithm, and Test Loss plummets.

This visualizes the emergence of "Intelligence" (Generalization) out of pure "Data" (Memory).
"""

import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np

# --- Parameters ---
P = 97            # Prime modulo
TRAIN_FRAC = 0.5  # Fraction of all possible pairs used for training
HIDDEN_DIM = 256
EMBED_DIM = 128
WEIGHT_DECAY = 1e-2 # Weight decay is crucial for grokking to occur
LR = 1e-3
EPOCHS = 15000
PLOT_EVERY = 250

# --- Dataset Generation ---
# All possible pairs (a, b) where 0 <= a, b < P
a = torch.arange(P)
b = torch.arange(P)
grid_a, grid_b = torch.meshgrid(a, b, indexing='ij')

inputs = torch.stack([grid_a.flatten(), grid_b.flatten()], dim=1)
labels = (inputs[:, 0] + inputs[:, 1]) % P

total_size = len(inputs)
train_size = int(total_size * TRAIN_FRAC)

# Random train/test split
indices = torch.randperm(total_size)
train_idx = indices[:train_size]
test_idx = indices[train_size:]

train_inputs, train_labels = inputs[train_idx], labels[train_idx]
test_inputs, test_labels = inputs[test_idx], labels[test_idx]


# --- Model Architecture ---
class GrokkingNet(nn.Module):
    def __init__(self):
        super(GrokkingNet, self).__init__()
        # We embed the two integers
        self.embed = nn.Embedding(P, EMBED_DIM)
        # Simple MLP
        self.mlp = nn.Sequential(
            nn.Linear(EMBED_DIM * 2, HIDDEN_DIM),
            nn.ReLU(),
            nn.Linear(HIDDEN_DIM, P) # Output logits for all P classes
        )
        
    def forward(self, x):
        e1 = self.embed(x[:, 0])
        e2 = self.embed(x[:, 1])
        e = torch.cat([e1, e2], dim=1)
        return self.mlp(e)

# --- Training & Visualization ---
def run_simulation():
    print(f"Starting Grokking Simulation (P={P}, Train_Frac={TRAIN_FRAC})")
    print("This will take a moment. Watch the terminal or graph for the phase transition.")
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    model = GrokkingNet().to(device)
    optimizer = optim.AdamW(model.parameters(), lr=LR, weight_decay=WEIGHT_DECAY)
    criterion = nn.CrossEntropyLoss()
    
    ti, tl = train_inputs.to(device), train_labels.to(device)
    testi, testl = test_inputs.to(device), test_labels.to(device)
    
    history_train_loss = []
    history_test_loss = []
    history_train_acc = []
    history_test_acc = []
    history_epochs = []
    
    plt.ion()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.canvas.manager.set_window_title('The Grokking Phenomenon (Power et al. 2022)')
    
    for epoch in range(EPOCHS + 1):
        # Forward pass
        model.train()
        optimizer.zero_grad()
        out_train = model(ti)
        loss_train = criterion(out_train, tl)
        
        # Backward pass
        loss_train.backward()
        optimizer.step()
        
        if epoch % PLOT_EVERY == 0:
            model.eval()
            with torch.no_grad():
                out_test = model(testi)
                loss_test = criterion(out_test, testl)
                
                # Accuracy
                acc_train = (out_train.argmax(dim=1) == tl).float().mean().item()
                acc_test = (out_test.argmax(dim=1) == testl).float().mean().item()
            
            history_epochs.append(epoch)
            history_train_loss.append(loss_train.item())
            history_test_loss.append(loss_test.item())
            history_train_acc.append(acc_train * 100)
            history_test_acc.append(acc_test * 100)
            
            print(f"Epoch {epoch:05d} | Train Loss: {loss_train.item():.4f} | Test Loss: {loss_test.item():.4f} | Test Acc: {acc_test*100:.1f}%")
            
            if not plt.fignum_exists(fig.number):
                break
                
            # Update plots
            ax1.clear()
            ax1.set_title("Loss (Log Scale)")
            ax1.set_yscale('log')
            ax1.plot(history_epochs, history_train_loss, 'b-', label='Train Loss (Memorization)')
            ax1.plot(history_epochs, history_test_loss, 'r-', label='Test Loss (Generalization)')
            ax1.set_xlabel("Epochs")
            ax1.set_ylabel("Loss")
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Highlight Phase Transition
            if len(history_test_loss) > 1 and history_test_loss[-1] < 1.0 and history_test_loss[1] > 2.0:
                ax1.annotate('Phase Transition!\n(Grokking)', 
                             xy=(epoch, history_test_loss[-1]), 
                             xytext=(epoch - (EPOCHS*0.3), history_test_loss[-1] * 10),
                             arrowprops=dict(facecolor='black', shrink=0.05))

            ax2.clear()
            ax2.set_title("Accuracy")
            ax2.plot(history_epochs, history_train_acc, 'b-', label='Train Acc')
            ax2.plot(history_epochs, history_test_acc, 'r-', label='Test Acc')
            ax2.axhline(y=100, color='g', linestyle='--', alpha=0.5)
            ax2.set_xlabel("Epochs")
            ax2.set_ylabel("Accuracy (%)")
            ax2.set_ylim(-5, 105)
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            fig.canvas.draw()
            fig.canvas.flush_events()
            
            # Early stopping if completely grokked
            if acc_test > 0.99 and epoch > 2000:
                print("System has fully grokked the operations. Generalization achieved.")
                break

    plt.ioff()
    plt.show()

if __name__ == "__main__":
    run_simulation()
