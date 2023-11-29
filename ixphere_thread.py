import threading
import time
from queue import Queue
from time import sleep


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
        self.fim_do_A = 0
        self.fim_do_B = 0
        self.fim_do_C = 0

    def iniciaAtracao(self, pessoa: Pessoa):
        self.aberto = True
        self.atracao = pessoa.faixa_etaria
        print(f"[Ixfera] Iniciando a experiencia {pessoa.faixa_etaria}")
        gv.ocupado_start = time.time()
        self.calculaTempo(pessoa.faixa_etaria)
        

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
            pessoa.sem_entrar_atracao.release()
            sleep(0.1)

        self.clientes_atendidos += 1

        # checando se é a última pessoa a entrar na atração
        if self.clientes_atendidos == self.dados.n_pessoas:
            self.aguardarAtracaoAcabar()

    def aguardarAtracaoAcabar(self):
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
            self.aguardarAtracaoAcabar()
            self.iniciaAtracao(pessoa)
            self.entrarNaEsfera(pessoa)
            
            
    def calculaTempo(self, faixa):
        if faixa == "A":
            self.fim_do_A = time.time()
            gv.tempos_medios["A"][0] += self.fim_do_A - gv.tempoA
            gv.tempos_medios["A"][1] += 1
        elif faixa == "B":
            self.fim_do_B = time.time()
            gv.tempos_medios["B"][0] += self.fim_do_B - gv.tempoB
            gv.tempos_medios["B"][1] += 1
        else:
            self.fim_do_C = time.time()
            gv.tempos_medios["C"][0] += self.fim_do_C - gv.tempoC
            gv.tempos_medios["C"][1] += 1
            
            

    def run(self):
        while self.clientes_atendidos != self.dados.n_pessoas:
            self.esperaCliente()
