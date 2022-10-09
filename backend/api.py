from http import HTTPStatus
from lib2to3.pytree import Base
from fastapi import FastAPI
from database import DB
from pydantic import BaseModel

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
db = DB()

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Transection(BaseModel):
    content: str
    
@app.get("/api/blocks")
async def get_all_blocks():
    return {"message": db.fetch_blocks()}

@app.get("/api/blocks/tail")
async def get_tail_block():
    rest = db.fetch_last_block()
    return {"message": rest}

@app.get("/api/ping")
async def ping():
    return {"message": "pong"}

@app.get("/api/server_status")
async def get_server_status():
    res = db.fetch_server_status()
    msg = {"message": res}
    json_compatible_item_data = jsonable_encoder(msg)
    return JSONResponse(content=json_compatible_item_data)

@app.get("/api/transections")
async def get_transections():
    res = db.fetch_transections();
    msg = {"message": res}
    json_compatible_item_data = jsonable_encoder(msg)
    return JSONResponse(content=json_compatible_item_data)

@app.post("/api/add-transection")
async def create_transection(data: Transection):
    db.insert_transection(data.content)
    msg = {"message": HTTPStatus.OK}
    json_compatible_item_data = jsonable_encoder(msg)
    return JSONResponse(content=json_compatible_item_data)

# api server will communicate with Database
db.init()