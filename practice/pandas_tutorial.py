import pandas as pd


def ff1():
    data = {
        'Title': ['Inception', 'Dunkirk', 'Interstellar', 'The Prestige', 'Memento'],
        'Director': ['Christopher Nolan', 'Christopher Nolan', 'Christopher Nolan', 'Christopher Nolan', 'Christopher Nolan'],
        'Rating': [8.8, 7.9, 8.6, 8.5, 8.4]
    }
    df = pd.DataFrame(data)
    average_rating = df[df.Director == 'Christopher Nolan']['Rating'].mean()
    print("Average rating of Christopher Nolan movies:", average_rating)


# ff1()


def ff2():
    data = {
        'Product': ['Laptop', 'Desktop', 'Tablet', 'Phone', 'Smartwatch'],
        'Price': [25000, 12000, 8000, 22000, 5000]
    }
    df = pd.DataFrame(data)
    expensive_product = df[df.Price > 20000]
    print("Products with price greater than 20000:", expensive_product)
# ff2()


def ff3():
    data = {
        'Store': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B'],
        'Item': ['Apple', 'Banana', 'Orange', 'Grape', 'Apple', 'Banana', 'Orange', 'Grape'],
        'Price': [50, 20, 30, 60, 55, 22, 33, 65],
        'Quantity': [10, 12, 15, 16, 20, 25, 30, 35]
    }
    df = pd.DataFrame(data)
    result = df.groupby('Store').agg({'Price': 'mean', 'Quantity': 'sum'})
    print(result)

# ff3()


def ff4():
    data = {

        'Customer': ['Alice', 'Bob', 'Alice', 'Alice', 'Bob', 'Bob', 'Alice', 'Bob'],

        'Item': ['Pen', 'Pencil', 'Notebook', 'Eraser', 'Pen', 'Pencil', 'Notebook', 'Eraser'],

        'Price': [10, 5, 50, 20, 10, 5, 50, 20],

        'Quantity': [3, 4, 2, 5, 10, 6, 1, 2]

    }
    df = pd.DataFrame(data)
    df['Total'] = df['Price'] * df['Quantity']
    total_spent = df.groupby('Customer')['Total'].sum()
    print(total_spent)
ff4()