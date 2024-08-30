from random import randrange
from pyeasyga import pyeasyga
import matplotlib.pyplot as plt

# setup data
data = [{'name': 'green', 'value': 4, 'weight': 12},
        {'name': 'gray', 'value': 2, 'weight': 1},
        {'name': 'yellow', 'value': 10, 'weight': 4},
        {'name': 'orange', 'value': 1, 'weight': 1},
        {'name': 'blue', 'value': 2, 'weight': 2}]

tamanho_populacao = 14

ga = pyeasyga.GeneticAlgorithm(data, population_size=tamanho_populacao,
                               generations=2000,
                               crossover_probability=0.8,
                               mutation_probability=0.1,
                               elitism = True,
                               maximise_fitness=True
                               )

cont = 0
aptidoes_por_geracao = []
melhor_por_geracao = []


# define a fitness function
def aptidao(individual, data):
    global cont
    cont += 1
    #print("individual", individual)
    values, weights = 0, 0

    for gene, box in zip(individual, data):
        print(gene, box)
        values += box['value'] * gene
        weights += box['weight'] * gene
    if weights > 15:
        values = 0
    #print(values)
    #print()
    aptidoes_por_geracao.append(values)
    if(cont >= tamanho_populacao):
        print(aptidoes_por_geracao)
        melhor_por_geracao.append(max(aptidoes_por_geracao))
        aptidoes_por_geracao.clear()
        cont = 0
    return values


def mutar(individual):
    """Reverse the bit of a random index in an individual."""
    mutate_index = randrange(len(individual))
    if mutate_index == 0:
        individual[mutate_index] = randrange(0, 1)
    if mutate_index == 1:
        individual[mutate_index] = randrange(0, 15)
    if mutate_index == 2:
        individual[mutate_index] = randrange(0, 3)
    if mutate_index == 3:
        individual[mutate_index] = randrange(0, 15)
    if mutate_index == 4:
        individual[mutate_index] = randrange(0, 7)

ga.fitness_function = aptidao
ga.mutate_function = mutar

ga.run()
print(ga.best_individual())
plt.plot(melhor_por_geracao)
plt.savefig('graph.jpg')
