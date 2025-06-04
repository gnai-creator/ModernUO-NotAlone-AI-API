# actions.py
from enum import Enum

class AIActions(str, Enum):
    SEGUIR = "seguir jogador"
    DAR_DINHEIRO = "dar dinheiro"
    MONTAR_CAVALO = "montar cavalo"
    ATACAR = "atacar"
    ROTINA = "voltar à rotina"
    DIZER = "Say"
    NENHUMA = "nenhuma ação"
