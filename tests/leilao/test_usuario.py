import pytest
from src.leilao.dominio import Usuario, Leilao
from src.leilao.exceptions import SaldoInsuficienteError, LanceInvalidoError

class TestUsuario:

    @pytest.fixture
    def leilao(self):
        return Leilao("Celular")

    @pytest.fixture
    def josenaldo(self):
        return Usuario("Josenaldo", 500)

    @pytest.fixture
    def cassiana(self):
        return Usuario("Cassiana", 1000)

    def deve_iniciar_a_carteira_com_o_valor_passado(self, josenaldo):
        assert josenaldo.carteira == 500

    def test_deve_permitir_propor_um_lance_quando_o_valor_eh_menor_que_o_valor_da_carteira(self, leilao, josenaldo):
        josenaldo.propoe(leilao, 200.0)
        assert josenaldo.carteira == 500

    def test_deve_subtrair_valor_da_carteira_apenas_depois_do_ultimo_lance_dado_pelo_usuario(self, leilao, josenaldo, cassiana):
        josenaldo.propoe(leilao, 100.0)
        cassiana.propoe(leilao, 200.0)
        josenaldo.propoe(leilao, 300.0)
        cassiana.propoe(leilao, 350)
        leilao.encerra()

        assert josenaldo.carteira == 500.0
        assert cassiana.carteira == 650.0

    def test_deve_permitir_propor_lance_quando_o_valor_e_igual_ao_valor_da_carteira(self, leilao, josenaldo):
        josenaldo.propoe(leilao, 500)
        leilao.encerra()
        assert josenaldo.carteira == 0

    def test_nao_deve_permitir_propor_o_lance_quando_o_valor_e_maior_que_o_valor_da_carteira(self, leilao, josenaldo):
        with(pytest.raises(LanceInvalidoError)):
            josenaldo.propoe(leilao, 900)

        assert josenaldo.carteira == 500

    def test_nao_deve_permitir_debitar_um_valor_maior_que_o_saldo_da_conta(self, leilao, josenaldo):
        with(pytest.raises(SaldoInsuficienteError)):
            josenaldo.propoe(leilao, 500)
            josenaldo.debita_carteira(100)
            leilao.encerra()
