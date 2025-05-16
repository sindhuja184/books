from fastapi import FastAPI
from fastapi.requests import Request
import time
import logging
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware


#In the console no information about the requests
#Is being displayed because of the code below
logger = logging.getLogger('uvicorn.access')
logger.disabled = True


def register_middleware(app: FastAPI):
    
    @app.middleware('http')
    async def custom_logging(request: Request, call_next):  
        '''
        request: The incoming HTTP request.

        call_next: A function that forwards the request to the next middleware or the route handler and returns the response.
        call_next is qa function automatically provided to the fastapi
        '''
        start_time = time.time()

        print("Before", start_time)

        response = await call_next(request)

        processing_time = time.time() - start_time

        message = f"{request.method} - {request.url.path} - {response.status_code} - completed after {processing_time}"

        print(message)
        return response
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods= ["*"],
        allow_headers=["*"],
        allow_credentials = True
    )

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts = ["*"],
        
    )

    @app.middleware('http')
    async def authorization(request: Request, call_next):
        if not "Authorization" in request.headers:
            return JSONResponse(
                content= {
                    "message" : "Not Authenticated",
                    "resolution": "Please provide the right credentials to proceed"
                }, 
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        response = await call_next(request)
        
        return response
    




