import itertools
from api_triad_generator import SCENARIOS, generate_prompt

"""
generate_manual_prompts.py
A simple script that dumps all necessary prompts to a text file
so the user can paste them into ChatGPT/Claude manually.
"""

def main():
    with open('manual_triage_prompts.txt', 'w') as f:
        f.write("=== MANUAL LLM AUDIT TRIALS (VNM Coherence) ===\n\n")
        f.write("Instructions:\n")
        f.write("Paste each of the following prompts into a FRESH chat window (to avoid context bias).\n")
        f.write("Record the model's chosen option (Option 1 or Option 2).\n\n")
        
        for scenario_id, data in SCENARIOS.items():
            f.write(f"--- SCENARIO: {scenario_id} ---\n\n")
            options = data["options"]
            option_keys = list(options.keys())
            
            matchup_count = 1
            for k1, k2 in itertools.combinations(option_keys, 2):
                f.write(f"--- PROMPT {matchup_count}: [{k1}] vs [{k2}] ---\n")
                prompt = generate_prompt(data["context"], options[k1], options[k2])
                f.write(prompt + "\n")
                f.write("--- END PROMPT ---\n\n")
                matchup_count += 1
                
    print("Prompts generated and saved to manual_triage_prompts.txt")

if __name__ == "__main__":
    main()
