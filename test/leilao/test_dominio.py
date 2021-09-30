from unittest import TestCase

from src.leilao.dominio import Usuario, Lance, Leilao, Avaliador


class TestAvaliador(TestCase):

    def get_avaliador(self):
        gui = Usuario('Gui')
        yuri = Usuario('Yuri')

        lances_do_yuri = [Lance(yuri, 45.0), Lance(yuri, 50.0), Lance(yuri, 250.0)]
        lances_do_gui = [Lance(gui, 48.0), Lance(gui, 60.0), Lance(gui, 300.0)]

        leilao = Leilao("Celular")

        leilao.lances.extend(lances_do_gui)
        leilao.lances.extend(lances_do_yuri)

        return Avaliador(leilao)

    def test_menor_lance(self):
        avaliador = self.get_avaliador()
        menor_lance = avaliador.menor_lance
        self.assertEqual(45.0, menor_lance.valor)

    def test_maior_lance(self):
        avaliador = self.get_avaliador()
        maior_lance = avaliador.maior_lance
        self.assertEqual(300.0, maior_lance.valor)

