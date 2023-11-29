import threading
from queue import Queue


def init():
    global fila_entrada
    fila_entrada = Queue()

    global mutex_fila
    mutex_fila = threading.Lock()

    global count_pessoas_na_atracao
    count_pessoas_na_atracao = 0

    global mutex_count_pessoas_na_atracao
    mutex_count_pessoas_na_atracao = threading.Lock()

    global sem_aguarda_chamada
    sem_aguarda_chamada = threading.Semaphore(0)
