from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.api.routes.tasks import router as tasks_router

app = FastAPI(title="Secure Rate-Limited Task API")

app.include_router(auth_router)
app.include_router(tasks_router)

@app.get("/health")
def health():
    return {"status": "ok"}
