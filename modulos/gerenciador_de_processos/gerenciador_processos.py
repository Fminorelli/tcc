import sys
import os
import yaml
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from core.core_simulador import simulador
from modulos.gerenciador_de_processos.politicaGP import politicaGP
from core.bcp import BCP

def carregar_processos_arquivo(caminho_yaml):
    """Carrega e processa o arquivo YAML com a definição dos processos"""
    with open(caminho_yaml, 'r') as f:
        dados = yaml.safe_load(f)

    processos_eventos = []
    processos_definidos = dados['gp']['processos']

    processos_bcp = {}
    for nome_pid, info in processos_definidos.items():
        pid = int(nome_pid.replace("pid", ""))
        instrucoes = info['instrucoes']
        processos_bcp[pid] = {
            'start': None,
            'instrucoes': []
        }
        i = 0
        while i < len(instrucoes):
            tempo_ou_valor, acao = instrucoes[i].split()
            if acao == 'start':
                processos_bcp[pid]['start'] = int(tempo_ou_valor)
                i += 1
            elif acao == 'block':
                duracao, _ = instrucoes[i + 1].split()
                processos_bcp[pid]['instrucoes'].append(f"block {duracao}")
                i += 2
            else:
                processos_bcp[pid]['instrucoes'].append(f"{acao} {tempo_ou_valor}")
                i += 1

    eventos = []
    for pid, dados in processos_bcp.items():
        eventos.append({'tempo': dados['start'], 'pid': pid, 'acao': 'start'})
    eventos.sort(key=lambda e: e['tempo'])

    return eventos, processos_bcp

def carregar_politica_arquivo(caminho_yaml):
    """Carrega a política de escalonamento definida no arquivo YAML"""
    with open(caminho_yaml, 'r') as f:
        dados = yaml.safe_load(f)
    nome_politica = dados['gp']['config']['politica']['nome']
    return politicaGP.get_politica(nome_politica)

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    caminho_yaml = os.path.join(base_dir, 'core', 'processos', 'processos.yaml')

    politica = carregar_politica_arquivo(caminho_yaml)
    if politica:
        simulador_obj = simulador(politica)
        eventos, bcp_dados = carregar_processos_arquivo(caminho_yaml)
        simulador_obj.carregar_eventos(eventos)
        simulador_obj.preparar_processos(bcp_dados)
        print(eventos)
        print(bcp_dados)

        print("\nIniciando simulação...")
        while any(p.estado != 'FINALIZADO' for p in simulador_obj.lista_processos.values()):
            simulador_obj.tick()
            time.sleep(0.5)

        print("\n=== Relatório Final ===")
        for p in simulador_obj.lista_processos.values():
            print(f"Processo {p.pid}:")
            print(f"  - Instruções executadas: {p.instrucoes_executadas}")
            print(f"  - Tempo de execução: {p.tempo_executado} ticks")
            print(f"  - Tempo bloqueado: {p.tempo_bloqueado} ticks")
            print(f"  - Tempo total: {p.tempo_termino} ticks")
            print(f"  - Finalizou no clock: {p.tempo_termino}")