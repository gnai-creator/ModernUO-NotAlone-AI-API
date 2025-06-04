import requests

req = {
    "npc": "Oberon",
    "role": "mago",
    "background": "Oberon é misterioso e fala em enigmas.",
    "input": "Pode me ensinar magia?",
    "player": "Felipe"
}
r = requests.post("http://localhost:8000/think", json=req)
print(r.json())
