import importlib

class politicaGP:
    def __init__(self):
        self.fila_prontos = []
        self.fila_bloqueados = []
        self.fila_finalizados = []
        self.clock = 0  # se quiser armazenar o tempo atual
        self.quantum = None

    @staticmethod
    def get_politica(nome):
        """Carrega e instancia uma política de escalonamento pelo nome"""
        try:
            modulo = importlib.import_module(f"politicas.{nome}")
            classe_politica = getattr(modulo, nome.capitalize())
            politica = classe_politica()
            print(f"Política {nome.capitalize()} carregada com sucesso!")
            return politica
        except Exception as e:
            print(f"Erro ao carregar a política {nome}: {e}")
            return None
    

    def inicializar(self, bcp_dados, params):
        """Pode ser sobrescrito pelas políticas que usam contexto extra"""
        pass

    def selecionar_proximo(self,processo):
        """Método abstrato que deve ser implementado pelas políticas específicas"""
        raise NotImplementedError("A política deve implementar o método selecionar_proximo.")
    
    def desbloquear(self,processo):
        """Método abstrato que deve ser implementado pelas políticas específicas"""
        raise NotImplementedError("A política deve implementar o método desbloquear.")
    
    def bloquear(self,processo):
        """Método abstrato que deve ser implementado pelas políticas específicas"""
        raise NotImplementedError("A política deve implementar o método bloquear.")
    
    def finalizar(self,processo):
        """Método abstrato que deve ser implementado pelas políticas específicas"""
        raise NotImplementedError("A política deve implementar o método finalizar.")