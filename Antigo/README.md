
Feito:
    * Ignorar eventos de unblock na carga de eventos, ja que estes indicam o timer interno de block do processo
    * BCP do processo é criado na instrução de start
    * tratar block unblock como uma instrução só
    
A fazer 
    - * Inicializar lista de controle nas politicas
    - * Metodos block e unblock politicas
    - * Inserir callbacks das politicas
    - * Bloqueio deve agir como end?

- Ao carregar primeiro bloqueio sobrescreve o segundo e nao contabiliza a primeira contagem
- Ultimo processo finaliza 1 clock após o previsto

    Revisar rotina de bloqueio, para que bloqueie antes de carregar proxima instrução
