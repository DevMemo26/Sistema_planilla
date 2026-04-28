from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Planilla v3.0 (Arquitectura Profesional)")

class LoginRequest(BaseModel):
    username: str
    password: str

class PagoCreate(BaseModel):
    cita_id: int
    codigo_medico: str
    nombre_medico: str
    concepto: str
    monto: float

@app.get("/")
def read_root():
    return {"mensaje": "Backend de Planilla Operativo."}

@app.get("/pagos")
def obtener_pagos(db: Session = Depends(get_db)):
    return db.query(models.PagoPlanilla).all()

@app.post("/pagos")
def crear_pago(pago: PagoCreate, db: Session = Depends(get_db)):
    nuevo_pago = models.PagoPlanilla(
        cita_id=pago.cita_id,
        codigo_medico=pago.codigo_medico,
        nombre_medico=pago.nombre_medico,
        concepto=pago.concepto,
        monto=pago.monto
    )
    db.add(nuevo_pago)
    db.commit()
    db.refresh(nuevo_pago)
    return nuevo_pago

@app.post("/login")
def validar_login(credenciales: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(models.UsuarioRRHH).filter(models.UsuarioRRHH.username == credenciales.username).first()
    
    if not usuario or usuario.password != credenciales.password:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    return {"status": "ok", "mensaje": "Login exitoso", "nombre_completo": usuario.nombre_completo}