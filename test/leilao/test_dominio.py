from unittest import TestCase

from src.leilao.dominio import Usuario, Lance, Leilao

class TestBase(TestCase):
    def setUp(self) -> None:
        # Usuários
        self.gui = Usuario('Gui')
        self.yuri = Usuario('Yuri')
        self.felipe = Usuario('Felipe')

        self.lance = Lance(self.felipe, 400.0)

        self.lances = [
            Lance(self.yuri, 45.0),
            Lance(self.gui, 48.0),
            Lance(self.yuri, 50.0),
            Lance(self.gui, 60.0),
            Lance(self.felipe, 250.0),
            Lance(self.gui, 300.0)
        ]
        self.leilao = Leilao("Celular")


class TestLeilao(TestBase):
    def test_deve_retornar_o_menor_lance(self):
        self.leilao.propoe_lances(self.lances)
        menor_lance = self.leilao.menor_lance
        self.assertEqual(menor_lance, self.lances[0])

    def test_deve_retornar_o_maior_lance(self):
        self.leilao.propoe_lances(self.lances)
        maior_lance = self.leilao.maior_lance
        self.assertEqual(self.lances[len(self.lances) -1], maior_lance)

    def test_deve_retornar_o_mesmo_valor_para_o_menor_e_o_maior_lance_quando_o_leilao_tiver_um_lance(self):
        self.leilao.propoe(self.lance)
        menor_lance = self.leilao.menor_lance
        maior_lance = self.leilao.maior_lance
        self.assertEqual(menor_lance, maior_lance)

    def test_deve_retornar_o_numero_de_lances_dados_no_leilao(self):
        for lance in self.lances:
            self.leilao.propoe(lance)

        numero_de_lances = len(self.leilao)
        self.assertEqual(numero_de_lances, len(self.lances))

    def test_deve_retornar_excecao_se_o_lance_dado_for_menor_que_os_que_ja_ocorreram(self):
        self.leilao.propoe_lances(self.lances)
        lance = Lance(self.gui, 3.0)
        self.assertRaises(ValueError, self.leilao.propoe, lance)
