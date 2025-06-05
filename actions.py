# actions.py
from enum import Enum

class AIActions(str, Enum):
    # SEGUIR = "seguir jogador"
    # MONTAR_CAVALO = "montar cavalo"
    PEGAR_DINHEIRO = "pegar dinheiro"
    DAR_DINHEIRO = "dar dinheiro"
    DAR_ITEM = "dar item"
    ATACAR = "atacar"
    ROTINA = "voltar à rotina"
    DIZER = "Say"
    NENHUMA = "nenhuma ação"
