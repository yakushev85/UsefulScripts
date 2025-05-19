from datetime import datetime,  timedelta, timezone, UTC
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
import bcrypt
from fastapi import FastAPI, Header, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select


SECRET_KEY = "cmucugc98288u2ucmckl"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# Example salt from bcrypt.gensalt(), use a secure random salt in production
PASSWORD_SALT = b'$2b$12$ggFPQ/b1HyzucR28TkdV2e' 

app = FastAPI()

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str | None = Field(default=None, unique=True, index=True)
    password: str
    token: str
    created_at: datetime

class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    created_by: str
    created_at: datetime

connect_url = "mysql://nk:ydG8x0hXClMVn63TGoLD@notekeeper_database:3308/nk"
engine = create_engine(connect_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

class Login_Request(BaseModel):
    email: str
    password: str

class Signup_Request(BaseModel):
    name: str
    email: str
    password: str

class Auth_Response(BaseModel):
    token: str

class Note_Request(BaseModel):
    title: str
    content: str

class Note_Response(BaseModel):
    title: str
    content: str
    created_at: datetime

def create_access_token(user_email:str) -> str:
    exp:datetime = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "user_email": user_email, 
        "exp": datetime.timestamp(exp)
        }
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def get_data_token(token: str) -> tuple[str, datetime]:
    user_email = ""
    exp = datetime.now(timezone.utc)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("user_email")
        exp = payload.get("exp")
        
    except InvalidTokenError:
        print("Invalid token")

    return (user_email, exp)

def find_user_by_token(token: str, session: Session) -> User:
    user_email, exp = get_data_token(token)
    
    user_query = select(User).where(User.email == user_email)
    r_user = session.exec(user_query).first()

    if r_user is None or r_user.token != token or datetime.fromtimestamp(exp, UTC) < datetime.now(timezone.utc):
        return None
    
    return r_user

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), PASSWORD_SALT).decode('utf-8')


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/notes")
def create_note(req: Note_Request, api_token: Annotated[str, Header()], session: SessionDep) -> Note_Response:
    c_user = find_user_by_token(api_token, session)

    if c_user is None:
        raise HTTPException(status_code=400, detail="User not found")
    
    c_note = Note(
        title=req.title,
        content=req.content,
        created_by=c_user.email,
        created_at=datetime.now()
    )

    session.add(c_note)
    session.commit()
    session.refresh(c_note)

    note = Note_Response(
        title=c_note.title,
        content=c_note.content,
        created_at = c_note.created_at)
    
    return note

@app.get("/notes")
def get_notes(api_token: Annotated[str, Header()], session: SessionDep) -> list[Note_Response]:
    c_user = find_user_by_token(api_token, session)

    if c_user is None:
        raise HTTPException(status_code=400, detail="User not found")
    
    select_query = select(Note).where(Note.created_by == c_user.email)
    notes = session.exec(select_query).all()
    if not notes:
        return []
    
    notes_response = []
    for note in notes:
        notes_response.append(Note_Response(
            title=note.title,
            content=note.content,
            created_at=note.created_at))
        
    return notes_response

@app.post("/login")
def login(req: Login_Request, session: SessionDep) -> Auth_Response:
    hashed_password = hash_password(req.password)
    select_query = select(User).where(User.email == req.email)
    user = session.exec(select_query).first()

    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    
    if user.password != hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    user.token = create_access_token(user.email)

    session.add(user)
    session.commit()
    session.refresh(user)

    return Auth_Response(token=user.token)

@app.post("/signup")
def signup(req: Signup_Request, session: SessionDep) -> Auth_Response:
    select_query = select(User).where(User.email == req.email)
    e_user = session.exec(select_query).first()

    if e_user is not None:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user = User(
        name=req.name,
        email=req.email,
        password=hash_password(req.password),
        created_at=datetime.now())
    
    user.token = create_access_token(user.email)

    session.add(user)
    session.commit()
    session.refresh(user)
    
    return Auth_Response(token=user.token)

@app.get("/logout")
def logout(api_token: Annotated[str, Header()], session: SessionDep) -> str:
    user_email, _ = get_data_token(api_token)

    user_query = select(User).where(User.email == user_email)
    r_user = session.exec(user_query).first()

    r_user.token = ""

    session.add(r_user)
    session.commit()

    return "Logout successful"

