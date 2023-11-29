from sys import argv
import threading

from thread_cria_pessoas import thread_cria_pessoa

from ixphere_thread import Ixphere
from helper import *
from global_variables import init


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

    init()

    # random.seed(dados.semente)

    ixphere = Ixphere(dados=dados)
    cria_pessoas = threading.Thread(target=thread_cria_pessoa, args=[dados])

    print(f"[Ixfera] Simulação iniciada.")
    cria_pessoas.start()
    ixphere.start()

    cria_pessoas.join()
    ixphere.join()

    print(f"[Ixfera] Simulação finalizada.")


if __name__ == "__main__":
    main()
