import importlib
from bcp import bcp

modulo = "gp"

class politicaGP(object):
    def __init__(self, config, processos):
        self.config = config
        self.bcps = self.criar_bcps(processos)
        self.processos = list(processos.keys())
        self.prontos = []

    @staticmethod
    def criar_bcps(processos):
        pids = list(processos.keys())
        bcps = {}
        for p in pids:
            bcps.update ({p : bcp(p,processos[p])})
        return bcps

    @staticmethod
    def get_politica(config,processos):
        if config['nome'] == "random":
                politica = "random"

        m = importlib.import_module("%s_%s" % (modulo, politica))
        s = "m.%s%s" % (modulo, politica.capitalize())
        politica = eval(s)

        return politica(config,processos)

    def get_bcps():
        return self.bcps

    @property
    def get_processo(self):
        raise NotImplementedError

    @property
    def bloquear_processo(self,pid):
        raise NotImplementedError

    @property
    def desbloquear_processo(self,pid):
        raise NotImplementedError

    @property
    def tick (self):
        raise NotImplementedError

    @property
    def novo_processo (self,pid):
        raise NotImplementedError

    @property
    def end_processo (self):
        raise NotImplementedError


