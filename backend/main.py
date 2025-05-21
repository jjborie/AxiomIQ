from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "AxiomIQ backend"}

@app.get("/health")
async def health():
    return {"status": "ok"}
