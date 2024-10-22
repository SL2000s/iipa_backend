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
    prompt_with_history = Prompt(
        prompt='Explain more',
        history=[
            {
                'prompt': 'What is Switzerland?',
                'answer': 'Switzerland is a country in Europe.'
            }
        ]
    )
    assumptions_expansion_prompt = Prompt(
        prompt='What are the assumptions behind "The sum of two odd integers are even."',
    )
    eintailment_verification_prompt = Prompt(
        prompt='If x=1, is 2x=2?',
    )
    statement_verification_prompt = Prompt(
        prompt='Is it true that the square of an integer is always congruent to 0 or 1 modulo 3?',
    )
    proof_prompt = Prompt(
        prompt='Prove that a^2 + b^2 = c^2 for a right triangle with legs a and b, and hypothenuse c.',
    )
    proof_in_context = Prompt(
        prompt='Given the statements "A prime number is only divisible by 1 and itself", and "9 is divisible by 3", prove "9 is not a prime number."',
    )

    import asyncio
    ans = asyncio.run(submit_prompt(proof_in_context))
    print(ans)
