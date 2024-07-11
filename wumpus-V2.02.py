import random
import datetime
import matplotlib.pyplot as plt

import math

from heapq import heappop, heappush

class WumpusMundo:
    def __init__(self, tamanho=10, num_buracos=9):
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
        self.historico = {self.posicao_jogador}
        self.jogo_vencido = False

        # Inicialização das posições
        self.posicao_wumpus = self._gerar_posicao_aleatoria()
        self.posicao_ouro = self._gerar_posicao_aleatoria()
        self.posicao_buracos = [self._gerar_posicao_aleatoria() for _ in range(num_buracos)]

    def _gerar_posicao_aleatoria(self):
        while True:
            posicao = (random.randint(0, self.tamanho - 1), random.randint(0, self.tamanho - 1))
            if posicao != (0, 0) and posicao not in self.posicao_buracos and posicao != self.posicao_ouro and posicao != self.posicao_wumpus:
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
        percepcoes = {"cheiro horrivel": False, "brilho radiante": False, "brisa suave": False}
        adjacentes = self._checar_adjacentes(posicao)
        for adj_pos in adjacentes.values():
            if adj_pos == self.posicao_wumpus:
                percepcoes["cheiro horrivel"] = True
            if adj_pos in self.posicao_buracos:
                percepcoes["brisa suave"] = True

        # Verifica se o jogador está na posição do ouro
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
        elif direcao == "parado":
            self.pontuacao +=1
        else:
            print("Movimento inválido!")
            self.pontuacao -= 5
            return

        self.historico.add(self.posicao_jogador)
        percepcoes = self._checar_vizinhanca(self.posicao_jogador)
        self._exibir_percepcoes(percepcoes)
        
        if self.posicao_jogador == self.posicao_wumpus or self.posicao_jogador in self.posicao_buracos:
            print("Você morreu!")
            self.pontuacao -= 1000
            self.fim_jogo = True
        elif self.posicao_jogador == self.posicao_ouro:
            print("Você encontrou o ouro! Pegue-o e volte para a posição inicial para vencer.")
            self.ouro_pegado = True
            self.posicao_ouro = None
            self.pontuacao += 1000
        
        if self.posicao_jogador == (0, 0) and self.ouro_pegado:
            print("Você voltou para a posição inicial com o ouro! Você venceu!")
            self.pontuacao += 1000
            self.fim_jogo = True
            self.jogo_vencido = True

    def _exibir_percepcoes(self, percepcoes):
        percepcao_msg = ""
        if percepcoes["cheiro horrivel"]:
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
        return percepcoes

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
            self.pontuacao -= 100
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
                self.pontuacao += 1000
                return

        print("Você errou o tiro!")
        self.pontuacao -= 1000

    def resetar(self):
        self.posicao_jogador = (0, 0)
        self.fim_jogo = False
        self.pontuacao = 0
        self.flecha_disponivel = True
        self.ouro_pegado = False
        self.wumpus_morto = False
        self.historico = {self.posicao_jogador}

    def gerar_mapa(self):
        mapa = [['-' for _ in range(self.tamanho)] for _ in range(self.tamanho)]

        # Marcar posição do jogador
        mapa[self.posicao_jogador[0]][self.posicao_jogador[1]] = 'J'

        # Marcar posição do Wumpus
        if self.posicao_wumpus:
            mapa[self.posicao_wumpus[0]][self.posicao_wumpus[1]] = 'W'

        # Marcar posição do ouro
        if self.posicao_ouro:
            mapa[self.posicao_ouro[0]][self.posicao_ouro[1]] = 'O'

        # Marcar posição dos buracos
        for buraco in self.posicao_buracos:
            mapa[buraco[0]][buraco[1]] = 'B'

        return mapa

class AgenteInteligente:
    def __init__(self, mundo):
        self.mundo = mundo
        self.tamanho = self.mundo.tamanho
        #posicao do agente
        self.posicao = (0, 0)
        self.ouro_pegado = False
        self.mapa = set()
        self.casa_segura = set()
        self.casa_segura_nao_visitada = set()
        self.casa_suspeita = set()
        self.casa_perigo = False
        self.casa_anterior = (0, 0)
        self.matar = 0
        self.casa_suspeita_peso_1 = set()
        self.casa_suspeita_peso_2 = set()
        self.casa_suspeita_peso_3 = set()
        self.casa_suspeita_peso_4 = set()

        self.casa_segura.add(self.posicao)
        self.adicionar_casa_suspeita()
    def tomar_acao(self):
        self.mundo.mostrar()
        while not self.mundo.fim_jogo:
            if self.matar > 2:
                #agente vai tentar matar o wumpus
                pass
            if not self.mundo.ouro_pegado:
                direcao = self.direcao_segura()
                if not direcao:  # Se não há direção segura, pode indicar um loop
                    print("Nenhuma direção segura encontrada. Verifique as listas de casas seguras e suspeitas.")
                    break
                for dir in direcao:
                    self.mover(dir)
                    #self.adicionar_casa_segura_nao_visitada(self.posicao)
                    self.adicionar_casa_segura(self.posicao)
                    self.mundo.mostrar()
            else:
                direcao = self.encontra_direcao(self.posicao, (0, 0))
                print("Ouro encontrado. Agente retornando ao ponto inicial.")
                for dir in direcao:
                    print("Proxima Casa:", dir)
                    print("Posição:", self.posicao)
                    print("Direção Traduzida:", self.traduz_direcao(dir))
                    self.mover(self.traduz_direcao(dir))
                    #self.adicionar_casa_segura_nao_visitada(self.posicao)
                    self.mundo.mostrar()
            self.casa_segura_nao_visitada = self.casa_segura_nao_visitada.difference(self.casa_segura)
            self.casa_segura_nao_visitada.discard(self.posicao)
        
    def mover(self, direcao):
        self.mundo.mover(direcao)
        self.posicao = self.mundo.posicao_jogador
    def atirar(self, direcao):
        self.mundo.atirar(direcao)
    def cacar_wumpus(self):
        direcoes = ["cima", "baixo", "esquerda", "direita"]
        #busca a casa com maior peso para atirar
        adj = self.adjacentes(self.posicao[0], self.posicao[1])

        for casa in adj:
            #procura adj no conjunto de casas suspeitas_peso_4:
            if casa in self.casa_suspeita_peso_4:
                return self.traduz_direcao(casa)
            #procura adj no conjunto de casas suspeitas_peso_3:
            if casa in self.casa_suspeita_peso_3:
                return self.traduz_direcao(casa)
            #procura adj no conjunto de casas suspeitas_peso_2:
            if casa in self.casa_suspeita_peso_2:
                return self.traduz_direcao(casa)
            #procura adj no conjunto de casas suspeitas_peso_1:
            if casa in self.casa_suspeita_peso_1:
                return self.traduz_direcao(casa)
        
        #retorna a direcao da casa
        return random.choice(direcoes)

    def direcao_segura(self):
        direcoes = ["cima", "baixo", "esquerda", "direita"]
        percepcoes = self.mundo.verificar_vizinhanca()
        self.casa_perigo = False
        if percepcoes == {"cheiro horrivel": False, "brisa suave": False, "brilho radiante": False}:
            self.adicionar_casa_segura_nao_visitada(self.posicao)
            casa_mais_proxima = self.encontra_casa_segura_nao_visitada_mais_proxima()
            if casa_mais_proxima is None:
                casa_mais_proxima = self.encontra_casa_suspeita_mais_proxima()
            caminho = self.encontra_direcao(self.posicao, casa_mais_proxima)
            return [self.traduz_direcao(cam) for cam in caminho if self.traduz_direcao(cam) is not None]

        if percepcoes["brisa suave"]:
            self.casa_perigo = True
            casa_mais_proxima = self.encontra_casa_segura_nao_visitada_mais_proxima()
            if casa_mais_proxima is None:
                casa_mais_proxima = self.encontra_casa_suspeita_mais_proxima()
            caminho = self.encontra_direcao(self.posicao, casa_mais_proxima)
            return [self.traduz_direcao(cam) for cam in caminho if self.traduz_direcao(cam) is not None]
        
        if percepcoes["cheiro horrivel"]:
            self.matar += 1
            if((self.matar > 1) and (self.mundo.flecha_disponivel == True)):
                print("Caçando o wumpus")
                self.atirar(self.cacar_wumpus())
            if(self.posicao == (0,0) and (self.mundo.flecha_disponivel == True)):
                print("Caçando o wumpus")
                self.atirar(self.cacar_wumpus())
            casa_mais_proxima = self.encontra_casa_segura_nao_visitada_mais_proxima()
            if casa_mais_proxima is None:
                casa_mais_proxima = self.encontra_casa_suspeita_mais_proxima()
            caminho = self.encontra_direcao(self.posicao, casa_mais_proxima)
            return [self.traduz_direcao(cam) for cam in caminho if self.traduz_direcao(cam) is not None]
        
        return []
     
    def adjacentes(self, X, Y):
        adjacentes = []
        tamanhoMundo = self.tamanho
        #print("Adjacentes de Posicao X e Y : ", X , Y)
        if ((X - 1) >= 0):
            adjacentes.append((X - 1, Y))
        if X + 1 < tamanhoMundo:
            adjacentes.append((X + 1, Y))
        if Y - 1 >= 0:
            adjacentes.append((X, Y - 1))
        if Y + 1 < tamanhoMundo:
            adjacentes.append((X, Y + 1))

        return adjacentes        
    def adicionar_casa_segura_nao_visitada(self, posic):
        self.casa_segura.add(posic)
        self.casa_segura_nao_visitada.discard(posic)
        adjacentes = self.adjacentes(posic[0], posic[1])
        casas_para_retirar = []
        
        for adj_pos in adjacentes:
            if adj_pos not in self.casa_segura:
                self.casa_segura_nao_visitada.add(adj_pos)
            else:
                print ("Casa suspeita retirada: ", adj_pos)
                self.casa_segura_nao_visitada.discard(adj_pos)
            
            # Verifica se a casa adjacente está na lista de casas suspeitas
            if adj_pos in self.casa_suspeita:
                casas_para_retirar.append(adj_pos)
        
        for casa in casas_para_retirar:    
            self.retirar_casa_suspeita(casa)
            print("Casa retirada das casas suspeitas: ", casa)
        
        self.casa_segura_nao_visitada.discard(self.posicao)


            
    def adicionar_casa_segura(self, posicao):
        
        #print("casa segura nao visitada : ", self.casa_segura_nao_visitada)
        #print("lista de casas seguras : ", self.casa_segura)
        #print("casa segura :", posicao)
        self.casa_segura.add(posicao)
        print("casa retirada das casas não visitadas: ", self.casa_segura_nao_visitada.discard(posicao))
        #retirar a casa da lista de não visitadas
        #print("casa retirada das casas não visitadas: ", self.casa_segura_nao_visitada)
        #verifica se a casa nao visitada contém a casa segura
        

    def adicionar_casa_suspeita(self):
        #print("Casa Suspeita de Posicao X e Y : " , posicao[0], posicao[1])
        #print("self :", self)
        #adiciona todas as casas como suspeitas
        #print("todas as casa menos a (0,0) são suspeitas")
        for x in range(self.tamanho):
            for y in range(self.tamanho):
                self.casa_suspeita.add((x,y))

        #retira a casa (0,0) das suspeitas
        self.casa_suspeita.discard((0,0))
    
    def retirar_casa_suspeita(self, posicao):
        self.casa_suspeita.discard(posicao)

    def adicionar_casa_buraco(self):
        pass

    def adicionar_casa_wumpus(self):
        pass

    def adicionar_casa_anterior(self, posicao):
        self.casa_anterior(posicao)

    def encontra_casa_segura_nao_visitada_mais_proxima(self):
        posicao = self.posicao
        casa_mais_proxima = None
        distancia = float('inf')
        self.casa_segura.add(posicao)
        self.casa_segura_nao_visitada.discard(posicao)
        
        print("casa_segura_nao_visitada (encontra_casa_segura_nao_visitada): ", self.casa_segura_nao_visitada)
        
        for casa in self.casa_segura_nao_visitada:
            aux = self.heuristica(casa, posicao)
            if aux < distancia:
                distancia = aux
                casa_mais_proxima = casa

        return casa_mais_proxima  # Retorna None se não encontrar a casa
    
    def encontra_casa_suspeita_mais_proxima(self):
        posicao = self.posicao
        casa_mais_proxima = None
        distancia = float('inf')
        self.casa_segura.add(posicao)
        self.casa_suspeita.discard(posicao)

        print("posicoes_potencialmente_perigosas (encontra_casa_suspeita): ", self.casa_suspeita)
        
        casas_nao_pesadas = self.casa_suspeita - self.casa_suspeita_peso_1 - self.casa_suspeita_peso_2 - self.casa_suspeita_peso_3 - self.casa_suspeita_peso_4

        for casa in self.casa_suspeita_peso_4:
            casas_nao_pesadas.discard(casa)

        for casa in self.casa_suspeita_peso_3:
            casas_nao_pesadas.discard(casa)
        
        for casa in self.casa_suspeita_peso_2:
            casas_nao_pesadas.discard(casa)

        for casa in self.casa_suspeita_peso_1:
            casas_nao_pesadas.discard(casa)
        
        print("casas_nao_pesadas (encontra_casa_suspeita): ", casas_nao_pesadas)
        # Se houver casas suspeitas fora dos conjuntos de peso, seleciona a mais próxima
        if casas_nao_pesadas:
            for casa in casas_nao_pesadas:
                aux = self.heuristica(casa, posicao)
                if aux < distancia:
                    distancia = aux
                    casa_mais_proxima = casa
        else:
            # Se não houver casas fora dos conjuntos de peso, busca a mais próxima nos conjuntos de peso, começando pelo peso 1
            for casa in self.casa_suspeita_peso_1:
                aux = self.heuristica(casa, posicao)
                if aux < distancia:
                    distancia = aux
                    casa_mais_proxima = casa
            
            if casa_mais_proxima is None:
                for casa in self.casa_suspeita_peso_2:
                    aux = self.heuristica(casa, posicao)
                    if aux < distancia:
                        distancia = aux
                        casa_mais_proxima = casa

            if casa_mais_proxima is None:
                for casa in self.casa_suspeita_peso_3:
                    aux = self.heuristica(casa, posicao)
                    if aux < distancia:
                        distancia = aux
                        casa_mais_proxima = casa

            if casa_mais_proxima is None:
                for casa in self.casa_suspeita_peso_4:
                    aux = self.heuristica(casa, posicao)
                    if aux < distancia:
                        distancia = aux
                        casa_mais_proxima = casa

        return casa_mais_proxima  # Retorna None se não encontrar a casa

    
    def adiciona_peso_casa_suspeita(self, posicao):
        if posicao in self.casa_suspeita_peso_1:
            self.casa_suspeita_peso_1.remove(posicao)
            self.casa_suspeita_peso_2.add(posicao)
        elif posicao in self.casa_suspeita_peso_2:
            self.casa_suspeita_peso_2.remove(posicao)
            self.casa_suspeita_peso_3.add(posicao)
        elif posicao in self.casa_suspeita_peso_3:
            self.casa_suspeita_peso_3.remove(posicao)
            self.casa_suspeita_peso_4.add(posicao)
        elif posicao in self.casa_suspeita_peso_4:
            # A casa já está no maior peso, não faz nada
            pass
        else:
            # Se a casa não está em nenhum conjunto, adiciona no conjunto de peso 1
            self.casa_suspeita_peso_1.add(posicao)


    
    def traduz_direcao(self, posicao_objetivo):
        #print("posicao_objetivo : ", posicao_objetivo)
        linha_objetivo, coluna_objetivo = posicao_objetivo
        Linha_posicao, Coluna_posicao = self.posicao

        linha_objetivo = int(linha_objetivo)
        coluna_objetivo = int(coluna_objetivo)

        Linha_posicao = int(Linha_posicao)
        Coluna_posicao = int(Coluna_posicao)

        if ((linha_objetivo > Linha_posicao) and (coluna_objetivo == Coluna_posicao)):
            return 'baixo'
        if ((linha_objetivo < Linha_posicao) and (coluna_objetivo == Coluna_posicao)):
            return 'cima'
        if ((coluna_objetivo > Coluna_posicao) and (linha_objetivo == Linha_posicao)):
            return 'direita'
        if ((coluna_objetivo < Coluna_posicao) and (linha_objetivo == Linha_posicao)):
            return 'esquerda'

    def heuristica(self,a, b):
        #print("Posicao a e b : " , a, b)
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    def encontra_direcao(self, posicao_atual, posicao_objetivo): # algoritmo  A* (A estrela) ou Dijkstra
        #retira a posição objetivo se for para o mesmo lugar
        #if posicao_objetivo == posicao_atual:
        #    self.casa_segura_nao_visitada.remove(posicao_objetivo)
        
        #procura o menos caminho pelas casas usando as casa_segura
        #print("casa_segura (encontra_direcao): ", self.casa_segura)
        #print("casa_segura_nao_visitada (encontra_direcao): ", self.casa_segura_nao_visitada)
        self.casa_segura.add(posicao_atual)
        self.casa_segura_nao_visitada.discard(posicao_atual)
        self.casa_segura.add(posicao_objetivo)
        self.casa_segura_nao_visitada.discard(posicao_objetivo)

        
        #print("casa_segura (encontra_direcao): ", self.casa_segura)
        #print("casa_segura_nao_visitada (encontra_direcao): ", self.casa_segura_nao_visitada)

        matriz = self.gerar_matriz(self.tamanho, 0)
        #print("matriz : ", matriz)
        linhas, colunas = len(matriz), len(matriz[0])

        #conjunto_permitido = []
        #for casa in self.casa_segura:
        #    conjunto_permitido.append(casa)
        conjunto_permitido =  set()
        conjunto_permitido = self.casa_segura

        #print("conjunto_permitido : ", conjunto_permitido)
        
        #print("posicao atual : ", posicao_atual)
        #print("posicao objetivo : ", posicao_objetivo)

        conjunto_aberto = []
        heappush(conjunto_aberto, (0 + self.heuristica(posicao_atual, posicao_objetivo), 0, posicao_atual))
        veio_de = {}
        g_score = {casa: float('inf') for casa in conjunto_permitido}
        g_score[posicao_atual] = 0
        f_score = {casa: float('inf') for casa in conjunto_permitido}
        f_score[posicao_atual] = self.heuristica(posicao_atual, posicao_objetivo)
        
        while conjunto_aberto:
            _, g_atual, atual = heappop(conjunto_aberto)
            
            if atual == posicao_objetivo:
                caminho = []
                while atual in veio_de:
                    caminho.append(atual)
                    atual = veio_de[atual]
                #caminho.append(posicao_atual)
                self.casa_segura_nao_visitada.add(posicao_objetivo)
                self.casa_segura.discard(posicao_objetivo)
                cam = caminho[::-1]
                print("Caminho encontrado: ", cam)
                
                return caminho[::-1]
                
                
            #print("caminho (encontra_direcao): ", caminho)
            
            for direcao in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                vizinho = (atual[0] + direcao[0], atual[1] + direcao[1])
                if 0 <= vizinho[0] < linhas and 0 <= vizinho[1] < colunas and vizinho in conjunto_permitido:
                    g_score_tentativo = g_score[atual] + 1
                    if g_score_tentativo < g_score[vizinho]:
                        veio_de[vizinho] = atual
                        g_score[vizinho] = g_score_tentativo
                        f_score[vizinho] = g_score_tentativo + self.heuristica(vizinho, posicao_objetivo)
                        heappush(conjunto_aberto, (f_score[vizinho], g_score_tentativo, vizinho))
        print("Erro na busca do caminho (a estrela). Retorna objetivo : ", posicao_objetivo)
        #return None
        objetivo = []
        objetivo.append(posicao_objetivo)
        self.casa_segura_nao_visitada.add(posicao_objetivo)
        self.casa_segura.discard(posicao_objetivo)
        return objetivo

    def gerar_matriz(self, tamanho, valor_inicial=0):
        return [[valor_inicial for _ in range(tamanho)] for _ in range(tamanho)]
 

# Função para salvar o registro da partida
def salvar_registro(jogo, caminho_arquivo="registro-V2"):
    data_atual = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    caminho_arquivo = f"{caminho_arquivo}_{data_atual}.txt"
    
    with open(caminho_arquivo, "w") as file:
        file.write(f"Tamanho do mapa: {jogo.tamanho}\n")
        file.write(f"Posicao do Wumpus: {jogo.posicao_wumpus}\n")
        file.write(f"Posicao do Ouro: {jogo.posicao_ouro}\n")
        file.write(f"Posicoes dos Buracos: {jogo.posicao_buracos}\n")
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

            
        
        resultados.append((jogo.pontuacao))
        #salvar_registro(jogo)
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
    vitorias = sum(1 for resultado in resultados if resultado >= -1000)
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

