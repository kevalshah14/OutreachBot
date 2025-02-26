from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

# Import your app from routes
from app.api.routes import app

# Add CORS middleware
origins = [
    "http://localhost",  # Allow local development
    "http://localhost:3000",  # Allow local frontend (React, etc.)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Can be ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

def start():
    # Get settings from environment variables or use default values
    UVICORN_HOST = os.getenv("UVICORN_HOST", "127.0.0.1")
    UVICORN_PORT = int(os.getenv("UVICORN_PORT", "8000"))
    UVICORN_RELOAD = os.getenv("UVICORN_RELOAD", "True").lower() == "true"

    uvicorn.run(
        "app.main:app",
        host=UVICORN_HOST,
        port=UVICORN_PORT,
        reload=UVICORN_RELOAD,
    )

if __name__ == "__main__":
    start()
