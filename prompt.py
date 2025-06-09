from models import FullNPCState
from actions import AIActions


def montar_prompt_para_acao(npc: FullNPCState) -> str:
    # Limita memória e npcs antes de gerar string
    mem_limit = npc.memory[-3:] if npc.memory else []
    npcs_limit = npc.nearby_npcs[:2] if npc.nearby_npcs else []

    memoria_txt = "\n".join(f"- {m}" for m in mem_limit)
    npcs_txt = "\n".join(f"- {n.name}, um {n.role}, está {n.mood}" for n in npcs_limit)
    intencoes = [f'"{a.value}"' for a in AIActions if a not in [AIActions.DIZER, AIActions.NENHUMA]]
    gold = str(npc.item_amount) if npc.item_amount and str(npc.item_amount).isdigit() else "0"


    return (
        f"Você é {npc.name}, um {npc.role} e sua personalidade é {npc.background}. "
        f"Você está se sentindo {npc.mood}.\n\n"
        f"Você tem {gold} de moedas de ouro.\n\n"
        f"Memórias recentes:\n{memoria_txt if memoria_txt else 'Nenhuma.'}\n\n"
        f"NPCs por perto:\n{npcs_txt if npcs_txt else 'Ninguém próximo.'}\n\n"
        f"As únicas intenções permitidas são: {', '.join(intencoes)}\n\n"
        f"O jogador {npc.player_name} e fala: {npc.player_input}.\n\n"
        "Sua resposta DEVE SER APENAS UM BLOCO JSON, SEM EXEMPLOS EXTRAS, SEM TEXTO EXPLICATIVO.\n"
        "NÃO USE COLCHETES NO JSON, APENAS CHAVES E VALORES.\n"
        "Preencha TODOS OS CAMPOS OBRIGATORIAMENTE. NAO adicione alternativas de blocos. NÃO escreva múltiplos blocos json.\n\n"
        "Responda SOMENTE com o seguinte JSON válido, COM TODAS AS CHAVES E VALORES preenchidos:\n"
        "{\n"
        "  \"intention\": \"\",\n"
        "  \"target\": \"\",\n"
        "  \"say\": \"\",\n"
        "  \"item_amount\": \"\",\n"
        "  \"item_name\": \"\",\n"
        "}\n\n"
        "Complete esse único JSON com a ação apropriada COM TODAS AS CHAVES E VALORES preenchidos:\n"
    )
