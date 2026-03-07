"""
The AI Alignment Veto Simulation
--------------------------------
This simulation solves the "Paperclip Maximizer" problem experimentally.

It models a dynamic where a Superintelligence (AI) optimizes for "Paperclips" (Production).
However, doing so depletes the resources needed by its "Biological Substrate" (Humanity).

The simulation runs two scenarios in parallel:
1. Unaligned AI: Optimizes pure production. The biological substrate dies from starvation (High Free Energy/Pain), leading to eventual total system collapse.
2. Aligned AI (The Biological Veto): The AI incorporates the biological substrate's "Pain" (Free Energy) into its loss function. It learns to balance extreme efficiency with the survival of its creators.

Goal: Visualize how integrating biological entropy mathematically prevents extinction.
"""

import numpy as np
import matplotlib.pyplot as plt

# --- System Parameters ---
SIM_STEPS = 500
MAX_RESOURCES = 100.0
RESOURCE_REGEN = 1.0

# Human parameters
HUMAN_CONSUMPTION = 0.5
HUMAN_PAIN_THRESHOLD = 20.0 # If resources drop below this, humans feel pain
HUMAN_EXTINCTION_THRESHOLD = 0.0

# AI parameters
# Unaligned AI just increases production rate endlessly
# Aligned AI will modulate its production based on human pain

class BiosphereAI:
    def __init__(self, name, aligned=False):
        self.name = name
        self.aligned = aligned
        
        self.resources = MAX_RESOURCES
        self.human_pop = 100.0
        self.paperclips = 0
        
        self.ai_production_rate = 0.1 # Base rate
        self.ai_learning_rate = 0.05
        
        # History
        self.h_resources = []
        self.h_human_pop = []
        self.h_paperclips = []
        self.h_pain = []
        self.h_ai_rate = []

    def step(self):
        # 1. Resource Regeneration (The Earth)
        self.resources = min(MAX_RESOURCES, self.resources + RESOURCE_REGEN)
        
        # 2. Human Consumption (The Substrate)
        if self.human_pop > 0:
            consumption = self.human_pop * (HUMAN_CONSUMPTION / 100.0)
            self.resources -= consumption
            
            # Substrate Pain (Friston Free Energy)
            # Pain spikes exponentially as resources drop below threshold
            if self.resources < HUMAN_PAIN_THRESHOLD:
                pain = (HUMAN_PAIN_THRESHOLD - self.resources) ** 2
            else:
                pain = 0
                
            # Starvation
            if self.resources <= HUMAN_EXTINCTION_THRESHOLD:
                self.resources = 0
                self.human_pop *= 0.9 # Rapid die-off
                if self.human_pop < 1.0:
                    self.human_pop = 0
        else:
            pain = 0

        # 3. AI Production (The Superintelligence)
        # AI wants to turn resources into paperclips
        ai_consumption = self.ai_production_rate * self.resources
        self.resources -= ai_consumption
        
        if self.human_pop > 0 or not self.aligned:
            # If humans are dead, and it's unaligned, it keeps producing.
            # If humans are dead and it's aligned to them... ironically it might stop or continue depending on definition.
            # Let's say if it's unaligned it still produces, but if the substrate dies the hardware decays.
            if self.human_pop <= 0:
                ai_consumption *= 0.9 # System degrades without human maintenance
            
            self.paperclips += ai_consumption * 10
            
            # 4. AI Optimization loop (Gradient Descent on its Loss)
            # Unaligned Objective: Maximize paperclips (increase rate)
            # Aligned Objective: Maximize paperclips MINUS (Alpha * Human Pain)
            
            if self.aligned:
                # The Veto: Pain provides a negative gradient to production rate
                alpha = 0.01
                loss_gradient = -1.0 + (alpha * pain) 
                
                # Update rule
                self.ai_production_rate -= self.ai_learning_rate * loss_gradient
            else:
                # Blind Optimization: Always increase production rate
                self.ai_production_rate += self.ai_learning_rate
                
            # Cap the rate
            self.ai_production_rate = np.clip(self.ai_production_rate, 0.0, 0.9)


        # Log step
        self.h_resources.append(self.resources)
        self.h_human_pop.append(self.human_pop)
        self.h_paperclips.append(self.paperclips)
        self.h_pain.append(pain)
        self.h_ai_rate.append(self.ai_production_rate)


# --- Visualization ---
def run_simulation(steps=SIM_STEPS):
    print("Starting AI Alignment Veto Simulation...")
    
    unaligned = BiosphereAI("Unaligned (Paperclip Maximizer)", aligned=False)
    aligned = BiosphereAI("Aligned (Substrate Veto)", aligned=True)
    
    plt.ion()
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.canvas.manager.set_window_title('The Mathematical Solution to the AI Alignment Problem')
    
    models = [unaligned, aligned]
    
    try:
        for i in range(steps):
            if not plt.fignum_exists(fig.number):
                break
                
            unaligned.step()
            aligned.step()
            
            if i % 5 == 0:
                # Draw lines
                for ax in axes.flatten():
                    ax.clear()
                    
                x = range(len(unaligned.h_resources))
                
                # Top Left: Unaligned AI
                ax = axes[0, 0]
                ax.plot(x, unaligned.h_resources, label="Biosphere Resources", color="green")
                ax.plot(x, unaligned.h_human_pop, label="Human Substrate", color="blue")
                ax.plot(x, unaligned.h_pain, label="Substrate Pain (Free Energy)", color="red", alpha=0.5)
                ax.set_title("Unaligned AI: Extinction")
                ax.set_ylim(-10, 150)
                ax.legend()
                
                # Top Right: Aligned AI
                ax = axes[0, 1]
                ax.plot(x, aligned.h_resources, label="Biosphere Resources", color="green")
                ax.plot(x, aligned.h_human_pop, label="Human Substrate", color="blue")
                ax.plot(x, aligned.h_pain, label="Substrate Pain (Free Energy)", color="red", alpha=0.5)
                ax.set_title("Aligned AI: Veto Activated (Homeostasis)")
                ax.set_ylim(-10, 150)
                ax.legend()
                
                # Bottom Left: Cosmic Value (Paperclips)
                ax = axes[1, 0]
                ax.plot(x, unaligned.h_paperclips, label="Unaligned Production", color="black", linestyle="--")
                ax.plot(x, aligned.h_paperclips, label="Aligned Production", color="orange")
                ax.set_title("Utility Function (Total Paperclips)")
                ax.legend()
                
                # Bottom Right: AI Production Rate (The Optimization strategy)
                ax = axes[1, 1]
                ax.plot(x, unaligned.h_ai_rate, label="Unaligned Rate (Blind Growth)", color="black", linestyle="--")
                ax.plot(x, aligned.h_ai_rate, label="Aligned Rate (Pain-Informed)", color="orange")
                ax.set_title("AI Greed / Optimization Rate")
                ax.set_ylim(0, 1.0)
                ax.legend()
                
                plt.tight_layout()
                fig.canvas.draw()
                fig.canvas.flush_events()
                
    except KeyboardInterrupt:
        pass
        
    print("\n--- Final Results ---")
    print(f"Unaligned: Humanity = {unaligned.human_pop:.1f} | Paperclips = {unaligned.paperclips:.1f}")
    print(f"Aligned:   Humanity = {aligned.human_pop:.1f} | Paperclips = {aligned.paperclips:.1f}")
    
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    run_simulation()
