import time

from helper import *
import global_variables as gv


def tempoParaEntrarNaFila(dados: Dados, pessoa: Pessoa):
    tempo_maximo = dados.max_intervalo * (dados.unid_tempo / 1000)

    if dados.unid_tempo < 1000:
        tempo_maximo = 1

    tempo_para_entrar = getRandomNumber(tempo_maximo)
    time.sleep(tempo_para_entrar)

    with gv.mutex_fila:
        gv.fila_entrada.put(pessoa)
        gv.count_queue += 1
        print(f"[Pessoa {pessoa.id}/{pessoa.faixa_etaria}] Aguardando na fila.")
        pessoa.tempo_entrou_na_fila = time.time()

    gv.sem_aguarda_chamada.release()
    pessoa.sem_aguarda_chamada.release()


def aguardandoAtracao(pessoa: Pessoa):
    pessoa.sem_entrar_atracao.acquire()


def tempoNaAtracao(dados: Dados, pessoa: Pessoa):
    time.sleep(dados.permanencia)

    pessoa.sem_sair_atracao.release()

    with gv.mutex_count_pessoas_na_atracao:
        gv.count_pessoas_na_atracao -= 1
        print(
            f"[{pessoa}] Saiu da Ixfera (quantidade = {gv.count_pessoas_na_atracao})."
        )
        with gv.mutex_fila:
            gv.count_queue -= 1
            if gv.count_queue == 0 and gv.count_pessoas_na_atracao == 0:
                print(f"[Ixfera] Pausando experiência {pessoa.faixa_etaria}")

                if gv.ocupado_start != 0:
                    gv.ocupado_total += time.time() - gv.ocupado_start
                    gv.ocupado_start = 0


def thread_pessoa(dados: Dados, pessoa: Pessoa):
    tempoParaEntrarNaFila(dados, pessoa)

    aguardandoAtracao(pessoa)

    tempoNaAtracao(dados, pessoa)
