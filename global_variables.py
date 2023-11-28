import threading
from queue import Queue


def init(n_vagas):
    global myQueue
    myQueue = Queue()

    global count_queue
    count_queue = 0

    global pessoas_na_atracao
    pessoas_na_atracao = Queue(maxsize=n_vagas)

    global count_pessoas_na_atracao
    count_pessoas_na_atracao = 0

    global mutex_fila
    mutex_fila = threading.Lock()

    global sem_aguarda_chamada
    sem_aguarda_chamada = threading.Semaphore(0)
    
    global ocupado_start
    global ocupado_end
    global ocupado_total
    ocupado_total = 0
