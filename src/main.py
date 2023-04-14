import os
import sys

sys.path.insert(0, os.getcwd())
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.utils.common_logger import logger
from src.utils.custom_error_handlers import BaseError
from src.endpoints import status, docs, job

# Create Web API Application
app = FastAPI()

# Global error handler. All raised exceptions will be caught here.
@app.exception_handler(BaseError)
def validation_exception_handler(request: Request, err: BaseError) -> JSONResponse:
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    logger.error(base_error_message)
    return JSONResponse(
        status_code=err.status_code,
        content={"message": f"{base_error_message}", "detail": f"{err}"},
    )


# Add endpoints
app.include_router(docs.router)
app.include_router(status.router)
app.include_router(job.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


if __name__ == "__main__":
    # Run FastAPI
    uvicorn.run("main:app", host="0.0.0.0", port=5555, log_level="info", reload=True)
