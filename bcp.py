
class bcp:

    def __init__(self,pid,params):
        self.pid = pid
        self.instrucao_atual = 0
        self.instrucoes = params['instrucoes']
        self.entrada = ''
        self.prioridade = 0
        self.miss = 0
        self.hit = 0
        self.bloqueado = False
        self.timer_bloqueado = 0

