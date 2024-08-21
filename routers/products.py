from fastapi import APIRouter

router = APIRouter(prefix="/products",
                   tags=["products"],
                   responses={404: {"message": "No Econtrado"}})  # Nota el paréntesis aquí

prodcts_list = ["Producto 1", "Producto 2", "Producto 3", "Producto 4", "Producto 5"]


@router.get("/")
async def products():
    return prodcts_list

# creamo un nuevo producto 

@router.get("/{id}")
async def products(id: int):
    return prodcts_list[id]

