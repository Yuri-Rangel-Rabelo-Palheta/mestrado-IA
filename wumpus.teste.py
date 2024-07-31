import datetime
import random
from matplotlib import pyplot as plt
import numpy as np

class WumpusMundo:
    def __init__(self, tamanho=4, num_buracos=2):
        self.tamanho = tamanho
        self.num_buracos = num_buracos
        self.posicao_jogador = (0, 0)
        self.posicao_wumpus = None
        self.posicao_ouro = None
        self.posicao_buracos = []
        self.fim_jogo = False
        self.pontuacao = 0
        self.flecha_disponivel = True
        self.ouro_pegado = False
        self.wumpus_morto = False
        self.visitados = set()
        self.historico = set()
        self.winner = False

        self.posicao_wumpus = self._gerar_posicao_aleatoria()
        self.posicao_ouro = self._gerar_posicao_aleatoria()
        self.posicao_buracos = [self._gerar_posicao_aleatoria() for _ in range(num_buracos)]

        self.posicao_wumpus_inicial = self.posicao_wumpus
        self.posicao_ouro_inicial = self.posicao_ouro
        self.posicao_buracos_inicial = self.posicao_buracos

        # flag para saber se é o AG ou o jogo normal
        self.jogo_normal = True

    def reset(self):
        self.posicao_jogador = (0, 0)
        self.posicao_wumpus = self.posicao_wumpus_inicial
        self.posicao_ouro = self.posicao_ouro_inicial
        self.posicao_buracos = self.posicao_buracos_inicial
        self.fim_jogo = False
        self.pontuacao = 0
        self.flecha_disponivel = True
        self.ouro_pegado = False
        self.wumpus_morto = False
        self.visitados = set()
        self.historico = set()
        self.jogo_normal = True
        self.winner = False

    def jogo_AG(self):
        self.jogo_normal = False   

    def _gerar_posicao_aleatoria(self):
        while True:
            posicao = (random.randint(0, self.tamanho - 1), random.randint(0, self.tamanho - 1))
            if posicao != (0, 0) and posicao != self.posicao_wumpus and posicao != self.posicao_ouro and posicao not in self.posicao_buracos:
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
        # Diminui a pontuação do agente a cada movimento
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
            if self.jogo_normal:
                self.fim_jogo = True
            else:
                self.fim_jogo = False
        elif self.posicao_jogador == self.posicao_ouro:
            self.ouro_pegado = True
            self.posicao_ouro = None
            self.pontuacao += 1000

        if self.posicao_jogador == (0, 0) and self.ouro_pegado:
            self.pontuacao += 1000
            if self.jogo_normal:
                self.fim_jogo = True
                self.winner = True
            else:
                self.fim_jogo = False

    def _exibir_percepcoes(self, percepcoes):
        percepcao_msg = ""
        if percepcoes["cheiro horrível"]:
            percepcao_msg += "Você sente um cheiro horrível! "
        if percepcoes["brilho radiante"]:
            percepcao_msg += "Você vê um brilho radiante! "
        if percepcoes["brisa suave"]:
            percepcao_msg += "Você sente uma brisa suave! "

    def verificar_vizinhanca(self):
        percepcoes = self._checar_vizinhanca(self.posicao_jogador)
        self._exibir_percepcoes(percepcoes)

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

class Agente:
    def __init__(self, mundo):
        self.mundo = mundo
        self.posicao = (0, 0)
        self.score = 0
        self.ouro_pegado = False

    def mover(self, direcao):
        self.mundo.mover(direcao)
        self.score = self.mundo.pontuacao

        if self.mundo.fim_jogo:
            return True  # Indica fim de jogo
        return False

class AlgoritmoGenetico:
    def __init__(self, tamanho_populacao, taxa_mutacao, taxa_crossover, geracoes, mundo, max_geracoes_sem_melhoria=50):
        self.tamanho_populacao = tamanho_populacao
        self.taxa_mutacao = taxa_mutacao
        self.taxa_crossover = taxa_crossover
        self.geracoes = geracoes
        self.mundo = mundo
        self.max_geracoes_sem_melhoria = max_geracoes_sem_melhoria
        self.populacao = self.inicializar_populacao()
        self.melhor_individuo = None

    def inicializar_populacao(self):
        populacao = []
        for _ in range(self.tamanho_populacao):
            tamanho_mundo = self.mundo.tamanho
            media = (tamanho_mundo + 10) / 2
            desvio_padrao = abs((tamanho_mundo - 5) / 2)
            tamanho_caminho = 400
            caminho = [random.choice(['cima', 'baixo', 'esquerda', 'direita']) for _ in range(tamanho_caminho)]
            populacao.append(caminho)
        return populacao

    def avaliar_individuo(self, individuo):
        self.mundo.reset()
        agente = Agente(self.mundo)
        for acao in individuo:
            terminou = agente.mover(acao)
            if terminou:
                break
        return agente.score

    def avaliar_populacao(self):
        avaliacoes = [self.avaliar_individuo(individuo) for individuo in self.populacao]
        return avaliacoes

    def selecionar_pais(self, avaliacoes):
        ordenados = sorted(enumerate(avaliacoes), key=lambda x: x[1], reverse=True)
        pais = [self.populacao[i] for i, _ in ordenados[:self.tamanho_populacao // 2]]
        return pais

    def crossover(self, pai1, pai2):
        ponto_crossover = random.randint(1, len(pai1) - 1)
        filho1 = pai1[:ponto_crossover] + pai2[ponto_crossover:]
        filho2 = pai2[:ponto_crossover] + pai1[ponto_crossover:]
        return filho1, filho2

    def mutacao(self, individuo):
        for _ in range(int(len(individuo) * self.taxa_mutacao)):
            indice = random.randint(0, len(individuo) - 1)
            individuo[indice] = random.choice(['cima', 'baixo', 'esquerda', 'direita'])
        return individuo

    def proxima_geracao(self, pais):
        nova_populacao = []
        while len(nova_populacao) < self.tamanho_populacao:
            pai1, pai2 = random.sample(pais, 2)
            filho1, filho2 = self.crossover(pai1, pai2)
            nova_populacao.append(self.mutacao(filho1))
            nova_populacao.append(self.mutacao(filho2))
        return nova_populacao

    def executar(self):
        melhores_pontuacoes = []
        piores_pontuacoes = []
        geracao_sem_melhoria = 0
        melhor_pontuacao = -float('inf')

        for geracao in range(self.geracoes):
            avaliacoes = self.avaliar_populacao()
            melhor_geracao = max(avaliacoes)
            pior_geracao = min(avaliacoes)

            if melhor_geracao > melhor_pontuacao:
                melhor_pontuacao = melhor_geracao
                geracao_sem_melhoria = 0
            else:
                geracao_sem_melhoria += 1

            melhores_pontuacoes.append(melhor_geracao)
            piores_pontuacoes.append(pior_geracao)

            if geracao_sem_melhoria >= self.max_geracoes_sem_melhoria:
                print(f"Estagnação detectada na geração {geracao}. Recriação de metade da população.")
                pais = self.selecionar_pais(avaliacoes)
                self.populacao = self.proxima_geracao(pais)
                geracao_sem_melhoria = 0
            else:
                pais = self.selecionar_pais(avaliacoes)
                self.populacao = self.proxima_geracao(pais)

        return melhores_pontuacoes, piores_pontuacoes

def plotar_performance(melhores_pontuacoes, piores_pontuacoes):
    geracoes = list(range(len(melhores_pontuacoes)))
    plt.plot(geracoes, melhores_pontuacoes, label="Melhores Pontuações")
    plt.plot(geracoes, piores_pontuacoes, label="Piores Pontuações")
    plt.xlabel("Geração")
    plt.ylabel("Pontuação")
    plt.title("Desempenho dos Indivíduos ao Longo das Gerações")
    plt.legend()
    plt.show()

# Uso do Algoritmo Genético
tamanho_populacao = 50
taxa_mutacao = 0.05
taxa_crossover = 0.85
geracoes = 1000
mundo = WumpusMundo(tamanho=20, num_buracos=10)
ag = AlgoritmoGenetico(tamanho_populacao, taxa_mutacao, taxa_crossover, geracoes, mundo)
melhores_pontuacoes, piores_pontuacoes = ag.executar()

# Plotar a performance
plotar_performance(melhores_pontuacoes, piores_pontuacoes)


