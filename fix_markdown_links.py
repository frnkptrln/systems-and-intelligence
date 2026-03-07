import os
import re

directories_to_check = ['theory', 'docs/book']

count = 0
for d in directories_to_check:
    for root, dirs, files in os.walk(d):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                
                # Match links like [text](../path/to/dir/) and append README.md
                new_content = re.sub(r'\]\(([^)]*\/)\)', r'](\1README.md)', content)
                
                if new_content != content:
                    with open(filepath, 'w') as f:
                        f.write(new_content)
                    print(f"Fixed links in {filepath}")
                    count += 1
print(f"Fixed {count} files.")
