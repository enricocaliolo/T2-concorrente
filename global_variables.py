import threading
import queue


global faixaEtariaProportion
faixaEtariaProportion = {"A": 0, "B": 0, "C": 0}

global mutex_faixa_etaria_proportion
mutex_faixa_etaria_proportion = threading.Lock()

global myQueue
myQueue = queue.Queue()

global mutex_fila
mutex_fila = threading.Lock()

global mutex_verifica_atracao
mutex_verifica_atracao = threading.Lock()

global sem_aguarda_chamada
sem_aguarda_chamada = threading.Semaphore(0)

global sem_entrar_atracao
sem_entrar_atracao = threading.Semaphore(0)

global sem_sair_atracao
sem_sair_atracao = threading.Semaphore(0)
