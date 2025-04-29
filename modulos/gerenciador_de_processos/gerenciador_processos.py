
import sys
import os
import yaml
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from core.core_simulador import simulador
from modulos.gerenciador_de_processos.politicaGP import politicaGP

def carregar_processos_arquivo(caminho_yaml):
    with open(caminho_yaml, 'r') as f:
        dados = yaml.safe_load(f)

    processos_eventos = []
    for nome_pid, info in dados['gp']['processos'].items():
        pid = int(nome_pid.replace("pid", ""))
        instrucoes = info['instrucoes']
        i = 0
        while i < len(instrucoes):
            tempo_ou_bloqueio, acao = instrucoes[i].split()
            if acao == 'block':
                tempo_bloqueio, _ = instrucoes[i + 1].split()
                processos_eventos.append({
                    'tempo': int(tempo_ou_bloqueio),
                    'pid': pid,
                    'acao': 'block',
                    'bloqueio_duracao': int(tempo_bloqueio)
                })
                i += 2
            else:
                processos_eventos.append({
                    'tempo': int(tempo_ou_bloqueio),
                    'pid': pid,
                    'acao': acao
                })
                i += 1

    processos_eventos.sort(key=lambda e: e['tempo'])
    return processos_eventos

def carregar_politica_arquivo(caminho_yaml):
    with open(caminho_yaml, 'r') as f:
        dados = yaml.safe_load(f)
    nome_politica = dados['gp']['config']['politica']['nome']
    politica = politicaGP.get_politica(nome_politica)
    if politica is None:
        print("Erro ao carregar a política.")
    return politica

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    caminho_yaml = os.path.join(base_dir, 'core', 'processos', 'processos.yaml')

    politica = carregar_politica_arquivo(caminho_yaml)
    if politica:
        simulador_obj = simulador(politica)
        eventos = carregar_processos_arquivo(caminho_yaml)
        simulador_obj.carregar_eventos(eventos)

        while simulador_obj.indice_evento < len(eventos) or simulador_obj.processo_atual or simulador_obj.fila_prontos or simulador_obj.fila_bloqueados:
            simulador_obj.tick()
            time.sleep(1)

        for p in simulador_obj.lista_processos.keys():
            print(f"Processo {p} rodou por clock: {simulador_obj.lista_processos[p].tempo_executado}")
            print(f"Processo {p} finalizou no clock: {simulador_obj.lista_processos[p].tempo_termino}")
