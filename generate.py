from typing import List
from llm_sdk import Small_LLM_Model


def generate(
    model: Small_LLM_Model,
    prompt: str,
    max_new_tokens: int = 200,
    eos_token_id: int | None = None,
) -> str:
    """Generate text from a prompt using simple greedy decoding.

    Parameters
    ----------
    model: Small_LLM_Model
        The loaded model wrapper.
    prompt: str
        The input prompt text.
    max_new_tokens: int
        Safety cap on generation length.
    eos_token_id: int | None
        Token id that signals "stop". If None, generation only stops at max_new_tokens.

    Returns
    -------
    str
        The generated text (prompt not included).
    """
    input_ids: List[int] = model.encode(prompt)[0].tolist()  # encode() returns a 2D tensor -> take row 0
    generated: List[int] = []

    for _ in range(max_new_tokens):
        current_ids = input_ids + generated
        logits = model.get_logits_from_input_ids(current_ids)
        next_id = max(range(len(logits)), key=lambda i: logits[i])  # greedy argmax

        if eos_token_id is not None and next_id == eos_token_id:
            break

        generated.append(next_id)

    return model.decode(generated)

model = Small_LLM_Model()
output = generate(model, "What is the sum of 2 and 3?")
print(output)