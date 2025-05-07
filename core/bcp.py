class BCP:
    def __init__(self, pid, dados):
        self.pid = pid
        self.instrucoes = dados.get('instrucoes', [])
        self.instrucao_atual = 0
        self.prioridade = dados.get('prioridade', 0)
        self.tempo_chegada = dados['start']
        self.instrucoes_totais = dados['end']
        self.tempo_termino = None
        self.tempo_executado = 0      # Tempo real de execução
        self.tempo_bloqueado_total = 0      # Tempo em estado bloqueado total
        
        self.estado = 'EM ESPERA'
        
        self.tempo_bloqueado = 0      # Tempo em estado bloqueado
        self.tick_block = 0      # Instruções executadas ate bloquear
        self.timer_unblock = 0    # Número de ticks para desbloquear
        
        print(f"BCP criado para processo {pid} com {len(self.instrucoes)} instruções")

       
    def proxima_instrucao(self):
        if self.instrucao_atual < len (self.instrucoes):
            instrucao = self.instrucoes[self.instrucao_atual]
            print(f"Processo {self.pid} processando instrução {self.instrucao_atual}: {instrucao}")
            try:
                _, timer_unblock, tempo_block = instrucao.split()
                self.timer_unblock = timer_unblock
                self.tick_block = tempo_block
                self.instrucao_atual += 1

            except (ValueError, IndexError) as e:
                print(f"Erro ao processar instrução block: {e}")
        else:
            print(f"Processo {self.pid} ja consumiu sua ultima instrução")

    def finalizar(self, tempo_termino):
        self.estado = "FINALIZADO"
        self.tempo_termino = tempo_termino
    
    def bloquear(self):
        print(f"Processo {self.pid} bloqueado")
        self.estado = 'BLOQUEADO'

    def desbloquear(self):
        print(f"Processo {self.pid} foi desbloqueado")
        self.tempo_bloqueado = 0
        self.proxima_instrucao()
        self.estado = 'PRONTO'