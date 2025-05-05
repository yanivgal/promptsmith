import dspy

class JudgeReadability(dspy.Signature):
    """
    You are a readability expert.

    Your task is to evaluate how clear and easy it is to read the provided text.

    Please consider:
    1. Are the sentences simple, natural, and easy to follow?
    2. Are the paragraphs organized logically?
    3. Does the text flow smoothly from one idea to the next?
    4. Is the vocabulary accessible, avoiding unnecessarily complex words?

    Assign a score between 0 (very hard to read) and 1 (very easy and natural to read).

    Explain your reasoning clearly and specifically.
    """
    output_text: str = dspy.InputField(desc="The restructured text to evaluate.")
    reasoning: str = dspy.OutputField(desc="Explain why the text is easy or hard to read.")
    score: float = dspy.OutputField(desc="A score between 0 (poor readability) and 1 (excellent readability).")
