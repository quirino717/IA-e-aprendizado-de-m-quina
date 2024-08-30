# fiz esse A* com base num video do YouTube, pois tava com muita dificuldade
# pro programa começar a rodar, tem que usar o mouse pra desenhar o mapa
# o primeiro clique define o ínicio, o segundo o goal, e se apertar de novo desenha os obstaculos
# o botão esquerdo é pra apagar os pontos desenhados
# pra ele achar o caminho é só apertar o espaço depois que terminar de desenhar

import pygame
from math import sqrt
from queue import PriorityQueue

width = 650
janela = pygame.display.set_mode((width, width))

vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)
branco = (255, 255, 255)
preto = (0, 0, 0)
roxo = (255, 0, 255)
laranja = (255, 165, 0)
cinza = (128, 128, 128)


class Quadrado:
    def __init__(self, fileira, coluna, largura, total_fil):
        self.fileira = fileira
        self.coluna = coluna
        self.x = fileira * largura
        self.y = coluna * largura
        self.cor = branco
        self.vizinhos = []
        self.largura = largura
        self.total_fil = total_fil

    def posicao(self):
        return self.fileira, self.coluna

    def checa_closed(self):
        return self.cor == vermelho

    def checa_open(self):
        return self.cor == verde

    def checa_obstaculo(self):
        return self.cor == preto

    def checa_inicio(self):
        return self.cor == laranja

    def checa_fim(self):
        return self.cor == azul

    def reset(self):
        self.cor = branco

    def faz_closed(self):
        self.cor = vermelho

    def faz_open(self):
        self.cor = verde

    def faz_obstaculo(self):
        self.cor = preto

    def faz_comeco(self):
        self.cor = laranja

    def faz_fim(self):
        self.cor = azul

    def faz_caminho(self):
        self.cor = roxo

    def desenhar(self, janela):
        pygame.draw.rect(janela, self.cor, (self.x, self.y, self.largura, self.largura))

    def atualiza_vizinho(self, grid):
        self.vizinhos = []

        if self.fileira < self.total_fil - 1 and not grid[self.fileira + 1][self.coluna].checa_obstaculo(): # checa se da pra ir pra baixo
            self.vizinhos.append(grid[self.fileira + 1][self.coluna])

        if self.fileira > 0 and not grid[self.fileira - 1][self.coluna].checa_obstaculo(): # checa se da pra ir pra cima
            self.vizinhos.append(grid[self.fileira - 1][self.coluna])

        if self.coluna < self.total_fil - 1 and not grid[self.fileira][self.coluna + 1].checa_obstaculo(): # checa se da pra ir pra direita
            self.vizinhos.append(grid[self.fileira][self.coluna + 1])

        if self.coluna > 0 and not grid[self.fileira][self.coluna - 1].checa_obstaculo(): # checa se da pra ir pra esquerda
            self.vizinhos.append(grid[self.fileira][self.coluna - 1])

    def __lt__(self, other): # lt significa less than, vai comparar os lugares
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def refaz_caminho(de_onde_veio, atual, desenhar):
    while atual in de_onde_veio:
        atual = de_onde_veio[atual]
        atual.faz_caminho()
        desenhar()


def algorithm(desenhar, grid, start, goal):
    cont = 0
    open_set = PriorityQueue() # pega o menor elemento
    open_set.put((0, cont, start))
    de_onde_veio = {} # guarda de onde cada nó tá vindo

    g_score = {quadrado: float('inf') for fileira in grid for quadrado in fileira} # guarda o menor caminho ATUAL
    g_score[start] = 0
    f_score = {quadrado: float('inf') for fileira in grid for quadrado in fileira} # guarda a previsão de distância até o goal
    f_score[start] = h(start.posicao(), goal.posicao())

    open_set_hash = {start} # pra ajudar a ver se tá no open_set

    while not open_set.empty():
        for event in pygame.event.get(): # checa pra ver se não tá saindo do jogo
            if event.type == pygame.QUIT:
                pygame.quit()

        atual = open_set.get()[2] # o atual é o nó do menor elemento
        open_set_hash.remove(atual) # tira ele do open_set

        if atual == goal: # se tá no final, tá no final
            refaz_caminho(de_onde_veio, goal, desenhar)
            goal.faz_fim()
            start.faz_comeco()
            return True

        for vizinho in atual.vizinhos: # se não tá no final, checa os vizinhos do nó atual
            temp_g_score = g_score[atual] + 1 # calcula o menor caminho deles

            if temp_g_score < g_score[vizinho]: # se achou um caminho melhor, atualiza
                de_onde_veio[vizinho] = atual
                g_score[vizinho] = temp_g_score
                f_score[vizinho] = temp_g_score + h(vizinho.posicao(), goal.posicao())

                if vizinho not in open_set_hash: # então coloca no open_set_hash
                    cont += 1
                    open_set.put((f_score[vizinho], cont, vizinho))
                    open_set_hash.add(vizinho)
                    vizinho.faz_open()

        desenhar()

        if atual != start:
            atual.faz_closed()

    return False


def faz_grid(fileiras, largura):
    grid = []
    espaco = largura // fileiras

    for i in range(fileiras): # representa fileira
        grid.append([])
        for j in range(fileiras): # representa coluna
            quadrado = Quadrado(i, j, espaco, fileiras) # x, y, tamanho e colunas
            grid[i].append(quadrado)

    return grid


def desenha_grid(janela, fileiras, largura):
    espaco = largura // fileiras

    for i in range(fileiras):
        pygame.draw.line(janela, cinza, (0, i * espaco), (largura, i * espaco))
        for j in range(fileiras):
            pygame.draw.line(janela, cinza, (j * espaco, 0), (j * espaco, largura))


def desenhar(janela, grid, fileiras, largura):
    janela.fill(branco)

    for fileira in grid:
        for quadrado in fileira:
            quadrado.desenhar(janela)

    desenha_grid(janela, fileiras, largura)
    pygame.display.update()


def pega_posicao_mouse(pos, fileiras, largura):
    espaco = largura // fileiras
    x, y = pos

    fileira = y // espaco
    coluna = x // espaco

    return fileira, coluna


def main(janela, largura):
    FILEI = 25
    grid = faz_grid(FILEI, largura)

    start = None
    goal = None

    run = True
    while run:
        desenhar(janela, grid, FILEI, largura)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # 0 é o botão esquerdo
                pos = pygame.mouse.get_pos()
                coluna, fileira = pega_posicao_mouse(pos, FILEI, largura)
                quadrado = grid[fileira][coluna]

                if not start and quadrado != goal: # se não tem começo já pega o próximo clique
                    start = quadrado
                    start.faz_comeco()

                elif not goal and quadrado != start: # se não tem fim já pega o próximo clique
                    goal = quadrado
                    goal.faz_fim()

                elif quadrado != goal and quadrado != start: # faz os obstaculos
                    quadrado.faz_obstaculo()

            elif pygame.mouse.get_pressed()[2]: # 2 é o botão direito (1 deve ser o scroll)
                pos = pygame.mouse.get_pos()
                coluna, fileira = pega_posicao_mouse(pos, FILEI, largura)
                quadrado = grid[fileira][coluna]
                quadrado.reset()

                if quadrado == start:
                    start = None
                elif quadrado == goal:
                    goal = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and goal:
                    for fileira in grid:
                        for quadrado in fileira:
                            quadrado.atualiza_vizinho(grid)

                    algorithm(lambda: desenhar(janela, grid, FILEI, largura), grid, start, goal) # Lambda é uma função anônima

    pygame.quit()


main(janela, width)
