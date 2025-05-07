class BCP:
    def __init__(self, pid, params, tempo_chegada=0):
        self.pid = pid
        self.instrucoes = params.get('instrucoes', [])
        self.instrucao_atual = 0
        self.prioridade = params.get('prioridade', 0)
        self.tempo_chegada = tempo_chegada
        self.tempo_termino = None
        self.tempo_executado = 0      # Tempo real de execução
        self.tempo_bloqueado = 0      # Tempo em estado bloqueado
        self.estado = 'Em Espera'
        
        # Contadores de instruções
        self.instrucoes_executadas = 0      # Total de instruções executadas
        self.instrucoes_desde_block = 0     # Instruções desde o último block
        self.instrucoes_bloqueadas = 0      # Instruções executadas enquanto bloqueado
        
        # Contadores de controle
        self.instrucoes_para_block = 0      # Número de ticks para bloquear
        self.instrucoes_para_end = 0        # Número total de instruções para finalizar
        self.instrucoes_para_unblock = 0    # Número de ticks para desbloquear
        
        print(f"BCP criado para processo {pid} com {len(self.instrucoes)} instruções")

    def esta_finalizado(self):
        # Um processo está finalizado se:
        # 1. Está no estado FINALIZADO
        # 2. OU se tem um end pendente e já executou o total de instruções necessárias
        # 3. OU se chegou ao final das instruções E não tem nenhum end pendente
        if self.estado == 'FINALIZADO':
            return True
            
        if self.instrucoes_para_end > 0:
            # Se tem um end pendente, só finaliza quando executar o total de instruções necessárias
            finalizado = self.instrucoes_executadas >= self.instrucoes_para_end
            if finalizado:
                print(f"Processo {self.pid} finalizado após executar {self.instrucoes_executadas} instruções (total necessário: {self.instrucoes_para_end})")
            return finalizado
            
        # Se não tem end pendente, finaliza quando chegar ao final das instruções
        finalizado = self.instrucao_atual >= len(self.instrucoes)
        if finalizado:
            print(f"Processo {self.pid} finalizado após executar todas as instruções")
        return finalizado

    def proxima_instrucao(self):
        # Se tem um end pendente, verifica se já atingiu o limite
        if self.instrucoes_para_end > 0 and self.instrucoes_executadas >= self.instrucoes_para_end:
            print(f"Processo {self.pid} atingiu {self.instrucoes_executadas} instruções totais, finalizando")
            self.estado = 'FINALIZADO'
            return "END"
            
        # Se o processo está bloqueado, apenas verifica se deve desbloquear
        if self.estado == 'BLOQUEADO':
            self.tempo_bloqueado += 1
            
            # Se instrucoes_para_unblock é 0, o processo está bloqueado indefinidamente
            if self.instrucoes_para_unblock == 0:
                print(f"Processo {self.pid} bloqueado indefinidamente (acumulou {self.tempo_bloqueado} ticks)")
                return "BLOQUEADO"
                
            print(f"Processo {self.pid} acumulou {self.tempo_bloqueado} ticks de bloqueio de {self.instrucoes_para_unblock}")
            
            if self.tempo_bloqueado >= self.instrucoes_para_unblock:
                print(f"Processo {self.pid} atingiu {self.tempo_bloqueado} ticks de bloqueio, desbloqueando")
                self.desbloquear()
                return "PRONTO"
            return "BLOQUEADO"
            
        # Se tem um end pendente, continua executando até atingir o número total de instruções
        if self.instrucoes_para_end > 0:
            self.instrucoes_desde_block += 1
            
            if self.instrucoes_para_block > 0 and self.instrucoes_desde_block >= self.instrucoes_para_block:
                print(f"Processo {self.pid} atingiu {self.instrucoes_desde_block} instruções desde o block, bloqueando")
                self.bloquear()
                return "BLOCK"
            
            # Incrementa o contador de instruções executadas depois de processar
            self.instrucoes_executadas += 1
            
            # Verifica se atingiu o limite após incrementar
            if self.instrucoes_executadas >= self.instrucoes_para_end:
                print(f"Processo {self.pid} atingiu {self.instrucoes_executadas} instruções totais, finalizando")
                self.estado = 'FINALIZADO'
                return "END"
            
            return "EXECUTANDO"
            
        if self.instrucao_atual >= len(self.instrucoes):
            print(f"Processo {self.pid} chegou ao final das instruções")
            return "END"
            
        instrucao = self.instrucoes[self.instrucao_atual]
        print(f"Processo {self.pid} processando instrução {self.instrucao_atual}: {instrucao}")
        
        # Ignora a instrução start, pois ela só indica quando o processo chega na fila de prontos
        if instrucao.startswith("start"):
            self.instrucao_atual += 1
            return "EXECUTANDO"
        
        # Processa as instruções de block e unblock
        if instrucao.startswith("block"):
            try:
                _, ticks_execucao = instrucao.split()
                self.instrucoes_para_block = int(ticks_execucao)
                if self.instrucoes_para_block <= 0:
                    raise ValueError("Número de ticks para block deve ser positivo")
                self.instrucoes_desde_block = 0  # Reseta o contador de instruções desde o block
                print(f"Processo {self.pid} configurado para executar por {self.instrucoes_para_block} ticks antes de bloquear")
            except (ValueError, IndexError) as e:
                print(f"Erro ao processar instrução block: {e}")
        elif instrucao.startswith("unblock"):
            try:
                _, ticks_bloqueio = instrucao.split()
                self.instrucoes_para_unblock = int(ticks_bloqueio)
                if self.instrucoes_para_unblock <= 0:
                    raise ValueError("Número de ticks para unblock deve ser positivo")
                print(f"Processo {self.pid} configurado para ficar bloqueado por {self.instrucoes_para_unblock} ticks")
            except (ValueError, IndexError) as e:
                print(f"Erro ao processar instrução unblock: {e}")
        elif instrucao.startswith("end"):
            try:
                _, instrucoes_necessarias = instrucao.split()
                self.instrucoes_para_end = int(instrucoes_necessarias)
                if self.instrucoes_para_end <= 0:
                    raise ValueError("Número de instruções para end deve ser positivo")
                print(f"Processo {self.pid} aguardando {self.instrucoes_para_end} instruções totais para finalizar")
            except (ValueError, IndexError) as e:
                print(f"Erro ao processar instrução end: {e}")
        
        # Incrementa os contadores apropriados baseado no estado atual
        self.instrucoes_desde_block += 1
        
        # Verifica se deve bloquear
        if self.instrucoes_para_block > 0 and self.instrucoes_desde_block >= self.instrucoes_para_block:
            print(f"Processo {self.pid} atingiu {self.instrucoes_desde_block} instruções desde o block, bloqueando")
            self.bloquear()
            return "BLOCK"
        
        self.instrucao_atual += 1
        # Incrementa o contador de instruções executadas depois de processar
        self.instrucoes_executadas += 1
        
        # Verifica se atingiu o limite após incrementar
        if self.instrucoes_para_end > 0 and self.instrucoes_executadas >= self.instrucoes_para_end:
            print(f"Processo {self.pid} atingiu {self.instrucoes_executadas} instruções totais, finalizando")
            self.estado = 'FINALIZADO'
            return "END"
        
        return instrucao

    def bloquear(self):
        print(f"Processo {self.pid} bloqueado")
        self.estado = 'BLOQUEADO'
        self.instrucoes_para_block = 0  # Reseta o contador de instruções para block
        self.instrucoes_desde_block = 0  # Reseta o contador de instruções desde o block
        self.tempo_bloqueado = 0  # Reseta o contador de tempo bloqueado

    def desbloquear(self):
        print(f"Processo {self.pid} foi desbloqueado")
        self.estado = 'PRONTO'
        self.tempo_bloqueado = 0  # Reseta o contador de tempo bloqueado
        self.instrucoes_para_unblock = 0  # Reseta o contador de tempo para desbloquear

    def finalizar(self, tempo_termino):
        print(f"Processo {self.pid} finalizando no tempo {tempo_termino}")
        self.estado = 'FINALIZADO'
        self.tempo_termino = tempo_termino
        print(f"Processo {self.pid} finalizado com tempo_termino={self.tempo_termino}, tempo_executado={self.tempo_executado}, tempo_bloqueado={self.tempo_bloqueado}, instrucoes_executadas={self.instrucoes_executadas}, instrucoes_para_end={self.instrucoes_para_end}")