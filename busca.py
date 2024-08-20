import copy


class Noh:
    def __init__(self, estado, profundidade, h):
        self.estado = estado
        self.level = profundidade
        self.h = h

    def find(self, estado, x):
        for i in range(0, len(self.estado)):
            for j in range(0, len(self.estado)):
                if estado[i][j] == x:
                    return i, j

    def shuffle(self, estado, x1, y1, x2, y2):
        if (x2 >= 0 and x2 < len(self.estado) and y2 >= 0 and y2 < len(self.estado)):
            estado_temp = copy.deepcopy(estado)
            temp = estado_temp[x2][y2]
            estado_temp[x2][y2] = estado_temp[x1][y1]
            estado_temp[x1][y1] = temp
            return estado_temp
        else:
            return None

    def gerar_filhos(self):
        x, y = self.find(self.estado, '0')
        val_list = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        children = []
        for tupla in val_list:
            child = self.shuffle(self.estado, x, y, tupla[0], tupla[1])
            if child is not None:
                child_node = Noh(child, self.level + 1, 0)
                children.append(child_node)
        return children


class Jogo:
    def __init__(self, tamanho):
        self.n = tamanho
        self.open = []
        self.closed = []
        self.start = []
        self.goal = []

    def inicio(self):
        # caso de problema: 6 3 8, 2 1 5, 4 7 0
        self.start = [['6', '3', '8'], ['2', '1', '5'], ['4', '7', '0']]
        self.goal = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '0']]
        # self.exibe(self.start)

    def h(self, estado_atual):
        contador = 0
        for i in range(0, self.n):
            for j in range(0, self.n):
                if estado_atual[i][j] != self.goal[i][j]:
                    contador += 1
        return contador

    def exibe(self, estado):
        print()
        for i in estado:
            for j in i:
                print(j, end=" ")
            print()

    def busca(self):
        noh_inicial = Noh(self.start, 0, 0)
        noh_inicial.h = self.h(noh_inicial.estado)
        self.open.append(noh_inicial)

        while True:
            print("---------------")
            noh_atual = self.open[0]
            self.exibe(noh_atual.estado)
            print('h:', noh_atual.h)
            print('level:', noh_atual.level)

            if noh_atual.h == 0:
                break

            if noh_atual.estado not in self.closed:
                filhos = noh_atual.gerar_filhos()
                for noh in filhos:
                    noh.h = self.h(noh.estado)
                    self.open.append(noh)
                    self.exibe(noh.estado)
                    print('h:', noh.h)
                    print('level:', noh.level)
                    print('-----------------')

            self.closed.append(noh_atual.estado)
            del self.open[0]

            self.open.sort(key=lambda x: x.h, reverse=False)
            input()


def main():
    jogo = Jogo(3)
    jogo.inicio()
    jogo.busca()


main()
