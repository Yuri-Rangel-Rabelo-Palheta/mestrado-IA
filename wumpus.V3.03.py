import random
from matplotlib import pyplot as plt
#import numpy as np

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

        self.posicao_wumpus = self._gerar_posicao_aleatoria()
        self.posicao_ouro = self._gerar_posicao_aleatoria()
        self.posicao_buracos = [self._gerar_posicao_aleatoria() for _ in range(num_buracos)]

        self.posicao_wumpus_inicial = self.posicao_wumpus
        self.posicao_ouro_inicial = self.posicao_ouro
        self.posicao_buracos_inicial = self.posicao_buracos

        # Flag para saber se é o AG ou o jogo normal
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

        self.jogo_normal = True

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
            #print("Movimento inválido!")
            self.pontuacao -= 50
            return

        self.visitados.add(self.posicao_jogador)
        percepcoes = self._checar_vizinhanca(self.posicao_jogador)
        self._exibir_percepcoes(percepcoes)

        if self.posicao_jogador == self.posicao_wumpus or self.posicao_jogador in self.posicao_buracos:
            #print("Você morreu!")
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
    def __init__(self, tamanho_populacao, taxa_mutacao, taxa_crossover, geracoes, mundo):
        self.tamanho_populacao = tamanho_populacao
        self.taxa_mutacao = taxa_mutacao
        self.taxa_crossover = taxa_crossover
        self.geracoes = geracoes
        self.mundo = mundo
        self.populacao = self.inicializar_populacao()
        self.melhor_individuo = None
        self.melhor_fitness_por_geracao = []
        self.pior_fitness_por_geracao = []

    def inicializar_populacao(self):
        populacao = []
        for _ in range(self.tamanho_populacao):
            tamanho_mundo = self.mundo.tamanho
            caminho = [random.choice(["cima", "baixo", "esquerda", "direita"]) for _ in range(tamanho_mundo * tamanho_mundo)]
            populacao.append(caminho)
        return populacao

    def avaliar_individuo(self, individuo):
        self.mundo.reset()
        agente = Agente(self.mundo)
        for movimento in individuo:
            fim_jogo = agente.mover(movimento)
            if fim_jogo:
                break

        if self.mundo.posicao_jogador == (0, 0) and self.mundo.ouro_pegado:
            return self.mundo.pontuacao
        else:
            # Penalidade para não retornar à posição inicial com o ouro
            return self.mundo.pontuacao - 500

    def selecionar_pais(self):
        pontuacoes = [self.avaliar_individuo(individuo) for individuo in self.populacao]
        # Adiciona um valor base para garantir que todas as pontuações sejam positivas
        base = abs(min(pontuacoes)) + 1
        pesos = [p + base for p in pontuacoes]
        selecionados = random.choices(self.populacao, k=2, weights=pesos)
        return selecionados

    def crossover(self, pai1, pai2):
        ponto_corte = random.randint(1, len(pai1) - 1)
        filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
        filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
        return filho1, filho2

    def mutacao(self, individuo):
        for i in range(len(individuo)):
            if random.random() < self.taxa_mutacao:
                individuo[i] = random.choice(["cima", "baixo", "esquerda", "direita"])
        return individuo

    def executar(self):
        

        for geracao in range(self.geracoes):
            nova_populacao = []
            while len(nova_populacao) < self.tamanho_populacao:
                pai1, pai2 = self.selecionar_pais()
                if random.random() < self.taxa_crossover:
                    filho1, filho2 = self.crossover(pai1, pai2)
                else:
                    filho1, filho2 = pai1, pai2

                filho1 = self.mutacao(filho1)
                filho2 = self.mutacao(filho2)

                nova_populacao.append(filho1)
                nova_populacao.append(filho2)

            self.populacao = nova_populacao

            melhor_individuo_geracao = max(self.populacao, key=self.avaliar_individuo)
            if self.melhor_individuo is None or self.avaliar_individuo(melhor_individuo_geracao) > self.avaliar_individuo(self.melhor_individuo):
                self.melhor_individuo = melhor_individuo_geracao

            melhor_pontuacao = self.avaliar_individuo(melhor_individuo_geracao)
            self.melhor_fitness_por_geracao.append(melhor_pontuacao)

            pior_individuo = min(self.populacao, key=self.avaliar_individuo)
            pior_pontuacao = self.avaliar_individuo(pior_individuo)
            self.pior_fitness_por_geracao.append(pior_pontuacao)

            #print(f"Geração {geracao + 1}: Melhor pontuação = {melhor_pontuacao}")

            esquema = []
            for caminho in melhor_individuo_geracao:
                if caminho == 'cima':
                    esquema.append('↑')
                elif caminho == 'baixo':
                    esquema.append('↓')
                elif caminho == 'esquerda':
                    esquema.append('←')
                elif caminho == 'direita':
                    esquema.append('→')

            #print(f"Caminho: {esquema}")

            pior_individuo = min(self.populacao, key=self.avaliar_individuo)
            pior_pontuacao = self.avaliar_individuo(pior_individuo)
            #print(f"Geração {geracao + 1}: Pior Pontuação: {pior_pontuacao}")

            esquema2 = []
            for caminho in pior_individuo:
                if caminho == 'cima':
                    esquema2.append('↑')
                elif caminho == 'baixo':
                    esquema2.append('↓')
                elif caminho == 'esquerda':
                    esquema2.append('←')
                elif caminho == 'direita':
                    esquema2.append('→')

            #print(f"Caminho: {esquema2}")

        return self.melhor_individuo


    def plotar(self, melhor_fitness_por_geracao, pior_fitness_por_geracao):
        plt.plot(melhor_fitness_por_geracao, label="Melhor pontuação")
        plt.plot(pior_fitness_por_geracao, label="Pior pontuação")
        plt.xlabel("Gerações")
        plt.ylabel("Pontuação")
        plt.title("Evolução da Pontuação ao Longo das Gerações")
        plt.legend()
        plt.show()



# Parâmetros do algoritmo genético
tamanho_populacao = 50
taxa_mutacao = 0.05
taxa_crossover = 0.85
geracoes = 1000

# Criação do mundo do Wumpus
mundo = WumpusMundo(tamanho=10, num_buracos=5)

# Execução do algoritmo genético
ag = AlgoritmoGenetico(tamanho_populacao, taxa_mutacao, taxa_crossover, geracoes, mundo)
melhor_solucao = ag.executar()

ag.plotar(ag.melhor_fitness_por_geracao, ag.pior_fitness_por_geracao)

# Mostra a melhor solução encontrada
print("Melhor solução encontrada:")
print(melhor_solucao)
print("Score da melhor solução:", ag.avaliar_individuo(melhor_solucao))

# Resetando o mundo
ag.mundo.reset()

# Simulando os movimentos do melhor caminho encontrado
print("Simulação dos movimentos do melhor caminho encontrado:")
mundo.mostrar()
for movimento in melhor_solucao:
    if mundo.fim_jogo:
        break
    print(f"Movendo para: {movimento}")
    mundo.mover(movimento)
    mundo.mostrar()
