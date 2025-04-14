
class politica:

    def __init__(self,modulo,params):
        self.params = params


    def get_politica(modulo,params):

        #print(modulo)
        #print (params)

        if modulo == 'gp':
            if params['nome'] == 'random':
                #return politicas/random(params)
                return gp_random

        elif modulo == 'gm':
            if params['nome'] == 'rr':
                #return politicas/rr(params)
                return "Round Robin"

