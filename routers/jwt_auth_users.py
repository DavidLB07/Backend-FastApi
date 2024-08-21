from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

# El algoritmo que vamos a utilizar
ALGORITHM = "HS256"

# Duración de nuestro token de acceso en minutos
ACCESS_TOKEN_DURATION = 1  # Ajusta esto según tus necesidades

# Ruta de acceso al código encriptado
SECRET = "5dad9e89f7724f74e0ea6edfd545735ee6b3a955259ef1d353a3802c4c8ce6f8"

# Creamos la API
app = FastAPI()

# Creamos la autenticación del usuario y contraseña
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Contexto de encriptación
crypt = CryptContext(schemes=["bcrypt"])

# Clase de usuario
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

# Clase de usuario con contraseña
class UserDB(User):
    password: str

# Base de datos de usuarios
users_db = {
    "JuanGua": {
        "username": "JuanGua",
        "full_name": "JuanGuaido",
        "email": "juangua@gmail.com",
        "disabled": False,
        "password": "$2a$12$rJLJKMDNo5WX0qULU/N.4eG0AX2iGLpp3HVdsUOuKttTL5b.eGlL6"
    },
    "NicoMadu": {
        "username": "NicoMadu",
        "full_name": "NicolasMaduro",
        "email": "nicoma@gmail.com",
        "disabled": True,
        "password": "$2a$12$79Bppzp7ZQA9S4vUZISAZ.m2cxdz8DGHAZZC6ZfpJTCCxLLqxgZ8a"
    }
}

# Búsqueda de usuario
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    return None

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    return None

# Autenticación de usuario
async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de Autenticación Inválidas",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise exception
        user = search_user(username)
        if user is None:
            raise exception
    except JWTError:
        raise exception

    return user

# Usuario actual
async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return user

# Autenticación al acceder
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_data = users_db.get(form.username)
    if not user_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El Usuario no es Correcto")

    user = search_user_db(form.username)

    # Verificar si la contraseña es correcta
    if not user or not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta"
        )

    # Crear un access token
    access_token = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }

    return {
        "access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM),
        "token_type": "bearer"
    }

# Acceso al usuario
@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user



#### inicia el server: uvicorn basic_auth_users:app --reload