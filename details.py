from enum import Enum

class AIDetails(str, Enum):
    NENHUMA = "nenhuma"
    PEGAR_DINHEIRO = "pegar"
    DAR_DINHEIRO = "dar"
    PEGAR_ITEM = "pegar"
    DAR_ITEM = "dar"
    ATACAR = "atacar"
    SEGUIR = "seguir"
    ROTINA = "rotina"
    DIZER = "dizer"
    MONTAR_CAVALO = "montar"
    DESMONTAR_CAVALO = "desmontar"
    MOVER_PARA = "mover"
    MOVER_PARA_CAVALO = "mover"
    MOVER_PARA_AUTOR = "mover"
    FUGIR = "fugir"
