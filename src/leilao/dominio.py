import sys
from functools import total_ordering


class Usuario:

    def __init__(self, nome, carteira=500.0):
        self.__nome = nome
        self.__carteira = carteira

    def __repr__(self):
        return f"Usuario(nome='{self.nome}')"

    def __str__(self):
        return f"{self.nome} - R$ {self.carteira:.2f}"

    def __eq__(self, other):
        return self.nome == other.nome

    @property
    def nome(self):
        return self.__nome

    @property
    def carteira(self):
        return self.__carteira

    def debita_carteira(self, valor):
        if valor > self.__carteira:
            raise ValueError(f"Não é possível debitar o valor R$ {valor:.2f} da " +
                             f"carteira do usuário {self.nome}. Saldo insuficiente.")
        self.__carteira -= valor

    def pode_dar_lance(self, lance):
        return lance.valor <= self.carteira

    def propoe(self, leilao, valor):
        lance = Lance(self, valor)
        leilao.propoe(lance)


@total_ordering
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

    def __lt__(self, other):
        return self.valor < other.valor

    @property
    def usuario(self):
        return self.__usuario

    @property
    def valor(self):
        return self.__valor

    def ultimo_lance_tem_mesmo_usuario(self, ultimo_lance):
        return self.usuario == ultimo_lance.usuario

class Leilao:

    def __init__(self, descricao, lances=None):
        self.__descricao = descricao
        self.__valor_maior_lance = sys.float_info.min
        self.__valor_menor_lance = sys.float_info.max

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
    def ultimo_lance(self):

        if (self.lances):
            lances = self.lances
            return lances[len(lances) - 1]
        else:
            return None

    @property
    def menor_lance(self):
        if self.lances:
            return self.lances[0]
        else:
            return None

    @property
    def maior_lance(self):
        return self.ultimo_lance

    @property
    def vencedor(self):
        if self.lances:
            return self.maior_lance.usuario
        else:
            return None

    def propoe(self, lance: Lance):
        usuario = lance.usuario
        ultimo_lance = self.ultimo_lance

        if not usuario.pode_dar_lance(lance):
            raise ValueError(f"O usuário {usuario} não pode propor o lance " +
                             f"R$ {lance.valor:.2f}. Saldo insuficiente.")

        if self.tem_lances():

            if(lance.ultimo_lance_tem_mesmo_usuario(ultimo_lance)):
                raise ValueError(f"O usuário {usuario} não pode propor dois lances seguidos.")

            if(lance <= self.maior_lance):
                raise ValueError("Para um lance ser aceito, ele deve ser maior que os lances anteriores")

        self.__lances.append(lance)

    def tem_lances(self):
        tem_lances = len(self.lances) > 0
        return tem_lances

    def propoe_lances(self, lances):
        for lance in lances:
            self.propoe(lance)

    def encerra(self):
        lance_vencedor = self.maior_lance
        usuario = lance_vencedor.usuario
        usuario.debita_carteira(lance_vencedor.valor)
