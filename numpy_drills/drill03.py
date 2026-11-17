import numpy as np
splits = input().split()
print(splits)
n, m = map(int, splits)
print("n:", n, "m:", m)

rows = []
for _ in range(n):
    rows.append(list(map(int, input().split())))
print("rows:", rows)

arr = np.array(rows)

print("shape:", arr.shape)
print("orders per day (axis=0):", arr.sum(axis=0))
print("orders per store (axis=1):", arr.sum(axis=1))