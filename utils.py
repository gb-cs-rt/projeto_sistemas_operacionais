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

def gerarDiagramaGantt(escalonador):
    with open('grafico.txt', 'w') as arquivo_grafico:
        arquivo_grafico.write(f'Diagrama de Gantt ({escalonador.tipo}):\n')
        arquivo_grafico.write('-' * (len(escalonador.historico_execucao) * 5) + '\n')
        arquivo_grafico.write('| ' + ' | '.join(escalonador.historico_execucao) + ' |\n')
        arquivo_grafico.write('-' * (len(escalonador.historico_execucao) * 5) + '\n')

        calculaTempoEspera(escalonador, arquivo_grafico)