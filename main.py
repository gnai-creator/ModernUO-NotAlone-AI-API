from ai_decision_service import app

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 10000)) 
    uvicorn.run(app, host="0.0.0.0", port=port)
