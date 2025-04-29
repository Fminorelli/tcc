class BCP:
    def __init__(self, pid, params, tempo_chegada=0):
        self.pid = pid
        self.instrucoes = params.get('instrucoes', [])
        self.instrucao_atual = 0
        self.prioridade = params.get('prioridade', 0)
        self.tempo_chegada = tempo_chegada
        self.tempo_termino = None
        self.tempo_executado = 0
        self.estado = 'Em Espera'
        self.timer_bloqueado = 0
        self.tempo_restante_end = 0
        print(f"BCP criado para processo {pid} com {len(self.instrucoes)} instruções")

    def esta_finalizado(self):
        finalizado = self.estado == 'FINALIZADO' or self.instrucao_atual >= len(self.instrucoes)
        if finalizado:
            print(f"Processo {self.pid} está finalizado (estado={self.estado}, instr_atual={self.instrucao_atual}, total_instr={len(self.instrucoes)})")
        return finalizado

    def proxima_instrucao(self):
        if self.instrucao_atual >= len(self.instrucoes):
            print(f"Processo {self.pid} chegou ao final das instruções")
            return "END"
            
        instrucao = self.instrucoes[self.instrucao_atual]
        print(f"Processo {self.pid} processando instrução {self.instrucao_atual}: {instrucao}")
        
        if instrucao.startswith("block"):
            duracao = int(instrucao.split()[1])
            self.bloquear(duracao)
            return "BLOCK"
        elif instrucao.startswith("end"):
            if self.tempo_restante_end == 0:
                # Primeira vez que encontramos o end, extraímos o tempo
                _, tempo = instrucao.split()
                self.tempo_restante_end = int(tempo)
                self.estado = 'EXECUTANDO'  # Marca como executando durante a contagem regressiva
                print(f"Processo {self.pid} iniciou contagem regressiva do end: {self.tempo_restante_end} ticks")
            
            if self.tempo_restante_end > 0:
                self.tempo_restante_end -= 1
                print(f"Processo {self.pid} contagem regressiva do end: {self.tempo_restante_end} ticks")
                return "EXECUTANDO"
            else:
                print(f"Processo {self.pid} finalizando após contagem regressiva do end")
                self.instrucao_atual += 1  # Avança a instrução apenas quando o timer acaba
                self.estado = 'FINALIZADO'
                self.tempo_restante_end = -1  # Marca que o end já foi processado
                return "END"
        else:
            self.instrucao_atual += 1
            return instrucao

    def bloquear(self, duracao):
        print(f"Processo {self.pid} será bloqueado por {duracao} ticks")
        self.estado = 'BLOQUEADO'
        self.timer_bloqueado = duracao
        self.instrucao_atual += 1

    def desbloquear(self):
        print(f"Processo {self.pid} foi desbloqueado")
        self.estado = 'PRONTO'
        self.timer_bloqueado = 0

    def finalizar(self, tempo_termino):
        print(f"Processo {self.pid} finalizando no tempo {tempo_termino}")
        self.estado = 'FINALIZADO'
        self.tempo_termino = tempo_termino
        self.tempo_restante_end = -1  # Garante que o end não será processado novamente