from random import randint, uniform, seed
from time import sleep, time

# ===========================
#         DEFINIÇÕES
# ===========================

alfa = 0.2  # taxa de aprendizado = 20%
gamma = 0.9  # fator de desconto = 90%
epsilon = 0.2  # porcentagem de exploração = 20%

# quantidade de estados, ações e experimentos
A = 4  # 4 ações (cima, baixo, esquerda, direita)
COL = 5  # 3 colunas livres e 2 paredes
LIN = 5  # 3 linhas livre e duas paredes
S = COL*LIN  # define quantide de estados S
EPISODIOS = 50  # define quantidade de episódios

# define a representação no mapa/mundo
LIVRE = 0
OBSTACULO = 1
SAIDA = 2

# inicializa a matriz Q (valor estado-ação) com números aleatórios
Q = [[0.0 for _ in range(A)] for _ in range(S)]

# posicao na grade (x, y)
x = y = 0

# auxiliar de recompensa
rew = 0

# Mundo de grades:
# livre = 0
# obstaculo = 1
# saida = 2
mapa = [[1, 1, 1, 2, 1], [1, 0, 0, 0, 1], [1, 0, 1, 1, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]]


# =========================
#         FUNÇÕES
# =========================

# inicializa função Q com números aleatorios entre 0 e 1
def initq(Q):
    s = a = 0
    for s in range(len(Q)):
        for a in range(len(Q[s])):
            Q[s][a] = uniform(0, 1)  # números aleatórios entre 0 e 1


# inicio aleatório do agente no mapa/mundo
def inicioaleatorio():
    global x, y

    # while para testar se o agente não está começando na saída ou no obstáculo
    while True:
        x = randint(0, 32767) % LIN
        y = randint(0, 32767) % COL

        if mapa[y][x] != OBSTACULO and mapa[y][x] != SAIDA:
            break


# a partir de x e y cria o estado s
def estado(x, y):
    s = c = 0
    for i in range(LIN):
        for j in range(COL):
            if x == i and y == j:
                s = c
            c += 1
    return s


# seleciona uma acao: estratégia e-greedy
# dados Q e s
def selecionaacao(Q, s):
    a_qmax = 0

    # encontra a ação com Q maximo, dado o estado s
    for i in range(1, A):
        if Q[s][i] > Q[s][a_qmax]:
            a_qmax = i
    acao = a_qmax

    # e-greedy: escolhe a ação com Q maximo ou escolhe ação aleatória
    e = uniform(0, 1)  # gera número aleatório
    if e < epsilon:
        acao = randint(0, 32767) % A  # gera ação aleatória

    return acao


# obtém o próximo estado e verifica se há colisões
# utiliza rew para armazenar colisão
def proximoestado(a):
    global rew, x, y
    rew = 0

    # ações: a = {0, 1, 2, 3}
    # {para baixo, para direita, para cima, para esquerda}

    # para baixo
    if a == 0:
        if mapa[y + 1][x] != 1:
            y += 1
        else:
            rew = 1

    # para direita
    elif a == 1:
        if mapa[y][x + 1] != 1:
            x += 1
        else:
            rew = 1

    # para cima
    elif a == 2:
        if mapa[y - 1][x] != 1:
            y -= 1
        else:
            rew = 1

    # para esquerda
    elif a == 3:
        if mapa[y][x - 1] != 1:
            x -= 1
        else:
            rew = 1

    return estado(x, y)


# retorna a recompensa
def recompensa():
    # 100 caso encontre o objetivo
    # -5 quando colidir
    # -1 para cada ação que não resultar no objetivo
    if mapa[y][x] == SAIDA:
        return 100
    else:
        if rew == 1:
            return -5
        else:
            return -1


# função para atualizar o valor de Q
def atualizaq(s, a, r, Q, next_s, next_a):
    Q[s][a] = Q[s][a] + alfa * (r + gamma * Q[next_s][next_a] - Q[s][a])


# desenha a política de ações
# simula o mundo
def desenhamapapolitica(espaco, episodio):
    linha = coluna = 0

    print("\n\n\n===== Q-LEARNING =====\n")
    print(f"Episódio: {episodio}\n")

    for linha in range(LIN):
        for coluna in range(COL):
            if mapa[linha][coluna] == LIVRE:
                esp = estado(coluna, linha)

                if espaco[esp] == 0:
                    print('v', end='')  # seta para baixo
                elif espaco[esp] == 1:
                    print('>', end='')  # seta para direita
                elif espaco[esp] == 2:
                    print('^', end='')  # seta para cima
                elif espaco[esp] == 3:
                    print('<', end='')  # seta para esquerda

            elif mapa[linha][coluna] == OBSTACULO:
                print('#', end='')
            elif mapa[linha][coluna] == SAIDA:
                print(' ', end='')
        print()


# ========================
#     CÓDIGO PRINCIPAL
# ========================

at = 0  # ação a ser tomada
s = 0  # estado
s_proximo = a_proximo = 0  # próximo estado e próxima ação
r = 0  # recompensa
episodio = 0  # para contar quantidade de episódios

initq(Q)  # inicializa Q aleatoriamente

# imprime Q inicial - somente para debug
# linhas são estados, colunas são ações
print('Tabela Q inicial')
for s in range(S):
    for a in range(A):
        print(Q[s][a], end='')
    print()

# repete EPISODIOS vezes
for episodio in range(EPISODIOS):
    inicioaleatorio()  # inicia o agente aleatoriamente

    s = estado(x,y)  # pega estado inicial e localiza na grade

    # repete até encontrar o objetivo
    while mapa[y][x] != SAIDA:
        at = selecionaacao(Q, s)  # seleciona uma ação at, dados Q e s

        s_proximo = proximoestado(at)  # com a ação escolhida, obtém o próximo estado s

        r = recompensa()  # recebe a recompensa

        a_proximo = selecionaacao(Q, s_proximo)  # seleciona próxima ação

        atualizaq(s, at, r, Q, s_proximo, a_proximo)  # atualiza a matriz Q

        s = s_proximo  # o estado atual passa a ser igual ao próximo estado

    # desenha a política no terminal a cada x episodios
    x = 5
    politica = [0] * S
    if episodio % x == 0:
        for s in range(0, S):
            a_qmax = 0

            for i in range(1, A):
                if Q[s][i] > Q[s][a_qmax]:
                    a_qmax = i

            politica[s] = a_qmax

        # imprime na tela somente a ação que maximiza Q
        desenhamapapolitica(politica, episodio)
        sleep(1)  # atualiza a cada 1 segundo

# imprime Q final - somente para debug
# linhas são estados, colunas são ações
print('\nTabela Q final')
for s in range(0, S):
    for a in range(0, A):
        print(Q[s][a], end='')
    print()
