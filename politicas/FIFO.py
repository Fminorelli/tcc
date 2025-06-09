from modulos.gerenciador_de_processos.politicaGP import politicaGP

class Fifo(politicaGP):

    def inicializar(self, bcp_dados, params):
        pass

    def selecionar_proximo(self):
        return self.fila_prontos[0] if self.fila_prontos else None
    
    def bloquear(self, processo):
        self.fila_bloqueados.append(processo.pid)
        self.fila_prontos.remove(processo.pid)
        return True

    def desbloquear(self,processo):
        self.fila_prontos.append(processo)
        self.fila_bloqueados.remove(processo)
    
    def iniciar (self, processo):
        self.fila_prontos.append(processo)

    def finalizar (self,processo):
        self.fila_prontos.remove(processo)

    def tick(self,processo):
        pass