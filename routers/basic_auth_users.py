# importamos las librerias que vamos a utilizar

from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# creamos la API

app = FastAPI()

# creamos la autenticacion del usuario 

oauth2 = OAuth2PasswordBearer(tokenUrl="logion")

# creamos la clase con la que realizamos la API

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool
    


# Creamos una nueva clase de userdb que tiene el password

class UserDB(User):
    password: str

# Creamos una Base de Datos no Relacional

users_db = {
    "JuanGua":{
        "username": "JuanGua",
        "full_name": "JuanGuaido",
        "email": "juangua@gmail.com",
        "disabled": False,
        "password":"1234567"
    },

    "NocoMadu":{
        "username": "NicoMadu",
        "full_name": "NicolasMaduro",
        "email": "nicoma@gmail.com",
        "disabled": True,
        "password":"246810"
    }
}

# Vamos a ver si nuestro usuario se encuentra en la base de datos 

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])



async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"})

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )

    return user


# Autentificamos 
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_data = users_db.get(form.username)
    if not user_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El Usuario no es Correcto")
    
    user = UserDB(**user_data)
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La Contraseña no es Correcta")
    
    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def me(user:User = Depends(current_user)):
    return user


#### inicia el server: uvicorn basic_auth_users:app --reload