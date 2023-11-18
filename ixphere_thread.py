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
        self.clientes_na_atracao = 0

    def esperaCliente(self):
        sem_aguarda_chamada.acquire()

        mutex_fila.acquire()
        pessoa: Pessoa = myQueue.get()
        mutex_fila.release()

        # print(
        #     f"Pessoa {pessoa.id}/{pessoa.faixa_etaria} está vendo se pode entrar na atracao {self.atracao}"
        # )

        mutex_verifica_atracao.acquire()
        if not self.aberto:
            self.aberto = True
            self.atracao = pessoa.faixa_etaria
        mutex_verifica_atracao.release()

        if pessoa.faixa_etaria == self.atracao:
            sem_entrar_atracao.release()
            self.clientes_na_atracao += 1
            self.clientes_atendidos += 1

        else:
            # aguardar todos na atracao sairem e iniciar uma nova
            while self.clientes_na_atracao != 0:
                sem_sair_atracao.acquire()
                self.clientes_na_atracao -= 1

            mutex_verifica_atracao.acquire()
            self.atracao = pessoa.faixa_etaria
            print(f"[Ixfera] Iniciando a experiencia {pessoa.faixa_etaria}")
            sem_entrar_atracao.release()
            self.clientes_na_atracao += 1
            self.clientes_atendidos += 1
            mutex_verifica_atracao.release()

    def run(self):
        print("[Ixfera] Simulação iniciada")
        while self.clientes_atendidos != self.dados.n_pessoas:
            self.esperaCliente()
