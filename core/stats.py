import matplotlib.pyplot as plt
from collections import defaultdict
import random

class AnaliseSimulacao:
    def __init__(self,diagrama_eventos,lista_bcp):
        self.eventos = self._parse_eventos(diagrama_eventos)
        self.bcp = lista_bcp
    
    def _parse_eventos(self, lista_eventos):
        eventos = []
        for linha in lista_eventos:
            partes = linha.strip().split()
            if len(partes) >= 3:
                tempo = int(partes[0])
                pid = int(partes[1])
                acao = partes[2].upper()
                eventos.append((tempo, pid, acao))
        return sorted(eventos, key=lambda x: x[0])

    def gerar_gantt(self):
        execucoes = []
        em_execucao = None  # (pid, inicio)

        for tempo, pid, acao in self.eventos:
            if acao == "EXEC":
                if em_execucao is not None:
                    # Finaliza execução anterior
                    execucoes.append((em_execucao[0], em_execucao[1], tempo))
                em_execucao = (pid, tempo)

            elif acao in ("BLOQUEIO", "TERMINO"):
                if em_execucao and em_execucao[0] == pid:
                    execucoes.append((pid, em_execucao[1], tempo))
                    em_execucao = None

        # Se ainda restar processo em execução no final
        if em_execucao:
            ultimo_tick = max(e[0] for e in self.eventos)
            execucoes.append((em_execucao[0], em_execucao[1], ultimo_tick + 1))

        self._plot_gantt(execucoes)

    def _plot_gantt(self, execucoes):
        cores = ['#a6ce39', '#0052cc', '#c678dd', '#ff7043', '#26a69a']
        fig, ax = plt.subplots()
        for pid, inicio, fim in execucoes:
            ax.broken_barh([(inicio, fim - inicio)], (pid - 0.4, 0.8), facecolors=cores[(pid - 1) % len(cores)])

        ax.set_xlabel("Tempo (ticks)")
        ax.set_ylabel("Processos")
        ax.set_title("Diagrama de Gantt - Execução dos Processos")
        ax.set_yticks(sorted(set(pid for pid, _, _ in execucoes)))
        ax.set_yticklabels([f"P{pid}" for pid in sorted(set(pid for pid, _, _ in execucoes))])
        ax.grid(True)
        plt.tight_layout()
        plt.show()

    def calcular_tempo_medio_retorno(self):
        """Retorno = tempo_termino - tempo_chegada"""
        tempos = []
        for proc in self.bcp:
            if proc.tempo_termino is not None:
                retorno = proc.tempo_termino - proc.tempo_chegada
                tempos.append(retorno)
        return sum(tempos) / len(tempos) if tempos else 0

    def calcular_tempo_medio_espera(self):
        """Espera = tempo de retorno - tempo executado"""
        tempos = []
        for proc in self.bcp:
            if proc.tempo_termino is not None:
                espera = (proc.tempo_termino - proc.tempo_chegada) - proc.tempo_executado
                tempos.append(espera)
        return sum(tempos) / len(tempos) if tempos else 0

    def calcular_vazao(self):
        """Vazão por intervalo de 1000 unidades de tempo"""
        contagem = defaultdict(int)
        for proc in self.bcp:
            if proc.tempo_termino is not None:
                intervalo = proc.tempo_termino // 1000
                contagem[intervalo] += 1

        resultado = {}
        for intervalo in sorted(contagem):
            faixa = f"{intervalo*1000}-{intervalo*1000 + 999}"
            resultado[faixa] = contagem[intervalo]
        return resultado
