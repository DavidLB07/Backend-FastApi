from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hola FastAPI"}

@app.get("/url")
async def url():
    return {"url_curso": "https://maguix.com/el_mejor_pisto"}
