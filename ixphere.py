from sys import argv
import threading

import time

from thread_cria_pessoas import thread_cria_pessoa

from ixphere_thread import Ixphere
from helper import *
import global_variables as gv


def getCLIArguments():
    arguments = [int(arg) for arg in argv[1:]]

    if 0 in arguments:
        raise Exception("Nenhum dos parâmetros deve ser zero.")

    if sum(arg < 0 for arg in arguments):
        raise Exception("Nenhum dos parâmetros deve ser negativo.")

    if len(arguments) != 6:
        raise Exception(
            "Argumento(s) faltando. Esteja certo de estar compilando com a estrutura: \n<n_pessoas> <n_vagas> <permanencia> <max_intervalo> <semente> <unid_tempo>"
        )

    return Dados(*arguments)


def main():
    try:
        dados = getCLIArguments()
    except Exception as inst:
        print(inst)
        return

    gv.init()

    # random.seed(dados.semente)

    ixphere = Ixphere(dados=dados)
    cria_pessoas = threading.Thread(target=thread_cria_pessoa, args=[dados])

    print(f"[Ixfera] Simulação iniciada.")
    start_total = time.time()
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
        print('Faixa A: {:.2f} ms'.format(media_A * 1000))
        
        
    if gv.tempos_medios["B"][1] == 0:
        print("Faixa B: Não houveram pessoas dessa faixa etaria.")
    else:
        media_B = gv.tempos_medios["B"][0]/gv.tempos_medios["B"][1]
        print('Faixa B: {:.2f} ms'.format(media_B * 1000))
        
        
        
    if gv.tempos_medios["C"][1] == 0:
        print("Faixa C: Não houveram pessoas dessa faixa etaria.")
    else:
        media_C = gv.tempos_medios["C"][0]/gv.tempos_medios["C"][1]
        print('Faixa C: {:.2f} ms'.format(media_C * 1000))
    
    print('Taxa de ocupacao: {:.2f}%'.format((gv.ocupado_total/tempo_total) * 100))
    print(f'Tempo total: {tempo_total}')


if __name__ == "__main__":
    main()
