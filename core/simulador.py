import yaml

class simulador:
    def __init__(self, politica_escalonamento):
        self.politica = politica_escalonamento
        self.lista_processos = {}     # dicionário {pid: BCP}
        self.fila_prontos = []        # lista de pids prontos
        self.fila_bloqueados = []     # lista de pids bloqueados
        self.processo_atual = None
        self.tempo = 0                # clock global
        
    def carregar_processos_arquivo(caminho_yaml):
        with open(caminho_yaml, 'r') as f:
            dados = yaml.safe_load(f)

        processos_eventos = []

        for nome_pid, info in dados['gp']['processos'].items():
            pid = int(nome_pid.replace("pid", ""))
            for evento in info['instrucoes']:
                tempo, acao = evento.split()
                processos_eventos.append({
                    'tempo': int(tempo),
                    'pid': pid,
                    'acao': acao
                })

    # Ordena todos os eventos por tempo de execução
        processos_eventos.sort(key=lambda e: e['tempo'])
        return processos_eventos

    def adicionar_processo(self, bcp):
        self.lista_processos[bcp.pid] = bcp
        self.fila_prontos.append(bcp.pid)

    def tick(self):
        self.tempo += 1
        print(f"\n[TICK {self.tempo}]")

        self._processar_eventos_tick()
        self._atualizar_bloqueados()
        self._executar_processo_atual()

        if self._precisa_escalonar():
            self._escalonar_proximo()

    def _processar_eventos_tick(self):
        while self.indice_evento < len(self.eventos) and self.eventos[self.indice_evento]['tempo'] == self.tempo:
            evento = self.eventos[self.indice_evento]
            self.indice_evento += 1
            pid = evento['pid']
            acao = evento['acao']

            if pid not in self.lista_processos:
                self.lista_processos[pid] = BCP(pid=pid, params={'instrucoes': []})
            
            bcp = self.lista_processos[pid]

            if acao == 'start':
                print(f"PID {pid} adicionado ao sistema.")
                self.fila_prontos.append(pid)
            elif acao == 'block':
                if bcp.estado == 'EXECUTANDO':
                    bcp.bloquear(3)
                    self.fila_bloqueados.append(pid)
                    self.processo_atual = None
            elif acao == 'unblock':
                if pid in self.fila_bloqueados:
                    bcp.desbloquear()
                    self.fila_bloqueados.remove(pid)
                    self.fila_prontos.append(pid)
            elif acao == 'end':
                bcp.finalizar(self.tempo)
                print(f"PID {pid} finalizado.")
                if pid == self.processo_atual:
                    self.processo_atual = None


    def _atualizar_bloqueados(self):
        desbloqueados = []
        for pid in list(self.fila_bloqueados):
            bcp = self.lista_processos[pid]
            bcp.timer_bloqueado -= 1
            if bcp.timer_bloqueado <= 0:
                bcp.desbloquear()
                desbloqueados.append(pid)
                self.fila_bloqueados.remove(pid)
                self.fila_prontos.append(pid)
        if desbloqueados:
            self.politica.atualizar_fila(self.fila_prontos)

    def _executar_processo_atual(self):
        if not self.processo_atual:
            return

        bcp = self.lista_processos[self.processo_atual]
        instrucao = bcp.proxima_instrucao()

        print(f"Executando PID {bcp.pid}: {instrucao}")

        if instrucao == 'IO':
            bcp.bloquear(3)  # por exemplo, bloqueia por 3 ticks
            self.fila_bloqueados.append(bcp.pid)
            self.processo_atual = None
        elif bcp.esta_finalizado():
            bcp.finalizar(self.tempo)
            print(f"PID {bcp.pid} finalizado.")
            self.processo_atual = None
        elif self.politica.quantum_expirado():
            print(f"Quantum expirado para PID {bcp.pid}")
            self.fila_prontos.append(bcp.pid)
            self.processo_atual = None

    def _precisa_escalonar(self):
        return self.processo_atual is None and self.fila_prontos

    def _escalonar_proximo(self):
        pid = self.politica.selecionar_proximo(self.fila_prontos)
        if pid is not None:
            self.fila_prontos.remove(pid)
            self.processo_atual = pid
            self.politica.atualizar_quantum(pid)
            self.lista_processos[pid].estado = 'EXECUTANDO'
            print(f"Escalonado PID {pid}")
    
    def carregar_eventos(self, eventos):
        self.eventos = eventos
        self.indice_evento = 0