import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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
        criacoes = []
        terminos = []
        desbloqueios = []

        for tempo, pid, acao in self.eventos:
            if acao == "CRIAÇÃO":
                criacoes.append((tempo, pid))

            elif acao == "EXEC":
                if em_execucao is not None:
                    if em_execucao[0] != pid:
                        fim = max(tempo, em_execucao[1] + 1)
                        execucoes.append((em_execucao[0], em_execucao[1], fim))
                em_execucao = (pid, tempo)

            elif acao in ("BLOQUEIO", "TERMINO"):
                if acao == "TERMINO":
                    terminos.append((tempo, pid))
                if em_execucao and em_execucao[0] == pid:
                    fim = max(tempo, em_execucao[1] + 1)
                    execucoes.append((pid, em_execucao[1], fim))
                    em_execucao = None

            elif acao == "DESBLOQUEIO":
                desbloqueios.append((tempo, pid))

        if em_execucao:
            fim_simulacao = max(e[0] for e in self.eventos)
            fim = max(fim_simulacao + 1, em_execucao[1] + 1)
            execucoes.append((em_execucao[0], em_execucao[1], fim))

        self._plot_gantt(execucoes, criacoes, terminos, desbloqueios)
    
    def _plot_gantt(self, execucoes, criacoes, terminos, desbloqueios):

        fig, ax = plt.subplots(figsize=(12, 5))

        processos = sorted(set(pid for pid, _, _ in execucoes))
        cmap = plt.get_cmap('tab20')

        legenda_pids = {}

        for i, pid in enumerate(processos):
            if i < 20:
                legenda_pids[pid] = cmap(i)
            else:
                # Fallback aleatório
                random.seed(pid)  # manter reprodutível por PID
                legenda_pids[pid] = (random.random(), random.random(), random.random())

        # Plotar execuções
        for pid, inicio, fim in execucoes:
            cor = legenda_pids[pid]
            ax.broken_barh([(inicio, fim - inicio)], (pid - 0.4, 0.8), facecolors=cor)
            ax.text(inicio + (fim - inicio) / 2, pid, f"P{pid}", va='center', ha='center', color='white', fontsize=8)

        # CRIAÇÃO: triângulo preto com legenda próxima
        for tempo, pid in criacoes:
            ax.plot(tempo, pid, marker='v', color='black', markersize=6)
            ax.text(tempo, pid - 0.25, "CRIADO", ha='center', va='top', fontsize=7, color='black')

        # Mapear fim real por PID
        fim_execucao_por_pid = {}
        for pid, inicio, fim in execucoes:
            if pid not in fim_execucao_por_pid or fim > fim_execucao_por_pid[pid]:
                fim_execucao_por_pid[pid] = fim

        # TERMINO: círculo vermelho no fim real, legenda próxima
        for _, pid in terminos:
            fim_real = fim_execucao_por_pid.get(pid)
            if fim_real:
                ax.plot(fim_real, pid, marker='o', color='red', markersize=6)
                ax.text(fim_real + 0.3, pid, "FIM", ha='left', va='center', fontsize=7, color='red')

        # Legenda
        patches = [mpatches.Patch(color=cor, label=f"P{pid}") for pid, cor in legenda_pids.items()]
        ax.legend(handles=patches, title="Processos", bbox_to_anchor=(1.01, 1), loc='upper left')

        ax.set_xlabel("Tempo (ticks)")
        ax.set_ylabel("Processos")
        ax.set_title("Diagrama de Gantt - Execução dos Processos")
        ax.set_yticks(processos)
        ax.set_yticklabels([f"P{pid}" for pid in processos])
        ax.set_xticks(range(0, max(fim for _, _, fim in execucoes) + 1))
        ax.grid(True, axis='x', linestyle='dotted', alpha=0.6)
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
