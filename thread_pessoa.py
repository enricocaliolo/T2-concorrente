from time import sleep

from helper import *
import global_variables as gv


def tempoParaEntrarNaFila(dados: Dados, pessoa: Pessoa):
    tempo_maximo = dados.max_intervalo * (dados.unid_tempo / 1000)

    if dados.unid_tempo < 1000:
        tempo_maximo = 1

    # travou aqui quando o getRandomNumber recebia um valor float
    tempo_para_entrar = getRandomNumber(tempo_maximo)
    print(f"{pessoa} vai entrar na fila em {tempo_para_entrar} segundos.")
    sleep(tempo_para_entrar)

    gv.mutex_fila.acquire()
    gv.myQueue.put(pessoa)
    gv.count_queue += 1
    print(f"[Pessoa {pessoa.id}/{pessoa.faixa_etaria}] Aguardando na fila.")
    gv.mutex_fila.release()

    gv.sem_aguarda_chamada.release()
    pessoa.sem_aguarda_chamada.release()


def aguardandoAtracao(pessoa: Pessoa):
    pessoa.sem_entrar_atracao.acquire()


def tempoNaAtracao(dados: Dados, pessoa: Pessoa):
    sleep(dados.permanencia)

    pessoa.sem_sair_atracao.release()

    gv.mutex_count_pessoas_na_atracao.acquire()
    gv.count_pessoas_na_atracao -= 1
    print(f"[{pessoa}] Saiu da Ixfera (quantidade = {gv.count_pessoas_na_atracao}).")
    gv.mutex_count_pessoas_na_atracao.release()

    gv.mutex_fila.acquire()
    gv.count_queue -= 1
    gv.mutex_fila.release()

    gv.mutex_fila.acquire()
    if gv.count_queue == 0 and gv.count_pessoas_na_atracao == 0:
        print(f"[Ixfera] Pausando experiencia {pessoa.faixa_etaria}")
    gv.mutex_fila.release()


def thread_pessoa(dados: Dados, pessoa: Pessoa):
    tempoParaEntrarNaFila(dados, pessoa)

    aguardandoAtracao(pessoa)

    tempoNaAtracao(dados, pessoa)
