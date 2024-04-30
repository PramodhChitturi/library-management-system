import matplotlib.pyplot as plt

# fig = plt.figure(figsize = (5,4))
# axes = fig.add_axes(rect = [0.2, 0.2, 0.6, 1])
dates = ['12/12/2023','13/12/2023','14/12/2023','15/12/2023','16/12/2023']
x = [1, 2, 3, 4, 5]
y = [10, 11, 2, 12, 13]
plt.plot(x, y)
plt.show()
width = 0.3
fig = plt.figure(figsize = (7, 5))
axes = fig.add_axes(rect = [0.1, 0.1, 0.8, 0.8])
plt.legend()
plt.bar(dates,x, width=width, label = 'Borrows')
plt.bar(dates+width, y,width=width, label = 'Returned')
plt.show()