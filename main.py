from fastapi import FastAPI
from routers import products, users  # Importa el módulo products desde el directorio routers
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Incluye el router
app.include_router(products.router)
app.include_router(users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ruta raíz
@app.get("/")
async def root():
    return {"message": "Hola FastAPI"}

@app.get("/url")
async def url():
   return {"url_curso": "https://maguix.com/el_mejor_pisto"}


# inicia el server: uvicorn main:app --reload
# uvicorn main:app --reload


# Documentacion con Swagger: http://127.0.0.1:8000/docs
# Docuemntacion con Redocly: http://127.0.1:8000/redoc
 