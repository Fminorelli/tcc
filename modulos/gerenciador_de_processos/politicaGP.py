import importlib

class politicaGP:
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

    def selecionar_proximo(self, fila_prontos):
        """Método abstrato que deve ser implementado pelas políticas específicas"""
        raise NotImplementedError("A política deve implementar o método selecionar_proximo.")