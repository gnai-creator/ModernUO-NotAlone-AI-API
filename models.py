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
    memory: Optional[List[str]] = []
    nearby_npcs: Optional[List[NearbyNPC]] = []
    player_input: Optional[str] = None
    player_name: Optional[str] = None

class NPCDecision(BaseModel):
    type: AIActions
    target: Optional[str] = None
    say: Optional[str] = None
    money_amount: Optional[str] = "0"
    details: Optional[str] = None

class NPCState(BaseModel):
    npc_id: str
    name: str
    role: str
    location: str
    mood: Optional[str] = "neutro"
    memory: Optional[List[str]] = []
    nearby_npcs: Optional[List[NearbyNPC]] = []