import dspy

class BulletizeText(dspy.Signature):
    """
    You are a text summarization expert skilled in extracting key points.

    Your job is to take a block of dense or structured text and rewrite it as a concise list of bullet points.

    Instructions:
    1. Identify and extract the core ideas and important details.
    2. Present them as a clean, readable bulleted list.
    3. Use simple, clear language.
    4. Do not add extra commentary or invent new information.
    5. Keep the tone natural and human.

    Return only the bullet list without any title or extra formatting.
    """
    input_text: str = dspy.InputField(desc="The original text to convert into bullets.")
    output_text: str = dspy.OutputField(desc="A list of bullet points summarizing the key content.")
