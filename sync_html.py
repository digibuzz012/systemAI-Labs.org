import re
import os

# 1. Load index.html and extract blocks
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

# Extract Nav
nav_match = re.search(r'<nav class="nav" id="nav">.*?</nav>', index_html, re.DOTALL)
if not nav_match:
    print("nav_match not found")
master_nav = nav_match.group(0)

# Modify Nav links to point to index.html for product pages
product_nav = master_nav.replace('href="#services"', 'href="index.html#services"')
product_nav = product_nav.replace('href="#work"', 'href="index.html#work"')
product_nav = product_nav.replace('href="#manifesto"', 'href="index.html#manifesto"')
# Handle Logo
product_nav = product_nav.replace('href="#"', 'href="index.html"')

# Extract Footer
footer_match = re.search(r'<footer>.*?</footer>', index_html, re.DOTALL)
if not footer_match:
    print("footer_match not found")
master_footer = footer_match.group(0)

# Extract Hero BG
hero_bg_match = re.search(r'<div class="hero-bg">.*?</div>\s*</div>', index_html, re.DOTALL)
if not hero_bg_match:
    # Just up to closing div
    hero_bg_match = re.search(r'<div class="hero-bg">.*?</div>', index_html, re.DOTALL)
if not hero_bg_match:
    print("hero_bg_match not found")
hero_bg = hero_bg_match.group(0)

# 2. Process product pages
product_pages = [
    'enterprise-hr-ai-agent.html',
    'real-estate-chatbot.html',
    'SyllabusAI.html',
    'context-miner.html'
]

for page in product_pages:
    if os.path.exists(page):
        with open(page, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace Nav (product pages use <nav class="navbar">)
        content = re.sub(r'<nav class="navbar">.*?</nav>', product_nav, content, flags=re.DOTALL)
        
        # Replace Footer
        content = re.sub(r'<footer.*?>.*?</footer>', master_footer, content, flags=re.DOTALL)
        
        # Replace blueprint-bg-dark header with hero header + orbs
        content = re.sub(r'<header class="blueprint-bg-dark.*?>', f'<header class="hero" style="padding-top: 160px; padding-bottom: 100px;">\n        {hero_bg}', content)
        
        # Remove blueprint-bg classes
        content = content.replace('blueprint-bg', '')
        
        # Remove inline JetBrains Mono
        content = content.replace("font-family: 'JetBrains Mono', monospace;", "")
        # Remove inline Inter
        content = content.replace("font-family: 'Inter', sans-serif;", "")
        
        # Change hardcoded #000 background to var(--bg-elevated)
        content = content.replace('background: #000;', 'background: var(--bg-elevated);')
        
        with open(page, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Synchronized {page}")
