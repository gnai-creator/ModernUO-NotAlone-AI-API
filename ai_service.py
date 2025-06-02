from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Chat"  # ou "Qwen/Qwen2.5-1.5B-Chat"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, trust_remote_code=True,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
)

generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=0 if torch.cuda.is_available() else -1
)

app = FastAPI()

class NPCRequest(BaseModel):
    npc: str
    role: str
    background: str
    input: str
    history: str = ""

def montar_prompt(npc, role, background, input_text, history=""):
    prompt = (
        f"SYSTEM: Você é {npc}, um {role}. Personalidade: {background}.\n"
    )
    if history:
        prompt += f"Histórico recente: {history}\n"
    prompt += f"USER: {input_text}\nASSISTANT:"
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
    resposta = output[len(prompt):].strip()
    if resposta.startswith(f"{req.npc}:"):
        resposta = resposta[len(f"{req.npc}:"):].strip()
    return {"action": "Say", "text": resposta}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
