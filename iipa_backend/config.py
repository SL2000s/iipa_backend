from dotenv import load_dotenv

load_dotenv()


ASSUMPTION_EXPANSION_LABEL = 'assumption_expansion'
PROOF_VERIFICATION_LABEL = 'proof_verification'
STATEMENT_VERIFICATION_LABEL = 'statement_verification'
PROOF_LABEL = 'proof'
PROOF_WITHIN_CONTEXT_LABEL = 'proof_within_context'
ADD_CONTEXT_LABEL = 'add_context'
ADD_STATEMENT_LABEL = 'add_statement'
RETRIEVE_PREMISES_LABEL = 'retrieve_premises'


TACTICS = {
    ASSUMPTION_EXPANSION_LABEL: {
        "description": "Expand the implied definitions and assumptions for a given statement.",
        "prompt": "Given a statement p_i, expand the implied definitions and assumptions by eliciting definitions for all terms used in p_i and all known premises behind p_i.",
        # "examples": [
        #     {
        #         "task": "Expand the assumptions for the statement 'For all x in R, if x > 0, then x^2 > 0'.",
        #         "answer": "The term 'x in R' refers to x being a real number. The assumption is that real numbers are ordered and have properties like being positive or negative. The premise behind 'x^2 > 0' assumes the standard properties of real numbers, particularly that squaring any positive real number results in a positive value."
        #     }
        # ],
    },
    PROOF_VERIFICATION_LABEL: {
        "description": "Verify if the entailment between two statements p_i and p_j is logically consistent.",
        "prompt": "Given two statements p_i and p_j, verify if the entailment between the two statements is logically consistent and sound by expanding the steps into granular operations and step-wise inference.",
        # "examples": [
        #     {
        #         "task": "Verify the entailment between 'If a matrix A is invertible, then det(A) ≠ 0' and 'det(A) = 0, so A is not invertible'.",
        #         "answer": "The entailment is logically valid. By contrapositive reasoning, if det(A) = 0, then A is not invertible, which aligns with the original statement 'If A is invertible, then det(A) ≠ 0'."
        #     }
        # ],
    },
    STATEMENT_VERIFICATION_LABEL: {
        "description": "Verify if a given statement is logically correct based on its premises and definitions.",
        "prompt": "Given a statement p_i, verify if the statement is correct by eliciting definitions for all terms used, eliciting relevant premises, and building a granular syllogistic inference.",
        "examples": [
            {
                "task": "Verify the statement 'The sum of two odd integers is always even'.",
                "answer": "The statement is correct. Let two odd integers be represented as 2a + 1 and 2b + 1, where a and b are integers. Their sum is (2a + 1) + (2b + 1) = 2(a + b + 1), which is even because it is divisible by 2."
            }
        ],
    },
    PROOF_LABEL: {
        "description": "Construct a proof to determine if a given statement is true or false.",
        "prompt": "Given a statement p_i, build a proof by eliciting definitions, relevant premises, and constructing a granular proof step-by-step.",
        "examples": [
            {
                "task": "Prove or disprove the statement 'The square of any even number is divisible by 4'.",
                "answer": "Proof: Let the even number be 2n, where n is an integer. The square of 2n is (2n)^2 = 4n^2, which is divisible by 4. Therefore, the statement is true."
            }
        ],
    },
    PROOF_WITHIN_CONTEXT_LABEL: {
        "description": "Construct a proof for a goal statement given a set of premises in a context.",
        "prompt": "Given a goal statement p_i and context P, build a proof by outlining a strategy and executing a step-wise proof based on the premises in the context.",
        # "examples": [
        #     {
        #         "task": "Given the context 'All prime numbers greater than 2 are odd' and '5 is a prime number', prove that '5 is odd'.",
        #         "answer": "Premises: (1) All prime numbers greater than 2 are odd, (2) 5 is a prime number, (3) 5 > 2. Proof: From (1) and (3), we conclude that 5 is odd."
        #     }
        # ],
    },
    ADD_CONTEXT_LABEL: {
        "description": "Add the previous context to the knowledge base.",
        "prompt": "Add the current proof context to the knowledge base for future reference.",
        # "examples": [
        #     {
        #         "task": "Add the context 'The derivative of a constant function is zero' to the knowledge base.",
        #         "answer": "Context 'The derivative of a constant function is zero' successfully added to the knowledge base for future retrieval."
        #     }
        # ],
    },
    ADD_STATEMENT_LABEL: {
        "description": "Add a given statement to the knowledge base with an optional proof and description.",
        "prompt": "Add statement p_i to the knowledge base, optionally including a proof and description.",
        # "examples": [
        #     {
        #         "task": "Add the statement 'The integral of x^n from 0 to 1 is 1/(n+1) for n ≠ -1' to the knowledge base.",
        #         "answer": "Statement 'The integral of x^n from 0 to 1 is 1/(n+1) for n ≠ -1' has been added to the knowledge base with proof included."
        #     }
        # ],
    },
    RETRIEVE_PREMISES_LABEL: {
        "description": "Retrieve premises related to a given search term from the knowledge base.",
        "prompt": "Retrieve premises from the knowledge base related to the search term or statement s.",
        # "examples": [
        #     {
        #         "task": "Retrieve premises related to the term 'Pythagorean theorem'.",
        #         "answer": "Premises retrieved: (1) In a right triangle, the square of the hypotenuse is equal to the sum of the squares of the other two sides (c^2 = a^2 + b^2)."
        #     }
        # ],
    }
}
