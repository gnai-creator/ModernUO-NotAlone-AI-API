from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
)

generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    # device=0 if torch.cuda.is_available() else -1
)

app = FastAPI()

class NPCRequest(BaseModel):
    npc: str
    role: str
    background: str
    input: str
    player: str

def montar_prompt(npc, role, background, input_text, history_list=None):
    prompt = (
        "<|im_start|>system\n"
        "Você está em um mundo fictício, interpretando um personagem para um jogo de RPG chamado Ultima Online.\n"
        "Não mencione nada realativo ao seu sistema, ou seu role, apenas faça roleplay.\n"
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


# Memória longa simples (RAM)
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

@app.post("/think")
async def think(req: NPCRequest):
    # Resgata histórico
    history_list = get_memory(req.npc, req.player)
    prompt = montar_prompt(req.npc, req.role, req.background, req.input, history_list)
    output = generator(
        prompt,
        max_new_tokens=40,
        do_sample=True,
        temperature=0.9,
        top_p=0.92,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id
    )[0]['generated_text']
    resposta = output[len(prompt):].strip()
    # Remove possíveis repetições do prefixo
    if resposta.startswith("<|im_start|>assistant"):
        resposta = resposta[len("<|im_start|>assistant"):].strip()
    palavras = resposta.split()
    if len(palavras) > 16:
        resposta = ' '.join(palavras[:16]) + "..."
    resposta = ' '.join(resposta.replace('\n', ' ').replace('\r', ' ').split())
    # Salva o histórico
    add_to_memory(req.npc, req.player, "player", req.input)
    add_to_memory(req.npc, req.player, "npc", resposta)
    return {"action": "Say", "text": resposta}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
