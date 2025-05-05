import dspy

class JudgeCoverage(dspy.Signature):
    """
    You are an expert in evaluating semantic coverage.

    Your task is to determine whether the rewritten text captures all the key ideas from the original input.

    Please consider:
    1. Are all major points from the original present in the output?
    2. Are any important ideas missing or glossed over?
    3. Is the output faithful in scope, even if rephrased or condensed?

    Assign a score between 0 (poor coverage) and 1 (excellent coverage).

    Focus only on inclusion of ideas — do not judge formatting, tone, or phrasing.

    Provide reasoning that highlights any missing or well-covered points.
    """
    input_text: str = dspy.InputField(desc="The original input text.")
    output_text: str = dspy.InputField(desc="The rewritten version to check for idea coverage.")
    reasoning: str = dspy.OutputField(desc="Explain which ideas were preserved or missed.")
    score: float = dspy.OutputField(desc="Score between 0 and 1 based on coverage.")
