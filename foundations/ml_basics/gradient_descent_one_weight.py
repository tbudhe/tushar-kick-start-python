# Step 1 (still open)

# Create ml-foundations/gradient_descent_one_weight.py and write:

# data = [(1, 3), (2, 6), (3, 9), (4, 12)]
# w = 0.0 and lr = 0.01
# errors: for each (x, y), the prediction w * x minus y
# loss: the mean of the squared errors
# print(loss)

# My prediction: 67.5. Run it and paste the output, or your code if the number doesn't match.
# Goal: when it works, the final output looks exactly like this.

# epoch  1 | loss  67.5000 | w 0.4500
# epoch 10 | loss   3.6211 | w 2.4094
# epoch 20 | loss   0.1404 | w 2.8837
# epoch 30 | loss   0.0054 | w 2.9771
# epoch 40 | loss   0.0002 | w 2.9955
# epoch 50 | loss   0.0000 | w 2.9991

# Steps:

# Data, a starting weight, and the loss at w = 0
# The gradient, and one update to w
# Wrap it in a 50-epoch loop and print
# Read the output: which number is the model, and which is the report card?
# Break it: flip -= to +=
data = [(1, 3), (2, 6), (3, 9), (4, 12)]
w = 0.0 
lr = 0.01

for epoch in range(1, 51):
    loss_total = 0
    grad_total = 0
    for d in data:
        [x, y] = d
        prediction = w*x
        error = prediction - y
        loss_total += error*error
        grad_total += 2 * error * x
    loss = loss_total/len(data)
    gradient = grad_total/len(data)
    w = w + lr * gradient

    if epoch == 1 or epoch % 10 == 0:
        print(f'epoch {epoch:2d} | loss {loss:8.4f} | w {w:.4f}')
