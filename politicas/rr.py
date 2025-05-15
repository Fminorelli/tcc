from modulos.gerenciador_de_processos.politicaGP import politicaGP

class Rr(politicaGP):
    
    def inicializar(self,bcp_dados, params):
        if 'quantum' in params.keys():
            self.quantum = params['quantum']
            print (f"Quamtum politica= {self.quantum}")

    def selecionar_proximo(self):
        """Seleciona o próximo processo usando a política RR (Round Robin)"""
        if self.fila_prontos:
            proc = self.fila_prontos[0]
            self.fila_prontos.remove(proc)
            return proc 
        else:
            return None
    
    def bloquear(self, processo):
        self.fila_bloqueados.append(processo.pid)
        if processo.pid in self.fila_prontos:
            self.fila_prontos.remove(processo.pid)

    def desbloquear(self,processo):
        self.fila_prontos.append(processo)
        self.fila_bloqueados.remove(processo)
    
    def iniciar (self, processo):
        self.fila_prontos.append(processo)

    def finalizar (self,processo):
        print(f"processo FINALIZADO {processo}")
        if processo in self.fila_prontos:
            self.fila_prontos.remove(processo)
        
    def tick(self,processo):
        print(f">LISTA PRONTOS POLITICA {self.fila_prontos}")
        if self.fila_prontos:
            if int(processo.tempo_executado) % int(self.quantum) == 0:
                print(f"Porcesso atual precisa ROTACIONAR {processo.tempo_executado}  {self.quantum}")
                print(f"Removendo processo {processo.pid}")
                if processo.pid in self.fila_prontos:
                    self.fila_prontos.remove(processo.pid)
                self.fila_prontos.append(processo.pid)
                proc = self.fila_prontos[0]
                return proc if self.fila_prontos else None
            else:
                return None
        else:
            return None