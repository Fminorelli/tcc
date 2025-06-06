import sys
import os
import yaml
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from modulos.gerenciador_de_processos.gerenciador_de_processos import simulador
from modulos.gerenciador_de_processos.politicaGP import politicaGP
from core.stats import AnaliseSimulacao


def carregar_processos_arquivo(caminho_yaml):
    """Carrega e processa o arquivo YAML com a definição dos processos"""
    with open(caminho_yaml, 'r') as f:
        dados = yaml.safe_load(f)

    processos_yaml = dados['gp']['processos']
    processos_bcp = {}

    for nome_pid, info in processos_yaml.items():
        pid = int(nome_pid.replace("pid ", ""))
        instrucoes = info['instrucoes']
        processos_bcp[pid] = {
            'start': None,
            'instrucoes': []
        }

        for instrucao in instrucoes:
            
            tempo, acao = instrucao.split(maxsplit=1)
            if acao == 'start':
                processos_bcp[pid]['start'] = int(tempo)
            elif acao =='end':
                processos_bcp[pid]['end'] = int(tempo)
            else:
                processos_bcp[pid]['instrucoes'].append(f"{acao} {tempo}")

    eventos = []
    for pid, dados in processos_bcp.items():
        eventos.append({'tempo': dados['start'], 'pid': pid, 'acao': 'start'})
       
    eventos.sort(key=lambda e: e['tempo'])

    return eventos, processos_bcp


def carregar_politica_arquivo(nome):   
    return politicaGP.get_politica(nome)


if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    caminho_yaml = os.path.join(base_dir, 'core', 'processos', 'processos.yaml')

    """Carrega a política de escalonamento definida no arquivo YAML"""
    with open(caminho_yaml, 'r') as f:
        dados = yaml.safe_load(f)
    nome_politica = dados['gp']['config']['politica']['nome']
    params = dados['gp']['config']['politica']['params']

    politica = carregar_politica_arquivo(nome_politica)
    if politica:
        simulador_gp = simulador(politica)
        eventos, bcp_dados = carregar_processos_arquivo(caminho_yaml)
        #print(f"Eventos {eventos}")
        simulador_gp.carregar_eventos(eventos)
        #print(f"Dados bcp: {bcp_dados}")
        simulador_gp.preparar_processos(bcp_dados)

        
        simulador_gp.politica.inicializar(bcp_dados,params)

        #print("\nIniciando simulação...")
        while any(p.estado != 'FINALIZADO' for p in simulador_gp.lista_processos.values()):
            simulador_gp.tick()
            #time.sleep(0.3)
        

        '''for p in simulador_gp.lista_processos.values():
            print(f"Processo {p.pid}:")
            print(f"  - Instruções executadas: {p.instrucoes_totais}")
            print(f"  - Tempo de execução: {p.tempo_executado} ticks")
            print(f"  - Tempo Termino: {p.tempo_termino} ticks")
            print(f"  - Tempo bloqueado: {p.tempo_bloqueado_total} ticks")'''
        

        analise = AnaliseSimulacao(simulador_gp.diagrama_eventos, simulador_gp.lista_processos.values())
        
        with open(os.path.join(base_dir, 'core', 'processos','saida.txt'),'w+', encoding="utf-8") as f:
            f.write("=== Relatório Final ===\n")
            f.write("Chaveamentos: %s\n" %simulador_gp.chaveamentos)

            f.write("Tempo Médio de Retorno: %s\n" % analise.calcular_tempo_medio_retorno())
            f.write("Tempo Médio de Espera: %s\n" % analise.calcular_tempo_medio_espera())
            f.write("Vazão por intervalo de 1000 ticks:\n")
            for intervalo, qtd in analise.calcular_vazao().items():
                f.write("  %s: %s processo(s)\n" %(intervalo,qtd))
            f.write("Termino: %s\n" % simulador_gp.processos_finalizados)


        #print("\nDiagrama de Eventos")
        #for e in simulador_gp.diagrama_eventos:
        #    print(e)
        analise.gerar_gantt()

        
