a = 30
b = a
for i in range(40):
  a = a * 0.98
  b += a
print(b)