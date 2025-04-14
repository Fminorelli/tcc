
from gerenciador_de_processos import gerenciador_de_processos
from gerenciador_de_memoria import gerenciador_de_memoria
#from import gerenciador_de_memoria
import yaml

def main():
    clock = 0
    with open('processos.yaml') as f:

        data = yaml.load(f, Loader=yaml.FullLoader)

    gp = gerenciador_de_processos(data['gp'])
    #gm = gerenciador_de_memoria(data['gm'])
    bcp = None

    while gp.done != True:
        clock += 1
        #bcp = gp.simular
        bcp = gp.simular(clock)
        #if bcp != None:
            #gm.simular(bcp)



    print ("\nSimulação concluida\n")


if __name__ == "__main__":
    main()
