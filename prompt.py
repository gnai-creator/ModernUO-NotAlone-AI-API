from models import FullNPCState
from actions import AIActions

def montar_prompt_para_acao(npc: FullNPCState) -> str:
    memoria_txt = "\n".join(f"- {m}" for m in npc.memory)
    npcs_txt = "\n".join(f"- {n.name}, um {n.role}, está {n.mood}" for n in npc.nearby_npcs)
    intencoes = [f'"{a.value}"' for a in AIActions if a not in [AIActions.DIZER, AIActions.NENHUMA]]

    return (
        f"Você é {npc.name}, um {npc.role} e sua personalidade é {npc.background}. Você está localizado em {npc.location}. "
        f"Você está se sentindo {npc.mood}.\n\n"
        f"Você tem {npc.gold} de ouro.\n\n"
        f"Memórias recentes:\n{memoria_txt if memoria_txt else 'Nenhuma.'}\n\n"
        f"NPCs por perto:\n{npcs_txt if npcs_txt else 'Ninguém próximo.'}\n\n"
        f"As únicas intenções permitidas são: {', '.join(intencoes)}\n\n"
        f"O jogador {npc.player_name} está em {npc.location} e fala: {npc.player_input}.\n\n"
        "Sua resposta DEVE SER APENAS UM BLOCO JSON, SEM EXEMPLOS EXTRAS, SEM TEXTO EXPLICATIVO.\n"
        "NÃO USE COLCHETES NO JSON, APENAS CHAVES E VALORES.\n"
        "Preencha TODOS OS CAMPOS OBRIGATORIAMENTE. NAO adicione alternativas de blocos. NÃO escreva múltiplos blocos json.\n\n"
        "O campo details é opcional, mas só pode conter até 5 palavras.\n\n"
        "{\n"
        "  \"intention\": \"\",\n"
        "  \"target\": \"\",\n"
        "  \"say\": \"\",\n"
        "  \"money_amount\": \"\",\n"
        "  \"item_name\": \"\",\n"
        "  \"details\": \"\"\n"
        "}\n\n"
        "Complete esse único JSON com a ação apropriada."
    )

