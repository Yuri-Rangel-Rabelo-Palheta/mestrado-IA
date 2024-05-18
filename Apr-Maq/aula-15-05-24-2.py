#aula 15-05-24-2
#yuri rangel rabelo palheta
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_circles
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score
from mpl_toolkits import mplot3d

X, y = make_circles(n_samples=1000, factor=0.2, noise=0.15, random_state=0)

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

plt.scatter(X[:, 0], X[:, 1], c=y)
plt.show()

algoritmo = Perceptron()
algoritmo.fit(X_train, y_train)

yp = algoritmo.predict(X_test)

print("acuracia score",accuracy_score(y_test, yp))

Z = np.zeros((len(y),3))

##criar uma 3ª feature
Z[:,0] = X[:,0]
Z[:,1] = X[:,1]
Z[:,2] = X[:,0]**2 + X[:,1]**2

Z_train, Z_test, y_train, y_test = train_test_split(Z, y, stratify=y, random_state=42)

algoritmoZ = Perceptron()
algoritmoZ.fit(Z_train, y_train)

ypZ = algoritmoZ.predict(Z_test)

print("acuracia score com mais uma feature",accuracy_score(y_test, ypZ))

fig = plt.figure(figsize = (9,9))
ax = plt.axes(projection='3d')


ax.scatter(Z[:,0] , Z[:,1] , Z[:,2], c=y )
ax.set_xlabel('Z1')
ax.set_ylabel('Z2')
ax.set_zlabel('Z3')
ax.set_title('Gráfico Tridimensional')
ax.view_init(0, 45, 0)
plt.show()


