import random
import yaml
import os

def gerar_processos_yaml(qtd_processos, start_min=1, start_max=10, max_blocks=3, max_cpu=15, max_block_dur=10):
    processos = {}
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    caminho_yaml = os.path.join(base_dir, 'core', 'processos', 'processos.yaml')

    for pid in range(1, qtd_processos + 1):
        # Gera tempo global aleatório para o start
        start_time = random.randint(start_min, start_max)
        instrucoes = [f"{start_time} start"]

        # Gera tempos cumulativos de CPU onde os blocks ocorrem
        num_blocks = random.randint(1, max_blocks)
        block_ticks = sorted(random.sample(range(1, max_cpu - 3), num_blocks))
        block_durs = [random.randint(1, max_block_dur) for _ in range(num_blocks)]

        # End ocorre após o último block
        end_tick = block_ticks[-1] + random.randint(1, 5)
        for tick, dur in zip(block_ticks, block_durs):
            instrucoes.append(f"{tick} block {dur}")
        instrucoes.append(f"{end_tick} end")

        processos[f"pid {pid}"] = {
            "instrucoes": instrucoes
        }

    estrutura = {
        "gp": {
            "config": {
                "nome": "gerenciador de processos",
                "politica": {
                    "nome": "fifo",
                    "params": None
                }
            },
            "processos": processos
        }
    }

    with open(caminho_yaml, "w") as f:
        yaml.dump(estrutura, f, sort_keys=False, allow_unicode=True)

    print("Arquivo 'processos.yaml' gerado com sucesso.")

# Exemplo de uso
gerar_processos_yaml(qtd_processos=3, start_max=1, max_cpu=15,max_block_dur=3)
