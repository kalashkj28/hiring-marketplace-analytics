import re

with open('dashboard.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Add cliponaxis=False
text = text.replace('textposition="outside"', 'textposition="outside", cliponaxis=False')
text = text.replace('textposition="inside" if is_large else "outside",', 'textposition="inside" if is_large else "outside", cliponaxis=False,')

# Extend right margin significantly so text fits in the empty space
text = re.sub(r'r=\d+', 'r=120', text)

with open('dashboard.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Done fixing!")
