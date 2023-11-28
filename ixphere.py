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
    start_total = time.time()
    gv.tempoA = time.time()
    gv.tempoB = time.time()
    gv.tempoC = time.time()
    cria_pessoas.start()
    ixphere.start()

    cria_pessoas.join()
    ixphere.join()

    print(f"[Ixfera] Simulação finalizada.")
    end_total = time.time()
    tempo_total = end_total - start_total

    print("Tempo médio de espera: ")
    if gv.tempos_medios["A"][1] == 0:
        print("Faixa A: Não houveram pessoas dessa faixa etaria.")
    else:
        media_A = gv.tempos_medios["A"][0]/gv.tempos_medios["A"][1]
        print(f"Faixa A: {media_A}")
        
        
    if gv.tempos_medios["B"][1] == 0:
        print("Faixa B: Não houveram pessoas dessa faixa etaria.")
    else:
        media_B = gv.tempos_medios["B"][0]/gv.tempos_medios["B"][1]
        print(f"Faixa B: {media_B}")
        
        
    if gv.tempos_medios["C"][1] == 0:
        print("Faixa C: Não houveram pessoas dessa faixa etaria.")
    else:
        media_C = gv.tempos_medios["C"][0]/gv.tempos_medios["C"][1]
        print(f"Faixa C: {media_C}")

    print(f'Taxa de ocupacao: {gv.ocupado_total/tempo_total}')

if __name__ == "__main__":
    main()
