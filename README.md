
#### TODO:

1. Standard Deviation
2. Mean of array
3. Identical matrix 
4. GPU vs CPU 


# NumPy and Pandas Documentation

## NumPy

NumPy (Numerical Python) is a powerful library for numerical computing in Python. It provides support for large, multi-dimensional arrays and matrices, along with a collection of mathematical functions to operate on these arrays.

### Key Features:
- Efficient handling of large datasets with multi-dimensional arrays (`ndarray`)
- Mathematical operations such as linear algebra, Fourier transforms, and random number generation
- Broadcasting for element-wise operations
- Integration with other libraries like SciPy and Matplotlib

### Example Usage:
```python
import numpy as np

# Create a 1D array
array = np.array([1, 2, 3, 4, 5])

# Create a 2D array
matrix = np.array([[1, 2], [3, 4]])

# Perform operations
mean = np.mean(array)  # Calculate mean
std_dev = np.std(array)  # Calculate standard deviation

print("Mean:", mean)
print("Standard Deviation:", std_dev)
```

### Common Functions:
- `np.mean()`: Calculate the mean of an array
- `np.std()`: Calculate the standard deviation
- `np.sum()`: Sum of array elements
- `np.random.randint()`: Generate random integers
- `np.dot()`: Perform matrix multiplication

---

## Pandas

Pandas is a library for data manipulation and analysis. It provides data structures like `DataFrame` and `Series` for handling structured data.

### Key Features:
- DataFrame: 2D labeled data structure (like a table)
- Series: 1D labeled array
- Handling missing data
- Grouping, merging, and reshaping data
- Integration with NumPy for numerical operations

### Example Usage:
```python
import pandas as pd

# Create a DataFrame
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'Department': ['HR', 'IT', 'Finance']
}
df = pd.DataFrame(data)

# Access data
print(df.head())  # Display first few rows

# Filter data
filtered_df = df[df['Age'] > 28]
print(filtered_df)

# Add a new column
df['Salary'] = [50000, 60000, 70000]
print(df)
```

### Common Functions:
- `df.head()`: Display the first few rows of a DataFrame
- `df.describe()`: Summary statistics of numerical columns
- `df.sort_values()`: Sort DataFrame by a column
- `df.merge()`: Merge two DataFrames
- `df.groupby()`: Group data and perform aggregate operations

---

### When to Use NumPy vs Pandas
- **NumPy**: For numerical computations and working with raw arrays/matrices
- **Pandas**: For structured data analysis and manipulation (e.g., tabular data)

Both libraries are essential for data science and machine learning workflows.
