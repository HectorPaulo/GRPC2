from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from . import db


class VehicleIn(BaseModel):
    matricula: str
    vin: str
    modelo: str
    marca: str
    tipo: str


class VehicleOut(VehicleIn):
    pass


app = FastAPI(title="Vehiculos API")

# Configurar CORS para permitir peticiones del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    db.init_db()


@app.post("/vehicles", response_model=dict)
def create_vehicle(v: VehicleIn):
    try:
        db.create_vehicle(v.model_dump())
        return {"ok": True, "message": "Creado"}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/vehicles/{matricula}", response_model=VehicleOut)
def get_vehicle(matricula: str):
    v = db.get_vehicle(matricula)
    if not v:
        raise HTTPException(status_code=404, detail="No encontrado")
    return v


@app.get("/vehicles", response_model=list[VehicleOut])
def list_vehicles():
    return db.list_vehicles()


@app.delete("/vehicles/{matricula}", response_model=dict)
def delete_vehicle(matricula: str):
    ok = db.delete_vehicle(matricula)
    if not ok:
        raise HTTPException(status_code=404, detail="No encontrado")
    return {"ok": True, "message": "Eliminado"}
