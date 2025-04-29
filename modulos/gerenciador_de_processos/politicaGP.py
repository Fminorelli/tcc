import importlib

class politicaGP:
    @staticmethod
    def get_politica(nome):
        try:
            m = importlib.import_module(f"politicas.{nome}")
            s = nome.capitalize()
            politica_class = getattr(m, s)
        except Exception as e:
            print(f"Erro ao carregar a política {nome}: {e}")
            return None
        # Retorna uma instância da política
        politica = politica_class()
        print(f"Política {s} carregada com sucesso!")
        return politica

    def selecionar_proximo(self, fila_prontos):
        raise NotImplementedError("A política deve implementar o método selecionar_proximo.")
