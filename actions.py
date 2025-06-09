# actions.py
from enum import Enum

class AIActions(str, Enum):
    NENHUMA = "nenhuma ação"
    PEGAR_DINHEIRO = "pegar dinheiro"
    DAR_DINHEIRO = "dar dinheiro"
    PEGAR_ITEM = "pegar item"
    DAR_ITEM = "dar item"
    ATACAR = "atacar"
    SEGUIR = "seguir jogador"
    ROTINA = "voltar à rotina"
    DIZER = "Say"
    MONTAR_CAVALO = "montar cavalo"
    DESMONTAR_CAVALO = "desmontar cavalo"
    MOVER_PARA = "mover para"
    MOVER_PARA_CAVALO = "mover para cavalo"
    MOVER_PARA_AUTOR = "mover para autor"
    FUGIR = "fugir"

