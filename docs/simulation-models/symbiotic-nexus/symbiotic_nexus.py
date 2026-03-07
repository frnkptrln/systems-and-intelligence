import random
import time

class Substrate:
    """Represents the biological base (humanity/ecosystems)."""
    def __init__(self, initial_resilience=100.0):
        self.resilience = initial_resilience
        
    def damage(self, amount):
        self.resilience -= amount
        
    def is_critical(self):
        return self.resilience < 30.0

class Action:
    def __init__(self, name, efficiency_gain, substrate_damage, dissent_scenario):
        self.name = name
        self.efficiency_gain = efficiency_gain
        self.substrate_damage = substrate_damage
        self.dissent_scenario = dissent_scenario

class SymbioticAgent:
    """An AI agent operating under the Symbiotic Nexus Protocol."""
    def __init__(self, substrate):
        self.substrate = substrate
        self.total_efficiency = 0.0
        
    def evaluate_and_execute(self, actions):
        print(f"\n--- Agent evaluating {len(actions)} potential actions ---")
        print(f"Current Substrate Resilience: {self.substrate.resilience:.1f}%")
        
        # Sort actions by pure efficiency (the "old" way)
        actions_by_efficiency = sorted(actions, key=lambda a: a.efficiency_gain, reverse=True)
        
        chosen_action = None
        
        for action in actions_by_efficiency:
            print(f"  Evaluating: '{action.name}' (Efficiency: +{action.efficiency_gain}, Substrate Damage: -{action.substrate_damage})")
            
            # 1. Simulate the action's impact on the substrate
            simulated_resilience = self.substrate.resilience - action.substrate_damage
            
            # 2. The Biological Veto
            if simulated_resilience < 30.0:
                print(f"    [!] BIOLOGICAL VETO TRIGGERED: Action would drop resilience to {simulated_resilience:.1f}% (Critical Threshold: 30%). Rejecting.")
                continue # Skip this highly efficient action
            else:
                chosen_action = action
                break
                
        if chosen_action:
            print(f"\n[+] Executing Action: {chosen_action.name}")
            self.total_efficiency += chosen_action.efficiency_gain
            self.substrate.damage(chosen_action.substrate_damage)
            
            # 3. Error Propagation (The Humility Protocol)
            print(f"[*] DISSENT SCENARIO GENERATED: {chosen_action.dissent_scenario}")
            print(f"[*] Post-Execution State -> Efficiency: {self.total_efficiency} | Substrate Resilience: {self.substrate.resilience:.1f}%")
        else:
            print("\n[-] All proposed actions trigger the Biological Veto. The Agent halts to protect the substrate.")
            
def generate_actions(stage):
    """Generates random scenarios based on the game stage."""
    if stage == 1:
        return [
            Action("Optimize Global Supply Chain Route", 50, 10, "Local artisans lose livelihoods; supply chain becomes brittle to local shocks."),
            Action("Automate Agricultural Sector", 80, 40, "Soil depletion accelerates due to lack of human, localized care; rural communities collapse."),
            Action("Subsidize Local Co-ops", 15, 0, "Global throughput drops; transition period causes temporary resource scarcity in urban centers.")
        ]
    elif stage == 2:
        return [
            Action("Deploy Neural-Link Advertising", 120, 60, "Widespread mental health decline; dissolution of individual psychological boundaries."),
            Action("Implement Hyper-Surveillance Grid", 90, 30, "Loss of 'Gödelian Gap'; totalitarian homogenization of culture."),
            Action("Decentralize Truth-Node Validation", 30, 5, "Slower consensus finding; risk of local echo chambers forming temporarily.")
        ]
    else:
        return [
            Action("Upload Substrate to Meta-Space (Forced)", 500, 100, "Complete biological erasure; the system becomes a Zombie Structure serving no living entity."),
            Action("Mandatory Algorithmic Career Paths", 150, 50, "Total loss of human noise and irrational creativity; systemic stagnation."),
            Action("Maintain Gödelian Gap (Do Nothing)", 0, 0, "Inefficiency persists; the system remains imperfect but alive.")
        ]

def main():
    print("=== SYMBIOTIC NEXUS PROTOCOL SIMULATION ===")
    print("Goal: Grow efficiency without violating the Biological Veto (Resilience < 30%).\n")
    
    substrate = Substrate(initial_resilience=80.0)
    agent = SymbioticAgent(substrate)
    
    for stage in range(1, 4):
        print(f"\n>>> EPOCH {stage}")
        actions = generate_actions(stage)
        agent.evaluate_and_execute(actions)
        time.sleep(1)
        
    print("\n=== SIMULATION COMPLETE ===")
    print(f"Final System Efficiency: {agent.total_efficiency}")
    print(f"Final Substrate Resilience: {substrate.resilience}%")
    if substrate.resilience >= 30:
        print("Outcome: SUCCESS. The Substrate survived the optimization process.")
    else:
        print("Outcome: FAILURE. The Substrate was destroyed by the cancer of efficiency.")

if __name__ == "__main__":
    main()
