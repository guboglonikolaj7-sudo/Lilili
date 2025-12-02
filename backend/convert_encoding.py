# convert_encoding.py
import sys

# Конвертируем models.py
with open('apps/subscriptions/models.py', 'r', encoding='cp1251') as f:
    content = f.read()

with open('apps/subscriptions/models.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ models.py конвертирован в UTF-8")

# Конвертируем admin.py
with open('apps/subscriptions/admin.py', 'r', encoding='cp1251') as f:
    content = f.read()

with open('apps/subscriptions/admin.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ admin.py конвертирован в UTF-8")