import dspy

class JudgeMeaning(dspy.Signature):
    """
    You are an expert in evaluating meaning preservation.

    Your task is to determine whether the restructured text preserves the essential meaning of the original input text.

    Please consider:
    1. Are all key ideas and important details still present?
    2. Were any important parts of the original meaning lost or changed significantly?
    3. Are minor rephrasings or small generalizations acceptable if they don't distort the overall meaning?

    Assign a score between 0 (poor preservation) and 1 (perfect preservation).

    Explain your reasoning clearly, mentioning what was preserved well and any important losses or changes.
    """
    input_text: str = dspy.InputField(desc="The original text before restructuring.")
    output_text: str = dspy.InputField(desc="The restructured text to evaluate.")
    reasoning: str = dspy.OutputField(desc="Explain where meaning was preserved or changed, and whether the changes are acceptable.")
    score: float = dspy.OutputField(desc="A score between 0 (bad) and 1 (perfect) for how well meaning is preserved.")
