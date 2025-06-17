from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware

import time
import logging


# note that for adding a seperate middleware compliant with ASGI Unicorn servers 
# we register it eg CORS built in the FAST API.

# from src.errors import logging
# Just disabling the default logger by the Uvicorn server:
logger = logging.getLogger("uvicorn.access")
logger.disabled = True


def register_middleware(app: FastAPI):

    @app.middleware("http")
    async def custom_logging(req: Request, callNext):
        s_time = time.time()
        # print("Before")

        result = await callNext(req)
        e_time = time.time()
        message = f"{req.client.host}:{req.client.port} - {req.method} - {req.url.path} - {result.status_code} Time taken: {e_time-s_time}s" # type: ignore

        print(message)
        return result
    
    # @app.middleware("http")
    # async def auth(req:Request,call_next):
    #     if not "Authorization" in req.headers:
    #         return JSONResponse(content=
    #             {
    #                 "Message":"Not authenticated",
    #                 "Solution":"please provide correct credentials to proceed."
    #             }
    #         )
    #     response=await call_next(req)
    #     return response
    
    app.add_middleware(CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=['*'],
        allow_credentials=True,
    ) # type: ignore
    