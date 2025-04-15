import importlib

class politicaGP:
    @staticmethod
    def get_politica(nome):
        try:
            print(f"Tentando importar o módulo politicas.{nome}")  # Depuração
            m = importlib.import_module(f"politicas.{nome}")  # Importa o módulo da pasta politicas
            s = nome.capitalize()  # Classe deve ter o nome da política com a primeira letra maiúscula
            politica = getattr(m, s)  # Acessa a classe dentro do módulo, com o nome correto

            print(f"Política {s} carregada com sucesso!")  # Depuração
        except Exception as e:
            print(f"Erro ao carregar a política {nome}: {e}")
            return None
        
        return politica



    def selecionar_proximo(self, fila_prontos):
        raise NotImplementedError("A política deve implementar o método selecionar_proximo.")

    def atualizar_fila(self, fila_prontos):
        return fila_prontos