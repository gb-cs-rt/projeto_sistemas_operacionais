class Processo:

    def __init__(self, pid, chegada, duracao, io=[]):
        self.pid = pid
        self.chegada = chegada
        self.duracao = duracao
        self.io = io
        self.tempo_decorrido = 0
        self.tempo_entrada_fila = chegada
        self.tempo_espera_total = 0

class Escalonador:

    def __init__(self, quantum):
        self.quantum = quantum
        self.cpu = None
        self.fila_espera = []
        self.tempo_atual = 0
        self.tempo_espera = 0
        self.tempo_espera_medio = 0
        self.fila_processos = []
        self.quantum_atual = 0

    def adicionar_Processo(self, processo):
        if processo.chegada == 0:
            self.cpu = processo
        else:
            self.fila_processos.append(processo)

    def escalonar_Processo(self):
        if self.cpu is None and self.fila_espera:
            if self.fila_espera:
                self.cpu = self.fila_espera.pop(0)
                self.cpu.tempo_espera_total += self.tempo_atual - self.cpu.tempo_entrada_fila
                self.quantum_atual = 0
            else:
                return None

    def chegada_Processo(self):
        for processo in self.fila_processos:
            if processo.chegada == self.tempo_atual:
                print(f'#[evento] CHEGADA <{processo.pid}>')
                processo.tempo_entrada_fila = self.tempo_atual
                self.fila_espera.append(processo)

    def incrementar_Tempo_Decorrido(self):
        self.cpu.tempo_decorrido += 1

    def decrementar_Duracao(self):
        self.cpu.duracao -= 1

    def verifica_IO(self):
        if self.cpu is not None:
            if self.cpu.tempo_decorrido in self.cpu.io:
                print(f'#[evento] OPERACAO I/O <{self.cpu.pid}>')
                self.cpu.tempo_entrada_fila = self.tempo_atual
                self.fila_espera.append(self.cpu)
                self.cpu = None

    def encerrar_Processo(self):
        if self.cpu is not None:
            if self.cpu.duracao == 0:
                print(f'#[evento] ENCERRANDO <{self.cpu.pid}>')
                self.cpu = None

    def verifica_Quantum(self):
        if self.cpu is not None:
            if self.quantum_atual == self.quantum:
                print(f'#[evento] FIM QUANTUM <{self.cpu.pid}>')
                self.cpu.tempo_entrada_fila = self.tempo_atual
                self.fila_espera.append(self.cpu)
                self.cpu = None
                self.quantum_atual = 0

    def calcula_Tempo_Espera_(self):
        total_tempo_espera = sum(processo.tempo_espera_total for processo in self.fila_processos)
        media_tempo_espera = total_tempo_espera / len(self.fila_processos)
        print('***********************************')
        print(f'TEMPO TOTAL DE ESPERA: {total_tempo_espera}')
        print(f'MEDIA DE TEMPO DE ESPERA: {media_tempo_espera:.2f}')
        print('***********************************')

    def print_Status(self):
        if not self.fila_espera and not self.cpu:
            print('FILA: Nao ha processos na fila')
            print('ACABARAM OS PROCESSOS!!!')
        elif not self.fila_espera:
            print('FILA: Nao ha processos na fila')
            print(f'CPU: {self.cpu.pid} ({self.cpu.duracao})')
        else:
            print('FILA:', ' '.join(f'{processo.pid} ({processo.duracao})' for processo in self.fila_espera))
            print(f'CPU: {self.cpu.pid if self.cpu else "LIVRE"} ({self.cpu.duracao if self.cpu else "-"})')

    def executar(self):
        print('***********************************')
        print('***** ESCALONADOR ROUND ROBIN *****')
        print('-----------------------------------')
        print('------- INICIANDO SIMULACAO -------')
        print('-----------------------------------')
        print(f'************ TEMPO {self.tempo_atual} **************')
        print('FILA: Nao ha processos na fila')
        print(f'CPU: {self.cpu.pid} ({self.cpu.duracao})')
        self.chegada_Processo()
        self.escalonar_Processo()
        while self.cpu or self.fila_espera:
            self.tempo_atual += 1
            self.quantum_atual += 1
            print(f'************ TEMPO {self.tempo_atual} **************')
            self.incrementar_Tempo_Decorrido()
            self.decrementar_Duracao()
            self.verifica_Quantum()
            self.verifica_IO()
            self.encerrar_Processo()
            self.chegada_Processo()
            self.escalonar_Processo()
            self.print_Status()
        print('-----------------------------------')
        print('--------- FIM DA SIMULACAO ---------')
        print('-----------------------------------')
        self.calcula_Tempo_Espera_()

def main():
    escalonador = Escalonador(4)
    with open('entrada.txt', 'r') as arquivo:
        for linha in arquivo:
            partes = linha.split()
            pid = partes[0]
            chegada = int(partes[1])
            duracao = int(partes[2])
            io = list(map(int, partes[3].split(','))) if len(partes) > 3 else []
            processo = Processo(pid, chegada, duracao, io)
            escalonador.adicionar_Processo(processo)
    escalonador.executar()
main()

