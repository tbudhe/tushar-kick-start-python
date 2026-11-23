import numpy as np
a = [[1, 2], [3, 4]]
b = [[5, 6], [7, 8]]
np_cols = np.concatenate((a,b),axis=0)
print(np_cols)
print(np_cols.shape)
np_rows = np.concatenate((a,b),axis=1)
print(np_rows)
print(np_rows.shape) 