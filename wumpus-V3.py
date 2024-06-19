import random

class WumpusMundo:
    def __init__(self, tamanho=3, num_buracos=1):
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

    #reseta as posições iniciais dos objetos
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
        
        self.visitados.add(self.posicao_jogador)
        percepcoes = self._checar_vizinhanca(self.posicao_jogador)
        self._exibir_percepcoes(percepcoes)
        
        if self.posicao_jogador == self.posicao_wumpus or self.posicao_jogador in self.posicao_buracos:
            print("Você morreu!")
            self.fim_jogo = True
        elif self.posicao_jogador == self.posicao_ouro:
            print("Você encontrou o ouro! Pegue-o e volte para a posição inicial para vencer.")
            self.ouro_pegado = True
            self.posicao_ouro = None
            self.pontuacao += 100
        if self.posicao_jogador == (0, 0) and self.ouro_pegado:
            print("Você voltou para a posição inicial com o ouro! Você venceu!")
            self.fim_jogo = True
    
    def _exibir_percepcoes(self, percepcoes):
        percepcao_msg = ""
        if percepcoes["cheiro horrível"]:
            percepcao_msg += "Você sente um cheiro horrível! "
        if percepcoes["brilho radiante"]:
            percepcao_msg += "Você vê um brilho radiante! "
        if percepcoes["brisa suave"]:
            percepcao_msg += "Você sente uma brisa suave! "
        if percepcao_msg:
            print(percepcao_msg)
    
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
        self.melhor_caminho = []

    def inicializar_populacao(self):
        return [{'caminho': [random.choice(['cima', 'baixo', 'esquerda', 'direita']) for _ in range(20)], 'pontuacao': 0} for _ in range(self.tamanho_populacao)]

    def avaliar(self, individuo):
        #reseta as variáveis
        self.mundo.reset()

        agente = Agente(self.mundo)
        ouro_pegado = False
        for movimento in individuo['caminho']:
            jogo.mostrar()
            if agente.mover(movimento):
                break
            if agente.mundo.posicao_jogador == agente.mundo.posicao_ouro:
                ouro_pegado = True
        
        # Pontuação baseada em evitar buracos e wumpus, pegar ouro e voltar à posição inicial
        if agente.mundo.fim_jogo:
            individuo['pontuacao'] = -1000  # Penalidade pesada por morte
        else:
            individuo['pontuacao'] = agente.score
            if ouro_pegado and agente.mundo.posicao_jogador == (0, 0):
                individuo['pontuacao'] += 1000  # Bônus por pegar o ouro e voltar à posição inicial

    def selecionar(self):
        return sorted(self.populacao, key=lambda x: x['pontuacao'], reverse=True)[:self.tamanho_populacao // 2]

    def crossover(self, pai1, pai2):
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
            self.melhor_caminho = melhor_individuo['caminho']
            print(f"Geração {geracao}: Melhor Pontuação: {melhor_individuo['pontuacao']}")

# Configuração do jogo
tamanho = 4
num_buracos = 2

jogo = WumpusMundo(tamanho=tamanho, num_buracos=num_buracos)
ag = AlgoritmoGenetico(tamanho_populacao=10, taxa_mutacao=0.01, taxa_crossover=0.7, geracoes=10, mundo=jogo)
ag.run()

# Mostrando os movimentos do melhor caminho encontrado pelo AG
print("Melhor caminho encontrado pelo AG:")
print(ag.melhor_caminho)

# Simulando os movimentos do melhor caminho encontrado
for movimento in ag.melhor_caminho:
    if jogo.fim_jogo:
        break
    print(f"Movendo para: {movimento}")
    jogo.mover(movimento)
    jogo.mostrar()

# Mostrando a percepção do mundo ao final do jogo
print("Percepção do mundo ao final do jogo:")
jogo.mostrar()
