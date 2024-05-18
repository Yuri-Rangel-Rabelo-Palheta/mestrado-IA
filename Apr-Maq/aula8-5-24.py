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

# Importando bibliotecas necessárias
import numpy as np  # Biblioteca para cálculos numéricos
import matplotlib.pyplot as plt  # Biblioteca para visualização de dados

# Definindo os parâmetros da equação da reta (y = ax + b)
a = -1.2
b = 0.8

# Criando a função lambda f(x) = ax + b
f = lambda x: a*x + b

# Testando a função com x = 1
f(1)

# Criando um array de valores de x variando de -1 a 4 com passo de 0.1
x = np.arange(-1, 4, 0.1)

# Calculando os valores de y correspondentes à função f(x)
y = f(x)

# Gerando ruído aleatório com distribuição normal para adicionar aos valores de y
np.random.seed(42)
e = np.random.normal(0, 0.3, len(y))

# Adicionando o ruído aos valores de y para simular dados reais (y + erro)
ym = y + e

# Plotando o gráfico da função original e dos dados com ruído
plt.plot(x, y)  # Função original
plt.plot(x, ym, '*r')  # Dados com ruído
plt.grid()  # Adicionando grade ao gráfico
plt.show()  # Mostrando o gráfico

# Algoritmo de Mínimos Quadrados para encontrar os parâmetros da reta (a e b)
# Criando a matriz A com os valores de x e uma coluna de 1s
A = np.zeros((N, 2))
A[:, 0] = x
A[:, 1] = 1

# Calculando theta (coeficientes a e b) utilizando a fórmula dos Mínimos Quadrados
theta = np.linalg.inv(A.T @ A) @ A.T @ ym

# Obtendo os valores de a e b ajustados (am e bm)
am = theta[0]
bm = theta[1]

# Criando a função lambda com os valores ajustados de a e b
fm = lambda x: am*x + bm

# Calculando os valores de y previstos com a função ajustada
yp = fm(x)

# Plotando o gráfico da função original e dos dados ajustados
plt.plot(x, y)  # Função original
plt.plot(x, yp, '*r')  # Dados ajustados
plt.grid()  # Adicionando grade ao gráfico
plt.show()  # Mostrando o gráfico

# Calculando o erro entre os valores reais e os valores previstos
e = ym - yp

# Plotando o gráfico do erro
plt.plot(e, '*b')  # Pontos azuis representando o erro
plt.grid()  # Adicionando grade ao gráfico
plt.show()  # Mostrando o gráfico

# Utilizando a biblioteca scikit-learn para realizar regressão linear
from sklearn.linear_model import LinearRegression

# Criando um objeto Reg que representa o modelo de regressão linear
Reg = LinearRegression()

# Ajustando o modelo aos dados (x, ym)
Reg.fit(x.reshape(-1, 1), ym.reshape(-1, 1))

# Obtendo os coeficientes (a) e o intercepto (b) do modelo
print(Reg.coef_)  # Coeficiente 'a'
print(Reg.intercept_)  # Intercepto 'b'

# Prevendo os valores de y utilizando o modelo ajustado
ysk = Reg.predict(x.reshape(-1, 1))

# Imprimindo os valores previstos tanto com o método manual quanto com o método do scikit-learn
print(yp)  # Valores previstos manualmente
print(ysk)  # Valores previstos com scikit-learn
