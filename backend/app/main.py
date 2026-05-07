from fastapi import FastAPI

from app.routes.inscricoes import router as inscricoes_router

app = FastAPI(
    title="Sistema de Inscrições",
    description="API para inscrições do Formação e Escola de Gastronomia Social",
    version="0.1.0",
)

app.include_router(inscricoes_router)


@app.get("/")
def health_check():
    return {"status": "API funcionando"}