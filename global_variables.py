import threading
from queue import Queue


def init(n_vagas):
    global mutex_clientes_na_atracao
    mutex_clientes_na_atracao = threading.Lock()

    global myQueue
    myQueue = Queue()

    global pessoas_na_atracao
    pessoas_na_atracao = Queue(maxsize=n_vagas)

    global mutex_fila
    mutex_fila = threading.Lock()

    global mutex_verifica_atracao
    mutex_verifica_atracao = threading.Lock()

    global sem_aguarda_chamada
    sem_aguarda_chamada = threading.Semaphore(0)

    global sem_pessoas_na_atracao
    sem_pessoas_na_atracao = threading.Semaphore(n_vagas)
