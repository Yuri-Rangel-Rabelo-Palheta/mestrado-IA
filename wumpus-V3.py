import random

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

    def jogo_AG(self):
        self.jogo_normal = False  

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
            self.pontuacao -= 100
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
        return [{'caminho': [random.choice(['cima', 'baixo', 'esquerda', 'direita']) for _ in range(40)], 'pontuacao': 0} for _ in range(self.tamanho_populacao)]

    def avaliar(self, individuo):
        self.mundo.reset()

        self.mundo.jogo_AG()

        agente = Agente(self.mundo)
        ouro_pegado = False
        caminho_ate_ouro = []
        caminho_de_volta = []
        encontrou_ouro = False

        for movimento in individuo['caminho']:
            if agente.mover(movimento):
                break
            if agente.mundo.posicao_jogador == agente.mundo.posicao_ouro and not encontrou_ouro:
                encontrou_ouro = True
                ouro_pegado = True
            if not encontrou_ouro:
                caminho_ate_ouro.append(movimento)
            else:
                caminho_de_volta.append(movimento)

        if agente.mundo.fim_jogo:
            individuo['pontuacao'] = -1000
        else:
            individuo['pontuacao'] = agente.score
            if ouro_pegado and agente.mundo.posicao_jogador == (0, 0):
                individuo['pontuacao'] += 1000
            elif ouro_pegado:
                individuo['pontuacao'] -= 500

    def selecionar(self):
        min_pontuacao = min(individuo['pontuacao'] for individuo in self.populacao)
        ajuste = abs(min_pontuacao) + 1 if min_pontuacao < 0 else 0
        return random.choices(self.populacao, weights=[individuo['pontuacao'] + ajuste for individuo in self.populacao], k=self.tamanho_populacao // 2)

    def crossover(self, pai1, pai2):
        if random.random() > self.taxa_crossover:
            return pai1, pai2

        ponto_corte = random.randint(1, len(pai1['caminho']) - 2)
        filho1 = {'caminho': pai1['caminho'][:ponto_corte] + pai2['caminho'][ponto_corte:], 'pontuacao': 0}
        filho2 = {'caminho': pai2['caminho'][:ponto_corte] + pai1['caminho'][ponto_corte:], 'pontuacao': 0}
        return filho1, filho2

    def mutacao(self, individuo):
        if random.random() < self.taxa_mutacao:
            ponto_mutacao = random.randint(0, len(individuo['caminho']) - 1)
            individuo['caminho'][ponto_mutacao] = random.choice(['cima', 'baixo', 'esquerda', 'direita'])

    def run(self):
        for geracao in range(self.geracoes):
            for individuo in self.populacao:
                self.avaliar(individuo)

            self.populacao = self.selecionar()
            nova_populacao = []
            while len(nova_populacao) < self.tamanho_populacao:
                pai1, pai2 = random.sample(self.populacao, 2)
                filho1, filho2 = self.crossover(pai1, pai2)
                self.mutacao(filho1)
                self.mutacao(filho2)
                nova_populacao.extend([filho1, filho2])
            self.populacao = nova_populacao

            melhor_individuo = max(self.populacao, key=lambda x: x['pontuacao'])
            self.melhor_individuo = melhor_individuo
            print(f"Geração {geracao}: Melhor Pontuação: {melhor_individuo['pontuacao']}")

# Configuração do jogo
tamanho = 10
num_buracos = 5

jogo = WumpusMundo(tamanho=tamanho, num_buracos=num_buracos)

#solicita os parametros para o algoritmo genetico
"""print("Configuração do Algoritmo Genetico:")
tamanho_populacao = int(input("Tamanho da População: "))
taxa_mutacao = float(input("Taxa de Mutação: "))
taxa_crossover = float(input("Taxa de Crossover: "))
geracoes = int(input("Gerações: "))"""

ag = AlgoritmoGenetico(tamanho_populacao=50, taxa_mutacao=0.25, taxa_crossover=0.5, geracoes=1000, mundo=jogo)

#ag = AlgoritmoGenetico(tamanho_populacao=tamanho_populacao, taxa_mutacao=taxa_mutacao, taxa_crossover=taxa_crossover, geracoes=geracoes, mundo=jogo)

ag.run()

# Mostrando os movimentos do melhor caminho encontrado pelo AG
print("Melhor caminho encontrado pelo AG:")
print(ag.melhor_individuo['caminho'])

# Resetando o mundo
ag.mundo.reset()

# Simulando os movimentos do melhor caminho encontrado
print("Simulação dos movimentos do melhor caminho encontrado:")
for movimento in ag.melhor_individuo['caminho']:
    if jogo.fim_jogo:
        break
    print(f"Movendo para: {movimento}")
    jogo.mover(movimento)
    jogo.mostrar()

jogo.mostrar()
