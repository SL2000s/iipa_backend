from dotenv import load_dotenv

load_dotenv()


TACTICS = {
    "assumption_expansion": {
        "label": "ASSUMPTION_EXPANSION",
        "description": "Expand the implied definitions and assumptions for a given statement.",
        "prompt": "Given a statement p_i, expand the implied definitions and assumptions by eliciting definitions for all terms used in p_i and all known premises behind p_i."
    },
    "proof_verification": {
        "label": "PROOF_VERIFICATION",
        "description": "Verify if the entailment between two statements p_i and p_j is logically consistent.",
        "prompt": "Given two statements p_i and p_j, verify if the entailment between the two statements is logically consistent and sound by expanding the steps into granular operations and step-wise inference."
    },
    "statement_verification": {
        "label": "STATEMENT_VERIFICATION",
        "description": "Verify if a given statement is logically correct based on its premises and definitions.",
        "prompt": "Given a statement p_i, verify if the statement is correct by eliciting definitions for all terms used, eliciting relevant premises, and building a granular syllogistic inference."
    },
    "proof": {
        "label": "PROOF",
        "description": "Construct a proof to determine if a given statement is true or false.",
        "prompt": "Given a statement p_i, build a proof by eliciting definitions, relevant premises, and constructing a granular proof step-by-step."
    },
    "proof_within_context": {
        "label": "PROOF_WITHIN_CONTEXT",
        "description": "Construct a proof for a goal statement given a set of premises in a context.",
        "prompt": "Given a goal statement p_i and context P, build a proof by outlining a strategy and executing a step-wise proof based on the premises in the context."
    },
    "add_context": {
        "label": "ADD_CONTEXT",
        "description": "Add the previous context to the knowledge base.",
        "prompt": "Add the current proof context to the knowledge base for future reference."
    },
    "add_statement": {
        "label": "ADD_STATEMENT",
        "description": "Add a given statement to the knowledge base with an optional proof and description.",
        "prompt": "Add statement p_i to the knowledge base, optionally including a proof and description."
    },
    "retrieve_premises": {
        "label": "RETRIEVE_PREMISES",
        "description": "Retrieve premises related to a given search term from the knowledge base.",
        "prompt": "Retrieve premises from the knowledge base related to the search term or statement s."
    }
}
