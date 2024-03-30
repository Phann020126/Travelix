from fastapi import APIRouter, HTTPException, Path, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.config import get_db

from schemas import AgentSchema, AgentCreateSchema, Token, TokenData, UserSchema, UserCreateSchema
from models import UserModel
import db.crud.user_crud as crud
import db.crud.auth_crud as auth
from db.crud.auth_crud import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from datetime import timedelta

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/role", response_model=str)
async def get_role(current_user: UserSchema = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return current_user.role

@router.post("/create/agent", response_model=str)
async def create_agent(agent: AgentCreateSchema, current_user: UserModel = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    if current_user.role != "marketing":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The current user has no permisson to perform this action")
    
    agent.role = "agent"
    agent.agency_id = crud.get_agent(db, current_user.id).agency_id    

    return crud.create_agent(db, agent)

@router.post("/create/agent/any", response_model=str)
async def create_agent_any(agent: AgentCreateSchema, current_user: UserModel = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The current user has no permisson to perform this action")

    if agent.role != "agent" and agent.role != "marketing":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{agent.role} is not a valid role")
    
    return crud.create_agent(db, agent) if agent.role == "agent" else crud.create_marketing(db, agent)