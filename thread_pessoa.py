import time
from time import sleep

from helper import *
import global_variables as gv


def tempoParaEntrarNaFila(dados: Dados, pessoa: Pessoa):
    tempo_maximo = dados.max_intervalo * (dados.unid_tempo / 1000)

    if dados.unid_tempo < 1000:
        tempo_maximo = 1

    # travou aqui quando o getRandomNumber recebia um valor float
    tempo_para_entrar = getRandomNumber(tempo_maximo)
    # print(f"{pessoa} vai entrar na fila em {tempo_para_entrar} segundos.")
    sleep(tempo_para_entrar)

    with gv.mutex_fila:
        gv.fila_entrada.put(pessoa)
        gv.count_queue += 1
        print(f"[Pessoa {pessoa.id}/{pessoa.faixa_etaria}] Aguardando na fila.")

    gv.sem_aguarda_chamada.release()
    pessoa.sem_aguarda_chamada.release()


def aguardandoAtracao(pessoa: Pessoa):
    pessoa.sem_entrar_atracao.acquire()


def tempoNaAtracao(dados: Dados, pessoa: Pessoa):
    sleep(dados.permanencia)

    pessoa.sem_sair_atracao.release()
    

    with gv.mutex_count_pessoas_na_atracao:
        gv.count_pessoas_na_atracao -= 1
        print(f"[{pessoa}] Saiu da Ixfera (quantidade = {gv.count_pessoas_na_atracao}).")
        with gv.mutex_fila:
            gv.count_queue -= 1
            if gv.count_pessoas_na_atracao == 0:
                if pessoa.faixa_etaria == "A":
                    gv.tempoA = time.time()
                elif pessoa.faixa_etaria == "B":
                    gv.tempoB = time.time()
                else:
                    gv.tempoC = time.time()
            if gv.count_queue == 0 and gv.count_pessoas_na_atracao == 0:
                print(f"[Ixfera] Pausando experiencia {pessoa.faixa_etaria}")
                gv.ocupado_end = time.time()
                gv.ocupado_total += gv.ocupado_end - gv.ocupado_start



def thread_pessoa(dados: Dados, pessoa: Pessoa):
    tempoParaEntrarNaFila(dados, pessoa)

    aguardandoAtracao(pessoa)

    tempoNaAtracao(dados, pessoa)
