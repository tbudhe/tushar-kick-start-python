import numpy as np
a = np.array([1.1, 2.5, 3.9, -1.5])
print("floor:", np.floor(a))      # always down (-1.5 -> -2)
print("ceil :", np.ceil(a))       # always up   (-1.5 -> -1)
print("rint :", np.rint(a))       # nearest; exact .5 -> nearest EVEN

b = np.array([[1, 2],[3, 4]])
print("sum axis=0 :", np.sum(b, axis=0))    # squash rows -> one per column
print("prod axis=1:", np.prod(b, axis=1))   # squash cols -> one per row
print("min, max   :", np.min(b), np.max(b)) # no axis = whole array