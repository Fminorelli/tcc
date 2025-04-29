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
            if proc.timer_bloqueado > 0:
                print(f"Processo {pid} bloqueado ({proc.timer_bloqueado} ticks restantes).")
                proc.timer_bloqueado -= 1
            if proc.timer_bloqueado == 0:
                desbloquear_pids.append(pid)

        for pid in desbloquear_pids:
            print(f"> Processo {pid} desbloqueado.")
            self.lista_processos[pid].desbloquear()
            self.fila_bloqueados.remove(pid)
            self.fila_prontos.append(pid)

    def executar_processo_atual(self):
        if not self.processo_atual:
            return
            
        proc = self.lista_processos[self.processo_atual]
        resultado = proc.proxima_instrucao()
        
        # Incrementa o tempo de execução para qualquer instrução
        proc.tempo_executado += 1
        
        if resultado == "BLOCK":
            print(f"> Processo {proc.pid} será bloqueado.")
            self.fila_bloqueados.append(proc.pid)
            self.processo_atual = None
        elif resultado == "END":
            if proc.estado != 'FINALIZADO':
                proc.finalizar(self.tempo)
                print(f"> Processo {proc.pid} finalizado.")
                # Remove o processo da fila de prontos se estiver lá
                if proc.pid in self.fila_prontos:
                    self.fila_prontos.remove(proc.pid)
                self.processo_atual = None
                # Força o escalonamento do próximo processo
                if self.precisa_escalonar():
                    self.escalonar_proximo()
        elif resultado == "EXECUTANDO":
            # Atualiza o estado do processo para EXECUTANDO
            proc.estado = 'EXECUTANDO'
            # Verifica se o processo deve finalizar
            if proc.esta_finalizado() or proc.tempo_restante_end == 0:
                proc.finalizar(self.tempo)
                print(f"> Processo {proc.pid} finalizado após executar todas as instruções.")
                if proc.pid in self.fila_prontos:
                    self.fila_prontos.remove(proc.pid)
                self.processo_atual = None
                if self.precisa_escalonar():
                    self.escalonar_proximo()
        else:
            print(f"> Executando processo {proc.pid}")
            proc.estado = 'EXECUTANDO'

    def precisa_escalonar(self):
        # Precisa escalonar se:
        # 1. Não há processo atual em execução
        # 2. Há processos na fila de prontos
        # 3. O processo atual não está bloqueado ou finalizado
        if self.processo_atual is None:
            return bool(self.fila_prontos)
        else:
            proc = self.lista_processos[self.processo_atual]
            return (proc.estado in ['BLOQUEADO', 'FINALIZADO'] and bool(self.fila_prontos))

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