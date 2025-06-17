from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.excel_loader import load_data
from utils.oferta_calculator import calculeaza_oferta

app = FastAPI()

# ✅ Activare CORS complet (pentru WordPress sau orice domeniu)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Poți restrânge la ["https://siteultau.ro"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Structura cerere de ofertă
class CerereOferta(BaseModel):
    dimensiune: str
    material: str
    maner: str = "plat"
    imprimare: str = "mică"
    cantitate: int

# ✅ Încarcă datele Excel o singură dată la pornire
data = load_data()

# ✅ Răspuns pe homepage (opțional, evită 404 pe /)
@app.get("/")
def index():
    return {"mesaj": "FlexoAI rulează. Folosește /static/widget.html pentru ofertare."}

# ✅ Endpoint principal
@app.post("/oferta")
async def oferta(cerere: CerereOferta):
    try:
        oferta_text = calculeaza_oferta(data, cerere)
        return {"răspuns": oferta_text}
    except Exception as e:
        return {"eroare": str(e)}
