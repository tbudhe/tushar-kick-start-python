import numpy as np
data = [[1, 2, 3, 4],
        [2, 3, 4, 5],
        [3, 4, 5, 6]]

np_array = np.array(data)
print("shape:", np_array.shape)      # every number has the same type
print("times 2:\n", np_array * 2)       # math on every number, no loop
print("first row:", np_array[0])        # row 0, like JS data[0]
print("one cell:", np_array[1, 2])      # row 1, column 2 (JS: data[1][2])