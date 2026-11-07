import json
import os
from arc_agi_benchmarking.schemas import ARCPair
from typing import List

# Harbor parity (branch harbor-parity): the Harbor adapter `arc-agi-2-autoadapter`
# appends this paragraph to the prompt, so that agents know where to write the
# answer. It is appended here too, so that both sides send the same prompt.
HARBOR_OUTPUT_INSTRUCTION = (
    "\n\nWrite your final answer to the file `/app/output.json`: the output grid for the "
    "test input as JSON, a list of rows where each row is a list of integers from 0 to 9 "
    "(for example `[[0, 1], [2, 3]]`).\n"
)

def _load_prompt(prompt_name: str) -> str:
    """
    Load a prompt from the prompts directory
    """

    # Get the directory where this file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, f"{prompt_name}.txt")
    
    with open(prompt_path, "r") as f:
        return f.read()

def convert_task_pairs_to_prompt(training_pairs: List[ARCPair], test_input: ARCPair) -> str:
    """
    Convert the training pairs to a prompt
    """

    prompt_template = _load_prompt("system_prompt")

    training_examples = ""
    for i, pair in enumerate(training_pairs):
        training_examples += f"--Example {i}-- \n\n INPUT: \n\n"
        training_examples += json.dumps(pair.input) + "\n\n"
        training_examples += f"OUTPUT: \n\n"
        training_examples += json.dumps(pair.output) + "\n\n"

    test_input_str = json.dumps(test_input.input)

    return prompt_template.format(training_examples=training_examples, test_input=test_input_str) + HARBOR_OUTPUT_INSTRUCTION