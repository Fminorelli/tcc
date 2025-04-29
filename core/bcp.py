class BCP:
    def __init__(self, pid, params, tempo_chegada=0):
        self.pid = pid
        self.instrucoes = params.get('instrucoes', [])
        self.instrucao_atual = 0
        self.prioridade = params.get('prioridade', 0)
        self.tempo_chegada = tempo_chegada
        self.tempo_termino = None
        self.tempo_executado = 0
        self.estado = 'PRONTO'
        self.timer_bloqueado = 0

    def esta_finalizado(self):
        return self.instrucao_atual >= len(self.instrucoes)

    def proxima_instrucao(self):
        if not self.esta_finalizado():
            instr = self.instrucoes[self.instrucao_atual]
            self.instrucao_atual += 1
            return instr
        return None

    def bloquear(self, timer):
        self.estado = 'BLOQUEADO'
        self.timer_bloqueado = timer

    def desbloquear(self):
        self.estado = 'PRONTO'
        self.timer_bloqueado = 0

    def finalizar(self, tempo_termino):
        self.estado = 'FINALIZADO'
        self.tempo_termino = tempo_termino
