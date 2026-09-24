import re

with open('dashboard.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Change all r=120 to r=30 to remove the huge empty space on the right
text = re.sub(r'r=120', 'r=30', text)

with open('dashboard.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Empty space fixed!")
