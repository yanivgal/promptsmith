import dspy

class JudgeRedundancy(dspy.Signature):
    """
    You are an expert in identifying redundancy in rewritten text.

    Your task is to evaluate whether the output contains repeated ideas, phrases, or points that could have been expressed once.

    Please consider:
    1. Are there any bullet points or paragraphs that repeat the same idea using different words?
    2. Is the output unnecessarily verbose due to repetition?
    3. Would a human reader feel like certain content is repeated?

    Assign a score between 0 (highly redundant) and 1 (no noticeable redundancy).

    Focus only on repetition, not grammar or formatting.

    Provide a short explanation of any repeated content you found.
    """
    input_text: str = dspy.InputField(desc="The original input text.")
    output_text: str = dspy.InputField(desc="The rewritten version to check for redundancy.")
    reasoning: str = dspy.OutputField(desc="Describe any repeated content and how it could be simplified.")
    score: float = dspy.OutputField(desc="Score between 0 (very redundant) and 1 (no redundancy).")
