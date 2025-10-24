from fastapi import FastAPI
from pydantic import BaseModel
from interference_engine import forward_chaining
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# === Izinkan akses dari Next.js (localhost:3000) ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # bisa dibatasi ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    usia: int
    profil_risiko: str
    tujuan_finansial: str
    status_investor: str
    investable_income: int

@app.post("/interference")
def inferensi(data: UserInput):
    hasil = forward_chaining(data.dict())
    return hasil
