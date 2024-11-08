from src.escalonador_FCFS import EscalonadorFCFS
from src.escalonador_SJF import EscalonadorSJF
from src.escalonador_PRIORIDADE import EscalonadorPrioridade
from src.escalonador_RR import EscalonadorRR
from src.utils import Processo, ProcessoPrioridade
import os, time, sys

def clear():
    if sys.platform == 'linux':
        os.system('clear')
    else:
        os.system('cls')

def main():

    while True:

        try:
            print('***************************************************')
            print('***** SELECIONE O ALGORITMO DE ESCALONAMENTO ******')
            print('***************************************************')
            print('1 - FIRST COME FIRST SERVED (FCFS)')
            print('2 - SHORTEST JOB FIRST (SJF)')
            print('3 - ESCALONAMENTO POR PRIORIDADE')
            print('4 - ROUND ROBIN')
            print('5 - SAIR')
            print('***************************************************')
            algoritmo = input('Digite o número do algoritmo desejado: ')
            print('***************************************************')

            if algoritmo == '5':
                break

            if not os.path.exists('entrada.txt'):
                print('Arquivo "entrada.txt" não encontrado')
                continue
            
            match algoritmo:
                case '1':
                    escalonador = EscalonadorFCFS()
                case '2':
                    escalonador = EscalonadorSJF()
                case '3':
                    escalonador = EscalonadorPrioridade()
                case '4':
                    quantum = int(input('Digite o quantum: '))
                    escalonador = EscalonadorRR(quantum)
                case _:
                    raise Exception('Algoritmo inválido')
            
            arq = open('entrada.txt', 'r')
            for linha in arq.readlines():
                partes = linha.split()
                if len(partes) < 3:
                    raise Exception('Arquivo "entrada.txt" inválido. Cada linha deve conter o PID, o tempo de chegada e a duração do processo.')

                pid = partes[0]
                chegada = int(partes[1])
                duracao = int(partes[2])

                if len(partes) > 3 and partes[3] != "-":
                    io = list(map(int, partes[3].split(',')))
                else:
                    io = []
                
                if algoritmo == '3':
                    if len(partes) < 5:
                        raise Exception('Arquivo "entrada.txt" inválido. Para o escalonamento por prioridade, é necessário informar a prioridade de cada processo.')

                    prioridade = int(partes[4])
                    processo = ProcessoPrioridade(pid, chegada, duracao, prioridade, io)
                else:
                    processo = Processo(pid, chegada, duracao, io)

                escalonador.adicionarProcesso(processo)
            arq.close()

            try:
                clear()
                escalonador.executar()
            except Exception as e:
                print(f'Erro ao simular: {e}\n')

        except Exception as e:
            clear()
            print(f'Erro ao iniciar: {e}\n')

        time.sleep(1)

if __name__ == '__main__':
    try:
        clear()
        main()
    except:
        pass
