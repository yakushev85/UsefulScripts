from fastapi import FastAPI
from pydantic import BaseModel, Field
import hashlib

# Basic Model
class User(BaseModel):
    uname: str = Field(..., min_length=3)
    password: str = Field(..., min_length=3)

class Note(BaseModel):
    title: str = Field(..., min_length=2)
    description: str = ""
    uname: str = Field(..., min_length=3)

class UserSession(BaseModel):
    token: str = Field(..., min_length=6)
    user: User

# DTO
class UserDto(BaseModel):
    uname: str = Field(..., min_length=3)
    password: str = Field(..., min_length=3)
    repassword: str = ""

class NoteDto(BaseModel):
    title: str = Field(..., min_length=2)
    description: str = ""
    token: str = Field(..., min_length=6)

# Initialization
notes = []
users = []
logined_users = []

app = FastAPI()

def do_login(user: UserDto):
    for cuser in users:
        if cuser.uname == user.uname:
            if cuser.password == user.password:
                prep_token_data = user.uname+user.password
                token = hashlib.sha224(prep_token_data.encode("utf-8")).hexdigest()
                logined_users.append(UserSession(token=token, user=cuser))
                return token
            else:
                return "Wrong password"
    
    return "User doesn't exist"

# Requests handling
@app.post("/login")
def login(user: UserDto):
    return do_login(user)

@app.post("/signup")
def signup(user: UserDto):
    for cuser in users:
        if cuser.uname == user.uname:
            return "User already exists";

    if user.password != user.repassword:
        return "Please validate password and repassword"

    users.append(User(uname=user.uname, password=user.password))

    return do_login(user)

@app.get("/notes")
def all_notes():
    return notes

@app.get("/note/{id}")
def note_by_id(id:int):
    return notes[id]

@app.post("/note")
def add_note(note: NoteDto):
    for logined_user in logined_users:
        if logined_user.token == note.token:
            cnote = Note(title=note.title, description=note.description, uname=logined_user.user.uname)
            notes.append(cnote)
            return cnote
    
    return "User is not logged in"

# use /docs to see generated documentation for API

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("notes:app", reload=True)
