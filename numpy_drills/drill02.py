import numpy as np
data = [[1, 2, 3, 4],
        [2, 3, 4, 5],
        [3, 4, 5, 6]]

np_array = np.array(data)
print("shape:", np_array.shape)
print("mean per column (axis=0):", np_array.mean(axis=0))
print("mean per row (axis=1):", np_array.mean(axis=1))