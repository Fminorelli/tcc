import sys
import os
import yaml

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from core.core_simulador import simulador
from modulos.gerenciador_de_processos.politicaGP import politicaGP

if __name__ == "__main__":
    def carregar_processos_arquivo(caminho_yaml):
        with open(caminho_yaml, 'r') as f:
            dados = yaml.safe_load(f)

        processos_eventos = []

        for nome_pid, info in dados['gp']['processos'].items():
            pid = int(nome_pid.replace("pid", ""))
            for evento in info['instrucoes']:
                tempo, acao = evento.split()
                processos_eventos.append({
                    'tempo': int(tempo),
                    'pid': pid,
                    'acao': acao
                })

        processos_eventos.sort(key=lambda e: e['tempo'])
        return processos_eventos

    def carregar_politica_arquivo(caminho_yaml):
        with open(caminho_yaml, 'r') as f:
            dados = yaml.safe_load(f)
        
        nome_politica = dados['gp']['config']['politica']['nome']
        print(f"Carregando política: {nome_politica}")  # Depuração para verificar o nome da política
        
        politica = politicaGP.get_politica(nome_politica)
        if politica is None:
            print("Erro ao carregar a política.")
        return politica
    
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    caminho_yaml = os.path.join(base_dir, 'core', 'processos', 'processos.yaml')   

    politica = carregar_politica_arquivo(caminho_yaml)

    if politica:
        simulador_obj = simulador(politica)

        eventos = carregar_processos_arquivo(caminho_yaml)
        simulador_obj.carregar_eventos(eventos)

        while simulador_obj.indice_evento < len(eventos) or simulador_obj.processo_atual or simulador_obj.fila_prontos or simulador_obj.fila_bloqueados:
            simulador_obj.tick()
        
        for p in simulador_obj.lista_processos.keys():
            print("Processo %s rodou por clock: %s" % (p,simulador_obj.lista_processos[p].tempo_executado))
            print("Processo %s finalizou no clock: %s" % (p,simulador_obj.lista_processos[p].tempo_termino))
        