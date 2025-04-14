
from politicas.politicaGP import politicaGP
import time
import random
from datetime import datetime

class gerenciador_de_processos:

    def __init__(self, params):
        self.params = params
        self.politica = politicaGP.get_politica(self.params['config']['politica'],params['processos'])
        self.done = False
        self.time_now = datetime.now()
        self.inst_atual = None
        self.concluidos = []
        self.processos = list(params['processos'])


    def check_novos_processos(self,clock):
        for p in self.processos:
            if self.params['processos'][p]['instrucoes'][0].split(" ")[0] == str(clock):
                self.politica.novo_processo(p)

    def tick_bloqueados(bcps):
        for b in bcps:
            if b.bloqueado == True:
                b.timer_bloqueado -= 1
                if b.timer_bloqueado == 0:
                    self.politica.desbloqueiar_processo(b.pid)
        self.politica.bcps = bcps


    def simular(self,clock):

        self.check_novos_processos(clock)

        if self.inst_atual == None:
            self.processo = self.politica.get_processo()

        if self.processo == None:
            print("Nenhum processo pronto ainda, clock: %s" % clock)
            self.processo = self.politica.get_processo()
            time.sleep(1)
            return None

            self.tick_bloqueados(self.politica.get_bcps())

        else:

            print ("Processo: %s Instrução sendo consumida: %s  Len insts: %s Inst atual: %s, clock %s" % (self.processo.pid,self.processo.instrucoes[self.processo.instrucao_atual], len(self.processo.instrucoes), self.processo.instrucao_atual,clock))
            self.inst_atual = self.processo.instrucoes[self.processo.instrucao_atual].split(" ")[1]
            self.processo.instrucao_atual += 1
            self.politica.tick(self.processo)

            if self.inst_atual == "block":
                self.politica.bloquear_processo(self.processo.pid)
                self.processo = self.politica.get_processo()

            # ou if instrucao.endswith(' end')
            if self.processo == None:
                print("Nenhum processo pronto ainda, clock: %s" % clock)
               
                return None
            
            if self.processo.instrucao_atual == "end":
                return

            else:
                print(self.processo.instrucao_atual)

                if self.processo.instrucao_atual == len(self.processo.instrucoes):

                    #ao concluir todas as instruções do processo
                    self.politica.end_processo(self.processo.pid)


                    print ('\nConcluiu o processo: %s no tempo %s, clock %s' % (self.processo.pid, datetime.now().strftime("%H:%M:%S"),clock))
                    self.concluidos.append(self.processo.pid)


                    if len(self.processos) == len(self.concluidos):
                        #print ultima instrução ultimo processo
                        #print ("Processo: %s Instrução sendo consumida: %s  Len insts: %s Inst atual: %s" % (self.processo.pid,self.processo.instrucoes[self.processo.instrucao_atual], len(self.processo.instrucoes), self.processo.instrucao_atual))
                        self.done = True
                        print('\nTempo total de execução %s' % (datetime.now()-self.time_now))
                        ordem=''
                        for p in self.concluidos:
                            ordem = ordem+" "+p
                        print("Ordem de conclusão: %s" % ordem.lstrip())
                        return self.processo

                    else:
                        self.processo = self.politica.get_processo()
    


'''

Definir pontos de chamada de get_processo()
    Como encerrar ou bloquear um processo e retornar o bcp anterior? Manter cópia?

Função de solicitar um novo processo na instrução de "block" é responsabilidade do gerenciador ou da politica?

Implementar desbloqueio de processo gp_random

Quem segura o contador de desbloqueio? Bcp ou lista na politica?
    Se for na politica, manter uma lista de bloqueados?
    Se for no bcp, olhar todos os processos e -= 1, checar clock e chamar desbloqueia_processo?
        Mas se a politica que mantem a lista de bcp, essa operação é comum pra todas as politicas? Tick?

- Implementar get bcp list
    Fazer decremento dos processos bloqueados

'''
