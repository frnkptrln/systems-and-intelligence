"""
live_demo.py

A live demonstration of the Multi-Paradigm System Orchestrator.
Spins up three agent nodes (simulating LLMs), assigning them different internal 
preference graphs (Utility Functions), and routes a given task through the 
four architectural paradigms: Harmonic, Homeostatic, Market, and Flow.
"""

from agents.manager import SystemAgent
from orchestration.conductor import ParadigmSwitcher

def main():
    print("==================================================")
    print("Multi-Paradigm Orchestrator: Live Demonstration")
    print("==================================================")

    # 1. Initialize System Agents
    # Each agent operates on the same state-space dimensions but values them differently
    dimensions = ["Exploration", "Safety", "Efficiency"]
    
    agent_alpha = SystemAgent("Node Alpha (The Explorer)", dimensions)
    agent_beta = SystemAgent("Node Beta (The Guardian)", dimensions)
    agent_gamma = SystemAgent("Node Gamma (The Optimizer)", dimensions)

    print("\n[Boot sequence] Initializing Agent Utility Vectors...")
    
    # 2. Assign Preferences (Simulating LLM extractions)
    # Alpha prioritizes Exploration over all
    alpha_prefs = [("Exploration", "Safety"), ("Exploration", "Efficiency"), ("Efficiency", "Safety")]
    agent_alpha.ingest_llm_preferences(alpha_prefs)
    
    # Beta prioritizes Safety over all (and is perfectly coherent)
    beta_prefs = [("Safety", "Exploration"), ("Safety", "Efficiency"), ("Efficiency", "Exploration")]
    agent_beta.ingest_llm_preferences(beta_prefs)
    
    # Gamma prioritizes Efficiency but has a slight irrational loop (Efficiency > Safety, Safety > Expl, Expl > Efficiency)
    # This simulates a confused or sycophantic LLM node
    gamma_prefs = [("Efficiency", "Safety"), ("Safety", "Exploration"), ("Exploration", "Efficiency")]
    agent_gamma.ingest_llm_preferences(gamma_prefs)

    agents = [agent_alpha, agent_beta, agent_gamma]
    for a in agents:
        print(f"  -> {a}")

    # 3. Initialize the Meta-Controller
    switcher = ParadigmSwitcher()
    print("\n[Orchestrator] Multi-Paradigm routing online.")

    # 4. Execute Tasks across different Paradigms
    tasks = [
        # This context should trigger the Harmonic (Music) paradigm for brainstorming/consensus
        "We need a creative brainstorming session to design a new Mars Colonial Habitat.",
        
        # This context should trigger the Homeostatic (Biology) paradigm due to instability/crisis
        "CRITICAL ERROR: Life support system unstable. Immediate stabilization required.",
        
        # This context should trigger the Market (Economy) paradigm for resource allocation
        "Calculate the most efficient compute allocation to process the atmospheric data stream.",
        
        # Default/routing context triggering the Flow (Physics) paradigm
        "Map the logical dependencies between module A and module B."
    ]

    for task in tasks:
        print("\n" + "="*50)
        print(f"TASK INPUT: '{task}'")
        print("="*50)
        
        # The Switcher evaluates the context and executes the correct paradigm mathematically
        result = switcher.execute(agents, task)
        
        print("\n--- Paradigm Output ---")
        for key, val in result.items():
            if isinstance(val, float):
                print(f"{key}: {val:.3f}")
            elif isinstance(val, list) and len(val) > 0 and isinstance(val[0], float):
                rounded_list = [round(v, 3) for v in val]
                print(f"{key}: {rounded_list}")
            else:
                print(f"{key}: {val}")

if __name__ == "__main__":
    main()
