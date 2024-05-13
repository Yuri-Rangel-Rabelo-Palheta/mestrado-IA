import random

class WumpusMundo:
    def __init__(self, tamanho=4):
        self.tamanho = tamanho
        self.posicao_wumpus = self._gerar_posicao_aleatoria()
        self.posicao_ouro = self._gerar_posicao_aleatoria()
        self.posicao_buracos = [self._gerar_posicao_aleatoria() for _ in range(tamanho)]
        self.posicao_jogador = (0, 0)
        self.fim_jogo = False
        self.pontuacao = 0

    def _gerar_posicao_aleatoria(self):
        return (random.randint(0, self.tamanho - 1), random.randint(0, self.tamanho - 1))

    def _checar_adjacentes(self, posicao):
        adjacentes = []
        x, y = posicao
        if x > 0:
            adjacentes.append((x - 1, y))
        if x < self.tamanho - 1:
            adjacentes.append((x + 1, y))
        if y > 0:
            adjacentes.append((x, y - 1))
        if y < self.tamanho - 1:
            adjacentes.append((x, y + 1))
        return adjacentes

    def _checar_vizinhanca(self, posicao):
        if posicao == self.posicao_wumpus:
            print("Você sente um cheiro horrível!")
        for buraco in self.posicao_buracos:
            if buraco in self._checar_adjacentes(posicao):
                print("Você sente uma brisa suave!")
        if posicao == self.posicao_ouro:
            print("Você vê um brilho radiante!")

    def mover(self, direcao):
        x, y = self.posicao_jogador
        if direcao == "cima" and x > 0:
            self.posicao_jogador = (x - 1, y)
        elif direcao == "baixo" and x < self.tamanho - 1:
            self.posicao_jogador = (x + 1, y)
        elif direcao == "esquerda" and y > 0:
            self.posicao_jogador = (x, y - 1)
        elif direcao == "direita" and y < self.tamanho - 1:
            self.posicao_jogador = (x, y + 1)
        else:
            print("Movimento inválido!")
            return
        self._checar_vizinhanca(self.posicao_jogador)
        if self.posicao_jogador == self.posicao_wumpus or self.posicao_jogador in self.posicao_buracos:
            print("Você morreu!")
            self.fim_jogo = True
        elif self.posicao_jogador == self.posicao_ouro:
            print("Você encontrou o ouro! Parabéns!")
            self.pontuacao += 100
            self.fim_jogo = True

    def mostrar(self):
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if (i, j) == self.posicao_jogador:
                    print("J", end=" ")
                elif (i, j) == self.posicao_wumpus:
                    print("W", end=" ")
                elif (i, j) == self.posicao_ouro:
                    print("O", end=" ")
                elif (i, j) in self.posicao_buracos:
                    print("B", end=" ")
                else:
                    print("-", end=" ")
            print()


jogo = WumpusMundo()
jogo.mostrar()
while not jogo.fim_jogo:
    direcao = input("Digite uma direção (cima, baixo, esquerda, direita): ")
    jogo.mover(direcao)
    jogo.mostrar()