from sys import argv
import threading
import time
import global_variables as gv

from thread_cria_pessoas import thread_cria_pessoa

from ixphere_thread import Ixphere
from helper import *
from global_variables import init

def getCLIArguments():
    n_pessoas = int(argv[1])
    n_vagas = int(argv[2])
    permanencia = int(argv[3])
    max_intervalo = int(argv[4])
    semente = int(argv[5])
    unid_tempo = int(argv[6])

    return Dados(n_pessoas, n_vagas, permanencia, max_intervalo, semente, unid_tempo)


def main():
    dados = getCLIArguments()

    init(dados.n_vagas)

    # random.seed(dados.semente)

    ixphere = Ixphere(dados=dados)
    cria_pessoas = threading.Thread(target=thread_cria_pessoa, args=[dados])

    print(f"[Ixfera] Simulação iniciada.")
    cria_pessoas.start()
    ixphere.start()
    start_total = time.time()

    cria_pessoas.join()
    ixphere.join()

    print(f"[Ixfera] Simulação finalizada.")
    end_total = time.time()
    tempo_total = end_total - start_total
    print(f'Tempo total do programa: {tempo_total}')

    print(f'Taxa de ocupacao: {gv.ocupado_total/tempo_total}')

if __name__ == "__main__":
    main()
