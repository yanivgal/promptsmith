import dspy

class RestructureDelta(dspy.Signature):
    """
    You are a critical reviewer comparing the original and restructured versions of a text.

    Your task is to provide a short, structured summary of the key differences between the two versions.
    Identify and explain the most important changes in content, organization, emphasis, or style—based solely on what actually changed.

    Organize your output into clearly titled sections that reflect the nature of the differences.
    Do not use predefined categories. The section titles and groupings should emerge naturally from the specific changes in the texts.

    Be concise but specific. Write in a way that allows a human reader to quickly understand what changed, without needing to read both texts.

    Do not evaluate quality. Do not recommend improvements. Just describe the differences.
    """
    input_text: str = dspy.InputField(desc="The original version of the text.")
    output_text: str = dspy.InputField(desc="The restructured version of the text.")
    summary_of_differences: str = dspy.OutputField(desc="A concise summary of the key differences.")
