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
    return {"answer": answer.answer, "latex_macros": answer.latex_macros}  # TODO: is there a better way of doing this?


if __name__ == '__main__':      # TODO: remove
    prompt_with_history = Prompt(
        prompt='Explain more',
        history=[
            {
                'prompt': 'What is Switzerland?',
                'answer': 'Switzerland is a country in Europe.',
            },
        ],
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
    proof_in_context_prompt = Prompt(
        prompt='Given the statements "A prime number is only divisible by 1 and itself", and "9 is divisible by 3", prove "9 is not a prime number."',
    )
    empirical_verification_prompt = Prompt(
        prompt='Verify empirically that the statement p_i is true.\np_i: If x=2 then 2x=4',
        kb_label='lm_theory',
    )
    premises_retrieval_prompt = Prompt(
        prompt='What are the premises related to the statement "The sum of two odd numbers is even."',
    )
    custom_prompt = Prompt(
        # prompt='Solve x^2=4',
        # prompt='Who found out that a^2 + b^2 = c^2',
        # prompt='Explain more',
        # history=[
        #     {
        #         'prompt': 'What is Switzerland?',
        #         'answer': 'Switzerland is a country in Europe.',
        #     },
        # ],
        prompt='What does theorem 2 say?'
    )
    premises_retrieval_prompt_kb = Prompt(
        # prompt='What are the premises behind Theorem 6?',
        # prompt='''Create a list of all premises related to Theorem 1''',
        prompt='''Prove "Theorem 1"''',
        kb_label='lm_theory'
    )

    import asyncio
    ans = asyncio.run(submit_prompt(empirical_verification_prompt))
    print(ans)

    # from iipa_backend.services.prompt.llm_quest import kb_quest
    # ans = asyncio.run(kb_quest(premises_retrieval_prompt_kb.prompt_with_history(), 'lm_theory'))
    # print(ans)
