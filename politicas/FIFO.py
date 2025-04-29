from modulos.gerenciador_de_processos.politicaGP import politicaGP

class Fifo(politicaGP):
    def selecionar_proximo(self, fila_prontos):
        if fila_prontos:
            return fila_prontos[0]
        return None
