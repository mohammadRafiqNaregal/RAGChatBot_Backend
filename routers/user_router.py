# Express:  const express = require('express')
# Express:  const { getAllUsers, getUserById, ... } = require('../controllers/userController')
from fastapi import APIRouter, Depends, status
from typing import List

from dependencies.auth import get_current_user
from models.user_model import UserCreate, UserUpdate, UserResponse
import controllers.user_controller as user_controller

# Express:  const router = express.Router()   ← no prefix inside the router file
# Express:  prefix '/users' is set in app.js: app.use('/users', router)
#
# FastAPI:  prefix is set HERE, inside the router itself (not in main.py)
router = APIRouter(
    prefix="/users",   # all routes below become /users/...
    tags=["Users"],    # used only for grouping in /docs
    dependencies=[Depends(get_current_user)],
)


# Express:  router.get('/', getAllUsers)
# FastAPI:  response_model tells FastAPI what shape to return (like a TS interface)
@router.get("/", response_model=List[UserResponse])
def get_all_users():
    return user_controller.get_all_users()


# Express:  router.get('/:id', getUserById)
# FastAPI:  {user_id} in the path → automatically passed as a function argument
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    return user_controller.get_user_by_id(user_id)


# Express:  router.post('/', createUser)        body comes from req.body
# FastAPI:  body: UserCreate  →  FastAPI reads JSON body and validates it automatically
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(body: UserCreate):
    return user_controller.create_user(body)


# Express:  router.put('/:id', updateUser)
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, body: UserUpdate):
    return user_controller.update_user(user_id, body)


# Express:  router.delete('/:id', deleteUser)
# status 204 = No Content (same as Express: res.status(204).send())
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    user_controller.delete_user(user_id)
