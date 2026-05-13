# Express:  const express = require('express')
# Express:  const { getAllUsers, getUserById, ... } = require('../controllers/userController')
from fastapi import APIRouter, Depends, status
from typing import Annotated, List
from sqlalchemy.orm import Session

from data.database import get_db
from dependencies.auth import get_current_user, require_role
from models.access_control import ROLE_ADMIN
from models.user_model import UserCreate, UserUpdate, UserResponse
import controllers.user_controller as user_controller

# Express:  const router = express.Router()   ← no prefix inside the router file
# Express:  prefix '/users' is set in app.js: app.use('/users', router)
#
# FastAPI:  prefix is set HERE, inside the router itself (not in main.py)
router = APIRouter(
    prefix="/api/users",   # all routes below become /api/users/...
    tags=["Users"],    # used only for grouping in /docs
    dependencies=[Depends(get_current_user)],
)


# Express:  router.get('/', getAllUsers)
# FastAPI:  response_model tells FastAPI what shape to return (like a TS interface)
@router.get("/", response_model=List[UserResponse])
def get_all_users(db: Annotated[Session, Depends(get_db)]):
    return user_controller.get_all_users(db)


# Express:  router.get('/:id', getUserById)
# FastAPI:  {user_id} in the path → automatically passed as a function argument
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    return user_controller.get_user_by_id(db, user_id)


# Express:  router.post('/', createUser)        body comes from req.body
# FastAPI:  body: UserCreate  →  FastAPI reads JSON body and validates it automatically
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_role(ROLE_ADMIN))])
def create_user(body: UserCreate, db: Annotated[Session, Depends(get_db)]):
    return user_controller.create_user(db, body)


# Express:  router.put('/:id', updateUser)
@router.put("/{user_id}", response_model=UserResponse,
            dependencies=[Depends(require_role(ROLE_ADMIN))])
def update_user(user_id: int, body: UserUpdate, db: Annotated[Session, Depends(get_db)]):
    return user_controller.update_user(db, user_id, body)


# Express:  router.delete('/:id', deleteUser)
# status 204 = No Content (same as Express: res.status(204).send())
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_role(ROLE_ADMIN))])
def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user_controller.delete_user(db, user_id)
