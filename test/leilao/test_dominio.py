from unittest import TestCase

from src.leilao.dominio import Usuario, Lance, Leilao, Avaliador


class TestAvaliador(TestCase):

    def setUp(self) -> None:
        self.gui = Usuario('Gui')
        self.yuri = Usuario('Yuri')
        self.felipe = Usuario('Felipe')

        self.muitos_lances = [
            Lance(self.yuri, 45.0),
            Lance(self.gui, 48.0),
            Lance(self.yuri, 50.0),
            Lance(self.gui, 60.0),
            Lance(self.yuri, 250.0),
            Lance(self.gui, 300.0)
        ]
        self.leilao_com_muitos_lances = Leilao("Celular", self.muitos_lances)
        self.avaliador_leilao_com_muitos_lances = Avaliador(self.leilao_com_muitos_lances)

        self.um_lance = Lance(self.felipe, 400.0)
        self.leilao_com_um_lance = Leilao("Computador", [self.um_lance])
        self.avaliador_leilao_com_um_lance = Avaliador(self.leilao_com_um_lance)


    def test_deve_retornar_o_menor_menor_lance(self):
        menor_lance = self.avaliador_leilao_com_muitos_lances.menor_lance
        self.assertEqual(Lance(Usuario('Yuri'),45.0), menor_lance)

    def test_deve_retornar_o_maior_lance(self):
        maior_lance = self.avaliador_leilao_com_muitos_lances.maior_lance
        self.assertEqual(Lance(Usuario('Gui'), 300.0), maior_lance)


    def test_deve_retornar_o_mesmo_valor_para_o_menor_e_o_maior_lance_quando_o_leilao_tiver_um_lance(self):
        menor_lance = self.avaliador_leilao_com_um_lance.menor_lance
        maior_lance = self.avaliador_leilao_com_um_lance.maior_lance

        self.assertEqual(menor_lance, maior_lance)

    def test_deve_retornar_o_numero_de_lances_dados_no_leilao(self):

        leilao = Leilao("Computador")
        leilao.dar_lance(Lance(self.felipe, 50.0))
        leilao.dar_lance(Lance(self.gui, 60.0))
        leilao.dar_lance(Lance(self.felipe, 70.0))
        leilao.dar_lance(Lance(self.gui, 80.0))
        leilao.dar_lance(Lance(self.felipe, 90.0))
        leilao.dar_lance(Lance(self.gui, 95.0))

        self.assertEqual(6, len(leilao))

    def test_deve_retornar_excecao_se_o_lance_dado_for_menor_que_os_que_ja_ocorreram(self):

        lance = Lance(self.gui, 4.0)
        self.assertRaises(ValueError, self.leilao_com_muitos_lances.dar_lance, lance)
