# from app.routes import tactics, kb                                            # TODO: implement or remove
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from types import SimpleNamespace

from iipa_backend.models.prompt import Prompt
from iipa_backend.controllers.prompt_controller import PromptController


app = FastAPI()

# Set up CORS so the frontend can communicate with the backend
allow_origins = os.getenv("ALLOW_ORIGINS", "http://localhost:3000").split(",")  # TODO: add ALLOW_ORIGINS to .env
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(tactics.router, prefix="/tactics", tags=["Tactics"])       # TODO: implement or remove
# app.include_router(kb.router, prefix="/kb", tags=["Knowledge Base"])          # TODO: implement or remove


context = SimpleNamespace()
context.prompt_controller = PromptController()


@app.get("/")
async def root():
    return {"message": "Welcome to the IIPA FastAPI Backend"}


@app.post("/submit_prompt")
async def submit_prompt(prompt_request: Prompt):
    """Submit a prompt and get an answer."""
    prompt = prompt_request.prompt
    answer = await context.prompt_controller.process_prompt(prompt)
    return {"answer": answer}
