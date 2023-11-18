import random


class Dados:
    def __init__(
        self, n_pessoas, n_vagas, permanencia, max_intervalo, semente, unid_tempo
    ):
        self.n_pessoas = n_pessoas
        self.n_vagas = n_vagas
        self.permanencia = permanencia
        self.max_intervalo = max_intervalo
        self.semente = semente
        self.unid_tempo = unid_tempo


class Pessoa:
    def __init__(self, id, faixa_etaria):
        self.id = id
        self.faixa_etaria = faixa_etaria


def getRandomNumber(endInterval):
    random_number = random.randint(1, endInterval)

    return random_number
