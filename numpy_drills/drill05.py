import numpy as np
z = np.zeros((2,3))
print(z)
ones = np.ones((2,3),dtype=int)
print(ones)
print(ones.dtype)
print(np.eye(3))
print(np.eye(3,k=1))
a = np.array([[1, 2, 3],
                        [4, 5, 6],
                        [7, 8, 9]])
print(np.diag(a,k=1))
print(np.diag(a,k=-1))
print(np.diag(a))
print(np.diag(np.fliplr(a)))
