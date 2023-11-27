import threading

from helper import Dados, Pessoa, getRandomNumber
from thread_pessoa import thread_pessoa

faixa_etarias = {"A": 0, "B": 0, "C": 0}


def thread_cria_pessoa(dados: Dados):
    threads = []

    for i in range(dados.n_pessoas):
        faixa_etaria = getFaixaEtaria()
        pessoa = Pessoa(i + 1, faixa_etaria)

        t = threading.Thread(target=thread_pessoa, args=[dados, pessoa])

        threads.append(t)
        threads[i].start()

    for i in range(dados.n_pessoas):
        threads[i].join()


def getFaixaEtaria():
    faixa_etaria = ""
    number = getRandomNumber(31)

    if 4 <= number and number <= 11:
        faixa_etaria = "A"

    elif 12 <= number and number <= 18:
        faixa_etaria = "B"

    elif number >= 19:
        faixa_etaria = "C"

    else:
        faixa_etaria = "B"

    return faixa_etaria
