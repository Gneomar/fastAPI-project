from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from src.core.database import get_session
from src.models.users import User
from src.schemas.users import UserCreate
from src.auth.auth import verify_password, hash_password, create_access_token
from fastapi.responses import JSONResponse

auth_router = APIRouter()

@auth_router.post("/login")
async def login(user_data: UserCreate, db: AsyncSession = Depends(get_session)):
    """Valida las credenciales y devuelve un token de acceso."""
    
    query = select(User).where(User.username == user_data.username)
    result = await db.execute(query)
    user = result.scalars().first()

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
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_session)):
    """Crea un nuevo usuario en la base de datos"""
    existing_user = await db.execute(select(User).where(User.username == user_data.username))
    
    if existing_user.scalars().first():
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    password_hash = hash_password(user_data.password)
    new_user = User(username=user_data.username, password_hash=password_hash)
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message": "Usuario creado correctamente"}