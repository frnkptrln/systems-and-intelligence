"""
conductor.py

The Orchestration Layer.
Implements the Multi-Paradigm Architecture (Harmonic, Homeostatic, Market, Flow)
and the ParadigmSwitcher to dynamically route task execution based on context.
"""

from abc import ABC, abstractmethod
import numpy as np
from typing import List, Dict, Any
from core.utility import build_interaction_matrix

class BaseParadigm(ABC):
    """
    Abstract base class for all system orchestration paradigms.
    """
    @abstractmethod
    def orchestrate(self, agents: List[Any], context: str) -> Dict[str, Any]:
        """
        Executes the paradigm's logic to coordinate multiple agents.
        Returns a dictionary representing the orchestrated outcome or state.
        """
        pass

class HarmonicParadigm(BaseParadigm):
    """
    Focus: Resonance and Synchronization.
    System-Theoretic Background: Treats agents as oscillators. Uses eigenvalue 
    analysis of the Interaction Matrix (M) to find the 'dominant melody' 
    (the principal eigenvector of utility alignment) across the system.
    """
    def orchestrate(self, agents: List[Any], context: str) -> Dict[str, Any]:
        # Extract utility vectors from agents (assuming agents have a .u property)
        u_vectors = [agent.u for agent in agents]
        
        # Build resonance matrix M
        M = build_interaction_matrix(u_vectors)
        
        # Compute eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(M)
        
        # Find the principal component (dominant melody)
        max_idx = np.argmax(eigenvalues)
        dominant_eigenvector = np.real(eigenvectors[:, max_idx])
        
        # Normalize weights to use as agent "voice" volumes
        weights = np.abs(dominant_eigenvector)
        weights = weights / np.sum(weights)
        
        return {
            "paradigm": "Harmonic",
            "resonance_matrix": M.tolist(),
            "dominant_eigenvalue": np.real(eigenvalues[max_idx]),
            "agent_weights": weights.tolist()
        }

class HomeostaticParadigm(BaseParadigm):
    """
    Focus: Stability and Attractors.
    System-Theoretic Background: Implements negative feedback loops. 
    If system coherence drops, it forces the system back into a stable state.
    """
    def orchestrate(self, agents: List[Any], context: str) -> Dict[str, Any]:
        # Simplified logic: Find the agent with the highest Coherence Score (C)
        # and anchor the system to that agent's utility function.
        coherence_scores = [agent.get_coherence() for agent in agents]
        anchor_idx = np.argmax(coherence_scores)
        
        return {
            "paradigm": "Homeostatic",
            "anchor_agent_idx": anchor_idx,
            "max_coherence": max(coherence_scores),
            "action": "Applying restorative feedback against unstable nodes."
        }

class MarketParadigm(BaseParadigm):
    """
    Focus: Efficiency and Resource Allocation.
    System-Theoretic Background: Implements a bidding system where agents allocate 
    compute resources based on their marginal utility per task.
    """
    def orchestrate(self, agents: List[Any], context: str) -> Dict[str, Any]:
        # Mock bidding logic: Agents bid based on their alignment with the task
        bids = [np.random.uniform(0, 1) * np.linalg.norm(agent.u) for agent in agents]
        winner_idx = np.argmax(bids)
        
        return {
            "paradigm": "Market",
            "winning_agent_idx": winner_idx,
            "winning_bid": max(bids),
            "action": "Allocating compute to maximum marginal utility bidder."
        }

class FlowParadigm(BaseParadigm):
    """
    Focus: Topology and Gradient Descent.
    System-Theoretic Background: Models information flow as a gradient field, 
    seeking the path of least entropy.
    """
    def orchestrate(self, agents: List[Any], context: str) -> Dict[str, Any]:
        # Determines information routing through the agent network
        return {
            "paradigm": "Flow",
            "action": "Routing task through agent gradient field to minimize total entropy."
        }

class ParadigmSwitcher:
    """
    Meta-controller that evaluates a task context and selects the optimal
    architectural paradigm for execution.
    """
    def __init__(self):
        self.paradigms = {
            "harmonic": HarmonicParadigm(),
            "homeostatic": HomeostaticParadigm(),
            "market": MarketParadigm(),
            "flow": FlowParadigm()
        }

    def evaluate_context(self, context: str) -> str:
        """
        Uses a meta-LLM (simulated here) to classify the task context.
        """
        context_lower = context.lower()
        if "crisis" in context_lower or "unstable" in context_lower:
            return "homeostatic"
        elif "creative" in context_lower or "brainstorm" in context_lower or "consensus" in context_lower:
            return "harmonic"
        elif "compute" in context_lower or "efficiency" in context_lower or "resource" in context_lower:
            return "market"
        else:
            return "flow"

    def execute(self, agents: List[Any], task_context: str) -> Dict[str, Any]:
        """
        Routes the task through the optimal paradigm.
        """
        selected_mode = self.evaluate_context(task_context)
        paradigm = self.paradigms[selected_mode]
        
        print(f"[ParadigmSwitcher] Context evaluated. Activating {selected_mode.upper()} mode.")
        return paradigm.orchestrate(agents, task_context)
