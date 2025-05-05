import dspy

class JudgeConciseness(dspy.Signature):
    """
    You are an expert in evaluating conciseness.

    Your task is to determine whether the restructured text conveys the same meaning as the original but with fewer or more efficient words.

    Please consider:
    1. Does the restructured text eliminate unnecessary repetition or filler?
    2. Are ideas expressed clearly and directly?
    3. Is the text shorter or more efficient without losing important meaning?

    Assign a score between 0 (not concise) and 1 (very concise).

    Explain your reasoning, highlighting any areas where the text could be trimmed or where it succeeds in being efficient.
    """
    input_text: str = dspy.InputField(desc="The original text before restructuring.")
    output_text: str = dspy.InputField(desc="The restructured text to evaluate.")
    reasoning: str = dspy.OutputField(desc="Explain whether the restructured version is more concise or still too wordy.")
    score: float = dspy.OutputField(desc="A score between 0 and 1 indicating how concise the restructured text is.")
