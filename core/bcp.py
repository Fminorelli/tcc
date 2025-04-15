class BCP:
    def __init__(self, pid, params, tempo_chegada=0):
        # Identificador do processo
        self.pid = pid

        # Instruções e controle de execução
        self.instrucoes = params['instrucoes']
        self.instrucao_atual = 0

        # Informações de escalonamento
        self.prioridade = params.get('prioridade', 0)  # pode vir como parâmetro
        self.tempo_chegada = tempo_chegada
        self.tempo_termino = None
        self.tempo_executado = 0  # tempo total em CPU

        # Estado do processo: PRONTO, EXECUTANDO, BLOQUEADO, FINALIZADO
        self.estado = 'PRONTO'

        # Controle de bloqueio
        self.timer_bloqueado = 0

    def esta_finalizado(self):
        return self.instrucao_atual >= len(self.instrucoes)

    def proxima_instrucao(self):
        if not self.esta_finalizado():
            instr = self.instrucoes[self.instrucao_atual]
            self.instrucao_atual += 1
            #self.tempo_executado += 1
            #self.tempo_restante -= 1
            return instr
        return None

    def bloquear(self):
        self.estado = 'BLOQUEADO'
        self.timer_bloqueado = 99999  # ou outro valor alto só para evitar auto-desbloqueio

    def desbloquear(self):
        self.estado = 'PRONTO'
        self.timer_bloqueado = 0

    def finalizar(self, tempo_termino):
        self.estado = 'FINALIZADO'
        self.tempo_termino = tempo_termino