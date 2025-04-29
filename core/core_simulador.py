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

    def tick(self):
        self.tempo += 1
        print(f"\n[TICK {self.tempo}]")

        self._executar_processo_atual()

        if self.indice_evento < len(self.eventos) and self.eventos[self.indice_evento]['tempo'] == self.tempo:
            print(f"Evento programado: {self.eventos[self.indice_evento]['acao']} (PID {self.eventos[self.indice_evento]['pid']})")
            self._processar_eventos_tick()
            
        else:
            print("Nenhum evento programado.")
            print(f"Processo Atual: {self.processo_atual}")

        self._atualizar_bloqueados()

        if self._precisa_escalonar():
            self._escalonar_proximo()

    def _processar_eventos_tick(self):
        for b in self.lista_processos.keys():
            print(f"pid: {self.lista_processos[b].pid} tempo executado:{self.lista_processos[b].tempo_executado}")

        # Processa todos os eventos deste tick
        if self.indice_evento < len(self.eventos) and self.eventos[self.indice_evento]['tempo'] == self.tempo:
            evento = self.eventos[self.indice_evento]
            self.indice_evento += 1
            pid = evento['pid']
            acao = evento['acao']

            if pid not in self.lista_processos and acao == 'start':
                self.lista_processos[pid] = BCP(pid=pid, params={'instrucoes': []})
                print(f"> Processo {pid} adicionado ao sistema.")
                self.fila_prontos.append(pid)

            elif acao == 'block':
                tempo_bloqueio = evento['bloqueio_duracao']
                
                self.lista_processos[self.processo_atual].bloquear(tempo_bloqueio)
                print(f"> Bloqueando processo {pid} por {tempo_bloqueio} ticks.")
                self.fila_bloqueados.append(pid)
                self.processo_atual = None

            elif acao == 'end':
                if self.lista_processos[self.processo_atual].estado != 'FINALIZADO':
                    print(f"> Processo {pid} finalizado.")
                    self.lista_processos[self.processo_atual].finalizar(self.tempo)
                    print(f">> Processo atual {self.processo_atual}, pid evento: {pid}")
                    if pid == self.processo_atual:
                        self.processo_atual = None

    def _atualizar_bloqueados(self):
        desbloquear_pids = []
        for pid in list(self.fila_bloqueados):
            self.lista_processos[self.processo_atual] = self.lista_processos[pid]
            if self.lista_processos[self.processo_atual].timer_bloqueado > 0:
                print(f"Processo {pid} está bloqueado (restam {self.lista_processos[self.processo_atual].timer_bloqueado} clocks).")
                self.lista_processos[self.processo_atual].timer_bloqueado -= 1
            if self.lista_processos[self.processo_atual].timer_bloqueado == 0:
                desbloquear_pids.append(pid)

        for pid in desbloquear_pids:
            print(f"> Processo {pid} desbloqueado e movido para fila de prontos.")
            self.lista_processos[self.processo_atual] = self.lista_processos[pid]
            self.lista_processos[self.processo_atual].desbloquear()
            self.fila_bloqueados.remove(pid)
            self.fila_prontos.append(pid)

    def _executar_processo_atual(self):
        if not self.processo_atual:
            return
        instrucao = self.lista_processos[self.processo_atual].proxima_instrucao()
        if self.processo_atual:
            print(f"Executando processo {self.lista_processos[self.processo_atual].pid}")
            self.lista_processos[self.processo_atual].tempo_executado += 1
        #if self.lista_processos[self.processo_atual].esta_finalizado():
        #    self.lista_processos[self.processo_atual].finalizar(self.tempo)
        #    print(f"> Processo {self.lista_processos[self.processo_atual].pid} finalizado.")
        #   self.processo_atual = None

    def _precisa_escalonar(self):
        return self.processo_atual is None and bool(self.fila_prontos)

    def _escalonar_proximo(self):
        pid = self.politica.selecionar_proximo(self.fila_prontos)
        if pid is not None:
            self.fila_prontos.remove(pid)
            self.processo_atual = pid
            print(f"> Escalonado processo {pid} para execução.")

    def carregar_eventos(self, eventos):
        self.eventos = eventos
        self.indice_evento = 0

    
    def carregar_eventos(self, eventos):
        self.eventos = eventos
        self.indice_evento = 0