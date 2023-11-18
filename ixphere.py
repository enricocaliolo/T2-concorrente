from sys import argv
import threading
import random

from thread_cria_pessoas import thread_cria_pessoa

from ixphere_thread import Ixphere
from helper import *


def getCLIArguments():
    n_pessoas = int(argv[1])
    n_vagas = int(argv[2])
    permanencia = int(argv[3])
    max_intervalo = int(argv[3])
    semente = int(argv[5])
    unid_tempo = int(argv[6])

    return Dados(n_pessoas, n_vagas, permanencia, max_intervalo, semente, unid_tempo)


def main():
    dados = getCLIArguments()

    random.seed(dados.semente)

    ixphere = Ixphere(dados=dados)
    cria_pessoas = threading.Thread(target=thread_cria_pessoa, args=[dados])

    ixphere.start()
    cria_pessoas.start()

    ixphere.join()
    cria_pessoas.join()

    print(f"[Ixfera] Simulação finalizada.")


if __name__ == "__main__":
    main()
