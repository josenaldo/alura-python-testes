from unittest import TestCase

from src.leilao.dominio import Usuario, Lance, Leilao

class TestLeilao(TestCase):
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

    def test_nao_deve_permitir_propor_um_lance_se_o_lance_dado_for_menor_que_os_lances_que_ja_ocorreram(self):
        self.leilao.propoe_lances(self.lances)
        lance = Lance(self.felipe, 3.0)
        self.assertRaises(ValueError, self.leilao.propoe, lance)

    # se o leilão não tiver lances, deve permitir propor um lance
    def test_deve_permitir_propor_um_lance_caso_o_leilao_nao_tenha_lances(self):
        self.assertEqual(len(self.leilao), 0)
        self.leilao.propoe(self.lance)
        self.assertEqual(len(self.leilao), 1)

    # se o último usuário for diferente, ele deve permitir propor um lance
    def test_deve_permitir_propor_um_lance_se_o_ultimo_usuario_for_diferente(self):
        self.leilao.propoe_lances(self.lances)
        ultimo_lance = self.leilao.ultimo_lance
        self.assertNotEqual(self.felipe, ultimo_lance.usuario)

        lance = Lance(self.felipe, 350.0)
        self.leilao.propoe(lance)
        self.assertEqual(self.leilao.ultimo_lance, lance)

    # se o último usuário for o mesmo, ele não deve permitir propor um lance
    def test_nao_deve_permitir_propor_um_lance_se_o_ultimo_usuario_for_o_mesmo_usuario(self):
        self.leilao.propoe_lances(self.lances)
        ultimo_lance = self.leilao.ultimo_lance
        self.assertEqual(ultimo_lance.usuario, self.gui)

        lance = Lance(self.gui, 350.0)
        with self.assertRaises(ValueError):
            self.leilao.propoe(lance)


    def test_deve_retornar_o_vencedor_do_leilao(self):
        self.leilao.propoe_lances(self.lances)
        vencedor = self.leilao.vencedor

        self.assertEqual(vencedor, self.gui)

    def test_deve_retornar_none_se_o_leilao_nao_tiver_lances(self):
        vencedor = self.leilao.vencedor
        self.assertIsNone(vencedor)