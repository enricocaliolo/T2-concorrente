import queue
import threading

from helper import *
import global_variables as gv

lock = threading.Lock()

sem_pausar_atracao = Semaphore(0)


class Ixphere(threading.Thread):
    def __init__(self, dados: Dados):
        threading.Thread.__init__(self)
        self.dados = dados
        self.atracao = ""
        self.aberto = False
        self.clientes_atendidos = 0

    def esperaCliente(self):
        gv.sem_aguarda_chamada.acquire(timeout=self.dados.max_intervalo)

        gv.mutex_fila.acquire()
        queue_size = gv.myQueue.qsize()
        gv.mutex_fila.release()

        if queue_size == 0:
            if gv.pessoas_na_atracao.qsize() != 0:
                q_pessoa: Pessoa = gv.pessoas_na_atracao.get()
                q_pessoa.sem_sair_atracao.acquire()

                print(f"Pausando experiencia {self.atracao}")
                gv.sem_aguarda_chamada.acquire()

        gv.mutex_fila.acquire()
        pessoa: Pessoa = gv.myQueue.get()
        gv.mutex_fila.release()

        pessoa.sem_aguarda_chamada.acquire()

        gv.mutex_verifica_atracao.acquire()
        if not self.aberto:
            self.aberto = True
            self.atracao = pessoa.faixa_etaria
            print(f"[Ixfera] Iniciando a experiencia {pessoa.faixa_etaria}")
        gv.mutex_verifica_atracao.release()

        if pessoa.faixa_etaria == self.atracao:
            if gv.pessoas_na_atracao.full():
                q_pessoa: Pessoa = gv.pessoas_na_atracao.get()
                q_pessoa.sem_sair_atracao.acquire()

            pessoa.sem_entrar_atracao.release()
            # self.clientes_na_atracao.append(pessoa)
            gv.pessoas_na_atracao.put(pessoa)
            self.clientes_atendidos += 1

        else:
            while gv.pessoas_na_atracao.qsize() != 0:
                # q_pessoa: Pessoa = self.clientes_na_atracao.pop(0)
                q_pessoa: Pessoa = gv.pessoas_na_atracao.get()
                q_pessoa.sem_sair_atracao.acquire()

            gv.mutex_verifica_atracao.acquire()
            self.atracao = pessoa.faixa_etaria
            print(f"[Ixfera] Iniciando a experiencia {pessoa.faixa_etaria}")
            pessoa.sem_entrar_atracao.release()
            # self.clientes_na_atracao.append(pessoa)
            gv.pessoas_na_atracao.put(pessoa)
            self.clientes_atendidos += 1
            gv.mutex_verifica_atracao.release()

    def run(self):
        # print("[Ixfera] Simulação iniciada")
        while self.clientes_atendidos != self.dados.n_pessoas:
            self.esperaCliente()
