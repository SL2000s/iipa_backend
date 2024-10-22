from dotenv import load_dotenv
import logging
import os
import re

from iipa_backend.config._prompts import(
    EXAMPLE_NL2TACTIC_TEMPLATE,
    NL2TACTIC_TEMPLATE,
    TACTIC_STR_TEMPLATE,
    PROMPT_WITH_HISTORY_TEMPLATE,
    EXAMPLE_PROMPT2TEMPLATE_VARIABLES_TEMPLATE,
    PROMPT2TEMPLATE_VARIABLES_TEMPLATE,
)


load_dotenv()


# Define paths
SRC_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)))
PKG_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
TACTICS_DIR = os.path.join(SRC_ROOT, 'services', 'tactics')
PROMPT_TACTICS_DIR = os.path.join(TACTICS_DIR, 'prompt_tactics')
LOG_DIR = os.path.join(PKG_ROOT, 'logs')


# Configure logging
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_DIR, 'iipa_backend.log')
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(),
    ],
)
logging.getLogger('httpcore').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('openai').setLevel(logging.WARNING)



# Azure OpenAI API parameters
PROMPT_TEMPLATE_FORMAT = 'jinja2'
OPENAI_MODEL_NAME = 'gpt-4o'
OPENAI_TEMPERATURE = 1e-16
OPENAI_API_TYPE = 'azure'
OPENAI_API_VERSION = '2024-02-01'
OPENAI_DEPLOYMENT_NAME = 'lunar-chatgpt-4o'
OPENAI_TOP_P = 1e-16
OPENAI_SEED = 1234


# Regex patterns
CODE_PATTERN = re.compile(r'```.*\n(.*?)\n```', re.DOTALL)


# Tactics
ASSUMPTIONS_EXPANSION_LABEL = 'assumptions_expansion'
ENTAILMENT_VERIFICATION_LABEL = 'entailment_verification'
STATEMENT_VERIFICATION_LABEL = 'statement_verification'
PROOF_LABEL = 'proof'
PROOF_WITHIN_CONTEXT_LABEL = 'proof_within_context'
ADD_CONTEXT_LABEL = 'add_context'
ADD_STATEMENT_LABEL = 'add_statement'
RETRIEVE_PREMISES_LABEL = 'retrieve_premises'
CUSTOM_PROMPT_LABEL = 'custom_prompt'

ACTIVE_TACTICS = [
    ASSUMPTIONS_EXPANSION_LABEL,
    ENTAILMENT_VERIFICATION_LABEL,
    PROOF_LABEL,
    STATEMENT_VERIFICATION_LABEL,
]

TACTICS_DATA = {
    ASSUMPTIONS_EXPANSION_LABEL: {
        "description": "Expands the implied definitions and assumptions for a given statement.",
        "tactic_prompt_template": "Given a statement p_i expand the implied definitions and assumptions by formally:\n-Eliciting definitions for all terms used in p_i.\n-Eliciting all known premises behind p_i.\n-Return a list with the definitions and premises.\n\n{p_i}",
        "template_variables": [
            "p_i",
        ],
        "examples": [
            {
                "user_prompt": "Expand the implied definitions and assumptions from p_i.\n\np_i: For all x in R, if x > 0, then x^2 > 0.",
                "template_variables": {
                    "p_i": "For all x in R, if x > 0, then x^2 > 0",
                },
                "answer": "The term 'x in R' refers to x being a real number. The assumption is that real numbers are ordered and have properties like being positive or negative. The premise behind 'x^2 > 0' assumes the standard properties of real numbers, particularly that squaring any positive real number results in a positive value.",
            },
            {
                "user_prompt": "Expand assumptions from 'All prime numbers greater than 2 are odd.'",
                "template_variables": {
                    "p_i": "All prime numbers greater than 2 are odd."
                },
                "answer": "### Definitions:\n\n1. **Prime number**: A natural number greater than 1 that has no positive divisors other than 1 and itself. Formally, a number \( p \) is prime if for any \( a \) and \( b \), if \( p = ab \), then either \( a = 1 \) or \( b = 1 \).\n2. **Odd number**: A number \( n \) that can be expressed in the form \( n = 2k + 1 \), where \( k \) is an integer.\n3. **Even number**: A number \( n \) that can be expressed in the form \( n = 2k \), where \( k \) is an integer.\n4. **Greater than 2**: A number is greater than 2 if it is larger than 2 in magnitude (i.e., \( n > 2 \)).\n  \n### Premises:\n\n1. **All prime numbers**: Every number that meets the definition of a prime number is considered.\n2. **Prime numbers are either 2 or odd**: The only even prime number is 2. All other prime numbers, if they exist, must be odd (as dividing by 2 would violate the prime property).\n3. **2 is not greater than 2**: The number 2 is explicitly excluded from the claim because it is not greater than itself.\n4. **All even numbers greater than 2 are composite**: Any even number \( n > 2 \) is not prime because it has divisors other than 1 and itself, namely 2.\n\n### Conclusion:\n\n- Every prime number that is greater than 2 must be odd, as an even number greater than 2 cannot be prime.\n  \n**List of Definitions and Premises:**\n1. **Prime number**: A number with no divisors other than 1 and itself.\n2. **Odd number**: A number of the form \( 2k + 1 \), where \( k \) is an integer.\n3. **Even number**: A number of the form \( 2k \), where \( k \) is an integer.\n4. **Greater than 2**: A number larger than 2.\n5. **Premise 1**: The number 2 is the only even prime.\n6. **Premise 2**: All numbers greater than 2 are either odd or composite.\n7. **Premise 3**: A number greater than 2 cannot be both even and prime.",
            },
        ],
        "location": {
            "module_path": os.path.join(PROMPT_TACTICS_DIR, 'assumptions_expansion.py'),
            "class_name": "AssumptionsExpander",
        },
    },
    ENTAILMENT_VERIFICATION_LABEL: {
        "description": "Verifies if the entailment between two statements p_i and p_j is logically consistent.",
        "tactic_prompt_template": "Given two statements p_i and p_j verify if the entailment between the two statements are logically consistent and sound by formally:\n-Expanding the steps into granular operations and step-wise inference steps.\n-Elicit all supported premises and definitions.\n-For each step validate the consistency and correctness.\n-Return a final assessment if p_j is entailed by  p_i and the supporting proof.\n\np_i: {p_i}\np_j: {p_j}",
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
            {
                "user_prompt": "If x=1, is 2x=2?",
                "template_variables": {
                    "p_i": "x=1",
                    "p_j": "2x=2"
                },
                "answer": "To assess whether the statement \( p_j: 2x = 2 \) is logically entailed by \( p_i: x = 1 \), we can break down the inference into granular steps, ensuring the consistency and correctness of each step.\n\n### 1. **Identify Premises**\n   - **Premise 1** \( p_i: x = 1 \)\n     - This is the given premise that defines the value of \( x \).\n   - **Premise 2** \( p_j: 2x = 2 \)\n     - This is the conclusion that we need to assess whether it is logically entailed by \( p_i \).\n\n### 2. **Definitions and Assumptions**\n   - **Entailment**: A statement \( p_j \) is logically entailed by \( p_i \) if and only if \( p_j \) must be true whenever \( p_i \) is true.\n   - **Consistency**: A set of statements is consistent if it is possible for all of them to be true at the same time.\n\n### 3. **Granular Steps and Inference Process**\n\n   #### Step 1: **Evaluate \( p_i \)**\n   - The statement \( p_i: x = 1 \) assigns the value 1 to \( x \).\n   - No inconsistencies are present with this assignment, and \( p_i \) is a sound statement.\n\n   #### Step 2: **Substitute \( x = 1 \) into \( p_j \)**\n   - The statement \( p_j: 2x = 2 \) involves \( x \).\n   - Substitute the value of \( x \) from \( p_i \) into \( p_j \):\n     \[\n     2x = 2 \quad 	ext{becomes} \quad 2(1) = 2\n     \]\n     \[\n     2 = 2\n     \]\n   - This equality holds true, so the substituted form of \( p_j \) is a valid and consistent statement.\n\n   #### Step 3: **Check Logical Entailment**\n   - Since \( p_j \) holds true under the assumption that \( p_i \) is true (because \( 2x = 2 \) simplifies to \( 2 = 2 \) after substitution), the truth of \( p_j \) is guaranteed by the truth of \( p_i \).\n   - Therefore, \( p_j \) is logically entailed by \( p_i \).\n\n### 4. **Validation of Consistency and Soundness**\n   - The steps taken in this process maintain consistency because no contradictions or inconsistencies arise.\n   - The substitution step and simplification are mathematically sound, as the operations follow the basic principles of arithmetic.\n\n### 5. **Final Assessment**\n   - \( p_j: 2x = 2 \) is logically entailed by \( p_i: x = 1 \).\n   - The supporting proof relies on substitution and simplification, confirming that the entailment is consistent and sound.\n\nThus, the conclusion is that \( p_j \) is **entailed by** \( p_i \).",
            },
        ],
        "location": {
            "module_path": os.path.join(PROMPT_TACTICS_DIR, 'entailment_verification.py'),
            "class_name": "EntailmentVerifier",
        },
    },
    PROOF_LABEL: {
        "description": "Constructs a proof to determine if a statements p_i is true or false.",
        "tactic_prompt_template": "Given a statement p_i build a proof if p_i is true or false, by formally:\n-Eliciting definitions for all terms used in p_i.\n-Eliciting all relevant premises behind p_i.\n-Building a granular proof (one operation per step) between the set of premises and the statement p_i.\n-Return a final assessment if p_i is entailed by the premises and definitions and the proof.\n\np_i: {p_i}",
        "template_variables": [
            "p_i",
        ],
        "examples": [
            {
                "user_prompt": "Prove p_i.\n\np_i: The square of any even number is divisible by 4.",
                "template_variables": {
                    "p_i": "The square of any even number is divisible by 4.",
                },
                "answer": "To prove or disprove the statement \( p_i \): \"The square of any even number is divisible by 4,\" let's break it down using the approach you suggested:\n\n### Step 1: Definitions of all terms\n- **Even number**: A number \( n \) is said to be even if there exists an integer \( k \) such that \( n = 2k \).\n- **Square of a number**: The square of a number \( n \) is \( n^2 = n \times n \).\n- **Divisibility by 4**: A number \( m \) is divisible by 4 if there exists an integer \( l \) such that \( m = 4l \).\n\n### Step 2: Relevant premises\n- Any even number can be written as \( n = 2k \), where \( k \) is an integer.\n- The square of any number is \( n^2 = n \times n \).\n- For a number to be divisible by 4, the result must be of the form \( m = 4l \), where \( l \) is an integer.\n\n### Step 3: Building the granular proof\n\n#### Proof:\n1. Let \( n \) be any even number. By definition, we can write \( n = 2k \), where \( k \) is an integer.\n2. The square of \( n \) is:\n   \[\n   n^2 = (2k)^2\n   \]\n3. Simplify the square:\n   \[\n   n^2 = 2k \times 2k = 4k^2\n   \]\n4. Now, observe that \( n^2 = 4k^2 \) is divisible by 4 because we can rewrite it as:\n   \[\n   n^2 = 4(k^2)\n   \]\n   where \( k^2 \) is an integer (since \( k \) is an integer, the square of an integer is also an integer).\n\n5. Thus, \( n^2 \) is of the form \( 4l \), where \( l = k^2 \) is an integer.\n\n### Step 4: Final assessment\nSince \( n^2 = 4k^2 \) is divisible by 4 for any even \( n \), we conclude that the statement \( p_i \) is **true**.",
            },
        ],
        "location": {
            "module_path": os.path.join(PROMPT_TACTICS_DIR, 'proof.py'),
            "class_name": "Prover",
        }
    },
    STATEMENT_VERIFICATION_LABEL: {
        "description": "Verifies if a given statement p_i is correct.",
        "tactic_prompt_template": "Given a statement p_i verify if the statement is correct by formally:\n-Eliciting definitions for all terms used in p_i.\n-Eliciting all relevant premises behind p_i.\n-Establishing the soundness of each premise and definition.\n-Building a granular syllogistic inference between the set of premises and the statement p_i.\n-Return a final assessment if p_i is entailed by the premises and definitions.\n\np_i: {p_i}",
        "template_variables": [
            "p_i",
        ],
        "examples": [
            {
                "user_prompt": "Is p_i correct?\n\np_i: The sum of two odd integers is always even.",
                "template_variables": {
                    "p_i": "The sum of two odd integers is always even."
                },
                "answer": "Let's verify the statement \( p_i \): \"The sum of two odd integers is always even,\" by following the requested steps.\n\n### Step 1: Eliciting Definitions\n\n1. **Odd Integer**: \n   - An integer \( n \) is called odd if it can be written in the form \( n = 2k + 1 \), where \( k \) is an integer.\n   \n2. **Even Integer**: \n   - An integer \( m \) is called even if it can be written in the form \( m = 2k \), where \( k \) is an integer.\n\n3. **Sum**: \n   - The sum of two integers \( a \) and \( b \) is defined as their arithmetic addition, i.e., \( a + b \).\n\n### Step 2: Eliciting Relevant Premises\n\nThe following premises are implicit behind the statement:\n\n1. **Premise 1 (P1)**: An odd integer can be expressed as \( 2k + 1 \), where \( k \) is any integer.\n2. **Premise 2 (P2)**: The sum of two integers is another integer.\n3. **Premise 3 (P3)**: The form of an even integer is \( 2m \), where \( m \) is any integer.\n4. **Premise 4 (P4)**: Arithmetic operations (such as addition) are closed under integers.\n\n### Step 3: Establishing the Soundness of Each Premise and Definition\n\n- **P1 (Odd Integer Definition)**: This is a standard definition in number theory and is universally accepted. Sound.\n- **P2 (Sum of Integers)**: The addition of two integers results in another integer, which is a property of integers under addition. Sound.\n- **P3 (Even Integer Definition)**: This is the definition of even integers in number theory. Sound.\n- **P4 (Closure under Addition)**: Integers are closed under addition, meaning adding any two integers results in another integer. Sound.\n\n### Step 4: Building a Granular Syllogistic Inference\n\nLet the two odd integers be \( a \) and \( b \). By definition of odd numbers:\n- \( a = 2k_1 + 1 \), where \( k_1 \) is an integer.\n- \( b = 2k_2 + 1 \), where \( k_2 \) is an integer.\n\nNow, consider the sum \( a + b \):\n\[\na + b = (2k_1 + 1) + (2k_2 + 1) = 2k_1 + 2k_2 + 2 = 2(k_1 + k_2 + 1)\n\]\nThus, the sum of two odd integers is \( 2(k_1 + k_2 + 1) \), which is an even number by definition (since it is divisible by 2).\n\n### Step 5: Final Assessment\n\nThe inference shows that the sum of two odd integers always results in an even integer. Thus, \( p_i \) (\"The sum of two odd integers is always even\") is **entailed** by the premises and definitions, and the statement is **true**.",
            },
            {
                "user_prompt": "Is it true that the square of an integer is always congruent to 0 or 1 modulo 3?",
                "template_variables": {
                    "p_i": "The square of an integer is always congruent to 0 or 1 modulo 3."
                },
                "answer": "Let's verify the statement \( p_i \): \"The square of an integer is always congruent to 0 or 1 modulo 3,\" by following the requested steps.\n\n### Step 1: Eliciting Definitions\n\n1. **Integer**: \n   - An integer is any whole number, positive, negative, or zero, denoted by \( \mathbb{Z} \).\n\n2. **Square of an Integer**: \n   - The square of an integer \( n \) is \( n^2 \), which is the result of multiplying \( n \) by itself: \( n^2 = n \times n \).\n\n3. **Congruence Modulo 3**: \n   - For integers \( a \) and \( b \), we say \( a \equiv b \mod 3 \) if \( a - b \) is divisible by 3. In other words, \( a \) and \( b \) have the same remainder when divided by 3.\n\n### Step 2: Eliciting Relevant Premises\n\nThe following premises are implicit behind the statement:\n\n1. **Premise 1 (P1)**: Any integer \( n \) can be written in one of three forms when considered modulo 3: \( n \equiv 0 \mod 3 \), \( n \equiv 1 \mod 3 \), or \( n \equiv 2 \mod 3 \).\n2. **Premise 2 (P2)**: The square of an integer \( n \), denoted \( n^2 \), is the product of \( n \) with itself.\n3. **Premise 3 (P3)**: Arithmetic operations such as squaring and modular reduction are well-defined operations on integers.\n4. **Premise 4 (P4)**: Modular arithmetic allows squaring to be performed before reducing modulo \( 3 \), i.e., \( n^2 \mod 3 = (n \mod 3)^2 \mod 3 \).\n\n### Step 3: Establishing the Soundness of Each Premise and Definition\n\n- **P1 (Integer forms mod 3)**: Every integer, when divided by 3, leaves a remainder of 0, 1, or 2. This is based on the division algorithm and is a sound and universally accepted premise.\n- **P2 (Squaring an Integer)**: The definition of squaring is well-founded in arithmetic. Sound.\n- **P3 (Operations under Integers)**: Arithmetic operations (addition, multiplication, and squaring) and modular reduction are well-defined over the set of integers. Sound.\n- **P4 (Modular Arithmetic Rule)**: The rule \( n^2 \mod 3 = (n \mod 3)^2 \mod 3 \) follows directly from the properties of modular arithmetic. Sound.\n\n### Step 4: Building a Granular Syllogistic Inference\n\nWe need to verify the square of any integer \( n \) is congruent to either 0 or 1 modulo 3. Based on **P1**, we know that any integer \( n \) can be congruent to one of the following values modulo 3:\n\n#### Case 1: \( n \equiv 0 \mod 3 \)\n- If \( n \equiv 0 \mod 3 \), then \( n^2 = 0^2 = 0 \).\n- Therefore, \( n^2 \equiv 0 \mod 3 \).\n\n#### Case 2: \( n \equiv 1 \mod 3 \)\n- If \( n \equiv 1 \mod 3 \), then \( n^2 = 1^2 = 1 \).\n- Therefore, \( n^2 \equiv 1 \mod 3 \).\n\n#### Case 3: \( n \equiv 2 \mod 3 \)\n- If \( n \equiv 2 \mod 3 \), then \( n^2 = 2^2 = 4 \).\n- Now reduce \( 4 \mod 3 \): \( 4 \equiv 1 \mod 3 \).\n- Therefore, \( n^2 \equiv 1 \mod 3 \).\n\n### Step 5: Final Assessment\n\nIn all cases, the square of an integer is congruent to either 0 or 1 modulo 3:\n- \( n^2 \equiv 0 \mod 3 \) if \( n \equiv 0 \mod 3 \),\n- \( n^2 \equiv 1 \mod 3 \) if \( n \equiv 1 \mod 3 \),\n- \( n^2 \equiv 1 \mod 3 \) if \( n \equiv 2 \mod 3 \).\n\nThus, \( p_i \) (\"The square of an integer is always congruent to 0 or 1 modulo 3\") is **entailed** by the premises and definitions, and the statement is **true**.",
            },
        ],
        "location": {
            "module_path": os.path.join(PROMPT_TACTICS_DIR, 'statement_verification.py'),
            "class_name": "StatementVerifier",
        },
    },
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
    CUSTOM_PROMPT_LABEL: {
        "description": "",
        "tactic_prompt": "{user_prompt}",
        "template_variables": [
            "user_prompt"
        ],
        "examples": [],
    },
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
