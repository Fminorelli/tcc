from politicas.politicaGM import politicaGM

class gerenciador_de_memoria:

	def __init__(self, params):
		self.params = params
		self.politica = politicaGM.get_politica(self.params['config']['politica'],params['processos'])
		self.atual = ''
		self.time_now = datetime.now()
		self.inst_atual = ""
		self.concluidos = []
		self.processos = list(params['processos'])
		self.paginas = []

def simular(self,bcp):

	acesso = bcp.inst_atual.spli(' ')[0]

	if acesso in self.paginas:
		bcp.hit += 1

	else:
		bcp.miss += 1
		politica.aloca_pagina(acesso)


'''

Toda instrução vai ser tratada como acesso a memória?
Sim

Contabiliza o acesso da instrução nos miss e hits?
Sim

Quem deve fazer a geração de estatistica? GP ou simulador?
Gerar uma classe cada um instacia uma copia e add suas estatiscas, simulador acessa as copias e imprime dps

O arquivo de experimento contem 1 lista de processos pra cada? Ou os 2 trabalham sobre a mesma lista de instruções?
2





Funções do GM:
  - Contar acessos a memoria
  	- Contablizar miss e hit
    - Manter um registro de todos os endereços acessados por cada processo

Manter registro de endereços ou paginas?

Get pagina? Adicionar pagina

Quando desalocar uma pagina? Quem define quantas paginas podem ser alocadas?

'''