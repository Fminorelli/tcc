import yaml
from core.bcp import BCP

class simulador:
    def __init__(self, politica_escalonamento):
        self.politica = politica_escalonamento
        self.lista_processos = {}  # dicionário {pid: BCP}
        self.fila_prontos = []     # lista de pids prontos
        self.fila_bloqueados = []  # lista de pids bloqueados
        self.processo_atual = None
        self.tempo = 0             # clock global
        self.eventos = []
        self.indice_evento = 0

    def carregar_processos_arquivo(self, caminho_yaml):
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
        self.eventos = processos_eventos
        self.indice_evento = 0

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
                    bcp.bloquear()
                    self.fila_bloqueados.append(pid)
                    print(f"Bloqueando PID {pid}")
                    self.processo_atual = None

            elif acao == 'unblock':
                if pid in self.fila_bloqueados:
                    print(f"Desbloqueando PID {pid}")
                    bcp.desbloquear()
                    self.fila_bloqueados.remove(pid)
                    self.fila_prontos.append(pid)

            elif acao == 'end':
                if bcp.estado != 'FINALIZADO':
                    print(f"PID {pid} finalizado.")
                    bcp.finalizar(self.tempo)
                    if pid == self.processo_atual:
                        self.processo_atual = None

        print(f"Processo atual: {self.processo_atual}")
    
    def _atualizar_bloqueados(self):
        # Se todos os unblock forem via evento, não é necessário atualizar os timers.
        pass

    def _executar_processo_atual(self):
        if not self.processo_atual:
            return

        bcp = self.lista_processos[self.processo_atual]
        instrucao = bcp.proxima_instrucao()

        # Verifica se a instrução é válida
        if instrucao:
            print(f"Executando PID {bcp.pid}: {instrucao}")
            bcp.tempo_executado += 1

        # Verifica se o processo está finalizado após a execução da instrução
        if bcp.esta_finalizado():
            bcp.finalizar(self.tempo)
            print(f"PID {bcp.pid} finalizado.")
            self.processo_atual = None

    def _precisa_escalonar(self):
        return self.processo_atual is None and self.fila_prontos

    def _escalonar_proximo(self):
        pid = self.politica.selecionar_proximo(self.fila_prontos)
        if pid is not None:
            self.fila_prontos.remove(pid)
            self.processo_atual = pid
            print(pid)
            self.lista_processos[pid].estado = 'EXECUTANDO'
            print(f"Escalonado PID {pid}")
            print("Processo Atual: %s" % self.processo_atual)
    
    def carregar_eventos(self, eventos):
        self.eventos = eventos
        self.indice_evento = 0