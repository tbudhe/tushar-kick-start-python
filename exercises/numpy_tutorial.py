import numpy as np

# 1. Create a 5x5 matrix with random integers from 1 to 100
# 2. Calculate the mean of the matrix
# 3. Calculate the standard deviation of the matrix


def ff1():
    matrix = np.random.randint(1, 101, size=(5, 5))
    mean = np.mean(matrix)
    standardDeviation = np.std(matrix)
    print(mean)
    print(standardDeviation)

# ff1()


def ff2():
    matrix = np.eye(5)
    matrix_add_five = matrix + 5
    matrix_multiply_five = matrix_add_five * 5
    print(matrix_multiply_five)
    # Create a 5x1 column vector with random integers between 1 and 10
    column_vector = np.random.randint(1, 11, size=(5, 1))
    print(column_vector)
    # Multiply the resulting matrix with the column vector
    product_column = matrix_multiply_five @ column_vector
    print(product_column)

# ff2()


def ff3():
    # Create two 3x3 matrices with random integers between 1 and 100
    matrix1 = np.random.randint(1, 101, size=(3, 3))
    matrix2 = np.random.randint(1, 101, size=(3, 3))

    # Compute element-wise multiplication
    element_wise_product = matrix1 * matrix2

    print("Matrix 1:")
    print(matrix1)
    print("\nMatrix 2:")
    print(matrix2)
    print("\nElement-wise multiplication result:")
    print(element_wise_product)


ff3()


def ff4():
    # Create a 1000-element array of random integers between 1 and 1000
    array = np.random.randint(1, 1001, size=1000)
    
    # Calculate the cumulative sum of the array
    cumulative_sum = np.cumsum(array)
    
    # Print the 10th, 100th, and 500th elements of the cumulative sum array
    print("Original array (first 10 elements):", array[:10])
    print("Cumulative sum array (first 10 elements):", cumulative_sum[:10])
    print(f"\n10th element of cumulative sum: {cumulative_sum[9]}")    # Index 9 for 10th element
    print(f"100th element of cumulative sum: {cumulative_sum[99]}")    # Index 99 for 100th element
    print(f"500th element of cumulative sum: {cumulative_sum[499]}")   # Index 499 for 500th element
    
    print(f"\nTotal sum of array: {cumulative_sum[-1]}")  # Last element equals total sum

ff4()