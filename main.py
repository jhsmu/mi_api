# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# ==========================
# Crear la app FastAPI
# ==========================
app = FastAPI(
    title="API Usuarios",
    description="API para buscar usuarios por NIT",
    version="1.0"
)

# ==========================
# Habilitar CORS
# ==========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen (para pruebas)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# Conexión a MongoDB remoto
# ==========================
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise Exception("No se encontró la variable de entorno MONGO_URI")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
try:
    client.admin.command('ping')
    print("✅ Conexión a MongoDB exitosa")
except Exception as e:
    print("❌ Error conectando a MongoDB:", e)

db = client.get_database()
user_collection = db["user"]

# ==========================
# Rutas de la API
# ==========================
@app.get("/")
def root():
    return {"message": "API Usuarios funcionando"}

@app.get("/usuarios/{nit}")
def get_usuario(nit: str):
    usuario = user_collection.find_one({"nit": nit.strip()})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario["_id"] = str(usuario["_id"])
    # Filtrar campos que quieres mostrar
    usuario_filtrado = {
        "_id": usuario.get("_id"),
        "name": usuario.get("name"),
        "lastname": usuario.get("lastname"),
        "business_name": usuario.get("business_name"),
        "quota": usuario.get("quota"),
        "available_quota": usuario.get("available_quota"),
        "quota_status": usuario.get("quota_status"),
        "status": usuario.get("status"),
        "phone": usuario.get("phone"),
        "email": usuario.get("email"),
        "nit": usuario.get("nit"),
        "branch_office": usuario.get("branch_office"),
        "created_at": usuario.get("created_at"),
        "created_by": usuario.get("created_by"),
        "balance": usuario.get("balance")
    }
    return usuario_filtrado

@app.get("/debug_usuarios")
def debug_usuarios():
    documentos = list(user_collection.find().limit(5))
    for d in documentos:
        d["_id"] = str(d["_id"])
    return documentos
