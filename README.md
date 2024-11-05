# Escalonador de Processos

Este projeto implementa um simulador de Escalonamento de Processos preemptivo para a disciplina de Sistemas Operacionais, com suporte a operações de I/O. O objetivo é simular o comportamento de processos em uma fila de espera, respeitando os algoritmos selecionados e lidando com interrupções de I/O.

## Principais Características
- **Simulação de Escalonamento First Come First Served (FCFS)** com operações de I/O
- **Simulação de Escalonamento Shortest job first** com operações de I/O
- **Simulação de Escalonamento por Prioridade** com operações de I/O
- **Simulação de Escalonamento Round-Robin** com operações de I/O
- **Implementado em linguagens**: Python
- **Saída de dados do escalonador** (saida.txt)
- **Gráfico de Gantt gerado em arquivo** (grafico.txt)
- **Cálculo de tempo de espera** para cada processo e tempo médio de espera

## Primeiros Passos

### Sistemas Operacionais Suportados
- ![Ubuntu 22 Shield](https://img.shields.io/badge/Ubuntu-22.04-orange)
- ![Windows 11 Shield](https://img.shields.io/badge/Windows-11-blue)

### Pré-requisitos
- **Python**
- **Git** para clonar o repositório

### Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/gb-cs-rt/projeto_sistemas_operacionais.git
   
2. Executar o arquivo main.py:
   ```bash
    python main.py
    ```
   
## Formato do arquivo de entrada
- **Nome do processo (PID)**
- **Tempo de chegada**
- **Duração**
- **Instantes de operação de I/O** (opcional), separados por vírgulas
- **Prioridade** (caso o escalonador esolhido seja o de Prioridade)

### Exemplos de arquivo de entrada para Escalonadores como FCFS, SJF e Round-Robin
```
P1 10 9 2,4,6,8
P2 4 10 5
P3 0 5 2
P4 1 7 3,6
P5 17 2
```
```
P1 0 6 2
P2 1 5 1
P3 5 5 1
P4 10 4
```

### Exemplo de arquivo de entrada para Escalonador por Prioridade

O arquivo de entrada deve ter um atributo a mais, que é a prioridade do processo. Além disso, caso não haja evento de I/O para um processo, deve-se colocar um hífen (-) no lugar.

```
P1 0 8 - 4
P2 0 5 - 3
P3 0 7 - 2
P4 0 3 - 1
```

Contudo, caso haja evento de I/O, deve-se colocar o evento de I/O no lugar do hífen.

```
P1 0 6 2 4 
P2 1 5 1 3 
P3 5 5 1 2 
P4 10 4 - 1
```

## Saída de Dados

A saída de dados é gerada no arquivo `saida.txt` e contém as seguintes informações:
- **Tempo da simulação**
- **Possível evento do processo**
- **Fila de espera**
- **Processo na CPU**
- **Tempo de espera de cada processo**
- **Tempo total de espera**
- **Tempo médio de espera**

## Diagrama de Gantt

O diagrama de Gantt é gerado no arquivo `grafico.txt` e contém as seguintes informações:
- **Simulaçãoo de escalonamento**
- **Tempo de espera de cada processo**
- **Tempo total de espera**
- **Tempo médio de espera**

## Membros
- Cauan Sousa - 24.124.084-5  
- Gustavo Baggio - 24.122.012-8  
- Ruan Turola - 24.122.050-8  