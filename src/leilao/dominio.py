from operator import attrgetter

class Usuario:

    def __init__(self, nome):
        self.__nome = nome

    def __repr__(self):
        return f"Usuario(nome='{self.nome}')"

    def __str__(self):
        return self.nome

    def __eq__(self, other):
        return self.nome == other.nome

    @property
    def nome(self):
        return self.__nome


class Lance:

    def __init__(self, usuario, valor):
        self.__usuario = usuario
        self.__valor = valor

    def __repr__(self):
        return f"Lance(usuario={repr(self.usuario)}, valor=R$ {self.valor:.2f})"

    def __str__(self):
        return f"Lance({self.usuario.nome}: R$ {self.valor:.2f})"

    def __eq__(self, other):
        return self.valor == other.valor and self.usuario == other.usuario

    @property
    def usuario(self):
        return self.__usuario

    @property
    def valor(self):
        return self.__valor


class Leilao:

    def __init__(self, descricao, lances = None):
        self.__descricao = descricao

        self.__lances = []
        if(lances):
            for lance in lances:
                self.propoe(lance)

    def __len__(self):
        return len(self.lances)

    @property
    def lances(self):
        return self.__lances[:]

    @property
    def descricao(self):
        return self.__descricao

    @property
    def menor_lance(self):
        return min(self.lances, key=attrgetter('valor'))

    @property
    def maior_lance(self):
        return max(self.lances, key=attrgetter('valor'))

    def propoe(self, lance: Lance):

        if len(self.lances) > 0:
            maior_lance = max(self.lances, key=attrgetter('valor'))

            if(lance.valor <= maior_lance.valor):
                raise ValueError("Para um lance ser aceito, ele deve ser maior que os lances anteriores")

        self.__lances.append(lance)

    def propoe_lances(self, lances):
        for lance in lances:
            self.propoe(lance)
