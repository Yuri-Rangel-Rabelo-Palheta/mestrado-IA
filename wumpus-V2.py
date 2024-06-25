""" import random

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

        self.posicao_wumpus = self._gerar_posicao_aleatoria()
        self.posicao_ouro = self._gerar_posicao_aleatoria()
        self.posicao_buracos = [self._gerar_posicao_aleatoria() for _ in range(num_buracos)]
        self.historico = set()  # Histórico de posições visitadas

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
        self.historico.add(self.posicao_jogador)  # Adiciona a posição ao histórico
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
        if self.posicao_jogador == (0, 0) and (self.ouro_pegado or self.wumpus_morto):
            print("Você voltou para a posição inicial com o ouro ou após matar o Wumpus! Você venceu!")
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

    def atirar(self, direcao):
        if not self.flecha_disponivel:
            print("Você já usou sua flecha!")
            return

        self.flecha_disponivel = False
        x, y = self.posicao_jogador
        while 0 <= x < self.tamanho and 0 <= y < self.tamanho:
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
                self.pontuacao += 100
                break

        if not self.wumpus_morto:
            print("Você errou o tiro!")
            self.pontuacao -= 100


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
                self.jogo.pontuacao += 100
                return
        print("Você errou o tiro!")
        self.jogo.pontuacao -= 100

    def _atirar_na_direcao(self, direcao):
        x, y = self.jogo.posicao_jogador
        while 0 <= x < self.jogo.tamanho and 0 <= y < self.jogo.tamanho:
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
        direcoes_seguras = []

        for direcao, pos in adjacentes.items():
            if pos not in self.jogo.historico and pos != self.jogo.posicao_wumpus and pos not in self.jogo.posicao_buracos:
                direcoes_seguras.append(direcao)

        if direcoes_seguras:
            direcao_escolhida = random.choice(direcoes_seguras)
            self.jogo.mover(direcao_escolhida)
        else:
            print("Não há direções seguras conhecidas, movendo aleatoriamente.")
            direcao_escolhida = random.choice(list(adjacentes.keys()))
            self.jogo.mover(direcao_escolhida)

    def mover_para_ouro(self):
        adjacentes = self.jogo._checar_adjacentes(self.jogo.posicao_jogador)
        for direcao, adj_pos in adjacentes.items():
            if adj_pos == self.jogo.posicao_ouro:
                self.jogo.mover(direcao)
                return


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

jogo = WumpusMundo(tamanho=tamanhoI, num_buracos=num_buracosI)
agente = AgenteInteligente(jogo)

jogo.mostrar()
while not jogo.fim_jogo:
    acao = input("Digite uma ação (cima, baixo, esquerda, direita, verificar, atirar, agente): ")
    if acao in ["cima", "baixo", "esquerda", "direita"]:
        jogo.mover(acao)
    elif acao == "verificar":
        jogo.verificar_vizinhanca()
    elif acao == "atirar":
        direcao = input("Digite a direção para atirar (cima, baixo, esquerda, direita): ")
        if direcao in ["cima", "baixo", "esquerda", "direita"]:
            jogo.atirar(direcao)
        else:
            print("Direção inválida!")
    elif acao == "agente":
        agente.tomar_acao()
    else:
        print("Ação inválida!")
    jogo.mostrar() """


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
        self.historico = set()  # Histórico de posições visitadas

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
        self.historico.add(self.posicao_jogador)  # Adiciona a posição ao histórico
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
        if self.posicao_jogador == (0, 0) and (self.ouro_pegado or self.wumpus_morto):
            print("Você voltou para a posição inicial com o ouro ou após matar o Wumpus! Você venceu!")
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

        if 0 <= x < self.tamanho and 0 <= y < self.tamanho:
            if (x, y) == self.posicao_wumpus:
                print("Você matou o Wumpus!")
                self.wumpus_morto = True
                self.posicao_wumpus = None
                self.pontuacao += 100
            else:
                print("Você errou o tiro!")
                self.pontuacao -= 100
        else:
            print("Você errou o tiro!")
            self.pontuacao -= 100


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
                self.jogo.pontuacao += 100
                return
        print("Você errou o tiro!")
        self.jogo.pontuacao -= 100

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

        if 0 <= x < self.jogo.tamanho and 0 <= y < self.jogo.tamanho:
            if (x, y) == self.jogo.posicao_wumpus:
                return True
        return False

    def mover_em_segurança(self):
        adjacentes = self.jogo._checar_adjacentes(self.jogo.posicao_jogador)
        direcoes_seguras = []

        for direcao, pos in adjacentes.items():
            if pos not in self.jogo.historico and pos != self.jogo.posicao_wumpus and pos not in self.jogo.posicao_buracos:
                direcoes_seguras.append(direcao)

        if direcoes_seguras:
            direcao_escolhida = random.choice(direcoes_seguras)
            self.jogo.mover(direcao_escolhida)
        else:
            print("Não há direções seguras conhecidas, movendo aleatoriamente.")
            direcao_escolhida = random.choice(list(adjacentes.keys()))
            self.jogo.mover(direcao_escolhida)

    def mover_para_ouro(self):
        adjacentes = self.jogo._checar_adjacentes(self.jogo.posicao_jogador)
        for direcao, adj_pos in adjacentes.items():
            if adj_pos == self.jogo.posicao_ouro:
                self.jogo.mover(direcao)
                return


# Loop principal do jogo
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

jogo = WumpusMundo(tamanho=tamanhoI, num_buracos=num_buracosI)
agente = AgenteInteligente(jogo)

jogo.mostrar()
while not jogo.fim_jogo:
    acao = input("Digite uma ação (cima, baixo, esquerda, direita, verificar, atirar, agente): ")
    if acao in ["cima", "baixo", "esquerda", "direita"]:
        jogo.mover(acao)
    elif acao == "verificar":
        jogo.verificar_vizinhanca()
    elif acao == "atirar":
        direcao = input("Digite a direção para atirar (cima, baixo, esquerda, direita): ")
        if direcao in ["cima", "baixo", "esquerda", "direita"]:
            jogo.atirar(direcao)
        else:
            print("Direção inválida!")
    elif acao == "agente":
        agente.tomar_acao()
    else:
        print("Ação inválida!")
    jogo.mostrar()

