from sklearn.model_selection import train_test_split

X = [[1], [2], [3], [4], [5], [6], [7], [8]]  # inputs
y = [2, 4, 6, 8, 10, 12, 14, 16]               # y = 2x

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

print("train:", X_train)  # model learns from these
print("test:", X_test)    # model NEVER sees these during training