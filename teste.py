import random
import matplotlib.pyplot as plt
import wumpusAgenteV1 as agente_v1
import wumpusAgenteV2 as agente_v2
import wumpusAgenteV3 as agente_v3
from datetime import datetime

quantidade_execucoes = 20
buracos = [1/4]
tamanho_mapa = [4, 5, 10, 15, 20]

resultadosV1 = []
resultadosV2 = []

loc_elementos = []

# Obtendo a data e hora atuais para o nome do arquivo
data_hora_atual = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
nome_arquivo = f"registro-{data_hora_atual}.txt"

# Função para salvar os resultados no arquivo
def salvar_resultados(nome_arquivo, resultados, agente, pos_buracos, pos_wumpus, pos_ouro):
    with open(nome_arquivo, 'a') as arquivo:
        arquivo.write(f"Resultados do {agente}:\n")
        arquivo.write(f"Localizações - Buracos: {pos_buracos}, Wumpus: {pos_wumpus}, Ouro: {pos_ouro}\n")
        for resultado in resultados:
            arquivo.write(f"{resultado}\n")
        arquivo.write("\n")

# Executando agente_v1 e armazenando resultados
for tamanho in tamanho_mapa:
    for buraco in buracos:
        jogo = agente_v1.WumpusMundo(tamanho=tamanho, num_buracos=int((tamanho * tamanho) * buraco))
        jogo.resetar()

        loc_elementos.append((tamanho, buraco, jogo.posicao_buracos, jogo.posicao_wumpus, jogo.posicao_ouro))

        vitorias = 0
        wumpusMortos = 0
        ourosPegos = 0
        vitoriasWumpus = 0

        for i in range(quantidade_execucoes):
            jogo.resetar()
            agente = agente_v1.AgenteInteligente(jogo)
            while not jogo.fim_jogo:
                agente.tomar_acao()

            if jogo.ouro_pegado:
                ourosPegos += 1
            if jogo.wumpus_morto:
                wumpusMortos += 1
            if jogo.winner and jogo.wumpus_morto:
                vitoriasWumpus += 1
            if jogo.winner:
                vitorias += 1

            resultadosV1.append((i, tamanho, buraco, vitorias, vitoriasWumpus, wumpusMortos, ourosPegos, jogo.pontuacao))

        # Salvando os resultados do agente_v1 no arquivo
        salvar_resultados(nome_arquivo, resultadosV1, "Agente V1", jogo.posicao_buracos, jogo.posicao_wumpus_inicial, jogo.posicao_ouro)

# Executando agente_v2 e armazenando resultados
for tamanho, buraco, pos_buracos, pos_wumpus, pos_ouro in loc_elementos:
    jogo = agente_v2.WumpusMundo(tamanho=tamanho, num_buracos=int((tamanho * tamanho) * buraco))
    jogo.resetar()

    # Setando os valores iniciais
    jogo.posicao_buracos = pos_buracos
    jogo.posicao_wumpus = pos_wumpus
    jogo.posicao_ouro = pos_ouro

    vitorias = 0
    wumpusMortos = 0
    ourosPegos = 0
    vitoriasWumpus = 0

    for i in range(quantidade_execucoes):
        jogo.resetar()
        agente = agente_v2.AgenteInteligente(jogo)
        while not jogo.fim_jogo:
            agente.tomar_acao()

        if jogo.ouro_pegado:
            ourosPegos += 1
        if jogo.wumpus_morto:
            wumpusMortos += 1
        if jogo.winner and jogo.wumpus_morto:
            vitoriasWumpus += 1
        if jogo.winner:
            vitorias += 1

        resultadosV2.append((i, tamanho, buraco, vitorias, vitoriasWumpus, wumpusMortos, ourosPegos, jogo.pontuacao))

    # Salvando os resultados do agente_v2 no arquivo
    salvar_resultados(nome_arquivo, resultadosV2, "Agente V2", pos_buracos, pos_wumpus, pos_ouro)

# Executando agente_v3 e coletando dados de desempenho
for tamanho, buraco, pos_buracos, pos_wumpus, pos_ouro in loc_elementos:
    jogo = agente_v3.WumpusMundo(tamanho=tamanho, num_buracos=int((tamanho * tamanho) * buraco))
    jogo.reset()

    # Setando os valores iniciais
    jogo.posicao_buracos = pos_buracos
    jogo.posicao_wumpus = pos_wumpus
    jogo.posicao_ouro = pos_ouro

    agente = agente_v3.AlgoritmoGenetico(tamanho_populacao=50, taxa_mutacao=0.05, taxa_crossover=0.85, geracoes=1000, mundo=jogo)
    
    melhor_fitness_por_geracao, pior_fitness_por_geracao, media_fitness_por_geracao = agente.executar()

    #print("Melhor caminho encontrado pelo AG:")
    #print(agente.melhor_individuo['caminho'])
    #print("Score: ", agente.melhor_individuo['pontuacao'])
    
    agente.mundo.reset()
    for movimento in agente.melhor_individuo['caminho']:
        if jogo.fim_jogo:
            break
        jogo.mover(movimento)

    # Plotando os resultados do agente_v3 para a configuração atual do mapa
    geracoes = list(range(len(melhor_fitness_por_geracao)))

    plt.figure(figsize=(12, 6))

    plt.plot(geracoes, melhor_fitness_por_geracao, label='Melhor Fitness')
    plt.plot(geracoes, pior_fitness_por_geracao, label='Pior Fitness')
    plt.plot(geracoes, media_fitness_por_geracao, label='Média Fitness')

    plt.xlabel('Gerações')
    plt.ylabel('Fitness')
    plt.title(f'Desempenho do Algoritmo Genético - Tamanho: {tamanho}, Buracos/Tamanho: {buraco}')
    plt.legend()
    plt.grid(True)
    plt.show()

# Preparando os dados para plotagem
rodadas = list(range(quantidade_execucoes))

for tamanho in tamanho_mapa:
    for buraco in buracos:
        vitorias_v1 = [r[3] for r in resultadosV1 if r[1] == tamanho and r[2] == buraco]
        vitoriasWumpus_v1 = [r[4] for r in resultadosV1 if r[1] == tamanho and r[2] == buraco]
        wumpusMortos_v1 = [r[5] for r in resultadosV1 if r[1] == tamanho and r[2] == buraco]
        ourosPegos_v1 = [r[6] for r in resultadosV1 if r[1] == tamanho and r[2] == buraco]
        pontuacoes_v1 = [r[7] for r in resultadosV1 if r[1] == tamanho and r[2] == buraco]

        vitorias_v2 = [r[3] for r in resultadosV2 if r[1] == tamanho and r[2] == buraco]
        vitoriasWumpus_v2 = [r[4] for r in resultadosV2 if r[1] == tamanho and r[2] == buraco]
        wumpusMortos_v2 = [r[5] for r in resultadosV2 if r[1] == tamanho and r[2] == buraco]
        ourosPegos_v2 = [r[6] for r in resultadosV2 if r[1] == tamanho and r[2] == buraco]
        pontuacoes_v2 = [r[7] for r in resultadosV2 if r[1] == tamanho and r[2] == buraco]

        plt.figure(figsize=(12, 6))

        plt.plot(rodadas, vitorias_v1, label='Vitórias V1')
        plt.plot(rodadas, vitoriasWumpus_v1, label='Vitórias com Wumpus Morto V1')
        plt.plot(rodadas, wumpusMortos_v1, label='Wumpus Mortos V1')
        plt.plot(rodadas, ourosPegos_v1, label='Ouros Pegos V1')
        plt.plot(rodadas, pontuacoes_v1, label='Pontuação V1', linestyle='--', marker='o')
        
        plt.plot(rodadas, vitorias_v2, label='Vitórias V2')
        plt.plot(rodadas, vitoriasWumpus_v2, label='Vitórias com Wumpus Morto V2')
        plt.plot(rodadas, wumpusMortos_v2, label='Wumpus Mortos V2')
        plt.plot(rodadas, ourosPegos_v2, label='Ouros Pegos V2')
        plt.plot(rodadas, pontuacoes_v2, label='Pontuação V2', linestyle='--', marker='x')

        plt.xlabel('Rodadas')
        plt.ylabel('Contagem')
        plt.title(f'Evolução das Rodadas - Tamanho: {tamanho}, Buracos/Tamanho: {buraco}')
        plt.legend()
        plt.grid(True)
        plt.show()
