from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from types import SimpleNamespace

from iipa_backend.controllers.tactic_controller import TacticController
from iipa_backend.models.prompt import Prompt


app = FastAPI()

# Set up CORS so the frontend can communicate with the backend
allow_origins = os.getenv("ALLOW_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


context = SimpleNamespace()
context.tactic_controller = TacticController()


@app.get("/")
async def root():
    return {"message": "Welcome to the IIPA FastAPI Backend"}


@app.post("/submit_prompt")
async def submit_prompt(prompt: Prompt):
    """Submit a prompt and get an answer."""
    answer = await context.tactic_controller.process_user_prompt(prompt)
    return {"answer": answer}


if __name__ == '__main__':      # TODO: remove
    prompt = Prompt(
        prompt='Explain more',
        history=[
            {
                'prompt': 'What is Switzerland?',
                'answer': 'Switzerland is a country in Europe.'
            }
        ]
    )
    prompt = Prompt(
        prompt='If x=1, is 2x=2?',
        # history=[
        #     {
        #         'prompt': 'What is Switzerland?',
        #         'answer': 'Switzerland is a country in Europe.'
        #     }
        # ]
    )
    import asyncio
    ans = asyncio.run(submit_prompt(prompt))
    print(ans)
