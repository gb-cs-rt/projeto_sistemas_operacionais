from src.utils import printStatus, gerarDiagramaGantt, gerarGraficos, criaDiretorioSaida
import time

class EscalonadorPrioridade:

    def __init__(self):
        self.tipo = 'Prioridade'
        self.cpu = None
        self.fila_espera = []
        self.tempo_atual = 0
        self.tempo_espera = 0
        self.tempo_espera_medio = 0
        self.fila_processos = []
        self.todos_processos = []
        self.historico_execucao = []
        self.processo_em_io = None
        self.arq = None

    def verificaPrioridade(self):
        if len(self.fila_espera) == 1:
            maior_prioridade = self.fila_espera[0].prioridade
        else:
            maior_prioridade = min(processo.prioridade for processo in self.fila_espera if processo != self.processo_em_io)

        for processo in self.fila_espera[:]:
            if processo.prioridade == maior_prioridade:
                self.cpu = processo
                self.cpu.tempo_espera_total += self.tempo_atual - self.cpu.tempo_entrada_fila
                self.fila_espera.remove(processo)
                break
        self.processo_em_io = None

    def adicionarProcesso(self, processo):
        self.fila_processos.append(processo)
        self.todos_processos.append(processo)

    def escalonarProcesso(self):
        if self.cpu is None and self.fila_espera:
            self.verificaPrioridade()

    def chegadaProcesso(self):
        for processo in self.fila_processos[:]:
            if processo.chegada == self.tempo_atual:
                self.arq.write(f'#[evento] CHEGADA <{processo.pid}>\n')
                processo.tempo_entrada_fila = self.tempo_atual
                self.fila_espera.append(processo)

    def incrementarTempoDecorrido(self):
        if self.cpu:
            self.cpu.tempo_decorrido += 1

    def decrementarDuracao(self):
        if self.cpu:
            self.cpu.duracao -= 1

    def verificaIO(self):
        if self.cpu is not None:
            if self.cpu.tempo_decorrido in self.cpu.io:
                self.arq.write(f'#[evento] OPERACAO I/O <{self.cpu.pid}>\n')
                if self.cpu.duracao > 0:
                    self.cpu.tempo_entrada_fila = self.tempo_atual
                    self.fila_espera.append(self.cpu)
                    self.processo_em_io = self.cpu
                self.cpu = None
                self.escalonarProcesso()

    def encerrarProcesso(self):
        if self.cpu is not None and self.cpu.duracao == 0:
            self.arq.write(f'#[evento] ENCERRANDO <{self.cpu.pid}>\n')
            self.fila_processos.remove(self.cpu)
            self.cpu = None

    def executar(self):
        criaDiretorioSaida()
        self.arq = open('output/saida.txt', 'w')
        self.arq.write('***********************************\n')
        self.arq.write('***** ESCALONADOR PRIORIDADE *****\n')
        self.arq.write('-----------------------------------\n')
        self.arq.write('------- INICIANDO SIMULACAO -------\n')
        self.arq.write('-----------------------------------\n')
        self.arq.write(f'************ TEMPO {self.tempo_atual} **************\n')
        self.arq.write('FILA: Nao ha processos na fila\n')

        self.chegadaProcesso()
        self.escalonarProcesso()
        self.arq.write(f'CPU: {self.cpu.pid} ({self.cpu.duracao})\n')

        while self.cpu or self.fila_espera or self.fila_processos:
            self.tempo_atual += 1
            self.arq.write(f'************ TEMPO {self.tempo_atual} **************\n')
            self.historico_execucao.append(self.cpu.pid if self.cpu else 'LIVRE')
            self.incrementarTempoDecorrido()
            self.decrementarDuracao()
            self.chegadaProcesso()
            self.encerrarProcesso()
            self.verificaIO()
            self.escalonarProcesso()
            printStatus(self)
            gerarGraficos(self)
            time.sleep(0.5)

        self.arq.write('-----------------------------------\n')
        self.arq.write('------- SIMULACAO FINALIZADA ------\n')
        self.arq.write('-----------------------------------\n')

        gerarDiagramaGantt(self)
        gerarGraficos(self)
        self.arq.close()

        print('\nSimulação por prioridade concluída. Resultados no arquivo "saida.txt". Gráficos no arquivo "grafico.txt".\n')