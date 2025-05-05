import dspy

class JudgeFocusRelevance(dspy.Signature):
    """
    You are an expert in evaluating focus and relevance.

    Your task is to determine whether the restructured text stays focused on the original message and avoids unrelated or generic content.

    Please consider:
    1. Does the restructured text stick closely to the main ideas of the original?
    2. Are all added sentences relevant, or do some go off-topic?
    3. Does the model avoid inserting generic filler or broad generalizations not present in the original?

    Assign a score between 0 (poor focus or relevance) and 1 (excellent focus and relevance).

    Explain your reasoning, pointing out any drift from the original topic or unnecessary content.
    """
    input_text: str = dspy.InputField(desc="The original input text.")
    output_text: str = dspy.InputField(desc="The restructured text to evaluate.")
    reasoning: str = dspy.OutputField(desc="Explain whether the rewrite stayed focused and relevant.")
    score: float = dspy.OutputField(desc="A score between 0 and 1 for focus and relevance.")
