# vovlemos a importar la libreria de fastapi
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Definición del modelo User
class User(BaseModel):
    id: int
    name: str
    surname: str  # Asegúrate de que este campo sea 'surname', no 'surename'
    url: str
    age: int

# Lista de usuarios
users_list = [
    User(id=1, name="Brais", surname="Moure", url="https://pisto.bueno", age=35),
    User(id=2, name="Eleaeleb", surname="ElMalilla", url="https://azulito.com", age=45),
    User(id=3, name="ELBoo", surname="Uzielito", url="https://monitas.com", age=30)
]

@app.get("/usersjson")
async def usersjson():
    return [
        {"name": "Brais", "surname": "Moure", "url": "https://pisto.bueno", "age": 35},
        {"name": "Eleaeleb", "surname": "ElMalilla", "url": "https://azulito.com", "age": 45},
        {"name": "ELBoo", "surname": "Uzielito", "url": "https://monitas.com", "age": 30}
    ]

# Path
@app.get("/users")
async def users():
    return users_list
#path
@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)    

#Query
# Vemos lo de user query
@app.get("/user/")
async def user(id: int):
    return search_user(id)

def search_user(id: int):

    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "Nose ha encontrado el usuario"}
