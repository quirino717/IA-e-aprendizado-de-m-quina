from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from sklearn import linear_model
import matplotlib.pyplot as plt
import numpy as np

# Exercício dos livros e frequência x notas
print('\n' + '\033[1m-=' * 30)
print('{:^60}'.format("Exercício dos livros e frequência x notas"))
print('\033[1m-=\033[m' * 30 + '\n')

ivros = [0, 1, 0, 2, 4, 4, 1, 4, 3, 0, 2, 1, 4, 1, 0, 1, 3, 0, 1, 4, 4, 0, 2, 3, 1, 0, 3, 3, 2, 2, 3, 2, 2, 3, 4, 4, 3, 1, 2, 0]
frequencia = [9, 15, 10, 16, 10,20,	11,	20,	15,	15,	8,	13,	18,	10,	8,	10,	16,	11,	19,	12,	11,	19,	15,	15,	20,	6,	15,	19,	14,	13,	17,	20,	11,	20,	20,	20,	9,	8,	16,	10]
notas = [45, 57, 45,51,	65,	88,	44,	87,	89,	59,	66,	65,	56,	47,	66,	41,	56,	37,	45,	58,	47,	64,	97,	55,	51,	61,	69,	79,	71,	62,	87,	54,	43,	92,	83,	94,	60,	56,	88,	62]

lf = [[0, 9], [1, 15], [0, 10], [2, 16], [4, 10], [4, 20], [1, 11], [4, 20], [3, 15], [0, 15],
      [2, 8], [1, 13], [4, 18], [1, 10], [0, 8], [1, 10], [3, 16], [0, 11], [1, 19], [4, 12],
      [4, 11], [0, 19], [2, 15], [3, 15], [1, 20], [0, 6], [3, 15], [3, 19], [2, 14], [2, 13],
      [3, 17], [2, 20], [2, 11], [3, 20], [4, 20], [4, 20], [3, 9], [1, 8], [2, 16], [0, 10]]


regressao = linear_model.LinearRegression()
regressao.fit(lf, notas)
a = regressao.coef_
b = regressao.intercept_

print("Coef Angular:", a, "Coef Linear:", b)

print(f'\nO aluno que leu 2 livros e vei em 11 aulas terá uma nota de: {regressao.predict([[2, 11]])}')
print(f'O aluno que leu 0 livros e vei em 5 aulas terá uma nota de: {regressao.predict([[0, 5]])}')
print(f'O aluno que leu 4 livros e vei em 20 aulas terá uma nota de: {regressao.predict([[4, 20]])}')
print(f'O aluno que leu 2 livros e vei em 10 aulas terá uma nota de: {regressao.predict([[2, 10]])}')
print(f'O aluno que leu 4 livros e vei em 15 aulas terá uma nota de: {regressao.predict([[4, 15]])}\n')

print(f"Precisão: {regressao.score(lf, notas) * 100:.2f}%")

# Exercício da classificação Iris Flower
print('\n' + '\033[1m-=' * 30)
print('{:^60}'.format("Exercício da classificação Iris Flower"))
print('\033[1m-=\033[m' * 30 + '\n')

iris_X, iris_y = load_iris(return_X_y=True) # importa os dados das flores

# iris_X são as informações das flores
print(len(iris_X))
print(iris_X)

print()

# iris_y são as especiés das flores
print(len(iris_y))
print(iris_y)

# comandos para transformar os dados das espécies de iris_y para um array
iris_y_np = np.array(iris_y)
especies = np.empty(iris_y_np.shape, dtype='U10')

# a partir dos valores do array, os valores numéricos são alterados para o nome de cada espécie
especies[iris_y_np == 0] = "setosa"
especies[iris_y_np == 1] = "versicolor"
especies[iris_y_np == 2] = "virginica"

# confirma o tamanho e mostra a lista atualizada
print()
print(len(especies))
print(especies)

# cria a classificação para o KNN com 5 vizinhos
knn = KNeighborsClassifier(n_neighbors = 5)
knn.fit(iris_X, especies)

# faz uma previsão da espécie que pode ser e mostra a probabilidade de pertencer aquele tipo
print(f'\nPara os dados fornecidos, essa flor provavelmente é da espécie: {str(knn.predict([[4.7,3.2,1.3,0.2]]))}')
print(knn.predict_proba([[4.7,3.2,1.3,0.2]]))

print(f'\nPara os dados fornecidos, essa flor provavelmente é da espécie: {str(knn.predict([[6.4,3.2,4.5,1.5]]))}')
print(knn.predict_proba([[6.4,3.2,4.5,1.5]]))

print(f'\nPara os dados fornecidos, essa flor provavelmente é da espécie: {str(knn.predict([[7.3,2.9,6.3,1.8]]))}')
print(knn.predict_proba([[7.3,2.9,6.3,1.8]]))

# mostra a precisão do KNN
print(f"Precisão: {knn.score(iris_X, especies) * 100:.2f}%")

# mostra em azul a distribuição da espécie setosa em azul
for i in range(50):
    plt.scatter(iris_X[i][0], iris_X[i][1], iris_X[i][2], color="blue")

# mostra em azul a distribuição da espécie versicolor em vermelho
for i in range(50,100):
    plt.scatter(iris_X[i][0], iris_X[i][1], iris_X[i][2], color="red")

# mostra em azul a distribuição da espécie virginica em verde
for i in range(100,150):
    plt.scatter(iris_X[i][0], iris_X[i][1], iris_X[i][2], color="green")

plt.show()
