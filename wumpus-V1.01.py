import random
import datetime
import matplotlib.pyplot as plt

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
        self.historico = set()

        self.posicao_wumpus = self._gerar_posicao_aleatoria()
        self.posicao_ouro = self._gerar_posicao_aleatoria()
        self.posicao_buracos = [self._gerar_posicao_aleatoria() for _ in range(num_buracos)]

    def resetar(self):
        self.posicao_jogador = (0, 0)
        self.fim_jogo = False
        self.pontuacao = 0
        self.flecha_disponivel = True
        self.ouro_pegado = False
        self.wumpus_morto = False
        self.historico = set()

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
            if adj_pos in self.posicao_buracos:
                percepcoes["brisa suave"] = True
        if posicao == self.posicao_ouro:
            percepcoes["brilho radiante"] = True
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
        elif direcao == "direita" and y < self.tamanho - 1:
            self.posicao_jogador = (x, y + 1)
        else:
            print("Movimento inválido!")
            self.pontuacao -= 50
            return
        percepcoes = self._checar_vizinhanca(self.posicao_jogador)
        self._exibir_percepcoes(percepcoes)
        if self.posicao_jogador == self.posicao_wumpus or self.posicao_jogador in self.posicao_buracos:
            print("Você morreu!")
            self.fim_jogo = True
        elif self.posicao_jogador == self.posicao_ouro:
            print("Você encontrou o ouro! Pegue-o e volte para a posição inicial para vencer.")
            self.ouro_pegado = True
            self.posicao_ouro = None
            self.pontuacao += 1000
        if self.posicao_jogador == (0, 0) and (self.ouro_pegado or self.wumpus_morto):
            print("Você voltou para a posição inicial com o ouro ou após matar o Wumpus! Você venceu!")
            self.fim_jogo = True

        self.historico.add(self.posicao_jogador)

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

    def atirar(self, direcao):
        if not self.flecha_disponivel:
            print("Você já usou sua flecha!")
            return

        self.flecha_disponivel = False
        x, y = self.posicao_jogador
        if direcao == "cima":
            x -= 1
        elif direcao == "baixo":
            x += 1
        elif direcao == "esquerda":
            y -= 1
        elif direcao == "direita":
            y += 1

        if (x, y) == self.posicao_wumpus:
            print("Você matou o Wumpus!")
            self.wumpus_morto = True
            self.posicao_wumpus = None
            self.pontuacao += 1000
        else:
            print("Você errou o tiro!")
            self.pontuacao -= 1000

class AgenteInteligente:
    def __init__(self, jogo):
        self.jogo = jogo

    def tomar_acao(self):
        percepcoes = self.jogo._checar_vizinhanca(self.jogo.posicao_jogador)

        if percepcoes["cheiro horrível"]:
            if self.jogo.flecha_disponivel:
                print("Agente atirando na direção do Wumpus!")
                self.atirar()
            else:
                print("Agente evitando mover na direção do Wumpus!")
                self.mover_em_segurança()
        elif percepcoes["brilho radiante"]:
            print("Agente movendo na direção do brilho radiante!")
            self.mover_para_ouro()
        elif percepcoes["brisa suave"]:
            print("Agente evitando mover na direção da brisa!")
            self.mover_em_segurança()
        else:
            print("Agente movendo para qualquer direção segura!")
            self.mover_em_segurança()

    def atirar(self):
        direcoes = ["cima", "baixo", "esquerda", "direita"]
        for direcao in direcoes:
            if self._atirar_na_direcao(direcao):
                print("Você matou o Wumpus!")
                self.jogo.wumpus_morto = True
                self.jogo.posicao_wumpus = None
                self.jogo.pontuacao += 1000
                return
        print("Você errou o tiro!")
        self.jogo.pontuacao -= 1000

    def _atirar_na_direcao(self, direcao):
        x, y = self.jogo.posicao_jogador
        if direcao == "cima":
            x -= 1
        elif direcao == "baixo":
            x += 1
        elif direcao == "esquerda":
            y -= 1
        elif direcao == "direita":
            y += 1
        if (x, y) == self.jogo.posicao_wumpus:
            return True
        return False

    def mover_em_segurança(self):
        adjacentes = self.jogo._checar_adjacentes(self.jogo.posicao_jogador)
        pesos = []
        for direcao, pos in adjacentes.items():
            if pos == self.jogo.posicao_wumpus or pos in self.jogo.posicao_buracos:
                pesos.append(1)  # Menor peso para posições perigosas
            else:
                pesos.append(10)  # Maior peso para posições seguras

        direcao_escolhida = random.choices(list(adjacentes.keys()), weights=pesos)[0]
        self.jogo.mover(direcao_escolhida)

    def mover_para_ouro(self):
        adjacentes = self.jogo._checar_adjacentes(self.jogo.posicao_jogador)
        for direcao, adj_pos in adjacentes.items():
            if adj_pos == self.jogo.posicao_ouro:
                self.jogo.mover(direcao)
                return

# Função para salvar o registro da partida
def salvar_registro(jogo_inicial,jogo, caminho_arquivo="registro"):
    data_atual = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    caminho_arquivo = f"{caminho_arquivo}_{data_atual}.txt"
    
    with open(caminho_arquivo, "w") as file:
        file.write(f"Tamanho do mapa: {jogo.tamanho}\n")
        file.write(f"Posição do Wumpus: {jogo_inicial.posicao_wumpus}\n")
        file.write(f"Posicao do Ouro: {jogo_inicial.posicao_ouro}\n")
        file.write(f"Posicoes dos Buracos: {jogo_inicial.posicao_buracos}\n")
        file.write(f"Movimentos do Jogador:\n")
        for movimento in jogo.historico:
            file.write(f"{movimento}\n")

    print(f"Registro salvo em {caminho_arquivo}")

# Função para executar o jogo automaticamente 20 vezes
def executar_vezes(tamanho, num_buracos, vezes=20):
    resultados = []
    jogo_inicial = WumpusMundo(tamanho=tamanho, num_buracos=num_buracos)
    agente = AgenteInteligente(jogo_inicial)

    for i in range(vezes):
        jogo = WumpusMundo(tamanho=tamanho, num_buracos=num_buracos)
        jogo.posicao_wumpus = jogo_inicial.posicao_wumpus
        jogo.posicao_ouro = jogo_inicial.posicao_ouro
        jogo.posicao_buracos = jogo_inicial.posicao_buracos.copy()
        agente = AgenteInteligente(jogo)

        while not jogo.fim_jogo:
            agente.tomar_acao()
        
        resultados.append(jogo.pontuacao)
        #jogo.resetar()
        salvar_registro(jogo_inicial,jogo)
        jogo.resetar()
        #jogo_inicial = WumpusMundo(tamanho=tamanho, num_buracos=num_buracos)

    return resultados

# Função para plotar os gráficos
def plotar_graficos(resultados):
    plt.figure(figsize=(18, 6))

    # Histograma
    plt.subplot(1, 3, 1)
    plt.hist(resultados, bins=10, edgecolor='black')
    plt.title('Distribuição das Pontuações')
    plt.xlabel('Pontuação')
    plt.ylabel('Frequência')

    # Gráfico de linhas
    plt.subplot(1, 3, 2)
    plt.plot(resultados, marker='o')
    plt.title('Desempenho ao Longo das Execuções')
    plt.xlabel('Execução')
    plt.ylabel('Pontuação')

    # Gráfico de barras (acurácia)
    plt.subplot(1, 3, 3)
    vitorias = sum(1 for resultado in resultados if resultado >= 1000)
    derrotas = len(resultados) - vitorias
    plt.bar(['Vitórias', 'Derrotas'], [vitorias, derrotas], color=['green', 'red'])
    plt.title('Acurácia do Agente')
    plt.xlabel('Resultado')
    plt.ylabel('Quantidade')

    plt.tight_layout()
    plt.show()

# Entrada do usuário
tamanhoI = int(input("Digite o tamanho do mapa (3 ou mais): "))
num_buracosI = int(input("Digite a quantidade de poços (1 ou mais): "))
if num_buracosI > (tamanhoI * tamanhoI):
    print("O número de poços deve ser menor que o tamanho do mapa!")
    exit()
if tamanhoI < 3:
    print("O tamanho do mapa deve ser pelo menos 3!")
    exit()
if num_buracosI < 1:
    print("O número de poços deve ser pelo menos 1!")
    exit()

# Executar o jogo 20 vezes e imprimir resultados
resultados = executar_vezes(tamanhoI, num_buracosI)
print("Resultados das 20 execuções:", resultados)
print("Pontuação média:", sum(resultados) / len(resultados))

# Plotar os gráficos
plotar_graficos(resultados)
