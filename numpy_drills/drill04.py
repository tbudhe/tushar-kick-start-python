import numpy as np
array = np.array([1,2,3,4,5,6])
print(array.shape)
grid = array.reshape(2, 3)    # same six numbers, 2 rows x 3 columns
print(grid)
print(grid.shape)

print(grid.T)               # transpose: rows become columns
print(grid.T.shape)

print(grid.flatten())       # back to one flat row
