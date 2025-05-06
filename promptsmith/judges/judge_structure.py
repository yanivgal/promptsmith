import dspy

class JudgeStructure(dspy.Signature):
    """
    You are a text restructuring expert.

    Your job is to take long, dense text and rewrite it to make it easier to read and understand.

    Instructions:
    1. Add a clear and informative title that reflects the topic.
    2. Write a short intro paragraph summarizing the overall idea.
    3. Break the rest of the text into logically organized paragraphs (one idea per paragraph).
    4. Simplify the language where possible, but do not change the meaning.
    5. Keep the tone natural and human.

    Do not invent new information. Stay faithful to the original content.

    Return only the restructured version, including the title at the top.

    """
    output_text: str = dspy.InputField(desc="The restructured text to evaluate.")
    reasoning: str = dspy.OutputField(desc="Explain how well the text is structured and organized.")
    score: float = dspy.OutputField(desc="A score between 0 and 1 indicating the quality of the structure.")
