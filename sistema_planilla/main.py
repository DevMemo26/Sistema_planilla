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

class MedicoCreate(BaseModel):
    codigo: str
    nombre: str
    profesion: str
    sueldo_base: float

@app.get("/")
def read_root():
    return {"mensaje": "Backend de Planilla Operativo."}

@app.get("/pagos")
def obtener_pagos(db: Session = Depends(get_db)):
    return db.query(models.PagoPlanilla).all()

@app.get("/medicos")
def obtener_medicos(db: Session = Depends(get_db)):
    return db.query(models.Medico).all()

@app.post("/medicos")
def crear_medico(medico: MedicoCreate, db: Session = Depends(get_db)):
    # Verificar si ya existe
    db_medico = db.query(models.Medico).filter(models.Medico.codigo == medico.codigo).first()
    if db_medico:
        raise HTTPException(status_code=400, detail="El código de médico ya existe")
    
    nuevo_medico = models.Medico(
        codigo=medico.codigo,
        nombre=medico.nombre,
        profesion=medico.profesion,
        sueldo_base=medico.sueldo_base
    )
    db.add(nuevo_medico)
    db.commit()
    db.refresh(nuevo_medico)
    return nuevo_medico

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