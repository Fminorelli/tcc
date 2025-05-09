from core.bcp import BCP

class simulador:
    def __init__(self, politica_escalonamento):
        self.politica = politica_escalonamento
        self.lista_processos = {}
        self.fila_prontos = []
        self.fila_bloqueados = []
        self.processos_finalizados = []
        self.processo_atual = None
        self.tempo = 0
        self.eventos = []
        self.chaveamentos = 0
        self.diagrama_eventos = []
        print("Simulador inicializado com política de escalonamento:", politica_escalonamento.__class__.__name__)



    def carregar_eventos(self, eventos):
        print(f"Carregando {len(eventos)} eventos")
        self.eventos = eventos

    def verifica_novos(self):
        for evento in self.eventos:
            if evento['tempo'] == self.tempo:
                print(f"> Processo {evento['pid']} chegou e foi colocado na fila de prontos.")
                self.diagrama_eventos.append(f"{self.tempo} {evento['pid']} CRIAÇÃO")
                self.fila_prontos.append(evento['pid'])
                ########################################################
                self.politica.iniciar(evento['pid'])
                ########################################################

    def preparar_processos(self, processos_dict):
        print(f"Preparando {len(processos_dict)} processos")
        for pid, dados in processos_dict.items():
            #Cria BCP
            self.lista_processos[pid] = BCP(pid=pid, dados=dados)
            #Carrega primeira instrução
            self.lista_processos[pid].proxima_instrucao()
            print(f"Processo {pid} preparado com {len(dados['instrucoes'])} instruções")
      
    def tick(self):
        self.tempo += 1
        print(f"\n=== [TICK {self.tempo}] ===")
        
        self.verifica_novos()
        self.atualizar_bloqueados()
        
        if self.processo_atual:
            self.executar_processo_atual()

        if self.precisa_escalonar():
            self.escalonar_proximo()

        print("--- Estado atual ---")
        for pid, proc in self.lista_processos.items():
            print(
                f"PID {pid}: estado={proc.estado}, exec={proc.tempo_executado}, instr={proc.instrucao_atual} | "
                f"executadas={proc.tempo_executado}, prox_block={proc.tick_block}, "
                f"unblock_em={proc.timer_unblock}, bloqueado_por={proc.tempo_bloqueado}")
            
    def atualizar_bloqueados(self):
        desbloquear_pids = []
        for pid in list(self.fila_bloqueados):
            proc = self.lista_processos[pid]
            if proc.estado == 'BLOQUEADO':
                self.lista_processos[pid].tempo_bloqueado += 1
                self.lista_processos[pid].tempo_bloqueado_total += 1

                if int(proc.timer_unblock) == int(proc.tempo_bloqueado):
                    self.diagrama_eventos.append(f"{self.tempo} {proc.pid} DESBLOQUEIO")
                    desbloquear_pids.append(proc.pid)

        for pid in desbloquear_pids:
            self.lista_processos[pid].desbloquear()
            self.fila_bloqueados.remove(pid)
            self.fila_prontos.append(pid)
            ######################################################
            self.politica.desbloquear(pid)
            ########################################################
            
    
    def precisa_escalonar(self):
        if self.processo_atual is None:
            # Verifica se há processos na fila de prontos ou processos em estado PRONTO
            for pid, proc in self.lista_processos.items():
                if proc.estado == 'PRONTO' and pid not in self.fila_prontos:
                    self.fila_prontos.append(pid)
            return bool(self.fila_prontos)
    
    def escalonar_proximo(self):             
        pid = self.politica.selecionar_proximo()
        print(f"LISTA DE PRONTOS SIMULADOR: {self.fila_prontos}")
        if pid is not None:
            self.chaveamentos += 1
            self.fila_prontos.remove(pid)
            self.processo_atual = pid
            self.diagrama_eventos.append(f"{self.tempo} {pid} EXEC")
            print(f"> Escalonado processo {pid} para execução.")
            self.executar_processo_atual()

    def executar_processo_atual(self):

        proc = self.lista_processos[self.processo_atual]
        
        # Incrementa o tempo de execução para todas as instruções
        proc.tempo_executado += 1

        if int(proc.tick_block) == int(proc.tempo_executado):
            self.fila_bloqueados.append(proc.pid)
            self.diagrama_eventos.append(f"{self.tempo} {proc.pid} BLOQUEIO")
            self.lista_processos[proc.pid].bloquear()
            self.processo_atual = None
            ########################################################
            self.politica.bloquear(proc.pid)
            ########################################################
        else:
            print(f"> Executando processo {proc.pid}")
            proc.estado = 'EXECUTANDO'

        # Verifica se o processo já atingiu seu limite de instruções
        if self.processo_atual:
            if int(proc.tempo_executado) == int(proc.instrucoes_totais):
                proc.finalizar(self.tempo)
                print(f"> Processo {proc.pid} finalizado após atingir o limite de instruções.")
                self.diagrama_eventos.append(f"{self.tempo} {proc.pid} TERMINO")
                self.processos_finalizados.append(proc.pid)
                if proc.pid in self.fila_prontos:
                    self.fila_prontos.remove(proc.pid)
                self.processo_atual = None
                ########################################################
                self.politica.finalizar(proc.pid)
                ########################################################
                
                '''if self.precisa_escalonar():
                    self.escalonar_proximo()
                return'''
