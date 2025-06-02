from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import uvicorn

# 1. Carregue seu modelo em português, ex: GPT-2 português
MODEL_NAME = "pierreguillou/gpt2-small-portuguese"  # Ou outro da Hugging Face

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

app = FastAPI()

class NPCRequest(BaseModel):
    npc: str
    role: str
    background: str
    input: str
    history: str = ""  # Opcional: últimas falas, se quiser

def montar_prompt(npc, role, background, input_text, history=""):
    prompt = (
        f"Você é {npc}, um {role}. Personalidade: {background}.\n"
    )
    if history:
        prompt += f"Histórico recente: {history}\n"
    prompt += f"Jogador diz: \"{input_text}\"\n"
    prompt += f"Responda como {npc}:"
    return prompt

@app.post("/think")
async def think(req: NPCRequest):
    prompt = montar_prompt(
        req.npc,
        req.role,
        req.background,
        req.input,
        req.history
    )
    # Gere a resposta
    output = generator(
        prompt,
        max_length=128,
        do_sample=True,
        temperature=0.9,
        top_p=0.92,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id
    )[0]['generated_text']
    # Extraia só a resposta (retire o prompt do início)
    resposta = output[len(prompt):].strip()
    # Limpeza básica
    if resposta.startswith(f"{req.npc}:"):
        resposta = resposta[len(f"{req.npc}:"):].strip()
    return {"action": "Say", "text": resposta}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

