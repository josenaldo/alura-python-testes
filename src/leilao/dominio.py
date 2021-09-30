from operator import attrgetter

class Usuario:

    def __init__(self, nome):
        self.__nome = nome

    def __repr__(self):
        return f"Usuario(nome='{self.nome}')"

    @property
    def nome(self):
        return self.__nome




class Lance:

    def __init__(self, usuario, valor):
        self.usuario = usuario
        self.valor = valor

    def __repr__(self):
        return f"Lance(usuario={repr(self.usuario)}, valor=R$ {self.valor:.2f})"

    def __str__(self):
        return f"Lance({self.usuario.nome}: R$ {self.valor:.2f})"

class Leilao:

    def __init__(self, descricao):
        self.descricao = descricao
        self.__lances = []

    @property
    def lances(self):
        return self.__lances

class Avaliador:
    def __init__(self, leilao: Leilao):
        self.__leilao = leilao

    @property
    def menor_lance(self):
        return min(self.__leilao.lances, key=attrgetter('valor'))

    @property
    def maior_lance(self):
        return max(self.__leilao.lances, key=attrgetter('valor'))