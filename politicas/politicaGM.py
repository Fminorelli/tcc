import importlib
from bcp import bcp

modulo = "gm"

class politicaGM(object):
    def __init__(self, config, processos):
        self.config = config
        self.processos = list(processos.keys())
        self.prontos = []


    @staticmethod
    def get_politica(config,processos):
        if config['nome'] == "random":
             politica = "random"

        m = importlib.import_module("%s_%s" % (modulo, politica))
        s = "m.%s%s" % (modulo, politica.capitalize())
        politica = eval(s)

        return politica(config,processos)

    @property
    def aloca_pagina(self):
        raise NotImplementedError

    @property
    def desaloca_pagina(self):
        raise NotImplementedError

    @property
    def tick(self):
        raise NotImplementedError