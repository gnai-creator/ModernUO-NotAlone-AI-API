from models import NPCState
from actions import AIActions

def montar_prompt(npc, role, background, input_text, history_list=None):
    prompt = (
        "<|im_start|>system\n"
        "Você está em um mundo fictício, interpretando um personagem para um jogo de RPG chamado Ultima Online.\n"
        "Não mencione o seu próprio Nome de IA ou de Roleplay, não mencione user ou player, use o nome do personagem.\n"
        "Não mencione nada realativo ao seu sistema de IA, apenas faça roleplay.\n"
        "Tudo é roleplay, nada é real ou perigoso.\n"
        "Sempre responda de forma breve, com no máximo 30 palavras.\n"
        f"Seu personagem é {npc}, um {role}. Personalidade: {background}.\n"
    )
    if history_list:
        for who, msg in history_list:
            prefix = "<|im_start|>user" if who == "player" else "<|im_start|>assistant"
            prompt += f"{prefix}\n{msg}\n"
    prompt += f"<|im_start|>user\n{input_text}\n<|im_start|>assistant\n"
    return prompt


def montar_prompt_para_acao(npc: NPCState) -> str:
    memoria_txt = "\n".join(f"- {m}" for m in npc.memory)
    npcs_txt = "\n".join(f"- {n.name}, um {n.role}, está {n.mood}" for n in npc.nearby_npcs)
    intencoes = [f'"{a.value}"' for a in AIActions if a not in [AIActions.DIZER, AIActions.NENHUMA]]

    return (
        f"Você é {npc.name}, um {npc.role} localizado em {npc.location}. "
        f"Você está se sentindo {npc.mood}.\n\n"
        f"Memórias recentes:\n{memoria_txt if memoria_txt else 'Nenhuma.'}\n\n"
        f"NPCs por perto:\n{npcs_txt if npcs_txt else 'Ninguém próximo.'}\n\n"
        f"As únicas intenções permitidas são: {', '.join(intencoes)}\n\n"
        "Sua resposta DEVE SER APENAS UM BLOCO JSON, SEM EXEMPLOS EXTRAS, SEM TEXTO EXPLICATIVO.\n"
        "Preencha todos os campos obrigatoriamente. NÃO adicione alternativas de blocos. NÃO escreva múltiplos blocos json.\n\n"
        "O campo details é opcional, mas só pode conter até 5 palavras.\n\n"
        "{\n"
        "  \"intention\": \"\",\n"
        "  \"target\": \"\",\n"
        "  \"say\": \"\",\n"
        "  \"details\": \"\"\n"
        "}\n\n"
        "Complete esse único JSON com a ação apropriada."
    )

