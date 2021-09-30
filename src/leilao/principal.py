from src.leilao.dominio import Usuario, Leilao, Lance, Avaliador

gui = Usuario('Gui')
yuri = Usuario('Yuri')

lances_do_yuri = [Lance(yuri, 45.0), Lance(yuri, 50.0), Lance(yuri, 250.0)]
lances_do_gui = [Lance(gui, 48.0), Lance(gui, 60.0), Lance(gui, 300.0)]

leilao = Leilao("Celular")

leilao.lances.extend(lances_do_gui)
leilao.lances.extend(lances_do_yuri)

for lance in leilao.lances:
    print(f"O usuário {lance.usuario.nome} deu um lance de R$ {lance.valor:.2f}")


avaliador = Avaliador(leilao)

print(f'Menor lance: {avaliador.menor_lance}')
print(f'Maior lance: {avaliador.maior_lance}')