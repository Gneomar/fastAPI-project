from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_session
from models.users import User
from schemas.users import UserCreate
from auth.auth import AccessTokenBearer, verify_password, create_access_token
from services.auth import UserService
from fastapi.responses import JSONResponse

auth_router = APIRouter()
access_scheme = AccessTokenBearer()
user_service = UserService()

@auth_router.post("/login")
async def login(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_session),
    ):
    """Valida las credenciales y devuelve un token de acceso."""
    
    user = await user_service.get_user_by_username(user_data.username, db)
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    # Generar token de acceso
    access_token = create_access_token(user_data={"uid": str(user.uid), "username": user.username})
    print(f"El token es el siguiente: {access_token}")
    return JSONResponse(content={
        "message": "Usuario autenticado correctamente",
        "access_token": access_token,
        "user": {"uid": str(user.uid), "username": user.username},
        "token_type": "bearer"})

@auth_router.post("/register/")
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_session),
    ):

    user_exist = await user_service.user_exists(user_data.username, db)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe",
        )
    
    new_user = await user_service.create_user(user_data, db)
    return {"message": f"Usuario {new_user.username} creado correctamente"}


@auth_router.get("/ruta-protegida")
def ruta_protegida(
    token_detail: dict = Depends(access_scheme),
    ):
    user = token_detail["user"]
    return {
        "mensaje": f"Hola {user['username']}, accediste a una ruta protegida.",
        "usuario_id": user["uid"],
        "user_name": user["username"],
    }