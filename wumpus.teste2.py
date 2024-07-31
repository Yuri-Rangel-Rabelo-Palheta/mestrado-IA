import random
import numpy as np
import matplotlib.pyplot as plt

# Definição da classe do Mundo de Wumpus
class WumpusMundo:
    def __init__(self, tamanho=3, num_buracos=1):
        self.tamanho = tamanho
        self.num_buracos = num_buracos
        self.posicao_jogador = (0, 0)
        self.posicao_wumpus = None
        self.posicao_ouro = None
        self.posicao_buracos = []  # Inicializado como uma lista vazia
        self.fim_jogo = False
        self.pontuacao = 0
        self.flecha_disponivel = True
        self.ouro_pegado = False
        self.wumpus_morto = False
        self.visitados = set()
        self.historico = set()
        self.winner = False
        self.jogo_normal = True
        self.reset()  # Chama reset para definir todas as posições

    def reset(self):
        self.posicao_jogador = (0, 0)
        self.posicao_wumpus = self._gerar_posicao_aleatoria()
        self.posicao_ouro = self._gerar_posicao_aleatoria()
        self.posicao_buracos = [self._gerar_posicao_aleatoria() for _ in range(self.num_buracos)]
        self.fim_jogo = False
        self.pontuacao = 0
        self.flecha_disponivel = True
        self.ouro_pegado = False
        self.wumpus_morto = False
        self.visitados = set()
        self.historico = set()
        self.winner = False
        self.jogo_normal = True

    def _gerar_posicao_aleatoria(self):
        while True:
            posicao = (random.randint(0, self.tamanho - 1), random.randint(0, self.tamanho - 1))
            if posicao != (0, 0) and posicao not in self.posicao_buracos and posicao != self.posicao_wumpus:
                return posicao

    def _checar_adjacentes(self, posicao):
        adjacentes = {}
        x, y = posicao
        if x > 0:
            adjacentes['cima'] = (x - 1, y)
        if x < self.tamanho - 1:
            adjacentes['baixo'] = (x + 1, y)
        if y > 0:
            adjacentes['esquerda'] = (x, y - 1)
        if y < self.tamanho - 1:
            adjacentes['direita'] = (x, y + 1)
        return adjacentes

    def _checar_vizinhanca(self, posicao):
        percepcoes = {"cheiro horrível": False, "brilho radiante": False, "brisa suave": False}
        adjacentes = self._checar_adjacentes(posicao)
        for adj_pos in adjacentes.values():
            if adj_pos == self.posicao_wumpus:
                percepcoes["cheiro horrível"] = True
            if adj_pos == self.posicao_ouro:
                percepcoes["brilho radiante"] = True
            if adj_pos in self.posicao_buracos:
                percepcoes["brisa suave"] = True
        return percepcoes

    def mover(self, direcao):
        if self.fim_jogo:
            return
        
        self.pontuacao -= 1
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
            self.pontuacao -= 50
            return

        self.visitados.add(self.posicao_jogador)
        percepcoes = self._checar_vizinhanca(self.posicao_jogador)
        self._exibir_percepcoes(percepcoes)

        if self.posicao_jogador == self.posicao_wumpus or self.posicao_jogador in self.posicao_buracos:
            self.pontuacao -= 1000
            self.fim_jogo = True
        elif self.posicao_jogador == self.posicao_ouro:
            self.ouro_pegado = True
            self.posicao_ouro = None
            self.pontuacao += 1000

        if self.posicao_jogador == (0, 0) and self.ouro_pegado:
            self.pontuacao += 1000
            self.fim_jogo = True
            self.winner = True

    def _exibir_percepcoes(self, percepcoes):
        percepcao_msg = ""
        if percepcoes["cheiro horrível"]:
            percepcao_msg += "Você sente um cheiro horrível! "
        if percepcoes["brilho radiante"]:
            percepcao_msg += "Você vê um brilho radiante! "
        if percepcoes["brisa suave"]:
            percepcao_msg += "Você sente uma brisa suave! "
        print(percepcao_msg)

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
        print(f"Score: {self.pontuacao}")
        if self.fim_jogo:
            print("Fim de jogo!")
        print()

# Definição da classe da Formiga
class Formiga:
    def __init__(self, mundo):
        self.mundo = mundo
        self.posicao = (0, 0)
        self.caminho = []
        self.pontuacao = 0

    def mover(self, direcao):
        self.mundo.mover(direcao)
        self.caminho.append(direcao)
        self.pontuacao = self.mundo.pontuacao
        return self.mundo.fim_jogo

# Definição da classe do Algoritmo de Formigas (ACO)
class AlgoritmoFormigas:
    def __init__(self, num_formigas, evaporacao, alfa, beta, iteracoes, mundo):
        self.num_formigas = num_formigas
        self.evaporacao = evaporacao
        self.alfa = alfa
        self.beta = beta
        self.iteracoes = iteracoes
        self.mundo = mundo
        self.feromonios = np.ones((mundo.tamanho, mundo.tamanho, 4))  # Feromônios para cada direção em cada posição
        self.melhor_caminho = None
        self.melhor_pontuacao = float('-inf')
        self.pontuacoes_melhores = []  # Para armazenar a melhor pontuação em cada iteração
        self.pontuacoes_medianas = []  # Para armazenar a pontuação média em cada iteração

    def atualizar_feromonios(self):
        self.feromonios *= self.evaporacao

    def escolher_direcao(self, posicao):
        adjacentes = self.mundo._checar_adjacentes(posicao)
        probabilidades = {}
        total = 0
        for i, (direcao, adj) in enumerate(adjacentes.items()):
            x, y = adj
            if direcao == 'cima':
                index = 0
            elif direcao == 'baixo':
                index = 1
            elif direcao == 'esquerda':
                index = 2
            elif direcao == 'direita':
                index = 3
            total += (self.feromonios[x, y, index] ** self.alfa)
        for i, (direcao, adj) in enumerate(adjacentes.items()):
            x, y = adj
            if direcao == 'cima':
                index = 0
            elif direcao == 'baixo':
                index = 1
            elif direcao == 'esquerda':
                index = 2
            elif direcao == 'direita':
                index = 3
            probabilidades[direcao] = (self.feromonios[x, y, index] ** self.alfa) / total
        return probabilidades

    def executar(self):
        for _ in range(self.iteracoes):
            caminhos_formigas = []
            pontuacoes = []

            for _ in range(self.num_formigas):
                formiga = Formiga(self.mundo)
                self.mundo.reset()
                fim_jogo = False
                while not fim_jogo:
                    probabilidades = self.escolher_direcao(formiga.posicao)
                    if probabilidades:
                        direcao = max(probabilidades, key=probabilidades.get)
                        fim_jogo = formiga.mover(direcao)
                        self.mundo.mostrar()
                caminhos_formigas.append(formiga.caminho)
                pontuacoes.append(formiga.pontuacao)

                if formiga.pontuacao > self.melhor_pontuacao:
                    self.melhor_pontuacao = formiga.pontuacao
                    self.melhor_caminho = formiga.caminho

            self.pontuacoes_melhores.append(self.melhor_pontuacao)
            self.pontuacoes_medianas.append(np.median(pontuacoes))
            self.atualizar_feromonios()

        print(f"Melhor caminho encontrado: {self.melhor_caminho}")
        print(f"Melhor pontuação: {self.melhor_pontuacao}")

        # Plotagem dos dados
        plt.figure(figsize=(12, 6))

        plt.plot(self.pontuacoes_melhores, label='Melhor Pontuação', color='red')
        plt.plot(self.pontuacoes_medianas, label='Pontuação Mediana', color='blue')
        plt.xlabel('Iterações')
        plt.ylabel('Pontuação')
        plt.title('Evolução das Pontuações das Formigas ao Longo das Iterações')
        plt.legend()
        plt.grid(True)
        plt.show()

# Exemplo de uso
mundo = WumpusMundo()
aco = AlgoritmoFormigas(num_formigas=10, evaporacao=0.5, alfa=1.0, beta=2.0, iteracoes=100, mundo=mundo)
aco.executar()
