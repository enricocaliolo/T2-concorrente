from queue import Queue
import threading
from time import sleep

from helper import *
from global_variables import *

lock = threading.Lock()


class Ixphere(threading.Thread):
    def __init__(self, dados: Dados):
        threading.Thread.__init__(self)
        self.dados = dados
        self.atracao = ""
        self.aberto = False
        self.clientes_atendidos = 0
        self.clientes_na_atracao = []

    def esperaCliente(self):
        sem_aguarda_chamada.acquire()

        mutex_fila.acquire()
        pessoa: Pessoa = myQueue.get()
        mutex_fila.release()

        pessoa.sem_aguarda_chamada.acquire()

        mutex_verifica_atracao.acquire()
        if not self.aberto:
            self.aberto = True
            self.atracao = pessoa.faixa_etaria
            print(f"[Ixfera] Iniciando a experiencia {pessoa.faixa_etaria}")
        mutex_verifica_atracao.release()

        if pessoa.faixa_etaria == self.atracao:
            pessoa.sem_entrar_atracao.release()
            self.clientes_na_atracao.append(pessoa)
            self.clientes_atendidos += 1

        else:
            while len(self.clientes_na_atracao):
                q_pessoa: Pessoa = self.clientes_na_atracao.pop(0)
                q_pessoa.sem_sair_atracao.acquire()

            mutex_verifica_atracao.acquire()
            self.atracao = pessoa.faixa_etaria
            print(f"[Ixfera] Iniciando a experiencia {pessoa.faixa_etaria}")
            pessoa.sem_entrar_atracao.release()
            self.clientes_na_atracao.append(pessoa)
            self.clientes_atendidos += 1
            mutex_verifica_atracao.release()

    def run(self):
        print("[Ixfera] Simulação iniciada")
        while self.clientes_atendidos != self.dados.n_pessoas:
            self.esperaCliente()
