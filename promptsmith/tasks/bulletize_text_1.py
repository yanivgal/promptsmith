import dspy

class BulletizeText(dspy.Signature):
    """
    Bulletize text
    """
    input_text: str = dspy.InputField(desc="The original text to convert into bullets.")
    output_text: str = dspy.OutputField(desc="A list of bullet points summarizing the key content.")
