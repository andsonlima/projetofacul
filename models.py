from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class EmergencyContactBase(SQLModel):
    nome: str
    grau_parentesco: str
    telefone: str

class EmergencyContact(EmergencyContactBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    biker_id: Optional[int] = Field(default=None, foreign_key="biker.id")

class EmergencyContactRead(EmergencyContactBase):
    id: int

class EmergencyContactCreate(EmergencyContactBase):
    pass

class BikerBase(SQLModel):
    nome: str
    tipo_bike: str  # MTB, SPEED, E-BIKE
    pedais_participa: str  # 3A, 5A, 3A;5A etc
    participa_trilha: bool
    problema_saude: Optional[str] = None  # None => Não; texto => Sim e qual

class Biker(BikerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class BikerRead(BikerBase):
    id: int

class BikerCreate(BikerBase):
    contatos_emergencia: List[EmergencyContactCreate] = []

class BikerReadWithContacts(BikerRead):
    contatos_emergencia: List[EmergencyContactRead] = []

class BikerUpdate(SQLModel):
    nome: Optional[str] = None
    tipo_bike: Optional[str] = None
    pedais_participa: Optional[str] = None
    participa_trilha: Optional[bool] = None
    problema_saude: Optional[str] = None
