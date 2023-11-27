import random
from time import sleep

from helper import *
import global_variables as gv


def tempoParaEntrarNaFila(dados: Dados, pessoa: Pessoa):
    tempo_para_entrar = getRandomNumber(dados.max_intervalo)

    sleep(tempo_para_entrar)

    gv.mutex_fila.acquire()
    gv.myQueue.put(pessoa)
    print(f"[Pessoa {pessoa.id}/{pessoa.faixa_etaria}] Aguardando na fila.")
    gv.mutex_fila.release()

    gv.sem_aguarda_chamada.release()
    pessoa.sem_aguarda_chamada.release()


def aguardandoAtracao(pessoa: Pessoa):
    pessoa.sem_entrar_atracao.acquire()
    print(f"[Pessoa {pessoa.id}/{pessoa.faixa_etaria}] Entra na Ixfera.")


def tempoNaAtracao(dados: Dados, pessoa: Pessoa):
    sleep(dados.permanencia)

    pessoa.sem_sair_atracao.release()
    print(f"[Pessoa {pessoa.id}/{pessoa.faixa_etaria}] Saiu da Ixfera.")


def thread_pessoa(dados: Dados, pessoa: Pessoa):
    tempoParaEntrarNaFila(dados, pessoa)

    aguardandoAtracao(pessoa)

    tempoNaAtracao(dados, pessoa)
