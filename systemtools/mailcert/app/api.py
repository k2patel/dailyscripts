from fastapi import Request, FastAPI
from typing import Optional
import app.mail as am
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel

class Register(BaseModel):
    hostname:str
    ssl_cert:str
    class Register:
        schema_extra = {
            "example": {
                "hostname": "fqdn - hostname",
                "ssl_cert": "----- start certificate -----\nasdfasdfadsfasdfas8784q234ihr32qj4\n----- end certificate -----",
                }
            }

app = FastAPI(title="Email ssl cert to authorize",
    description="This is simple tool to automate ssl submission",
    version="0.1")

@app.get("/", tags=["Home"])
async def get_root() -> dict:
    return {
        "message": "Welcome to the SSLAPI app."
    }

@app.get("/register")
async def get_body(request: Register):
    y = json.loads(request.json())
    json_compatible_item_data = jsonable_encoder(am.smail(y["hostname"], y["ssl_cert"]))
    return JSONResponse(content=json_compatible_item_data)