import random
import numpy as np
import matplotlib.pyplot as plt

class WumpusMundo:
    def __init__(self, tamanho=10, num_buracos=2):
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
        self.pontuacao -= 1

        x, y = self.posicao_jogador
        if direcao == "cima" and x > 0:
            self.posicao_jogador = (x - 1, y)
        elif direcao == "baixo" and x < self.tamanho - 1:
            self.posicao_jogador = (x + 1, y)
        elif direcao == "esquerda" and y > 0:
            self.posicao_jogador = (x, y - 1)
        elif direcao == "direita" and y < 0:
            self.posicao_jogador = (x, y + 1)
        else:
            self.pontuacao -= 100
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
            return True
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

    def inicializar_populacao(self):
        populacao = []
        for _ in range(self.tamanho_populacao):
            tamanho_mundo = self.mundo.tamanho
            media = (tamanho_mundo + 10) / 2
            desvio_padrao = abs((tamanho_mundo - 5) / 2)  # Garantir que o desvio padrão seja positivo
            tamanho_caminho = 200#int(np.clip(np.random.normal(media, desvio_padrao), 2, pow(tamanho_mundo, 2)))
            caminho = [random.choice(['cima', 'baixo', 'esquerda', 'direita']) for _ in range(tamanho_caminho)]
            populacao.append({'caminho': caminho, 'pontuacao': 1})  # Inicialização da pontuação para evitar zero

        return populacao

    def avaliar(self, individuo):
        self.mundo.reset()
        self.mundo.jogo_AG()
        agente = Agente(self.mundo)

        for movimento in individuo['caminho']:
            fim_jogo = agente.mover(movimento)
            if fim_jogo:
                break

        individuo['pontuacao'] = agente.score

    def selecionar_pais(self):
        total_pontuacao = sum(individuo['pontuacao'] for individuo in self.populacao)
        
        # Verifica se total_pontuacao é zero para evitar divisão por zero
        if total_pontuacao == 0:
            probabilidade = [1 / len(self.populacao) for _ in self.populacao]
        else:
            probabilidade = [individuo['pontuacao'] / total_pontuacao for individuo in self.populacao]
        
        pais = random.choices(self.populacao, weights=probabilidade, k=2)
        return pais

    def crossover(self, pai1, pai2):
        ponto_corte = random.randint(1, len(pai1['caminho']) - 1)
        filho1_caminho = pai1['caminho'][:ponto_corte] + pai2['caminho'][ponto_corte:]
        filho2_caminho = pai2['caminho'][:ponto_corte] + pai1['caminho'][ponto_corte:]
        return {'caminho': filho1_caminho, 'pontuacao': 0}, {'caminho': filho2_caminho, 'pontuacao': 0}

    def mutacao(self, individuo):
        for i in range(len(individuo['caminho'])):
            if random.random() < self.taxa_mutacao:
                individuo['caminho'][i] = random.choice(['cima', 'baixo', 'esquerda', 'direita'])

    def encontrar_melhor_individuo(self):
        return max(self.populacao, key=lambda individuo: individuo['pontuacao'])

    def executar(self):
        melhor_fitness_por_geracao = []

        for geracao in range(self.geracoes):
            nova_populacao = []

            for _ in range(self.tamanho_populacao // 2):
                pai1, pai2 = self.selecionar_pais()
                filho1, filho2 = self.crossover(pai1, pai2)

                self.mutacao(filho1)
                self.mutacao(filho2)

                self.avaliar(filho1)
                self.avaliar(filho2)

                nova_populacao.extend([filho1, filho2])

            self.populacao = nova_populacao
            melhor_individuo = self.encontrar_melhor_individuo()
            melhor_fitness_por_geracao.append(melhor_individuo['pontuacao'])

            print(f"Geração {geracao + 1}: Melhor pontuação = {melhor_individuo['pontuacao']}")

        self.melhor_individuo = self.encontrar_melhor_individuo()
        return melhor_fitness_por_geracao

    def plotar(self, fitness_por_geracao):
        plt.plot(range(1, self.geracoes + 1), fitness_por_geracao)
        plt.xlabel("Gerações")
        plt.ylabel("Melhor Pontuação")
        plt.title("Evolução da Pontuação ao Longo das Gerações")
        plt.show() 

# Inicialização do ambiente Wumpus e execução do Algoritmo Genético
mundo = WumpusMundo(tamanho=10, num_buracos=5)
ag = AlgoritmoGenetico(tamanho_populacao=50, taxa_mutacao=0.05, taxa_crossover=0.85, geracoes=100, mundo=mundo)

# Execução do Algoritmo Genético e plotagem dos resultados
melhor_fitness_por_geracao = ag.executar()
ag.plotar(melhor_fitness_por_geracao)

# Mostrar o melhor caminho encontrado
print("Melhor caminho encontrado:")
print(ag.melhor_individuo['caminho'])

# Simulação do melhor caminho encontrado
mundo.reset()
mundo.jogo_AG()
agente = Agente(mundo)
for movimento in ag.melhor_individuo['caminho']:
    fim_jogo = agente.mover(movimento)
    mundo.mostrar()
    if fim_jogo:
        break
