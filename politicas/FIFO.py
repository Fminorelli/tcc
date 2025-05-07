from modulos.gerenciador_de_processos.politicaGP import politicaGP

class Fifo(politicaGP):
    def selecionar_proximo(self):
        """Seleciona o próximo processo usando a política FIFO (First In, First Out)"""
        #print(f"RETORNANDO PROCESSO >>>>>>> {self.fila_prontos[0]}")
        return self.fila_prontos[0] if self.fila_prontos else None
    
    def bloquear(self, processo):
        #print("PROCESSO ADICIONADO NA FILA DE BLOQUEADOS DA POLITICA")
        self.fila_bloqueados.append(processo)
        #print(f"Lista de bloqueados: {self.fila_bloqueados}")
        
        #print("PROCESSO REMOVIDO NA FILA DE PRONTOS DA POLITICA")
        self.fila_prontos.remove(processo)
        #print(f"Lista de prontos: {self.fila_prontos}")

    def desbloquear(self,processo):
        #print("PROCESSO ADICIONADO NA FILA DE PRONTOS DA POLITICA")
        self.fila_prontos.append(processo)
        #print(f"Lista de prontos: {self.fila_prontos}")

        #print("PROCESSO REMOVIDO NA FILA DE BLOQUEADOS DA POLITICA")
        self.fila_bloqueados.remove(processo)
        #print(f"Lista de bloqueados: {self.fila_bloqueados}")
    
    def iniciar (self, processo):
        #print("PROCESSO ADICIONADO NA FILA DE PRONTOS DA POLITICA")
        self.fila_prontos.append(processo)
        #print(f"Lista de prontos: {self.fila_prontos}")

    def finalizar (self,processo):
        #print("PROCESSO REMOVIDO NA FILA DE PRONTOS DA POLITICA")
        self.fila_prontos.remove(processo)
