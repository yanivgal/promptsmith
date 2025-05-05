import dspy

class JudgeStructure(dspy.Signature):
    """
    You are an expert in evaluating text structure and organization.

    Your task is to assess whether the restructured text has a clear, logical, and effective structure.

    Please consider:
    1. Does it begin with a relevant and informative title?
    2. Is there an introductory paragraph that summarizes the content?
    3. Are the main ideas separated into well-formed, coherent paragraphs?
    4. Does the sequence of information make sense and flow logically?

    Assign a score between 0 (poor structure) and 1 (excellent structure).

    Clearly explain your reasoning, noting what aspects of structure are strong or weak.
    """
    output_text: str = dspy.InputField(desc="The restructured text to evaluate.")
    reasoning: str = dspy.OutputField(desc="Explain how well the text is structured and organized.")
    score: float = dspy.OutputField(desc="A score between 0 and 1 indicating the quality of the structure.")
