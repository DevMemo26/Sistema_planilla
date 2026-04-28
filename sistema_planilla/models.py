from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime

class PagoPlanilla(Base):
    __tablename__ = "pagos_planilla"

    id = Column(Integer, primary_key=True, index=True)
    cita_id = Column(Integer, unique=True, index=True) 
    codigo_medico = Column(String, index=True)
    nombre_medico = Column(String)             
    concepto = Column(String)
    monto = Column(Float)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    estado = Column(String, default="Pendiente")

class UsuarioRRHH(Base):
    __tablename__ = "usuarios_rrhh"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String) 
    nombre_completo = Column(String)