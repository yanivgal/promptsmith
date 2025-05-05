import dspy

class JudgeBulletStructure(dspy.Signature):
    """
    You are an expert in evaluating the structure of bullet-point formatting.

    Your task is to assess whether the output text follows a proper bullet structure.

    Please consider:
    1. Is the text formatted as a list of bullets (e.g., starts with '-', '*', or '•')?
    2. Does each bullet represent a single, coherent idea?
    3. Are the bullets visually separated and consistently styled?

    Do not judge the content quality or completeness—focus only on structural formatting.

    Assign a score between 0 (not a valid bullet structure) and 1 (clearly and correctly formatted as bullets).

    Explain your reasoning briefly, noting formatting issues if any.
    """
    input_text: str = dspy.InputField(desc="The original text before bulletizing.")
    output_text: str = dspy.InputField(desc="The bulletized output to evaluate.")
    reasoning: str = dspy.OutputField(desc="Explanation of whether the structure is correctly formatted as bullets.")
    score: float = dspy.OutputField(desc="A score between 0 and 1 based on structural correctness.")
