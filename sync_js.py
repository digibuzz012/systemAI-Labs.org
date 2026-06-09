import os
import glob
import re

# Read index.html to extract the main script
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

script_match = re.search(r'<script>.*?</script>', index_html, re.DOTALL)
if script_match:
    full_script = script_match.group(0)
else:
    print("Could not find script in index.html")
    exit(1)

html_files = glob.glob('*.html')
files_to_skip = ['index.html', 'index (1).html']

for file in html_files:
    if file in files_to_skip:
        continue
        
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace any existing <script> block at the bottom with the full_script
    content = re.sub(r'<script>.*?</script>', full_script, content, flags=re.DOTALL)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Injected JS into {file}")

