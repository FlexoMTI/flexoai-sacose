from fastapi import FastAPI, Request
from pydantic import BaseModel
from utils.excel_loader import load_data
from utils.oferta_calculator import calculeaza_oferta

app = FastAPI()
data = load_data()

class CerereOferta(BaseModel):
    dimensiune: str
    material: str
    maner: str = "plat"
    imprimare: str = "mică"
    cantitate: int

@app.post("/oferta")
async def oferta(cerere: CerereOferta):
    try:
        oferta_text = calculeaza_oferta(data, cerere)
        return {"răspuns": oferta_text}
    except Exception as e:
        return {"eroare": str(e)}