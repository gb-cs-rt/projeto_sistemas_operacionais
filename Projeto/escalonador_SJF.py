arq = open('saida.txt', 'w')
class Processo:

    def __init__(self, pid, chegada, duracao, io=[]):
        self.pid = pid
        self.chegada = chegada
        self.duracao = duracao
        self.io = io
        self.tempo_decorrido = 0
        self.tempo_entrada_fila = chegada
        self.tempo_espera_total = 0

class EscalonadorSJF:

    def __init__(self):
        self.cpu = None
        self.fila_espera = []
        self.tempo_atual = 0
        self.fila_processos = []
        self.todos_processos = []
        self.historico_execucao = []
        self.processo_em_io = None  # Guardar o processo que saiu para I/O

    def adicionar_Processo(self, processo):
        if processo.chegada == 0:
            self.cpu = processo
        else:
            self.fila_processos.append(processo)
        self.todos_processos.append(processo)

    def escalonar_Processo(self):
        # Se a CPU está vazia e há processos na fila de espera
        if self.cpu is None and self.fila_espera:
            # Seleciona o processo de menor duração que não seja o que acabou de sair para I/O
            if len(self.fila_espera) == 1:
                menor_duracao = self.fila_espera[0].duracao
            else:
                menor_duracao = min(processo.duracao for processo in self.fila_espera if processo != self.processo_em_io)  # Ignorar o processo que acabou de sair para I/O)
            for processo in self.fila_espera[:]:
                if processo.duracao == menor_duracao and processo != self.processo_em_io:
                    self.cpu = processo
                    self.cpu.tempo_espera_total += self.tempo_atual - self.cpu.tempo_entrada_fila
                    self.fila_espera.remove(processo)
                    break
            self.processo_em_io = None  # Libera o processo após o ciclo

    def chegada_Processo(self):
        for processo in self.fila_processos[:]:
            if processo.chegada == self.tempo_atual:
                print(f'#[evento] CHEGADA <{processo.pid}>')
                processo.tempo_entrada_fila = self.tempo_atual
                self.fila_espera.append(processo)

    def incrementar_Tempo_Decorrido(self):
        if self.cpu:
            self.cpu.tempo_decorrido += 1

    def decrementar_Duracao(self):
        if self.cpu:
            self.cpu.duracao -= 1

    def verifica_IO(self):
        if self.cpu is not None:
            if self.cpu.tempo_decorrido in self.cpu.io:
                print(f'#[evento] OPERACAO I/O <{self.cpu.pid}>')
                if self.cpu.duracao > 0:  # Se o processo ainda não terminou
                    self.cpu.tempo_entrada_fila = self.tempo_atual
                    self.fila_espera.append(self.cpu)
                    self.processo_em_io = self.cpu  # Marca o processo que acabou de sair
                self.cpu = None  # Libera a CPU

    def encerrar_Processo(self):
        if self.cpu is not None and self.cpu.duracao == 0:
            print(f'#[evento] ENCERRANDO <{self.cpu.pid}>')
            self.cpu = None

    def calcula_Tempo_Espera(self, arquivo_saida=None):
        print('***********************************')
        print('TEMPO DE ESPERA DE CADA PROCESSO:')
        for processo in self.todos_processos:
            tempo_espera = processo.tempo_espera_total
            print(f'{processo.pid}: {tempo_espera}')
            if arquivo_saida:
                arquivo_saida.write(f'{processo.pid}: {tempo_espera}\n')

        total_tempo_espera = sum(processo.tempo_espera_total for processo in self.todos_processos)
        media_tempo_espera = total_tempo_espera / len(self.todos_processos) if self.todos_processos else 0
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

    def gerar_diagrama_gantt(self):
        with open('grafico.txt', 'w') as arquivo_grafico:
            arquivo_grafico.write('Diagrama de Gantt:\n')
            arquivo_grafico.write('-' * (len(self.historico_execucao) * 5) + '\n')
            arquivo_grafico.write('| ' + ' | '.join(self.historico_execucao) + ' |\n')
            arquivo_grafico.write('-' * (len(self.historico_execucao) * 5) + '\n')
            self.calcula_Tempo_Espera(arquivo_grafico)

    def executarSJF(self):
        print('***********************************')
        print('***** SHORTEST JOB FIRST *****')
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
            print(f'************ TEMPO {self.tempo_atual} **************')
            self.historico_execucao.append(self.cpu.pid if self.cpu else 'LIVRE')
            self.incrementar_Tempo_Decorrido()
            self.decrementar_Duracao()
            self.verifica_IO()
            self.encerrar_Processo()
            self.chegada_Processo()
            self.escalonar_Processo()
            self.print_Status()
        print('-----------------------------------')
        print('------- SIMULACAO FINALIZADA ------')
        print('-----------------------------------')
        self.gerar_diagrama_gantt()
