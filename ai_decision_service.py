# ai_decision_service.py
from fastapi import FastAPI
from ai_extract_action import extrair_acao
from prompt import montar_prompt_para_acao
from actions import AIActions
from models import FullNPCState
from text_generator import gerar_texto_com_tolerancia



app = FastAPI()



@app.post("/npc/decide")
def npc_decide(state: FullNPCState):
    try:
        # === Caso 2: IA decide ação autônoma ===
        prompt = montar_prompt_para_acao(state)


        result = gerar_texto_com_tolerancia(prompt=prompt)
        if not result or not isinstance(result, str):
            raise ValueError("Resultado da geração está vazio ou inválido.")

        print("[DEBUG] Resultado gerado:", result)
        parsed = extrair_acao(result)
        print("[DEBUG] Ação extraída:", parsed["type"])
        print("[DEBUG] Item_name:", parsed["item_name"])
        return {
            "type": parsed.get("type", AIActions.NENHUMA),
            "target": parsed.get("target"),
            "say": parsed.get("say"),
            "item_amount": parsed.get("item_amount"),
            "item_name": parsed.get("item_name"),
            "details": parsed.get("details")
        }
    except Exception as e:
        print("[DEBUG] Erro ao decidir ação:", e)
        if "device meta" in str(e):
            print("[DEBUG] Pipeline possivelmente corrompido — reinício pode ser necessário futuramente.")
        return {
            "type": AIActions.NENHUMA,
            "target": None,
            "say": None,
            "item_amount": "0",
            "item_name": None,
            "details": "Erro ao decidir ação: " + str(e)
        }

