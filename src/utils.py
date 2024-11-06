import matplotlib.pyplot as plt
import os, time

class Processo:

    def __init__(self, pid, chegada, duracao, io=[]):
        self.pid = pid
        self.chegada = chegada
        self.duracao = duracao
        self.io = io
        self.tempo_decorrido = 0
        self.tempo_entrada_fila = chegada
        self.tempo_espera_total = 0

class ProcessoPrioridade:

    def __init__(self, pid, chegada, duracao, prioridade, io=[]):
        self.pid = pid
        self.chegada = chegada
        self.duracao = duracao
        self.prioridade = prioridade
        self.io = io
        self.tempo_decorrido = 0
        self.tempo_entrada_fila = chegada
        self.tempo_espera_total = 0

def printStatus(escalonador):
    if not escalonador.fila_espera and not escalonador.cpu and not escalonador.fila_processos:
        escalonador.arq.write('FILA: Nao ha processos na fila\n')
        escalonador.arq.write('ACABARAM OS PROCESSOS!!!\n')
    elif not escalonador.fila_espera:
        escalonador.arq.write('FILA: Nao ha processos na fila\n')
        escalonador.arq.write(f'CPU: {escalonador.cpu.pid if escalonador.cpu else "LIVRE"} ({escalonador.cpu.duracao if escalonador.cpu else "-"})\n')
    else:
        escalonador.arq.write('FILA: ' + ' '.join(f'{processo.pid} ({processo.duracao})' for processo in escalonador.fila_espera) + '\n')
        escalonador.arq.write(f'CPU: {escalonador.cpu.pid if escalonador.cpu else "LIVRE"} ({escalonador.cpu.duracao if escalonador.cpu else "-"})\n')

def calculaTempoEspera(escalonador, arquivo_saida):
        escalonador.arq.write('***********************************\n')
        escalonador.arq.write('TEMPO DE ESPERA DE CADA PROCESSO:\n')

        for processo in escalonador.todos_processos:
            tempo_espera = processo.tempo_espera_total
            escalonador.arq.write(f'{processo.pid}: {tempo_espera}\n')
            if arquivo_saida:
                arquivo_saida.write(f'{processo.pid}: {tempo_espera}\n')

        total_tempo_espera = sum(processo.tempo_espera_total for processo in escalonador.todos_processos)
        if len(escalonador.todos_processos) > 0:
            media_tempo_espera = total_tempo_espera / len(escalonador.todos_processos)
        else:
            media_tempo_espera = 0
        escalonador.arq.write('***********************************\n')
        escalonador.arq.write(f'TEMPO TOTAL DE ESPERA: {total_tempo_espera}\n')
        escalonador.arq.write(f'MEDIA DE TEMPO DE ESPERA: {media_tempo_espera:.2f}\n')
        escalonador.arq.write('***********************************\n')

        if arquivo_saida:
            arquivo_saida.write('***********************************\n')
            arquivo_saida.write(f'TEMPO TOTAL DE ESPERA: {total_tempo_espera}\n')
            arquivo_saida.write(f'MEDIA DE TEMPO DE ESPERA: {media_tempo_espera:.2f}\n')
            arquivo_saida.write('***********************************\n')

def gerarDiagramaGantt(escalonador, quantum=None):
    with open('output/grafico.txt', 'w') as arquivo_grafico:
        arquivo_grafico.write(f'Diagrama de Gantt ({escalonador.tipo}):\n')
        if quantum:
            arquivo_grafico.write(f'Quantum: {quantum}\n')
        arquivo_grafico.write('-' * (len(escalonador.historico_execucao) * 5) + '\n')
        arquivo_grafico.write('| ' + ' | '.join(escalonador.historico_execucao) + ' |\n')
        arquivo_grafico.write('-' * (len(escalonador.historico_execucao) * 5) + '\n')

        calculaTempoEspera(escalonador, arquivo_grafico)

def calculaTempoEsperaGrafico(escalonador):
    tempos_espera = [processo.tempo_espera_total for processo in escalonador.todos_processos]
    
    plt.figure(figsize=(10, 6))
    plt.bar([p.pid for p in escalonador.todos_processos], tempos_espera, color='skyblue')
    plt.xlabel("Processo")
    plt.ylabel("Tempo de Espera")
    plt.title("Tempo de Espera por Processo")
    plt.savefig('output/tempo_espera_por_processo.png')
    plt.close()

# Create a persistent figure and axes
fig, ax = plt.subplots()

def gerarGraficos(escalonador, quantum=None, close=False):
    # Ativar o modo interativo para atualização em tempo real
    plt.ion()
    
    # Clear the current axes to update the graph in the same window
    ax.clear()
    
    processos = set(escalonador.historico_execucao)  # Conjunto único de processos
    y = 1  # Posição inicial no eixo Y
    
    # Obter o tempo máximo para definir o range dos ticks do eixo X
    max_tempo = len(escalonador.historico_execucao)

    # Plotar os blocos de execução para cada processo no diagrama de Gantt
    for pid in processos:
        # Encontrar as posições de início e duração do processo
        indices = [i for i, p in enumerate(escalonador.historico_execucao) if p == pid]
        
        # Identificar os blocos consecutivos de execução
        blocos = []
        inicio = indices[0]
        duracao = 1
        for i in range(1, len(indices)):
            if indices[i] == indices[i - 1] + 1:
                duracao += 1
            else:
                blocos.append((inicio, duracao))
                inicio = indices[i]
                duracao = 1
        blocos.append((inicio, duracao))  # Adicionar o último bloco
        
        # Desenhar cada bloco no diagrama de Gantt
        for inicio, duracao in blocos:
            ax.broken_barh([(inicio, duracao)], (y, 0.8), facecolors=('tab:blue'))
            ax.text(inicio + duracao / 2, y + 0.4, f"{pid}", ha='center', va='center', color='white')
        
        y += 1  # Incrementar a posição Y para o próximo processo
    
    # Configurar os ticks do eixo X para variar de 1 em 1
    ax.set_xticks(range(0, max_tempo + 1))
    ax.set_xlim(0, max_tempo)

    # Definir as etiquetas do eixo Y com base nos pids ordenados
    ax.set_yticks([i + 0.4 for i in range(1, y)])
    ax.set_yticklabels(list(processos))
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Processos")
    if quantum:
        ax.set_title(f"Diagrama de Gantt ({escalonador.tipo}) - Quantum: {quantum}")
    else:
        ax.set_title(f"Diagrama de Gantt ({escalonador.tipo})")
    
    # Mostrar o gráfico atualizado e garantir que o buffer seja limpo
    plt.draw()
    plt.pause(0.5)  # Tempo de atualização em segundos
    plt.ioff()
    plt.savefig('output/diagrama_gantt.png')

    calculaTempoEsperaGrafico(escalonador)

def criaDiretorioSaida():
    if not os.path.exists('output'):
        os.makedirs('output')