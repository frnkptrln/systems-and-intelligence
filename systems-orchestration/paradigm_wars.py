#!/usr/bin/env python3
"""
paradigm_wars.py

A competitive MAS environment where different orchestration paradigms 
(Harmonic, Homeostatic, Market, Flow) compete for survival.

This script demonstrates the resilience and efficiency of each paradigm
under varying environmental stress.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Any

# Ensure we can import from the current directory structure
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from orchestration.conductor import HarmonicParadigm, HomeostaticParadigm, MarketParadigm, FlowParadigm
from agents.manager import SystemAgent

class Environment:
    """
    The competitive arena state space.
    The environment has a 'target' utility vector that drifts over time.
    """
    def __init__(self, dimensions: List[str]):
        self.dimensions = dimensions
        self.target = np.random.dirichlet(np.ones(len(dimensions)))
        self.drift_speed = 0.02
        self.volatility = 0.05

    def step(self):
        """Update the environmental target utility."""
        noise = np.random.normal(0, self.volatility, len(self.dimensions))
        self.target += noise * self.drift_speed
        self.target = np.clip(self.target, 0.01, 1.0)
        self.target /= self.target.sum()

    def get_reward(self, system_action_vector: np.ndarray) -> float:
        """Reward is the alignment (cosine similarity) with the target."""
        if np.linalg.norm(system_action_vector) == 0:
            return 0.0
        return np.dot(system_action_vector, self.target) / (
            np.linalg.norm(system_action_vector) * np.linalg.norm(self.target)
        )

class SystemCompetitor:
    """
    A 'system' consist of a group of agents and a fixed orchestration paradigm.
    """
    def __init__(self, name: str, paradigm: Any, agents: List[SystemAgent]):
        self.name = name
        self.paradigm = paradigm
        self.agents = agents
        self.resources = 1.0  # Normalized starting resources
        self.living = True
        self.history = []

    def act(self, context: str) -> np.ndarray:
        """Executes orchestration and returns the resulting utility vector."""
        result = self.paradigm.orchestrate(self.agents, context)
        
        # Depending on paradigm, we synthesize the collective action vector
        if self.name == "Harmonic":
            weights = np.array(result["agent_weights"])
            action = sum(w * agent.u for w, agent in zip(weights, self.agents))
        elif self.name == "Homeostatic":
            anchor_idx = result["anchor_agent_idx"]
            action = self.agents[anchor_idx].u
        elif self.name == "Market":
            winner_idx = result["winning_agent_idx"]
            action = self.agents[winner_idx].u
        else: # Flow
            # Simple average for flow in this toy model
            action = np.mean([agent.u for agent in self.agents], axis=0)
            
        return action / np.linalg.norm(action) if np.linalg.norm(action) > 0 else action

    def update(self, reward: float, cost: float):
        """Update internal state based on performance."""
        if not self.living:
            return
        
        self.resources += (reward - cost)
        self.resources = max(0, self.resources)
        
        if self.resources <= 0:
            self.living = False
            
        self.history.append(self.resources)

def run_competition(steps=500):
    print("═" * 60)
    print("  PARADIGM WARS: Orchestration Competition")
    print("═" * 60)
    
    dims = ["Speed", "Safety", "Efficiency", "Innovation", "Reliability"]
    env = Environment(dims)
    
    # Initialize agents with slightly different (noisy) utility functions
    def create_agents(count=5):
        agents = []
        for i in range(count):
            a = SystemAgent(f"Node-{i}", dims)
            # Random transitive preferences
            prefs = []
            shuffled_dims = dims.copy()
            np.random.shuffle(shuffled_dims)
            for j in range(len(shuffled_dims)-1):
                prefs.append((shuffled_dims[j], shuffled_dims[j+1]))
            a.ingest_llm_preferences(prefs)
            agents.append(a)
        return agents

    competitors = [
        SystemCompetitor("Harmonic", HarmonicParadigm(), create_agents()),
        SystemCompetitor("Homeostatic", HomeostaticParadigm(), create_agents()),
        SystemCompetitor("Market", MarketParadigm(), create_agents()),
        SystemCompetitor("Flow", FlowParadigm(), create_agents())
    ]
    
    cost_per_step = 0.75 # Threshold for survival
    
    for i in range(steps):
        env.step()
        context = "Normal operation"
        if i % 100 == 0:
            context = "CRITICAL UNSTABLE SHOCK"
            env.volatility *= 5.0
        elif i % 100 == 10:
            env.volatility = 0.05
            
        for comp in competitors:
            if comp.living:
                action = comp.act(context)
                reward = env.get_reward(action)
                comp.update(reward, cost_per_step)

    # --- Results ---
    print("\nFinal Rankings:")
    sorted_comps = sorted(competitors, key=lambda c: c.resources, reverse=True)
    for i, c in enumerate(sorted_comps):
        status = "ALIVE" if c.living else "DEAD"
        print(f" {i+1}. {c.name:12s} │ Resources: {c.resources:6.3f} │ Status: {status}")

    # --- Visualization ---
    plt.figure(figsize=(12, 6))
    plt.style.use('dark_background')
    plt.title("Paradigm Wars: Resource Resilience over Time", fontsize=14, color="#e0e0ff", pad=20)
    
    colors = ["#60a0ff", "#ff6060", "#80ffb0", "#ffaa44"]
    for idx, comp in enumerate(competitors):
        plt.plot(comp.history, label=comp.name, color=colors[idx], linewidth=2)
        
    plt.axhline(0, color="#555", linestyle="--")
    plt.xlabel("Step", color="#999")
    plt.ylabel("Resources", color="#999")
    plt.legend()
    plt.grid(alpha=0.1)
    
    # Save results
    output_path = "paradigm_wars_results.png"
    plt.savefig(output_path)
    print(f"\nVisual results saved to: {output_path}")
    print("═" * 60)

if __name__ == "__main__":
    run_competition()
