import json
import re

def extrair_acao(texto: str) -> dict:
    try:
        match = re.search(r"{.*}", texto, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        else:
            return {
                "intention": "idle",
                "target": None,
                "say": None,
                "details": "Nenhuma ação extraída"
            }
    except Exception as e:
        return {
            "intention": "idle",
            "target": None,
            "say": None,
            "details": f"Erro na extração: {str(e)}"
        }
