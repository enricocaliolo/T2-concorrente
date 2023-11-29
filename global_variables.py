import threading
from queue import Queue


def init():
    global fila_entrada
    fila_entrada = Queue()

    global mutex_fila
    mutex_fila = threading.Lock()

    global count_pessoas_na_atracao
    count_pessoas_na_atracao = 0
    
    global count_queue
    count_queue = 0
    
    global mutex_count_pessoas_na_atracao
    mutex_count_pessoas_na_atracao = threading.Lock()

    global sem_aguarda_chamada
    sem_aguarda_chamada = threading.Semaphore(0)
    
    global ocupado_start
    global ocupado_total
    ocupado_total = 0
    ocupado_start = 0
    
    global tempos_medios

    tempos_medios = {
        "A": [0, 0],
        "B": [0, 0],
        "C": [0, 0]
    }
    
    global tempoA
    global tempoB
    global tempoC
