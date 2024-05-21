import random

class WumpusMundo:
    def __init__(self, tamanho=3, num_buracos=1):
        self.tamanho = tamanho
        self.num_buracos = num_buracos
        self.posicao_jogador = (0, 0)
        self.posicao_wumpus = None  # Inicialize como None
        self.posicao_ouro = None  # Inicialize como None
        self.posicao_buracos = []  # Inicialize como lista vazia
        self.fim_jogo = False
        self.pontuacao = 0
        self.tem_flecha = True  # O jogador começa com uma flecha
        
        # Agora defina as posições evitando colisões
        self.posicao_wumpus = self._gerar_posicao_aleatoria()
        self.posicao_ouro = self._gerar_posicao_aleatoria()
        self.posicao_buracos = [self._gerar_posicao_aleatoria() for _ in range(num_buracos)]

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
        adjacentes = self._checar_adjacentes(posicao)
        wumpus_proximo = False
        ouro_proximo = False
        buraco_proximo = False

        for adj_pos in adjacentes.values():
            if adj_pos == self.posicao_wumpus:
                wumpus_proximo = True
            if adj_pos == self.posicao_ouro:
                ouro_proximo = True
            if adj_pos in self.posicao_buracos:
                buraco_proximo = True

        if wumpus_proximo:
            print(f"Você sente um cheiro horrível!")
        if ouro_proximo:
            print(f"Você vê um brilho radiante!")
        if buraco_proximo:
            print(f"Você sente uma brisa suave!")

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
        if self.posicao_jogador == self.posicao_wumpus:
            print("Você morreu!")
            self.fim_jogo = True
        elif self.posicao_jogador in self.posicao_buracos:
            print("Você caiu em um buraco!")
            self.fim_jogo = True
        elif self.posicao_jogador == self.posicao_ouro:
            print("Você encontrou o ouro! Parabéns!")
            self.pontuacao += 100
            self.fim_jogo = True

    def verificar_vizinhanca(self):
        self._checar_vizinhanca(self.posicao_jogador)

    def atirar(self, direcao):
        if not self.tem_flecha:
            print("Você já usou sua flecha!")
            return

        self.tem_flecha = False
        x, y = self.posicao_jogador

        if direcao == "cima":
            for i in range(x - 1, -1, -1):
                if (i, y) == self.posicao_wumpus:
                    print("Você acertou o Wumpus!")
                    self.pontuacao += 100
                    self.fim_jogo = True
                    return
        elif direcao == "baixo":
            for i in range(x + 1, self.tamanho):
                if (i, y) == self.posicao_wumpus:
                    print("Você acertou o Wumpus!")
                    self.pontuacao += 100
                    self.fim_jogo = True
                    return
        elif direcao == "esquerda":
            for j in range(y - 1, -1, -1):
                if (x, j) == self.posicao_wumpus:
                    print("Você acertou o Wumpus!")
                    self.pontuacao += 100
                    self.fim_jogo = True
                    return
        elif direcao == "direita":
            for j in range(y + 1, self.tamanho):
                if (x, j) == self.posicao_wumpus:
                    print("Você acertou o Wumpus!")
                    self.pontuacao += 100
                    self.fim_jogo = True
                    return

        print("Você errou o tiro!")
        self.pontuacao -= 100

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


tamanhoI = int(input("Digite o tamanho do mapa (3 ou mais): "))
num_buracosI = int(input("Digite a quantidade de poços (1 ou mais): "))
if num_buracosI > (tamanhoI * tamanhoI - 3):
    print("O número de poços deve ser menor que o tamanho do mapa!")
    exit()
if tamanhoI < 3:
    print("O tamanho do mapa deve ser pelo menos 3!")
    exit()

jogo = WumpusMundo(tamanho=tamanhoI, num_buracos=num_buracosI)

jogo.mostrar()
while not jogo.fim_jogo:
    acao = input("Digite uma ação (cima, baixo, esquerda, direita, verificar, atirar): ")
    if acao in ["cima", "baixo", "esquerda", "direita"]:
        jogo.mover(acao)
    elif acao == "verificar":
        jogo.verificar_vizinhanca()
    elif acao == "atirar":
        direcao_tiro = input("Digite a direção para atirar (cima, baixo, esquerda, direita): ")
        if direcao_tiro in ["cima", "baixo", "esquerda", "direita"]:
            jogo.atirar(direcao_tiro)
        else:
            print("Direção de tiro inválida!")
    else:
        print("Ação inválida!")
    jogo.mostrar()
