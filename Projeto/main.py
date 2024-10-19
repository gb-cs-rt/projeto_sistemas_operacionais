from escalonador_FCFS import EscalonadorFCFS, Processo
from escalonador_SJF import EscalonadorSJF, Processo
from escalonador_PRIORIDADE import EscalonadorPrioridade, Processo
from escalonador_RR import EscalonadorRR, Processo

def main():
    print('***************************************************')
    print('***** SELECIONE O ALGORITMO DE ESCALONAMENTO ******')
    print('***************************************************')
    print('1 - FIRST COME FIRST SERVED (FCFS)')
    print('2 - SHORTEST JOB FIRST (SJF)')
    print('3 - ESCALONAMENTO POR PRIORIDADE')
    print('4 - ROUND ROBIN')
    print('***************************************************')
    algoritmo = input('Digite o número do algoritmo desejado: ')
    print('***************************************************')

    match algoritmo:
        case '1':
            escalonador = EscalonadorFCFS()
            arq = open('entrada.txt', 'r')
            for linha in arq:
                partes = linha.split()
                pid = partes[0]
                chegada = int(partes[1])
                duracao = int(partes[2])
                io = list(map(int, partes[3].split(',')) if len(partes) > 3 else [])
                processo = Processo(pid, chegada, duracao, io)
                escalonador.adicionar_Processo(processo)
            escalonador.executarFCFS()
            arq.close()
        case '2':
            escalonador = EscalonadorSJF()
            arq = open('entrada.txt', 'r')
            for linha in arq:
                partes = linha.split()
                pid = partes[0]
                chegada = int(partes[1])
                duracao = int(partes[2])
                io = list(map(int, partes[3].split(',')) if len(partes) > 3 else [])
                processo = Processo(pid, chegada, duracao, io)
                escalonador.adicionar_Processo(processo)
            escalonador.executarSJF()
            arq.close()
        case '3':
            escalonador = EscalonadorPrioridade()
            arq = open('entrada.txt', 'r')
            for linha in arq:
                partes = linha.split()
                pid = partes[0]
                chegada = int(partes[1])
                duracao = int(partes[2])
                prioridade = int(partes[3])
                io = list(map(int, partes[4].split(',')) if len(partes) > 4 else [])
                processo = Processo(pid, chegada, duracao, prioridade, io)
                escalonador.adicionar_Processo(processo)
            escalonador.executarPrioridade()
            arq.close()
        case '4':
            quantum = int(input('Digite o quantum: '))
            escalonador = EscalonadorRR(quantum)
            arq = open('entrada.txt', 'r')
            for linha in arq:
                partes = linha.split()
                pid = partes[0]
                chegada = int(partes[1])
                duracao = int(partes[2])
                io = list(map(int, partes[3].split(',')) if len(partes) > 3 else [])
                processo = Processo(pid, chegada, duracao, io)
                escalonador.adicionar_Processo(processo)
            escalonador.executarRR()
            arq.close()
        case _:
            print('Algoritmo inválido')
            return



if __name__ == '__main__':
    main()

