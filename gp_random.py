import random
from politicas.politicaGP import politicaGP

class gpRandom(politicaGP):

    def __init__(self, config, processos):
        super().__init__(config, processos)


    def get_processo (self):
        print (self.prontos)
        if len(self.prontos) == 0:
            return None
        else:
            processo = random.choice(self.prontos)
            return self.bcps[processo]

    def tick(self,processo):
        pass

    def novo_processo(self,pid):
        self.prontos.append(pid)
        print ("\nProcesso entrando: %s\n" % pid)

    def bloquear_processo(self,pid):
        self.prontos.remove(pid)
        self.bcps[pid].bloqueado = True
        self.bcps[pid].timer_bloqueado = self.bcps[pid].instrucoes[self.bcps[pid].instrucao_atual].split(" ")[0]

    def desbloquear_processo(self,pid):
        self.prontos.append(pid)
        self.bcps[pid].bloqueado = False

    def end_processo(self,pid):
        self.processos.remove(pid)
        self.prontos.remove(pid)
        del self.bcps[pid]
        print ("Fim do processo: ", pid)
