from dotenv import load_dotenv
import os

from iipa_backend.config._prompts import(
    EXAMPLE_TEMPLATE,
    NL2TACTIC_PROMPT_TEMPLATE,
    TACTIC_STR_TEMPLATE,
    PROMPT_WITH_HISTORY_TEMPLATE,
)


load_dotenv()


ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)))
TACTICS_DIR = os.path.join(ROOT, 'services', 'tactics')
PROMPT_TACTICS_DIR = os.path.join(TACTICS_DIR, 'prompt_tactics')

# Azure OpenAI API parameters
PROMPT_TEMPLATE_FORMAT = 'jinja2'
OPENAI_MODEL_NAME = 'gpt-4o'
OPENAI_TEMPERATURE = 1e-16
OPENAI_API_TYPE = 'azure'
OPENAI_API_VERSION = '2024-02-01'
OPENAI_DEPLOYMENT_NAME = 'lunar-chatgpt-4o'
OPENAI_TOP_P = 1e-16
OPENAI_SEED = 1234


# Tactics
ASSUMPTION_EXPANSION_LABEL = 'assumption_expansion'
ENTAILMENT_VERIFICATION_LABEL = 'entailment_verification'
STATEMENT_VERIFICATION_LABEL = 'statement_verification'
PROOF_LABEL = 'proof'
PROOF_WITHIN_CONTEXT_LABEL = 'proof_within_context'
ADD_CONTEXT_LABEL = 'add_context'
ADD_STATEMENT_LABEL = 'add_statement'
RETRIEVE_PREMISES_LABEL = 'retrieve_premises'
CUSTOM_PROMPT_LABEL = 'custom_prompt'

ACTIVE_TACTICS = [
    ENTAILMENT_VERIFICATION_LABEL
]

TACTICS_DATA = {
    # ASSUMPTION_EXPANSION_LABEL: {
    #     "description": "Expand the implied definitions and assumptions for a given statement.",
    #     "prompt": "Given a statement p_i, expand the implied definitions and assumptions by eliciting definitions for all terms used in p_i and all known premises behind p_i.",
    #     # "examples": [
    #     #     {
    #     #         "task": "Expand the assumptions for the statement 'For all x in R, if x > 0, then x^2 > 0'.",
    #     #         "answer": "The term 'x in R' refers to x being a real number. The assumption is that real numbers are ordered and have properties like being positive or negative. The premise behind 'x^2 > 0' assumes the standard properties of real numbers, particularly that squaring any positive real number results in a positive value."
    #     #     }
    #     # ],
    # },
    ENTAILMENT_VERIFICATION_LABEL: {
        "description": "Verifies if the entailment between two statements p_i and p_j is logically consistent.",
        "tactic_prompt": "Given two statements p_i and p_j verify if the entailment between the two statements are logically consistent and sound by formally:\nExpanding the steps into granular operations and step-wise inference steps.\n-Elicit all supported premises and definitions.\n-For each step validate the consistency and correctness.\n-Return a final assessment if p_j is entailed by  p_i and the supporting proof.\n\np_i: {p_i}\np_j: {p_j}",
        "template_variables": [
            "p_i",
            "p_j",
        ],
        "examples": [
            {
                "user_prompt": "Verify that p_j follows from p_i.\n\np_i: 'A matrix A is invertible if and only if det(A) ≠ 0'\np_j: 'det(A) = 0, so A is not invertible'",
                "template_variables": {
                    "p_i": "A matrix A is invertible if and only if det(A) ≠ 0",
                    "p_j": "det(A) = 0, so A is not invertible",
                },
                "answer": "### Entailment Verification Example:\n\nWe are tasked with verifying whether the statement \( p_j \) follows logically from the statement \( p_i \).\n\n### Given Statements:\n- **Statement \( p_i \):**  \n  \"A matrix \( A \) is invertible if and only if \( \text{det}(A) \neq 0 \).\"  \n  (Formally: \( p_i = \text{Invertible}(A) \iff \text{det}(A) \neq 0 \))\n\n- **Statement \( p_j \):**  \n  \"det(A) = 0, so \( A \) is not invertible.\"  \n  (Formally: \( p_j = \text{det}(A) = 0 \rightarrow \neg \text{Invertible}(A) \))\n\n### Step-by-Step Verification Process\n\n#### 1. **Formal Definitions:**\n\n   - \( p_i \) (Invertibility condition):  \n     \( \text{Invertible}(A) \iff \text{det}(A) \neq 0 \)  \n     This is a biconditional statement that asserts a matrix \( A \) is invertible if and only if its determinant is not zero.\n   \n   - \( p_j \) (Non-invertibility conclusion):  \n     \( \text{det}(A) = 0 \rightarrow \neg \text{Invertible}(A) \)  \n     This is an implication that states if the determinant of \( A \) is zero, then \( A \) is not invertible.\n\n#### 2. **Expanding the Definitions:**\n\n   - \( p_i \) can be split into two implications:  \n     - If \( \text{Invertible}(A) \), then \( \text{det}(A) \neq 0 \) (i.e., \( \text{Invertible}(A) \rightarrow \text{det}(A) \neq 0 \)).\n     - If \( \text{det}(A) \neq 0 \), then \( A \) is invertible (i.e., \( \text{det}(A) \neq 0 \rightarrow \text{Invertible}(A) \)).\n\n   - The contrapositive of the second implication is:  \n     \( \text{det}(A) = 0 \rightarrow \neg \text{Invertible}(A) \).  \n     This is the key to the logic in \( p_j \).\n\n#### 3. **Establishing Supporting Premises and Definitions:**\n   - The contrapositive rule states that \( p \rightarrow q \) is logically equivalent to \( \neg q \rightarrow \neg p \).\n   - From \( p_i \), the second implication \( \text{det}(A) \neq 0 \rightarrow \text{Invertible}(A) \) is valid. Applying the contrapositive, we obtain \( \text{det}(A) = 0 \rightarrow \neg \text{Invertible}(A) \).\n\n#### 4. **Step-wise Inference:**\n   - From \( p_i \), we have the contrapositive:  \n     \( \text{det}(A) = 0 \rightarrow \neg \text{Invertible}(A) \).  \n   - This is exactly what is asserted by \( p_j \).\n\n#### 5. **Validation of Consistency and Correctness:**\n   - \( p_j \) directly matches the contrapositive of the second part of the biconditional in \( p_i \).\n   - Therefore, \( p_j \) is logically consistent with \( p_i \).\n\n#### 6. **Final Assessment:**\n   - \( p_j \) (\"If \( \text{det}(A) = 0 \), then \( A \) is not invertible\") follows directly from \( p_i \) (\"A matrix \( A \) is invertible if and only if \( \text{det}(A) \neq 0 \)) by the contrapositive of the second part of the biconditional.\n  \nThus, **\( p_j \) is entailed by \( p_i \)**. The proof is sound and logically consistent.",
            },
        ],
        "location": {
            "module_path": os.path.join(PROMPT_TACTICS_DIR, 'entailment_verification.py'),
            "class_name": "EntailmentVerifier",
        }
    },
    CUSTOM_PROMPT_LABEL: {
        "description": "",
        "tactic_prompt": "{user_prompt}",
        "template_variables": [
            "user_prompt"
        ],
        "examples": [],
    },
    # STATEMENT_VERIFICATION_LABEL: {
    #     "description": "Verify if a given statement is logically correct based on its premises and definitions.",
    #     "prompt": "Given a statement p_i, verify if the statement is correct by eliciting definitions for all terms used, eliciting relevant premises, and building a granular syllogistic inference.",
    #     "examples": [
    #         {
    #             "task": "Verify the statement 'The sum of two odd integers is always even'.",
    #             "answer": "The statement is correct. Let two odd integers be represented as 2a + 1 and 2b + 1, where a and b are integers. Their sum is (2a + 1) + (2b + 1) = 2(a + b + 1), which is even because it is divisible by 2."
    #         }
    #     ],
    # },
    # PROOF_LABEL: {
    #     "description": "Construct a proof to determine if a given statement is true or false.",
    #     "prompt": "Given a statement p_i, build a proof by eliciting definitions, relevant premises, and constructing a granular proof step-by-step.",
    #     "examples": [
    #         {
    #             "task": "Prove or disprove the statement 'The square of any even number is divisible by 4'.",
    #             "answer": "Proof: Let the even number be 2n, where n is an integer. The square of 2n is (2n)^2 = 4n^2, which is divisible by 4. Therefore, the statement is true."
    #         }
    #     ],
    # },
    # PROOF_WITHIN_CONTEXT_LABEL: {
    #     "description": "Construct a proof for a goal statement given a set of premises in a context.",
    #     "prompt": "Given a goal statement p_i and context P, build a proof by outlining a strategy and executing a step-wise proof based on the premises in the context.",
    #     # "examples": [
    #     #     {
    #     #         "task": "Given the context 'All prime numbers greater than 2 are odd' and '5 is a prime number', prove that '5 is odd'.",
    #     #         "answer": "Premises: (1) All prime numbers greater than 2 are odd, (2) 5 is a prime number, (3) 5 > 2. Proof: From (1) and (3), we conclude that 5 is odd."
    #     #     }
    #     # ],
    # },
    # ADD_CONTEXT_LABEL: {
    #     "description": "Add the previous context to the knowledge base.",
    #     "prompt": "Add the current proof context to the knowledge base for future reference.",
    #     # "examples": [
    #     #     {
    #     #         "task": "Add the context 'The derivative of a constant function is zero' to the knowledge base.",
    #     #         "answer": "Context 'The derivative of a constant function is zero' successfully added to the knowledge base for future retrieval."
    #     #     }
    #     # ],
    # },
    # ADD_STATEMENT_LABEL: {
    #     "description": "Add a given statement to the knowledge base with an optional proof and description.",
    #     "prompt": "Add statement p_i to the knowledge base, optionally including a proof and description.",
    #     # "examples": [
    #     #     {
    #     #         "task": "Add the statement 'The integral of x^n from 0 to 1 is 1/(n+1) for n ≠ -1' to the knowledge base.",
    #     #         "answer": "Statement 'The integral of x^n from 0 to 1 is 1/(n+1) for n ≠ -1' has been added to the knowledge base with proof included."
    #     #     }
    #     # ],
    # },
    # RETRIEVE_PREMISES_LABEL: {
    #     "description": "Retrieve premises related to a given search term from the knowledge base.",
    #     "prompt": "Retrieve premises from the knowledge base related to the search term or statement s.",
    #     # "examples": [
    #     #     {
    #     #         "task": "Retrieve premises related to the term 'Pythagorean theorem'.",
    #     #         "answer": "Premises retrieved: (1) In a right triangle, the square of the hypotenuse is equal to the sum of the squares of the other two sides (c^2 = a^2 + b^2)."
    #     #     }
    #     # ],
    # }
}

 
# EXAMPLES_LIST = []
# for tactic_key, tactic_data in TACTICS_DATA.items():
#     for example in tactic_data.get('examples', []):
#         EXAMPLES_LIST.append(
#             EXAMPLE_TEMPLATE.format(
#                 task=example['user_prompt'],
#                 answer=tactic_key,
#             )
#         )
# EXAMPLES_STR = '\n\n'.join(EXAMPLES_LIST)


# NL2TACTIC_PROMPT_TEMPLATE = NL2TACTIC_PROMPT_TEMPLATE_TEMPLATE.format(
#     tactics_str=TACTICS_STR,
#     examples_str=EXAMPLES_STR,
# )
