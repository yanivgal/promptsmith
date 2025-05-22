import dspy

class BulletizeText(dspy.Signature):
    """
    Bulletize text
    """
    input_text: str = dspy.InputField()
    output_text: str = dspy.OutputField()
