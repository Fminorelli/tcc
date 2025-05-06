from core.bcp import BCP

class simulador:
    def __init__(self, politica_escalonamento):
        self.politica = politica_escalonamento
        self.lista_processos = {}
        self.fila_prontos = []
        self.fila_bloqueados = []
        self.processo_atual = None
        self.tempo = 0
        self.eventos = []
        self.indice_evento = 0
        print("Simulador inicializado com política de escalonamento:", politica_escalonamento.__class__.__name__)

    def preparar_processos(self, processos_dict):
        print(f"Preparando {len(processos_dict)} processos")
        for pid, dados in processos_dict.items():
            self.lista_processos[pid] = BCP(pid=pid, params={'instrucoes': dados['instrucoes']})
            print(f"Processo {pid} preparado com {len(dados['instrucoes'])} instruções")

    def tick(self):
        self.tempo += 1
        print(f"\n=== [TICK {self.tempo}] ===")

        # Verifica se o processo atual atingiu seu limite de instruções
        if self.processo_atual:
            proc = self.lista_processos[self.processo_atual]
            if proc.instrucoes_para_end > 0 and proc.instrucoes_executadas >= proc.instrucoes_para_end:
                proc.finalizar(self.tempo)
                print(f"> Processo {proc.pid} finalizado após atingir o limite de instruções.")
                if proc.pid in self.fila_prontos:
                    self.fila_prontos.remove(proc.pid)
                self.processo_atual = None

        # Se não há processo atual ou o processo atual foi finalizado, tenta escalonar
        if not self.processo_atual and self.precisa_escalonar():
            self.escalonar_proximo()

        # Executa o processo atual se houver um
        if self.processo_atual:
            self.executar_processo_atual()

        while self.indice_evento < len(self.eventos) and self.eventos[self.indice_evento]['tempo'] == self.tempo:
            self.processar_eventos_tick()

        self.atualizar_bloqueados()

        print("--- Estado atual ---")
        for pid, proc in self.lista_processos.items():
            print(f"PID {pid}: estado={proc.estado}, exec={proc.tempo_executado}, instr={proc.instrucao_atual}")

        if self.precisa_escalonar():
            self.escalonar_proximo()

    def processar_eventos_tick(self):
        evento = self.eventos[self.indice_evento]
        self.indice_evento += 1
        pid = evento['pid']
        if evento['acao'] == 'start':
            print(f"> Processo {pid} chegou e foi colocado na fila de prontos.")
            self.fila_prontos.append(pid)

    def atualizar_bloqueados(self):
        desbloquear_pids = []
        for pid in list(self.fila_bloqueados):
            proc = self.lista_processos[pid]
            if proc.estado == 'BLOQUEADO':
                print(f"Processo {pid} bloqueado.")
                # Não incrementamos o tempo_bloqueado aqui, pois já é incrementado em proxima_instrucao()
                
                # Executa a próxima instrução para verificar se deve desbloquear
                resultado = proc.proxima_instrucao()
                if resultado == "PRONTO":
                    desbloquear_pids.append(pid)

        for pid in desbloquear_pids:
            print(f"> Processo {pid} desbloqueado.")
            self.fila_bloqueados.remove(pid)
            self.fila_prontos.append(pid)

    def executar_processo_atual(self):
        if not self.processo_atual:
            return
            
        proc = self.lista_processos[self.processo_atual]
        
        # Verifica se o processo já atingiu seu limite de instruções
        if proc.instrucoes_para_end > 0 and proc.instrucoes_executadas >= proc.instrucoes_para_end:
            proc.finalizar(self.tempo)
            print(f"> Processo {proc.pid} finalizado após atingir o limite de instruções.")
            if proc.pid in self.fila_prontos:
                self.fila_prontos.remove(proc.pid)
            self.processo_atual = None
            if self.precisa_escalonar():
                self.escalonar_proximo()
            return
            
        # Executa a próxima instrução
        resultado = proc.proxima_instrucao()
        
        # Se a instrução retornou END, o processo já foi finalizado
        if resultado == "END":
            proc.finalizar(self.tempo)
            print(f"> Processo {proc.pid} finalizado.")
            if proc.pid in self.fila_prontos:
                self.fila_prontos.remove(proc.pid)
            self.processo_atual = None
            if self.precisa_escalonar():
                self.escalonar_proximo()
            return
            
        # Incrementa o tempo de execução para todas as instruções, incluindo BLOCK e PRONTO
        proc.tempo_executado += 1
        
        if resultado == "BLOCK":
            print(f"> Processo {proc.pid} será bloqueado.")
            self.fila_bloqueados.append(proc.pid)
            self.processo_atual = None
        elif resultado == "PRONTO":
            # Processo foi desbloqueado automaticamente
            print(f"> Processo {proc.pid} desbloqueado automaticamente.")
            if proc.pid in self.fila_bloqueados:
                self.fila_bloqueados.remove(proc.pid)
            self.fila_prontos.append(proc.pid)
            self.processo_atual = None
            if self.precisa_escalonar():
                self.escalonar_proximo()
        else:
            print(f"> Executando processo {proc.pid}")
            proc.estado = 'EXECUTANDO'

    def precisa_escalonar(self):
        # Precisa escalonar se:
        # 1. Não há processo atual em execução
        # 2. Há processos na fila de prontos OU há processos em estado PRONTO
        if self.processo_atual is None:
            # Verifica se há processos na fila de prontos ou processos em estado PRONTO
            for pid, proc in self.lista_processos.items():
                if proc.estado == 'PRONTO' and pid not in self.fila_prontos:
                    self.fila_prontos.append(pid)
            return bool(self.fila_prontos)
        else:
            proc = self.lista_processos[self.processo_atual]
            # Verifica se há processos em estado PRONTO que não estão na fila
            for pid, p in self.lista_processos.items():
                if p.estado == 'PRONTO' and pid not in self.fila_prontos:
                    self.fila_prontos.append(pid)
            return (proc.estado in ['BLOQUEADO', 'FINALIZADO', 'PRONTO'] and bool(self.fila_prontos))

    def escalonar_proximo(self):
        if not self.fila_prontos:
            return
            
        pid = self.politica.selecionar_proximo(self.fila_prontos)
        if pid is not None:
            self.fila_prontos.remove(pid)
            self.processo_atual = pid
            print(f"> Escalonado processo {pid} para execução.")

    def carregar_eventos(self, eventos):
        print(f"Carregando {len(eventos)} eventos")
        self.eventos = eventos
        self.indice_evento = 0