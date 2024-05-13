#/* aula 08/05/24 */
# yuri rangel rabelo palheta
#problema da regressão, sobre duas perspectiva:
#1 computacional
#2 matemática

#Linear mono variável

#Linear multi variável

#Polinomial não linear

#Problema da regressao: Um conjunto de dados,
#leituras numericas de causa de um fenomeno chamada X,
#consequencia Y
#os dados podem guardar relações intrinsecas e podem ser
#capturados por uma função matemática

# y = f(x) + erro

## Regressão linear

#$$y = ax +b $$

import numpy as np
import matplotlib.pyplot as plt

a = -1.2
b = 0.8

f = lambda x: a*x + b

f(1)

x =np.arange(-1,4,0.1)

y = f(x)

#len(y)
np.random.seed(42)
e = np.random.normal(0,0.3,len(y))

ym = y + e

plt.plot(x,y)
plt.plot(x,ym,'*r')
plt.grid()
plt.show()


#Algorítmo Mínimos Quadrados

#theta = (At A)^-1 At y

N = len(y)

print('N:',N)

#Atheta = y

A = np.zeros((N,2))

A[:,0] = x

A[:,1] = 1

theta = np.linalg.inv(A.T@A)@ A.T @ ym

print(theta)

am = theta[0]

bm = theta[1]

fm = lambda x: am*x + bm

y = f(x)

yp = fm(x)


plt.plot(x,y)
plt.plot(x,yp,'*r')
plt.grid()
plt.show()

e=ym -yp

plt.plot(e, '*b')
plt.grid()
plt.show()

from sklearn.linear_model import LinearRegression

Reg = LinearRegression()

Reg.fit(x.reshape(-1,1),ym.reshape(-1,1))

print(Reg.coef_)

print(Reg.intercept_)

ysk = Reg.predict(x.reshape(-1,1))

print(yp)
print(ysk)