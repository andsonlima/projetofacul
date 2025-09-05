from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select, Session
from typing import List
import csv
from io import StringIO

from models import (
    Biker, BikerCreate, BikerRead, BikerReadWithContacts, BikerUpdate,
    EmergencyContact, EmergencyContactCreate, EmergencyContactRead
)
from db import init_db, get_session

app = FastAPI(title="Gestão de Pedal - Emergência", version="1.0.0")

# CORS (ajuste para o dominio do frontend se desejar)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

# ----------------- CRUD Bikers -----------------

@app.post("/bikers", response_model=BikerReadWithContacts)
def create_biker(payload: BikerCreate, session: Session = Depends(get_session)):
    biker = Biker(
        nome=payload.nome,
        tipo_bike=payload.tipo_bike,
        pedais_participa=payload.pedais_participa,
        participa_trilha=payload.participa_trilha,
        problema_saude=payload.problema_saude,
    )
    session.add(biker)
    session.commit()
    session.refresh(biker)

    for c in payload.contatos_emergencia:
        contact = EmergencyContact(
            nome=c.nome,
            grau_parentesco=c.grau_parentesco,
            telefone=c.telefone,
            biker_id=biker.id
        )
        session.add(contact)
    session.commit()

    contatos = session.exec(select(EmergencyContact).where(EmergencyContact.biker_id == biker.id)).all()
    return BikerReadWithContacts(**biker.model_dump(), contatos_emergencia=contatos)

@app.get("/bikers", response_model=List[BikerRead])
def list_bikers(session: Session = Depends(get_session)):
    return session.exec(select(Biker)).all()

@app.get("/bikers/{biker_id}", response_model=BikerReadWithContacts)
def get_biker(biker_id: int, session: Session = Depends(get_session)):
    biker = session.get(Biker, biker_id)
    if not biker:
        raise HTTPException(status_code=404, detail="Biker não encontrado")
    contatos = session.exec(select(EmergencyContact).where(EmergencyContact.biker_id == biker_id)).all()
    return BikerReadWithContacts(**biker.model_dump(), contatos_emergencia=contatos)

@app.patch("/bikers/{biker_id}", response_model=BikerRead)
def update_biker(biker_id: int, updates: BikerUpdate, session: Session = Depends(get_session)):
    biker = session.get(Biker, biker_id)
    if not biker:
        raise HTTPException(status_code=404, detail="Biker não encontrado")
    update_data = updates.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(biker, k, v)
    session.add(biker)
    session.commit()
    session.refresh(biker)
    return biker

@app.delete("/bikers/{biker_id}")
def delete_biker(biker_id: int, session: Session = Depends(get_session)):
    biker = session.get(Biker, biker_id)
    if not biker:
        raise HTTPException(status_code=404, detail="Biker não encontrado")
    session.delete(biker)
    session.commit()
    return {"ok": True}

# ----------------- Contatos Emergência -----------------

@app.post("/bikers/{biker_id}/contatos", response_model=EmergencyContactRead)
def add_contact(biker_id: int, payload: EmergencyContactCreate, session: Session = Depends(get_session)):
    if not session.get(Biker, biker_id):
        raise HTTPException(status_code=404, detail="Biker não encontrado")
    contact = EmergencyContact(**payload.model_dump(), biker_id=biker_id)
    session.add(contact)
    session.commit()
    session.refresh(contact)
    return contact

@app.delete("/contatos/{contact_id}")
def delete_contact(contact_id: int, session: Session = Depends(get_session)):
    contact = session.get(EmergencyContact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    session.delete(contact)
    session.commit()
    return {"ok": True}

# ----------------- Busca por nome -----------------

@app.get("/bikers/busca", response_model=List[BikerRead])
def search_biker(nome: str, session: Session = Depends(get_session)):
    stmt = select(Biker).where(Biker.nome.ilike(f"%{nome}%"))
    return session.exec(stmt).all()

# ----------------- Exportação CSV -----------------

@app.get("/export/csv")
def export_csv(session: Session = Depends(get_session)):
    bikers = session.exec(select(Biker)).all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "nome", "tipo_bike", "pedais_participa", "participa_trilha", "problema_saude"])
    for b in bikers:
        writer.writerow([b.id, b.nome, b.tipo_bike, b.pedais_participa, b.participa_trilha, b.problema_saude or "Não"])
    return {
        "filename": "bikers.csv",
        "content": output.getvalue()
    }
