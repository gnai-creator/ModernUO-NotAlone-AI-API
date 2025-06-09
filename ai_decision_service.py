# ai_decision_service.py
from fastapi import FastAPI
from ai_extract_action import extrair_acao
from prompt import montar_prompt_para_acao
from actions import AIActions
from models import FullNPCState
from text_generator import gerar_texto_com_tolerancia
from details import AIDetails  # Certifique-se que está importando o Enum correto


app = FastAPI()


@app.post("/npc/decide")
def npc_decide(state: FullNPCState):
    try:
        # === IA decide ação autônoma ===
        prompt = montar_prompt_para_acao(state)
        result = gerar_texto_com_tolerancia(prompt=prompt)

        if not result or not isinstance(result, str):
            raise ValueError("Resultado da geração está vazio ou inválido.")

        print("[DEBUG] Resultado gerado:", result)

        parsed = extrair_acao(result)

        action_type = parsed.get("type", AIActions.NENHUMA)

        # Garante que o detail está coerente com a ação
        details = AIDetails[action_type.name] if action_type.name in AIDetails.__members__ else AIDetails.NENHUMA

        print("[DEBUG] Ação extraída:", action_type)
        print("[DEBUG] Item_name:", parsed.get("item_name"))

        return {
            "type": action_type,
            "target": parsed.get("target"),
            "say": parsed.get("say"),
            "item_amount": parsed.get("item_amount", "0"),
            "item_name": parsed.get("item_name"),
            "details": details
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
            "details": AIDetails.NENHUMA
        }
