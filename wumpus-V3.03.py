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

        self.posicao_wumpus = self._gerar_posicao_aleatoria()
        self.posicao_ouro = self._gerar_posicao_aleatoria()
        self.posicao_buracos = [self._gerar_posicao_aleatoria() for _ in range(num_buracos)]

        self.posicao_wumpus_inicial = self.posicao_wumpus
        self.posicao_ouro_inicial = self.posicao_ouro
        self.posicao_buracos_inicial = self.posicao_buracos

        #flag para saber se é o AG ou o jogo normal
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
            #self.fim_jogo = True
            if self.jogo_normal:
                self.fim_jogo = True
            else:
                self.fim_jogo = False
        elif self.posicao_jogador == self.posicao_ouro:
            #print("Você encontrou o ouro! Pegue-o e volte para a posição inicial para vencer.")
            self.ouro_pegado = True
            self.posicao_ouro = None
            self.pontuacao += 1000
        if self.posicao_jogador == (0, 0) and self.ouro_pegado:
            #print("Você voltou para a posição inicial com o ouro! Você venceu!")
            self.pontuacao += 1000
            #self.fim_jogo = True
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
        #if percepcao_msg:
            #print(percepcao_msg)

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

    def inicializar_populacao(self):
        populacao = []
        for _ in range(self.tamanho_populacao):
            tamanho_mundo = self.mundo.tamanho
            media = (tamanho_mundo + 10) / 2
            desvio_padrao = abs((tamanho_mundo - 5) / 2)  # Garantir que o desvio padrão seja positivo
            tamanho_caminho = 200# int(np.clip(np.random.normal(media, desvio_padrao), 2, pow(tamanho_mundo, 2)))
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
        pais = []

        for _ in range(2):  # Seleciona dois pais
            # Seleciona aleatoriamente dois indivíduos da população para o torneio
            participantes = random.sample(self.populacao, k=2)
            
            # Escolhe o participante com melhor pontuação
            vencedor = max(participantes, key=lambda x: x['pontuacao'])
            
            pais.append(vencedor)

        return pais
###########################################
    def crossover(self, pai1, pai2):
        if random.random() > self.taxa_crossover:
            return pai1, pai2

        if len(pai1['caminho']) < 3 or len(pai2['caminho']) < 3:
            return pai1, pai2  # Retorna os pais inalterados se qualquer um dos caminhos for muito curto

        # Seleciona dois pontos de corte aleatórios
        ponto_corte1 = random.randint(1, min(len(pai1['caminho']), len(pai2['caminho'])) - 2)
        ponto_corte2 = random.randint(ponto_corte1 + 1, min(len(pai1['caminho']), len(pai2['caminho'])) - 1)

        # Cria os filhos combinando os caminhos dos pais nos pontos de corte
        filho1 = {
            'caminho': pai1['caminho'][:ponto_corte1] + pai2['caminho'][ponto_corte1:ponto_corte2] + pai1['caminho'][ponto_corte2:], 
            'pontuacao': 0
        }
        filho2 = {
            'caminho': pai2['caminho'][:ponto_corte1] + pai1['caminho'][ponto_corte1:ponto_corte2] + pai2['caminho'][ponto_corte2:], 
            'pontuacao': 0
        }

        return filho1, filho2


    def mutacao(self, individuo):
        if random.random() < self.taxa_mutacao:
            # Seleciona dois pontos de mutação diferentes no cromossomo
            ponto1 = random.randint(0, len(individuo['caminho']) - 1)
            ponto2 = random.randint(0, len(individuo['caminho']) - 1)
            
            # Garante que ponto1 é menor que ponto2
            if ponto1 > ponto2:
                ponto1, ponto2 = ponto2, ponto1
            
            # Inverte os genes entre ponto1 e ponto2
            individuo['caminho'][ponto1:ponto2+1] = individuo['caminho'][ponto1:ponto2+1][::-1]
        
        # Adiciona novos genes aleatórios ao cromossomo com uma certa probabilidade
        if random.random() < self.taxa_mutacao:
            # Decide quantos genes adicionar
            num_novos_genes = random.randint(1, 3)  # Por exemplo, adiciona de 1 a 3 novos genes
            novos_genes = [random.choice(['cima', 'baixo', 'esquerda', 'direita']) for _ in range(num_novos_genes)]
            
            # Insere os novos genes em posições aleatórias
            for novo_gene in novos_genes:
                posicao_insercao = random.randint(0, len(individuo['caminho']))
                individuo['caminho'].insert(posicao_insercao, novo_gene)

        
###########################################            


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

            esquema = []
            for caminho in melhor_individuo['caminho']:
                if caminho == 'cima':
                    esquema.append('↑')
                elif caminho == 'baixo':
                    esquema.append('↓')
                elif caminho == 'esquerda':
                    esquema.append('←')
                elif caminho == 'direita':
                    esquema.append('→')

            print(f"Caminho: {esquema}")

            pior_individuo = min(self.populacao, key=lambda x: x['pontuacao'])
            print(f"Geração {geracao}: Pior Pontuação: {pior_individuo['pontuacao']}")
            esquema2 = []
            for caminho in pior_individuo['caminho']:
                if caminho == 'cima':
                    esquema2.append('↑')
                elif caminho == 'baixo':
                    esquema2.append('↓')
                elif caminho == 'esquerda':
                    esquema2.append('←')
                elif caminho == 'direita':
                    esquema2.append('→')

            print(f"Caminho: {esquema2}")

            
            

        self.melhor_individuo = self.encontrar_melhor_individuo()
        return melhor_fitness_por_geracao
    
    def plotar(self, fitness_por_geracao):
        plt.plot(range(1, self.geracoes + 1), fitness_por_geracao)
        plt.xlabel("Gerações")
        plt.ylabel("Melhor Pontuação")
        plt.title("Evolução da Pontuação ao Longo das Gerações")
        plt.show() 
        

# Configuração do jogo
tamanho = 10
num_buracos = 4

jogo = WumpusMundo(tamanho=tamanho, num_buracos=num_buracos)

#solicita os parametros para o algoritmo genetico
"""print("Configuração do Algoritmo Genetico:")
tamanho_populacao = int(input("Tamanho da População: "))
taxa_mutacao = float(input("Taxa de Mutação: "))
taxa_crossover = float(input("Taxa de Crossover: "))
geracoes = int(input("Gerações: "))"""

#ag = AlgoritmoGenetico(tamanho_populacao=tamanho_populacao, taxa_mutacao=taxa_mutacao, taxa_crossover=taxa_crossover, geracoes=geracoes, mundo=jogo)

ag = AlgoritmoGenetico(tamanho_populacao=50, taxa_mutacao=0.05, taxa_crossover=0.85, geracoes=1000, mundo=jogo)

melhor_fitness_por_geracao = ag.executar()

# Mostrando os movimentos do melhor caminho encontrado pelo AG
print("Melhor caminho encontrado pelo AG:")
print(ag.melhor_individuo['caminho'])
print("Score: ", ag.melhor_individuo['pontuacao'])

ag.plotar(melhor_fitness_por_geracao)

# Resetando o mundo
ag.mundo.reset()

# Simulando os movimentos do melhor caminho encontrado
print("Simulação dos movimentos do melhor caminho encontrado:")
jogo.mostrar()
for movimento in ag.melhor_individuo['caminho']:
    if jogo.fim_jogo:
        break
    print(f"Movendo para: {movimento}")
    jogo.mover(movimento)
    jogo.mostrar() 
