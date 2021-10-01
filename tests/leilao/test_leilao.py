import pytest
from src.leilao.dominio import Usuario, Lance, Leilao
from src.leilao.exceptions import LanceInvalidoError


class TestLeilao:

    @pytest.fixture
    def gui(self):
        return Usuario('Gui')

    @pytest.fixture
    def yuri(self):
        return Usuario('Yuri')

    @pytest.fixture
    def felipe(self):
        return Usuario('Felipe')

    @pytest.fixture
    def lance(self, felipe):
        return Lance(felipe, 400.0)

    @pytest.fixture
    def lances(self, yuri, gui, felipe):
        return [
            Lance(yuri, 45.0),
            Lance(gui, 48.0),
            Lance(yuri, 50.0),
            Lance(gui, 60.0),
            Lance(felipe, 250.0),
            Lance(gui, 300.0)
        ]

    @pytest.fixture
    def menor_lance(self, yuri):
        return Lance(yuri, 45.0)

    @pytest.fixture
    def maior_lance(self, gui):
        return Lance(gui, 300.0)

    @pytest.fixture
    def leilao(self):
        return Leilao("Celular")

    def test_deve_retornar_o_menor_lance(self, leilao, lances, menor_lance):
        leilao.propoe_lances(lances)

        assert menor_lance == leilao.menor_lance

    def test_deve_retornar_o_maior_lance(self, leilao, lances, maior_lance):
        leilao.propoe_lances(lances)

        assert maior_lance == leilao.maior_lance

    def test_deve_retornar_o_mesmo_valor_para_o_menor_e_o_maior_lance_quando_o_leilao_tiver_um_lance(self,
                                                                                                     leilao,
                                                                                                     lance):
        leilao.propoe(lance)
        menor_lance = leilao.menor_lance
        maior_lance = leilao.maior_lance
        assert menor_lance == maior_lance

    def test_deve_retornar_o_numero_de_lances_dados_no_leilao(self, leilao, lances):
        for lance in lances:
            leilao.propoe(lance)

        numero_de_lances = len(leilao)
        assert numero_de_lances == len(lances)

    def test_nao_deve_permitir_propor_um_lance_se_o_lance_dado_for_menor_que_os_lances_que_ja_ocorreram(self,
                                                                                                        leilao,
                                                                                                        lances,
                                                                                                        felipe):
        leilao.propoe_lances(lances)
        lance = Lance(felipe, 3.0)

        with(pytest.raises(LanceInvalidoError)):
            leilao.propoe(lance)

    # se o leilão não tiver lances, deve permitir propor um lance
    def test_deve_permitir_propor_um_lance_caso_o_leilao_nao_tenha_lances(self, leilao, lance):
        assert len(leilao) == 0

        leilao.propoe(lance)

        assert len(leilao) == 1

    # se o último usuário for diferente, ele deve permitir propor um lance
    def test_deve_permitir_propor_um_lance_se_o_ultimo_usuario_for_diferente(self, leilao, lances, felipe):
        leilao.propoe_lances(lances)
        ultimo_lance = leilao.ultimo_lance
        assert felipe != ultimo_lance.usuario

        lance = Lance(felipe, 350.0)
        leilao.propoe(lance)
        assert leilao.ultimo_lance == lance

    # se o último usuário for o mesmo, ele não deve permitir propor um lance
    def test_nao_deve_permitir_propor_um_lance_se_o_ultimo_usuario_for_o_mesmo_usuario(self, leilao, lances, gui):
        leilao.propoe_lances(lances)
        ultimo_lance = leilao.ultimo_lance
        assert ultimo_lance.usuario == gui

        lance = Lance(gui, 350.0)
        with pytest.raises(LanceInvalidoError):
            leilao.propoe(lance)

    def test_deve_criar_o_leilao_no_estado_aberto(self, leilao):
        assert leilao.aberto == True

    def test_deve_fechar_o_leilao_apos_o_encerramento(self, leilao, lances):
        leilao.propoe_lances(lances)
        leilao.encerra()

        assert leilao.aberto == False

    def test_deve_retornar_none_se_o_leilao_nao_tiver_lances(self, leilao):
        vencedor = leilao.vencedor
        assert vencedor == None

    def test_deve_retornar_none_se_o_leilao_nao_tiver_sido_encerrado(self, leilao, lances):
        leilao.propoe_lances(lances)
        vencedor = leilao.vencedor
        assert vencedor == None

    def test_deve_retornar_o_vencedor_do_leilao_apos_o_encerramento(self, leilao, lances, gui):
        leilao.propoe_lances(lances)
        leilao.encerra()
        vencedor = leilao.vencedor

        assert vencedor == gui

