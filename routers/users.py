# vovlemos a importar la libreria de fastapi
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

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

@router.get("/usersjson")
async def usersjson():
    return [
        {"name": "Brais", "surname": "Moure", "url": "https://pisto.bueno", "age": 35},
        {"name": "Eleaeleb", "surname": "ElMalilla", "url": "https://azulito.com", "age": 45},
        {"name": "ELBoo", "surname": "Uzielito", "url": "https://monitas.com", "age": 30}
    ]

# Path
@router.get("/users")
async def users():
    return users_list
#query
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)    


# Vemos lo de user query
@router.post("/user/", response_model= User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code= 404, detail="El Usuario ya Existe")
 
    
    users_list.append(user)
    return user

@router.put("/user/")
async def user(user: User):

    found = False


    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "Nose ha actualizado el usuario"}
    
    return user

@router.delete("/user/{id}")
async def user(id: int):

    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return {"error": "Nose ha eliminado el usuario"}


def search_user(id: int):

    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "Nose ha encontrado el usuario"}
