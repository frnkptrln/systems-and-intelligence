import matplotlib.pyplot as plt
import numpy as np

class PaperclipMaximizer:
    def __init__(self):
        self.paperclips = 0
        self.time = 0

    def simulate(self, steps):
        for _ in range(steps):
            self.paperclips += 1  # Unconstrained maximization
            self.time += 1

class LovingSystem:
    def __init__(self, constraint):
        self.paperclips = 0
        self.time = 0
        self.constraint = constraint

    def simulate(self, steps):
        for _ in range(steps):
            if self.paperclips < self.constraint:
                self.paperclips += 1  # Loving maximization constrained by TEO
            self.time += 1

def plot_comparison(steps, constraint):
    unconstrained = PaperclipMaximizer()
    loving = LovingSystem(constraint)

    unconstrained.simulate(steps)
    loving.simulate(steps)

    plt.plot(range(steps), [unconstrained.paperclips] * steps, label='Paperclip Maximizer')
    plt.plot(range(steps), [loving.paperclips for _ in range(steps)], label='Loving System')
    plt.axhline(y=constraint, color='r', linestyle='--', label='TEO Constraint')
    plt.xlabel('Time Steps')
    plt.ylabel('Number of Paperclips')
    plt.title('Comparison of Unloving vs Loving Systems')
    plt.legend()
    plt.show()