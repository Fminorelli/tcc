from modulos.gerenciador_de_processos.politicaGP import politicaGP

class Fifo(politicaGP):
    def selecionar_proximo(self, fila_prontos):
        """Seleciona o próximo processo usando a política FIFO (First In, First Out)"""
        return fila_prontos[0] if fila_prontos else None