memory_store = {}
MEMORY_WINDOW = 10

def add_to_memory(npc, player, role, text):
    key = (npc, player)
    if key not in memory_store:
        memory_store[key] = []
    memory_store[key].append((role, text))
    if len(memory_store[key]) > 50:
        memory_store[key] = memory_store[key][-50:]

def get_memory(npc, player):
    key = (npc, player)
    if key in memory_store:
        return memory_store[key][-MEMORY_WINDOW:]
    return []