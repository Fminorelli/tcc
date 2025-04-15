# core/politicas/FIFO.py
from modulos.gerenciador_de_processos.politicaGP import politicaGP  # Importa a classe politicaGP

class Fifo(politicaGP):  # Herda de politicaGP
    def selecionar_proximo(fila_prontos):
        if fila_prontos:
            return fila_prontos[0]  # Retorna o primeiro processo na fila de prontos
        return None
    
    
    def atualizar_fila(fila_prontos):
        return fila_prontos