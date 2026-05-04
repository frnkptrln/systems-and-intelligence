#!/usr/bin/env python3
import os
import re
import subprocess
from pathlib import Path

REPO = "/Users/user/git/systems-and-intelligence"
SIMS_DIR = os.path.join(REPO, "simulation-models")

MAPPING = {
    "boids-flocking": "emergent-dynamics",
    "coupled-oscillators": "emergent-dynamics",
    "self-organized-criticality": "emergent-dynamics",
    "lenia": "emergent-dynamics",
    "reaction-diffusion": "emergent-dynamics",
    "phase-transition-explorer": "emergent-dynamics",
    "ecosystem-regulation": "emergent-dynamics",

    "active-inference": "cognitive-architectures",
    "hebbian-memory": "cognitive-architectures",
    "nested-learning-two-state": "cognitive-architectures",
    "prediction-error-field": "cognitive-architectures",
    "meta-learning-regime-shift": "cognitive-architectures",
    "grokking-phase-transition": "cognitive-architectures",
    "continuous-thought-machines": "cognitive-architectures",
    "tensor-logic-reasoning": "cognitive-architectures",
    "self-reading-universe": "cognitive-architectures",
    "archive-forgetting-purpose": "cognitive-architectures",

    "active-inference-veto": "alignment-and-veto",
    "ai-alignment-veto": "alignment-and-veto",
    "symbiotic-nexus": "alignment-and-veto",
    "teo-civilization": "alignment-and-veto",
    "teo-framework": "alignment-and-veto",
    "black-swan-resilience": "alignment-and-veto",
    "planetary-veto": "alignment-and-veto",
    "human-vital-systems": "alignment-and-veto",
    "utility-engineering": "alignment-and-veto",

    "stigmergy-swarm": "social-computation",
    "dao-ecosystem": "social-computation",
    "social-computation-network": "social-computation",
    "latent-introspective-society": "social-computation",
    "economic-trust-network": "social-computation",
    "coupled-lenia-boids": "social-computation",
    "political-utility-formalization": "social-computation",
    "cognitive-breathing-network": "social-computation",
    "trauma-and-deception-network": "social-computation",
    "symbiotic-breathing": "social-computation",
    "nested-emergence-demo": "social-computation",
    "rhythm-locks": "social-computation"
}

def get_new_path(old_abs_path):
    rel = os.path.relpath(old_abs_path, REPO)
    parts = rel.split(os.sep)
    if parts[0] == "simulation-models" and len(parts) > 1:
        sim_name = parts[1]
        if sim_name in MAPPING:
            cluster = MAPPING[sim_name]
            new_parts = ["simulation-models", cluster] + parts[1:]
            return os.path.join(REPO, *new_parts)
    return old_abs_path

def collect_files():
    md_files = []
    yml_files = []
    all_files = []
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in ('.git', '.venv', 'site', '__pycache__', '.pytest_cache', '.gemini', 'node_modules')]
        for f in files:
            p = os.path.join(root, f)
            all_files.append(p)
            if f.endswith('.md'):
                md_files.append(p)
            elif f.endswith('.yml') or f.endswith('.yaml'):
                yml_files.append(p)
    return all_files, md_files, yml_files

def run():
    print("=== Step 1: Create clusters ===")
    clusters = set(MAPPING.values())
    for c in clusters:
        os.makedirs(os.path.join(SIMS_DIR, c), exist_ok=True)
        print(f"Created {c}/")

    all_files, md_files, yml_files = collect_files()
    
    # Store old content before moves
    file_contents = {}
    for f in md_files + yml_files:
        with open(f, 'r') as file_obj:
            file_contents[f] = file_obj.read()

    print("\n=== Step 2: Fixing Cross-references ===")
    LINK_PATTERN = re.compile(r'(\[([^\]]*)\]\()([^)]+)(\))')
    
    # For mkdocs.yml, it doesn't use standard markdown links.
    # It uses: `  - Title: path/to/file.md`
    # We will do a generic replacement for mkdocs.yml
    mkdocs_path = os.path.join(REPO, "mkdocs.yml")
    if mkdocs_path in file_contents:
        content = file_contents[mkdocs_path]
        for sim, cluster in MAPPING.items():
            content = content.replace(f"simulation-models/{sim}/", f"simulation-models/{cluster}/{sim}/")
        file_contents[mkdocs_path] = content
        print("  Fixed mkdocs.yml")

    # Fix markdown links
    for old_file_path in md_files:
        content = file_contents[old_file_path]
        new_file_path = get_new_path(old_file_path)
        old_dir = os.path.dirname(old_file_path)
        new_dir = os.path.dirname(new_file_path)
        
        def link_replacer(match):
            prefix = match.group(1)
            link_target = match.group(3)
            suffix = match.group(4)
            
            if link_target.startswith(('http://', 'https://', 'mailto:', '#')):
                return match.group(0)
            
            # Extract anchor if any
            anchor = ""
            if '#' in link_target:
                link_target, anchor = link_target.split('#', 1)
                anchor = "#" + anchor
                
            # If the link ends with a slash (like simulation-models/teo-civilization/)
            is_dir_link = link_target.endswith('/')
            
            # Resolve old absolute path of the target
            target_abs = os.path.normpath(os.path.join(old_dir, link_target))
            
            # Check if this target is moving
            new_target_abs = get_new_path(target_abs)
            
            if new_target_abs != target_abs or old_file_path != new_file_path:
                # Need to re-relativize
                rel_link = os.path.relpath(new_target_abs, new_dir)
                if is_dir_link and not rel_link.endswith('/'):
                    rel_link += '/'
                return f"{prefix}{rel_link}{anchor}{suffix}"
            
            return match.group(0)
            
        new_content = LINK_PATTERN.sub(link_replacer, content)
        
        # Also fix plain text references in files like simulation-theory-map.md
        # where there might be bare links like `simulation-models/X/`
        for sim, cluster in MAPPING.items():
            # Only replace if it's not already clustered
            new_content = re.sub(rf'(?<!{cluster}/)simulation-models/{sim}/', f'simulation-models/{cluster}/{sim}/', new_content)
        
        file_contents[old_file_path] = new_content

    print("\n=== Step 3: Moving files ===")
    moved_count = 0
    for sim, cluster in MAPPING.items():
        src = os.path.join(SIMS_DIR, sim)
        dst = os.path.join(SIMS_DIR, cluster, sim)
        if os.path.exists(src):
            try:
                subprocess.run(['git', 'mv', src, dst], check=True, cwd=REPO)
                moved_count += 1
            except subprocess.CalledProcessError:
                os.rename(src, dst)
                moved_count += 1
    print(f"Moved {moved_count} simulation directories.")

    print("\n=== Step 4: Writing updated files ===")
    for old_path, content in file_contents.items():
        new_path = get_new_path(old_path)
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        with open(new_path, 'w') as f:
            f.write(content)
            
        # If the file moved, the old file was already moved via directory move.
        # But wait, git mv moves the whole directory, so the file AT new_path 
        # already exists and we just overwrite it with the updated links.
        # If the directory wasn't moved, we just update it in place.

if __name__ == "__main__":
    run()
