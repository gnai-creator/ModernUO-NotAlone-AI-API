def montar_prompt_para_acao(npc: NPCState) -> str:
    memoria_txt = "\n".join(f"- {m}" for m in npc.memory)
    npcs_txt = "\n".join(f"- {n.name}, um {n.role}, está {n.mood}" for n in npc.nearby_npcs)

    return (
        f"Você é {npc.name}, um {npc.role} localizado em {npc.location}. "
        f"Você está se sentindo {npc.mood}.\n\n"
        f"Memórias recentes:\n{memoria_txt if memoria_txt else 'Nenhuma.'}\n\n"
        f"NPCs por perto:\n{npcs_txt if npcs_txt else 'Ninguém próximo.'}\n\n"
        "Decida sua próxima ação com base no contexto. Responda no seguinte formato JSON:\n"
        "{\n"
        "  \"intention\": \"\",\n"
        "  \"target\": \"\",\n"
        "  \"say\": \"\",\n"
        "  \"details\": \"\"\n"
        "}"
    )