#aula 15-05-24
#yuri rangel rabelo palheta
#problema de regressão e classificação

#classificador linear: perception
#y=wx+b = w1x1+w2x2+b

#codigo de classificação de pinguins

#classificação de pinguins

from palmerpenguins import load_penguins
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Perceptron

penguins = load_penguins().dropna()


ys = penguins["species"].to_numpy()

#print(ys[0:5])

ys[ys == "Adelie"] = 0
ys[ys == "Chinstrap"] = 2
ys[ys == "Gentoo"] = 1

#print(ys)

x1 = penguins["bill_length_mm"].to_numpy()

#print(x1)

x2 = penguins["bill_depth_mm"].to_numpy()

#print(x2)

x3 = penguins["flipper_length_mm"].to_numpy()

x4 = penguins["body_mass_g"].to_numpy()

plt.figure(figsize=(6, 6))
plt.scatter(x1, x2, c=ys)

#plt.show()

#indices = np.where(data == 1)[0]
#ultimo_indice = indices.max()

###############
#np.unique(ys)
#tamanhox1 = np.size(np.unique(x1))
#tamanhox2 = np.size(np.unique(x2))
#tamanhox3 = np.size(np.unique(x3))
#tamanhox4 = np.size(np.unique(x4))
#tamanhox1, tamanhox2, tamanhox3, tamanhox4

y = ys[0:265]
x1 = x1[0:265]
x2 = x2[0:265]
x3 = x3[0:265]
x4 = x4[0:265]

plt.figure(figsize=(6, 6))
plt.scatter(x1, x3, c=y)
plt.xlabel("bill_length_mm")
plt.ylabel("flipper_length_mm")

#plt.show()

N = len(y)

#print(N)

X = np.zeros((N, 2))

#print(X)

X[:,0] = x1

X[:,1] = x2

#print(X)
y=y.astype(int)
#separar os dados de treinamento e de teste

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)


print('amostras de treinamento:', len(y_train))
print('amostras de teste:', len(y_test))

#algoritmo de classificação
algoritmo = Perceptron()

algoritmo.fit(X_train, y_train)


yp = algoritmo.predict(X_test)

##Metrica - acuracia

from sklearn.metrics import accuracy_score

print("acuracia score",accuracy_score(y_test, yp))

Ac = np.sum(1*(yp == y_test))/len(y_test)

print("acuracia formula",Ac)

#########################
#########################
#codigo de classificação não linear
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


ax.scatter(Z[:,0] , Z[:,1] , Z[:,2],c=y )
ax.set_xlabel('Z1')
ax.set_ylabel('Z2')
ax.set_zlabel('Z3')
ax.set_title('Gráfico Tridimensional')
ax.view_init(0, 45, 0)
plt.show()


