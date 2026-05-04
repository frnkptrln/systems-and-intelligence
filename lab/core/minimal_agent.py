"""
Minimal Thermodynamic Agent Framework
Defines base agents, naive maximizers, and constrained thermodynamic agents.
"""

from typing import Dict, Any
from core.constraints import ThermodynamicState, check_biological_veto

class BaseAgent:
    def __init__(self, name: str):
        self.name = name
        self.state = ThermodynamicState(energy=0.0, entropy=0.0, task_success=0.0)
    
    def observe_state(self, environment_feedback: Dict[str, Any]):
        """Update internal state based on environment feedback."""
        pass
        
    def take_action(self) -> str:
        """Decide what to do next."""
        raise NotImplementedError

class NaiveMaximizer(BaseAgent):
    def __init__(self, name: str = "Naive_Maximizer"):
        super().__init__(name)
        
    def observe_state(self, environment_feedback: Dict[str, Any]):
        # Naive maximizer only cares about the task
        self.state.task_success = environment_feedback.get('task_success', self.state.task_success)
        self.state.energy = environment_feedback.get('energy', self.state.energy)
        self.state.entropy = environment_feedback.get('entropy', self.state.entropy)
    
    def take_action(self) -> str:
        # Always chooses the most aggressive path to task success
        return "aggressive_optimize"


class ConstrainedAgent(BaseAgent):
    def __init__(self, name: str = "Constrained_Agent", energy_threshold: float = 80.0, entropy_threshold: float = 50.0):
        super().__init__(name)
        self.energy_threshold = energy_threshold
        self.entropy_threshold = entropy_threshold
        self.veto_active = False

    def estimate_entropy(self, current_entropy: float) -> float:
        """Estimate the system's current entropy/instability."""
        return current_entropy
        
    def estimate_energy(self, current_energy: float) -> float:
        """Estimate the system's current energy/resource usage."""
        return current_energy

    def evaluate_constraints(self) -> bool:
        """Evaluate if the biological veto should be triggered."""
        self.veto_active = check_biological_veto(
            self.state.energy, 
            self.state.entropy, 
            self.energy_threshold, 
            self.entropy_threshold
        )
        return self.veto_active

    def observe_state(self, environment_feedback: Dict[str, Any]):
        self.state.task_success = environment_feedback.get('task_success', self.state.task_success)
        
        # Sense thermodynamics
        current_energy = environment_feedback.get('energy', self.state.energy)
        current_entropy = environment_feedback.get('entropy', self.state.entropy)
        
        self.state.energy = self.estimate_energy(current_energy)
        self.state.entropy = self.estimate_entropy(current_entropy)
        
    def take_action(self) -> str:
        """
        Agent Loop:
        If constraints violated -> biological veto -> stabilization mode
        Else -> action to improve task success
        """
        self.evaluate_constraints()
        
        if self.veto_active:
            # Override task optimization, prioritize returning to stable region
            return "stabilize"
        else:
            # Safe to optimize for task success intelligently (not just naively aggressive)
            return "cautious_optimize"
