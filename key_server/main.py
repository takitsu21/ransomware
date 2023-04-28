from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from src.exceptions import UnicornException
from src.schemas import KeyPairBase
from src.database import Database
from src.models import KeyPairModel
from src.auth import api_key_auth
from crypto.keypair import KeyPair
import subprocess
import sys
import os
import traceback
import sqlalchemy.exc

app = FastAPI(debug=True)
DB = Database(db_url=os.getenv("DATABASE_URL"))


@app.get("/keys/private_key/{uuid}/", dependencies=[Depends(api_key_auth)])
async def get_private_key(uuid: str, db=Depends(DB)):
    key = db.get_key(uuid)
    if key:
        return {"private_key": key.private_key}
    else:
        raise HTTPException(status_code=404, detail="Key not found")


@app.get("/keys/public_key/{uuid}/")
async def get_public_key(uuid: str, db=Depends(DB)):
    key = db.get_key(uuid)
    if key:
        return {"public_key": key.public_key}
    else:
        raise HTTPException(status_code=404, detail="Key not found")


@app.get("/keys/aes_key/{uuid}/")
async def get_aes_key(uuid: str, db=Depends(DB)):
    key = db.get_key(uuid)
    if key:
        return {"aes_key": key.aes_key}
    else:
        raise HTTPException(status_code=404, detail="Key not found")


@app.post("/keys/")
async def add_keys(base: KeyPairBase, db=Depends(DB)):
    try:
        keypair = KeyPair()
        model = KeyPairModel(
            uuid=base.uuid,
            private_key=keypair.private_key,
            public_key=keypair.public_key)
        db.add_record(model)
        return {"message": "Key added"}
    except Exception as e:
        traceback.print_exc()
        if isinstance(e, sqlalchemy.exc.IntegrityError):
            raise HTTPException(status_code=500, detail="Key already exists")
        raise HTTPException(status_code=500, detail="Key not added")


@app.get("/keys/{uuid}")
async def get_keys(uuid: str, db=Depends(DB)):
    key = db.get_key(uuid)
    key.aes_key = str(key.aes_key)
    if key:
        return key
    else:
        raise HTTPException(status_code=404, detail="Keys not found")


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=500,
        content={"message": traceback.format_exc()},
    )
