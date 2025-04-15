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

        # Simulação de estatísticas (ex: memória/cache)
        self.hit = 0
        self.miss = 0

        # Simulação de I/O ou entrada (se necessário)
        self.entrada = params.get('entrada', '')

        # Tempo restante de execução (para políticas como SRTF)
        self.tempo_restante = len(self.instrucoes)

    def esta_finalizado(self):
        return self.instrucao_atual >= len(self.instrucoes)

    def proxima_instrucao(self):
        if not self.esta_finalizado():
            instr = self.instrucoes[self.instrucao_atual]
            self.instrucao_atual += 1
            self.tempo_executado += 1
            self.tempo_restante -= 1
            return instr
        return None

    def bloquear(self, tempo_bloqueio):
        self.estado = 'BLOQUEADO'
        self.timer_bloqueado = tempo_bloqueio

    def desbloquear(self):
        self.estado = 'PRONTO'
        self.timer_bloqueado = 0

    def finalizar(self, tempo_termino):
        self.estado = 'FINALIZADO'
        self.tempo_termino = tempo_termino