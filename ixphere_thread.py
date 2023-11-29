
import threading
from queue import Queue

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
        self.pessoas_na_atracao = Queue(maxsize=dados.n_vagas)
        
    def iniciaAtracao(self, pessoa: Pessoa):
        self.aberto = True
        self.atracao = pessoa.faixa_etaria
        print(f"[Ixfera] Iniciando a experiencia {pessoa.faixa_etaria}")
        
    def entrarNaEsfera(self, pessoa: Pessoa):
            if self.pessoas_na_atracao.full():
                q_pessoa: Pessoa = self.pessoas_na_atracao.get()
                q_pessoa.sem_sair_atracao.acquire()

            self.pessoas_na_atracao.put(pessoa)
            with gv.mutex_count_pessoas_na_atracao:
                gv.count_pessoas_na_atracao += 1
                print(
                    f"[{pessoa}] Entra na Ixfera (quantidade = {gv.count_pessoas_na_atracao})."
                )
                
            self.clientes_atendidos += 1
            
            pessoa.sem_entrar_atracao.release()

            # checando se é a última pessoa a entrar na atração
            if self.clientes_atendidos == self.dados.n_pessoas:
                while self.pessoas_na_atracao.qsize() != 0:
                    q_pessoa: Pessoa = self.pessoas_na_atracao.get()
                    q_pessoa.sem_sair_atracao.acquire()
                    
    def aguardarAtracaoAcabar(self, pessoa: Pessoa):
        while self.pessoas_na_atracao.qsize() != 0:
            q_pessoa: Pessoa = self.pessoas_na_atracao.get()
            q_pessoa.sem_sair_atracao.acquire()

    def esperaCliente(self):
        gv.sem_aguarda_chamada.acquire()

        with gv.mutex_fila:
            if gv.fila_entrada.qsize() == 0:
                if self.pessoas_na_atracao.qsize() != 0:
                    q_pessoa: Pessoa = self.pessoas_na_atracao.get()
                    q_pessoa.sem_sair_atracao.acquire()

            pessoa: Pessoa = gv.fila_entrada.get()

        pessoa.sem_aguarda_chamada.acquire()

        if not self.aberto:
            self.iniciaAtracao(pessoa)
        if pessoa.faixa_etaria == self.atracao:
           self.entrarNaEsfera(pessoa)
        else:
            self.aguardarAtracaoAcabar(pessoa)
            self.iniciaAtracao(pessoa)
            self.entrarNaEsfera(pessoa)

    def run(self):
        while self.clientes_atendidos != self.dados.n_pessoas:
            self.esperaCliente()
