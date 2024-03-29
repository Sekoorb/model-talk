from fastapi import APIRouter, HTTPException, Depends, status
from ..models import UserCreate, UserResponse, UserUpdate, UserLogin
from ..crud import create_user, get_user, update_user, delete_user, authenticate_user
from ..dependencies import get_current_user, hash_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    # Here, include logic to check if a user with the same username or email already exists
    # Hash the password before storing it
    user.password = hash_password(user.password)
    created_user = await create_user(user)
    if not created_user:
        raise HTTPException(status_code=400, detail="Error creating user")
    return created_user

@router.post("/login")
async def login_user(form_data: UserLogin):
    user = await authenticate_user(form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: str):
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user_details(user_id: str, user: UserUpdate):
    updated_user = await update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(user_id: str):
    await delete_user(user_id)
    return {"message": "User deleted successfully"}

# Note: The actual implementation of CRUD operations should handle the necessary database interactions.
