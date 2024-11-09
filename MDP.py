# importa todas as bibil
import numpy as np
import matplotlib.pyplot as plt
from GridWorld import GridWorld
from ValueIteration import ValueIteration


# o elemento principal para o funcionamento do MDP é a classe ValueIteration
# é ela que realizará o cálculo da política e o treinamento
class ValueIteration:
    # a primeira coisa a se fazer é inicializar os parâmetros que serão usados na funçõe da classe
    def __init__(self, reward_function, transition_model, gamma):
        self.num_states = transition_model.shape[0]  # parâmetro que determina o número de estados
        self.num_actions = transition_model.shape[1]  # parâmetro que determina o número de ações

        # o MDP funciona por meio de recompensas para decidir qual o melhor estado,
        # esse é o parâmetro que determina a recompensa de cada estado
        self.reward_function = np.nan_to_num(reward_function)

        # para realizar a mudança de um estado para o outro, precisa ser determinada a possibilidade dessa mudança
        # é isso que esse parâmetro faz
        self.transition_model = transition_model

        self.gamma = gamma  # o gama é o que define as recompensas futuras dos estados

        self.values = np.zeros(self.num_states)  # é aqui que serão guardados os valores de cada estado

        self.policy = None  # onde será guardado a política

    # o cálculo da política será realizado por meio da função abaixo
    # a forma que o cálculo é feito é realizando uma atualização dos valores com uma única iteração
    def one_iteration(self):
        delta = 0  # delta é a váriavel que será usada para medir a mudança de estados durante a iteração

        # o for abaixo realiza a iteração
        for s in range(self.num_states):
            temp = self.values[s]  # temp é uma variável temporária para guardar o valor do estado atual
            v_list = np.zeros(self.num_actions)

            # esse for realiza a interação para as ações a serem tomadas
            for a in range(self.num_actions):
                p = self.transition_model[s, a]  # p é a probabilidade de mudar pra cada estado
                # na lista é guardado o valor de cada estado para cada ação
                v_list[a] = self.reward_function[s] + self.gamma * np.sum(p * self.values)

            self.values[s] = max(v_list)  # nessa lista entram os melhores valores dos estados
            delta = max(delta, abs(temp - self.values[s]))  # então é feito a verificação de convergência
        return delta

    # após os valores serem determinados a função abaixo encontra a melhor política
    # isso é feito com base nas melhores ações de cada estado encontrados pela função anterior
    def get_policy(self):
        pi = np.ones(self.num_states) * -1  # é aqui que serão guardadas as políticas, e por não ter nenhuma ela começa em -1

        # esse for realiza acha o valor de cada ação de um estado
        for s in range(self.num_states):
            v_list = np.zeros(self.num_actions)  # os valores são guardados nessa lista

            # é nesse for que o cálculo de cada ação é realizado
            for a in range(self.num_actions):
                p = self.transition_model[s, a]
                v_list[a] = self.reward_function[s] + self.gamma * np.sum(p * self.values)

            max_index = []  # no max_index entram as ações que que apresentaram os maiores valores
            max_val = np.max(v_list)  # o maior valor encontrado do estado é guardado nessa lista

            # esse for verifica se o valor que se espera da ação equivale ao maior valor encontrado
            # se sim, guarda na lista com a ações dos maiores valores
            for a in range(self.num_actions):
                if v_list[a] == max_val:
                    max_index.append(a)

            pi[s] = np.random.choice(max_index)  # escolhe a melhor ação de forma aleatória
        return pi.astype(int)

    # a função de treino testa os valores, até que eles cheguem na melhor política
    def train(self, tol=1e-3):
        epoch = 0  # variável das épocas do treino
        delta = self.one_iteration()  # faz a medida dos valores, por meio da função de atualização pra uma iteração, e receobe o melhor
        delta_history = [delta]  # e então é guardado na lista com os outros deltas

        # o while abaixo vai procurando um delta que seja menor que a tolerância (1e-3) por meio do método de atualização pra uma iteração
        while delta > tol:
            epoch += 1
            delta = self.one_iteration()
            delta_history.append(delta)
            if delta < tol:
                break

        # após isso, guarda a melhor política
        self.policy = self.get_policy()

        print(f'# iterations of policy improvement: {len(delta_history)}')  # mostra quantas iterações foram feitas
        print(f'delta = {delta_history}')  # mostra a lista  dos melhores valores

        # essa seção exibe um gráfico que mostra a convergência dos valores
        fig, ax = plt.subplots(1, 1, figsize=(3, 2), dpi=200)
        ax.plot(np.arange(len(delta_history)) + 1, delta_history, marker='o', markersize=4,
                alpha=0.7, color='#2ca02c', label=r'$\gamma= $' + f'{self.gamma}')
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Delta')
        ax.legend()
        plt.tight_layout()
        plt.show()


problem = GridWorld('world00.csv', reward={0: -0.04, 1: 1.0, 2: -1.0, 3: np.nan}, random_rate=0.2)

solver = ValueIteration(problem.reward_function, problem.transition_model, gamma=0.9)
solver.train()

problem.visualize_value_policy(policy=solver.policy, values=solver.values)
problem.random_start_policy(policy=solver.policy, start_pos=(2, 0), n=1000)
