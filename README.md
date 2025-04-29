Formato do yaml nao apresenta ticks por instrução, mas sim o relogio global onde ocorre cada evento

Como controlar o processo atual?

Alem do quantum o que mais falta no BCP?

tratar block unblock como uma instrução só

criar função de consulta de bloqueio no simulador para politica

Feito:
    * Ignorar eventos de unblock na carga de eventos, ja que estes indicam o timer interno de block do processo
    * BCP do processo é criado na instrução de start