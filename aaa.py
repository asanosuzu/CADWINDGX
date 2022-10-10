from numpy import *
from math import *
from matplotlib import pyplot as plt
x = [0.0, 1.0, 3.0]
y = [0.0, 1.0, 3.0]
k2 = (y[1]-y[0])/(x[1]-x[0])
k1 = (y[2]-y[1])/(x[2]-x[1])
theta1 = arctan(k1)
theta2 = arctan(k2)
theta = (theta1+theta2)/2+pi/2


z = [1, cos(theta)*1+1]
w = [1, sin(theta)*1+1]
print(theta1)
print(theta2)
print(theta)
print(cos(theta*pi/180)*1+1+sin(theta*pi/180)*1+1)
print(sin(theta*pi/180)*1+1)
plt.plot(x,y)
plt.plot(z,w)
plt.axis("equal")
plt.show()







# plt.plot(X1, R1, '*-')
# plt.grid(True)
# plt.legend()
# plt.axis("equal")
# plt.show()