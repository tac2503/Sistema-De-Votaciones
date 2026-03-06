from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import create_tables, SessionLocal
from app.routers import voters, candidates, votes
from app import crud
import uvicorn
import pandas as pd
import matplotlib.pyplot as plt


def display_votes_chart():

    try:
        db = SessionLocal()
        data = crud.get_candidates_votes_for_chart(db)
        db.close()

        if not data:
            print("No hay datos de candidatos para graficar aún.\n")
            return

        candidates_names = [row[0] for row in data]
        votes_counts = [row[1] or 0 for row in data]

        df = pd.DataFrame({"Candidato": candidates_names, "Votos": votes_counts})

        plt.figure(figsize=(10, 6))
        plt.bar(df["Candidato"], df["Votos"], color="steelblue", edgecolor="navy")
        plt.xlabel("Candidatos", fontsize=12, fontweight="bold")
        plt.ylabel("Votos", fontsize=12, fontweight="bold")
        plt.title(
            "Estado Actual de Votos por Candidato", fontsize=14, fontweight="bold"
        )
        plt.grid(axis="y", alpha=0.3)
        plt.tight_layout()

        plt.show()

    except Exception as e:
        print(f"Error al generar gráfica: {e}\n")


@asynccontextmanager
async def lifespan(app: FastAPI):

    create_tables()
    print("Tablas creadas/verificadas exitosamente")
    print("\nGenerando gráfica de votos...\n")
    display_votes_chart()
    yield


app = FastAPI(
    title="Sistema de Votacion",
    description="API para gestionar un sistema de votaciones",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.include_router(voters.router)
app.include_router(candidates.router)
app.include_router(votes.router)


@app.get("/")
def read_root():
    return {"message": "Sistema de Votaciones API"}


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" SISTEMA DE VOTACIONES API")
    print("=" * 60)
    print(" API:           http://127.0.0.1:8000")
    print(" Documentación: http://127.0.0.1:8000/docs")
    print("=" * 60 + "\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)
