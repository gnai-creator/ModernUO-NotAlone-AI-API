from pydantic import BaseModel
from typing import List, Optional
from actions import AIActions

# Modelos para entrada
class NearbyNPC(BaseModel):
    id: str
    name: str
    role: str
    mood: Optional[str] = "neutro"

class FullNPCState(BaseModel):
    npc_id: str
    name: str
    role: str
    background: str
    location: str
    mood: Optional[str] = "neutro"
    gold: Optional[str] = "0"
    item_name: Optional[str] = ""
    memory: Optional[List[str]] = []
    nearby_npcs: Optional[List[NearbyNPC]] = []
    player_input: Optional[str] = ""	
    player_name: Optional[str] = ""

class NPCDecision(BaseModel):
    type: AIActions
    target: Optional[str] = ""
    say: Optional[str] = ""
    money_amount: Optional[str] = "0"
    item_name: Optional[str] = ""
    details: Optional[str] = ""

# class NPCState(BaseModel):
#     npc_id: str
#     name: str
#     role: str
#     background: str
#     location: str
#     mood: Optional[str] = "neutro"
#     memory: Optional[List[str]] = []
#     nearby_npcs: Optional[List[NearbyNPC]] = []